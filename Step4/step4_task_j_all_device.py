import torch
import torch.nn as nn
import coremltools as ct
import mlx.core as mx
import numpy as np
import time
import json
import os

# ============================================
# Task J: Dynamic Intelligence Benchmark (CPU vs GPU vs ANE)
# 目的：動的再構成プロセスを各デバイスで実行した際の 100ステップの所要時間を比較
# ============================================

def create_ane_flow_model(N):
    class PKGFFlow(nn.Module):
        def forward(self, omega, k):
            # 1ステップの更新論理をANEに焼き込む
            comm = torch.matmul(omega, k) - torch.matmul(k, omega)
            k_next = k + 0.05 * (comm - 0.1 * k)
            return torch.sigmoid(k_next * 2.5)

    model = PKGFFlow().eval()
    ex_omega = torch.rand(1, N, N)
    ex_k = torch.rand(1, N, N)
    return ct.convert(
        torch.jit.trace(model, (ex_omega, ex_k)),
        inputs=[ct.TensorType(shape=ex_omega.shape, name="omega"),
                ct.TensorType(shape=ex_k.shape, name="k")],
        compute_units=ct.ComputeUnit.ALL
    )

def benchmark_cpu(omega, k, steps=100):
    start = time.time()
    for _ in range(steps):
        comm = np.dot(omega, k) - np.dot(k, omega)
        k = k + 0.05 * (comm - 0.1 * k)
        k = 1 / (1 + np.exp(-k * 2.5))
    return (time.time() - start) * 1000

def benchmark_gpu(omega, k, steps=100):
    start = time.time()
    for _ in range(steps):
        comm = mx.matmul(omega, k) - mx.matmul(k, omega)
        k = k + 0.05 * (comm - 0.1 * k)
        k = mx.sigmoid(k * 2.5)
        mx.eval(k)
    return (time.time() - start) * 1000

def benchmark_ane(ane_model, omega, k, steps=100):
    start = time.time()
    for _ in range(steps):
        # ANEから戻ってきた結果を次のステップのKとして再投入
        out = ane_model.predict({'omega': omega, 'k': k})
        # predictの戻り値は辞書形式
        k = list(out.values())[0] 
    return (time.time() - start) * 1000

def run_all_device_duel(N=256):
    print(f"--- Task J: All-Device Intelligence Duel (N={N}) ---")
    
    # 準備
    omega_np = np.random.rand(N, N).astype(np.float32)
    k_np = np.random.rand(N, N).astype(np.float32)
    
    omega_mx = mx.array(omega_np)
    k_mx = mx.array(k_np)
    
    omega_ane = omega_np.reshape(1, N, N)
    k_ane = k_np.reshape(1, N, N)
    ane_model = create_ane_flow_model(N)

    # 実行
    print("Benchmarking CPU...")
    t_cpu = benchmark_cpu(omega_np, k_np)
    
    print("Benchmarking GPU...")
    t_gpu = benchmark_gpu(omega_mx, k_mx)
    
    print("Benchmarking ANE...")
    t_ane = benchmark_ane(ane_model, omega_ane, k_ane)

    print("-" * 45)
    print(f"{'Device':<15} | {'100-Step Time (ms)':<20}")
    print("-" * 45)
    print(f"{'CPU (NumPy)':<15} | {t_cpu:20.4f}")
    print(f"{'GPU (MLX)':<15} | {t_gpu:20.4f}")
    print(f"{'ANE (Dedicated)':<15} | {t_ane:20.4f}")
    print("-" * 45)

    results = {
        "N": N,
        "cpu_ms": t_cpu,
        "gpu_ms": t_gpu,
        "ane_ms": t_ane
    }
    with open("Step4/task_j_multi_device_dynamic_results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    # N=256 は ANE/GPU の並列性が活きる実用的な解像度
    run_all_device_duel(N=256)

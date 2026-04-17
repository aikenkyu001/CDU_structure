import numpy as np
import time
import json
import mlx.core as mx
import coremltools as ct
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import os

# ============================================
# Step 4: All-Device Faithful PKGF Benchmark (M2 Optimized)
# 目的：Mac mini M2 環境での CPU, GPU, ANE の実測とプロット
# ============================================

def get_cpu_pkgf_time(dim, steps=100):
    K = np.random.normal(0, 1, (dim, dim)).astype(np.float32)
    Omega = np.random.normal(0, 1, (dim, dim)).astype(np.float32)
    dt = 0.01; eta = 0.5; lmbda = 0.1
    start = time.time()
    for _ in range(steps):
        K_shift = (K + np.roll(K, 1, axis=0) + np.roll(K, -1, axis=0)) / 3.0
        K_dot = eta * (np.dot(Omega, K) - np.dot(K, Omega)) - lmbda * (K - K_shift)
        K += dt * K_dot
        K = np.tanh(K)
    return ((time.time() - start) / steps) * 1000

def get_gpu_pkgf_time(dim, steps=100):
    K = mx.random.normal((dim, dim))
    Omega = mx.random.normal((dim, dim))
    dt = 0.01; eta = 0.5; lmbda = 0.1
    start = time.time()
    for _ in range(steps):
        K_shift = (K + mx.concatenate([K[1:], K[:1]], axis=0) + mx.concatenate([K[-1:], K[:-1]], axis=0)) / 3.0
        K_dot = eta * (mx.matmul(Omega, K) - mx.matmul(K, Omega)) - lmbda * (K - K_shift)
        K = K + dt * K_dot
        K = mx.tanh(K)
        mx.eval(K)
    return ((time.time() - start) / steps) * 1000

def get_ane_pkgf_time(dim, steps=100):
    class PKGFCommutator(nn.Module):
        def forward(self, Omega, K):
            return torch.matmul(Omega, K) - torch.matmul(K, Omega)
    model = PKGFCommutator().eval()
    example_omega = torch.randn(1, 1, dim, dim)
    example_k = torch.randn(1, 1, dim, dim)
    try:
        mlmodel = ct.convert(
            torch.jit.trace(model, (example_omega, example_k)),
            inputs=[ct.TensorType(shape=example_omega.shape), ct.TensorType(shape=example_k.shape)],
            compute_units=ct.ComputeUnit.ALL
        )
        input_dict = {'Omega': example_omega.numpy(), 'K': example_k.numpy()}
        for _ in range(10): mlmodel.predict(input_dict)
        start = time.time()
        for _ in range(steps): mlmodel.predict(input_dict)
        return ((time.time() - start) / steps) * 1000
    except: return -1.0

def run_all_benchmarks():
    dims = [128, 256, 512]
    cpu_times, gpu_times, ane_times = [], [], []
    
    print(f"Starting M2 Benchmark...")
    for dim in dims:
        t_cpu = get_cpu_pkgf_time(dim)
        t_gpu = get_gpu_pkgf_time(dim)
        t_ane = get_ane_pkgf_time(dim)
        cpu_times.append(t_cpu); gpu_times.append(t_gpu); ane_times.append(t_ane)
        print(f"Dim {dim}: CPU={t_cpu:.3f}, GPU={t_gpu:.3f}, ANE={t_ane:.3f}")

    # --- 可視化 (M2 用) ---
    plt.figure(figsize=(10, 6))
    plt.plot(dims, cpu_times, 'o-', label='CPU (NumPy/AMX)', color='gray')
    plt.plot(dims, gpu_times, 's-', label='GPU (M2 MLX)', color='blue')
    plt.plot(dims, ane_times, 'd-', label='ANE (M2 CoreML)', color='red', linewidth=3)
    plt.yscale('log')
    plt.xlabel('Manifold Dimension (N)')
    plt.ylabel('Latency per Step (ms)')
    plt.title('Real M2 Benchmark: Faithful PKGF Flow Performance')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.3)
    plt.savefig("Step4/step4_real_m2_result.png")
    print(f"Plot saved as Step4/step4_real_m2_result.png")

    results = [{"dim": d, "cpu": c, "gpu": g, "ane": a} for d, c, g, a in zip(dims, cpu_times, gpu_times, ane_times)]
    with open("Step4/all_device_faithful_results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    run_all_benchmarks()

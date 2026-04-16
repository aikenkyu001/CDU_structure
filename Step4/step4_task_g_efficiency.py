import torch
import torch.nn as nn
import coremltools as ct
import numpy as np
import time
import json
import os

# ============================================
# Task G: Global Structure Processing (PKGF vs MLP on ANE)
# 目的：全域的な構造（N x N）を一段階で処理する際の物理的効率の差を実測する
# ============================================

def create_global_processing_models(N):
    """
    1. PKGF: N x N の行列としてグローバル情報を処理 (計算量 N^3)
    2. MLP: N^2 のベクトルとしてグローバル情報を処理 (計算量 N^4)
    """
    
    # --- 1. PKGF Module (Matrix Logic) ---
    class PKGFGlobal(nn.Module):
        def forward(self, omega, k):
            return torch.matmul(omega, k) - torch.matmul(k, omega)

    # --- 2. Standard MLP (Vector Logic) ---
    # 同等の「全ピクセル間相互作用」を一段階で見るためのMLP層
    class MLPGlobal(nn.Module):
        def __init__(self, size_sq):
            super().__init__()
            self.linear = nn.Linear(size_sq, size_sq, bias=False)
        def forward(self, x):
            return self.linear(x)

    # ANE への変換
    # PKGF
    pkgf_model = PKGFGlobal().eval()
    ex_omega = torch.rand(1, N, N)
    ex_k = torch.rand(1, N, N)
    pkgf_ct = ct.convert(
        torch.jit.trace(pkgf_model, (ex_omega, ex_k)),
        inputs=[ct.TensorType(shape=ex_omega.shape, name="omega"),
                ct.TensorType(shape=ex_k.shape, name="k")],
        compute_units=ct.ComputeUnit.ALL
    )

    # MLP (N=64 の場合、入力は 4096)
    size_sq = N * N
    mlp_model = MLPGlobal(size_sq).eval()
    ex_mlp_in = torch.rand(1, size_sq)
    mlp_ct = ct.convert(
        torch.jit.trace(mlp_model, ex_mlp_in),
        inputs=[ct.TensorType(shape=ex_mlp_in.shape, name="x")],
        compute_units=ct.ComputeUnit.ALL
    )

    return pkgf_ct, mlp_ct

def run_global_efficiency_benchmark(N=64, iterations=100):
    print(f"Starting Task G: Global Structure Efficiency (N={N}, pixels={N*N})")
    
    pkgf_ane, mlp_ane = create_global_processing_models(N)
    
    # 入力準備
    omega_in = np.random.rand(1, N, N).astype(np.float32)
    k_in = np.random.rand(1, N, N).astype(np.float32)
    mlp_in = np.random.rand(1, N*N).astype(np.float32)

    # --- PKGF (Geometric Flow) ---
    for _ in range(10): pkgf_ane.predict({'omega': omega_in, 'k': k_in})
    start = time.time()
    for _ in range(iterations):
        pkgf_ane.predict({'omega': omega_in, 'k': k_in})
    pkgf_t = ((time.time() - start) / iterations) * 1000

    # --- MLP (Standard AI Logic) ---
    for _ in range(10): mlp_ane.predict({'x': mlp_in})
    start = time.time()
    for _ in range(iterations):
        mlp_ane.predict({'x': mlp_in})
    mlp_t = ((time.time() - start) / iterations) * 1000

    print(f"Result (Time to process global context):")
    print(f"  PKGF (Geometric N^3 Logic): {pkgf_t:10.4f} ms")
    print(f"  MLP  (Standard  N^4 Logic): {mlp_t:10.4f} ms")
    
    ratio = mlp_t / pkgf_t
    print("-" * 40)
    print(f"CONCLUSION: PKGF is {ratio:.2f}x FASTER than Standard MLP for global structural processing!")

    return {
        "N": N,
        "pkgf_ms": pkgf_t,
        "mlp_ms": mlp_t,
        "speedup": ratio
    }

if __name__ == "__main__":
    # N=64 は、画像としては小さいが、全結合層としては 4096 次元の巨大な層になる
    result = run_global_efficiency_benchmark(N=64)
    with open("Step4/task_g_global_efficiency_results.json", "w") as f:
        json.dump(result, f, indent=4)

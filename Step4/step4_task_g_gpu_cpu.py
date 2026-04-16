import mlx.core as mx
import numpy as np
import time
import json
import os

# ============================================
# Task G 拡張版: Multi-Device Algorithm Duel (PKGF vs MLP)
# デバイス (GPU/CPU) を問わず、アルゴリズムの物理的優位性を検証する
# ============================================

def benchmark_gpu(N=64, iterations=100):
    """M1 GPU (MLX) での比較"""
    print(f"--- GPU (MLX) Benchmark (N={N}) ---")
    
    # 1. PKGF Logic (Matrix)
    omega = mx.random.normal((N, N))
    k = mx.random.normal((N, N))
    
    # ウォームアップ
    for _ in range(10): 
        _ = mx.matmul(omega, k) - mx.matmul(k, omega)
        mx.eval(_)

    start = time.time()
    for _ in range(iterations):
        comm = mx.matmul(omega, k) - mx.matmul(k, omega)
        mx.eval(comm)
    pkgf_t = ((time.time() - start) / iterations) * 1000

    # 2. MLP Logic (Vector)
    size_sq = N * N
    w = mx.random.normal((size_sq, size_sq))
    x = mx.random.normal((1, size_sq))

    # ウォームアップ
    for _ in range(10): 
        _ = mx.matmul(x, w)
        mx.eval(_)

    start = time.time()
    for _ in range(iterations):
        y = mx.matmul(x, w)
        mx.eval(y)
    mlp_t = ((time.time() - start) / iterations) * 1000

    print(f"  PKGF (N^3): {pkgf_t:10.4f} ms")
    print(f"  MLP  (N^4): {mlp_t:10.4f} ms")
    print(f"  Speedup: {mlp_t/pkgf_t:.2f}x")
    
    return pkgf_t, mlp_t

def benchmark_cpu(N=64, iterations=20):
    """M1 CPU (NumPy) での比較"""
    print(f"--- CPU (NumPy) Benchmark (N={N}) ---")
    
    # 1. PKGF Logic (Matrix)
    omega = np.random.rand(N, N).astype(np.float32)
    k = np.random.rand(N, N).astype(np.float32)

    start = time.time()
    for _ in range(iterations):
        comm = np.dot(omega, k) - np.dot(k, omega)
    pkgf_t = ((time.time() - start) / iterations) * 1000

    # 2. MLP Logic (Vector)
    size_sq = N * N
    w = np.random.rand(size_sq, size_sq).astype(np.float32)
    x = np.random.rand(1, size_sq).astype(np.float32)

    start = time.time()
    for _ in range(iterations):
        y = np.dot(x, w)
    mlp_t = ((time.time() - start) / iterations) * 1000

    print(f"  PKGF (N^3): {pkgf_t:10.4f} ms")
    print(f"  MLP  (N^4): {mlp_t:10.4f} ms")
    print(f"  Speedup: {mlp_t/pkgf_t:.2f}x")
    
    return pkgf_t, mlp_t

if __name__ == "__main__":
    N = 64
    gpu_pkgf, gpu_mlp = benchmark_gpu(N)
    cpu_pkgf, cpu_mlp = benchmark_cpu(N)
    
    results = {
        "N": N,
        "gpu": {"pkgf_ms": gpu_pkgf, "mlp_ms": gpu_mlp, "speedup": gpu_mlp/gpu_pkgf},
        "cpu": {"pkgf_ms": cpu_pkgf, "mlp_ms": cpu_mlp, "speedup": cpu_mlp/cpu_pkgf}
    }
    
    with open("Step4/task_g_multi_device_results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("\nMulti-device benchmark complete.")

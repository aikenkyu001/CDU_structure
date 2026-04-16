import mlx.core as mx
import numpy as np
import time
import matplotlib.pyplot as plt
import json

# ============================================
# Step 4: 真の本格実験 - M1 GPU (MLX) による PKGF 実測比較
# ============================================

class PKGFExperiment:
    def __init__(self, dim):
        self.dim = dim
        # Axiom U1: 複素並行鍵 K
        self.K_real = mx.random.normal((dim, dim))
        self.K_imag = mx.random.normal((dim, dim))
        self.Omega = mx.random.normal((dim, dim))
        
    def step_pkgf(self, dt=0.01, lmbda=0.1):
        """Axiom U3: Unification Flow の M1 GPU 実装"""
        # [Omega, K]
        comm = mx.matmul(self.Omega, self.K_real) - mx.matmul(self.K_real, self.Omega)
        dissipation = -lmbda * self.K_real
        self.K_real = self.K_real + dt * (comm + dissipation)
        mx.eval(self.K_real) # GPU実行を強制

    def step_standard_npu(self):
        """標準的な行列演算 (M1 GPU)"""
        W = mx.random.normal((self.dim, self.dim))
        X = mx.random.normal((self.dim, self.dim))
        Y = mx.matmul(W, X)
        Y = mx.maximum(Y, 0)
        mx.eval(Y) # GPU実行を強制

def run_benchmark():
    dims = [128, 256, 512, 1024, 2048]
    pkgf_times = []
    npu_times = []
    results_data = []

    print(f"Starting Real M1 GPU Benchmark using MLX...")
    print(f"{'Dimension':>10} | {'PKGF (ms)':>12} | {'Standard (ms)':>12}")
    print("-" * 40)

    for dim in dims:
        exp = PKGFExperiment(dim)
        
        # ウォームアップ
        for _ in range(10): 
            exp.step_pkgf()
            exp.step_standard_npu()
        
        # PKGF計測 (100回試行)
        start = time.time()
        for _ in range(100):
            exp.step_pkgf()
        pkgf_t = ((time.time() - start) / 100.0) * 1000 # 1回あたりのms
        pkgf_times.append(pkgf_t)

        # 標準演算計測 (100回試行)
        start = time.time()
        for _ in range(100):
            exp.step_standard_npu()
        npu_t = ((time.time() - start) / 100.0) * 1000
        npu_times.append(npu_t)

        print(f"{dim:10d} | {pkgf_t:12.4f} | {npu_t:12.4f}")
        results_data.append({
            "dimension": dim,
            "pkgf_ms": pkgf_t,
            "standard_ms": npu_t
        })

    # 結果の保存
    with open("Step4/real_m1_benchmark_results.json", "w") as f:
        json.dump(results_data, f, indent=4)

    # 可視化
    plt.figure(figsize=(10, 6))
    plt.plot(dims, pkgf_times, 'o-', label='PKGF Flow (M1 GPU/MLX)', color='red', linewidth=2)
    plt.plot(dims, npu_times, 's--', label='Standard Logic (M1 GPU/MLX)', color='blue', linewidth=2)
    plt.yscale('log')
    plt.xlabel('Manifold Dimension (N)')
    plt.ylabel('Execution Time per Step (ms)')
    plt.title('Real M1 Benchmark: PKGF vs Standard Logic (Axiom A1)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.savefig("Step4/step4_real_m1_result.png")
    
    print("-" * 40)
    print(f"Real M1 benchmark complete. Results saved as Step4/step4_real_m1_result.png")

if __name__ == "__main__":
    run_benchmark()

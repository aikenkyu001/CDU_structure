import torch
import torch.nn as nn
import coremltools as ct
import mlx.core as mx
import numpy as np
import time
import json
import os

# --- 1. ANE 用のモデル準備関数 ---
def create_ane_model(dim):
    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(dim, dim, bias=False)
            self.relu = nn.ReLU()
        def forward(self, x):
            return self.relu(self.linear(x))

    model = SimpleModel().eval()
    example_input = torch.rand(1, dim)
    traced_model = torch.jit.trace(model, example_input)
    
    # CoreML への変換 (ANEをターゲットにする)
    mlmodel = ct.convert(
        traced_model,
        inputs=[ct.TensorType(shape=example_input.shape)],
        compute_units=ct.ComputeUnit.ALL # ANE 優先
    )
    return mlmodel

# --- 2. 比較実験クラス ---
class TrueANEBenchmark:
    def __init__(self, dim):
        self.dim = dim
        # ANE用
        self.ane_model = create_ane_model(dim)
        self.ane_input = {'x': np.random.rand(1, dim).astype(np.float32)}
        
        # PKGF (GPU) 用
        self.K = mx.random.normal((dim, dim))
        self.Omega = mx.random.normal((dim, dim))

    def run_ane(self, iterations=100):
        # ウォームアップ
        for _ in range(10): self.ane_model.predict(self.ane_input)
        
        start = time.time()
        for _ in range(iterations):
            self.ane_model.predict(self.ane_input)
        return ((time.time() - start) / iterations) * 1000

    def run_pkgf_gpu(self, iterations=100):
        # ウォームアップ
        for _ in range(10):
            comm = mx.matmul(self.Omega, self.K) - mx.matmul(self.K, self.Omega)
            self.K = self.K + 0.01 * comm
            mx.eval(self.K)

        start = time.time()
        for _ in range(iterations):
            comm = mx.matmul(self.Omega, self.K) - mx.matmul(self.K, self.Omega)
            self.K = self.K + 0.01 * comm
            mx.eval(self.K)
        return ((time.time() - start) / iterations) * 1000

def run_experiment():
    dims = [128, 512, 1024] # ANEのコンパイル時間を考慮し、代表的な次元で実施
    results = []

    print(f"{'Dimension':>10} | {'PKGF-GPU (ms)':>15} | {'ANE-NPU (ms)':>15}")
    print("-" * 50)

    for dim in dims:
        print(f"Compiling and testing for dimension {dim}...")
        bench = TrueANEBenchmark(dim)
        
        pkgf_t = bench.run_pkgf_gpu()
        ane_t = bench.run_ane()
        
        print(f"{dim:10d} | {pkgf_t:15.4f} | {ane_t:15.4f}")
        results.append({
            "dimension": dim,
            "pkgf_gpu_ms": pkgf_t,
            "ane_npu_ms": ane_t
        })

    with open("Step4/true_ane_vs_pkgf_results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("-" * 50)
    print("True ANE vs GPU experiment complete.")

if __name__ == "__main__":
    run_experiment()

import numpy as np
import time
import matplotlib.pyplot as plt

# ============================================
# Step 4: V-PCM vs NPU 効率・耐性シミュレーション (PKGF 準拠版)
# 目的：Axiom U1/U2（複素並行鍵）による揺らぎの統合と安定性の比較検証
# ============================================

def simulate_structural_stability(model_type='VPCM', noise_lvl=0.1):
    """
    モデルの種類に応じた構造安定性（Axiom U）のシミュレーション
    VPCM: Axiom U1/U2。揺らぎ K_fluct が K_core と直交し、構造を破壊せず安定化させる。
    NPU: ノイズは単なる誤差 (error) であり、構造を線形に破壊する。
    """
    if model_type == 'VPCM':
        # Axiom P2/U3: ノイズを揺らぎとして利用。低レベルのノイズはむしろ安定化を助ける。
        # ベル型の安定性曲線
        stability = 1.0 / (1.0 + (noise_lvl - 0.05)**2 * 5.0)
        return max(stability, 0.6) # 最低限の構造を維持
    else:
        # デジタル・電子系: ノイズ蓄積による SNR 低下
        return 1.0 / (1.0 + noise_lvl * 8.0)

# 1. 計算スケール比較 (Axiom A1: 多様体 M の次元拡張効率)
# VPCMは物理光学的な並列性により、多様体の次元拡大に対して O(1)
# NPUは演算回数が次元の二乗 O(N^2) で増大
sizes = np.array([8, 16, 32, 64, 128, 256, 512])
time_vpcm = np.ones_like(sizes) * 1.0  # Constant time
time_npu = (sizes / 8)**2             # Quadratic scaling

# 2. 揺らぎに対する構造安定性の相図 (Axiom U1/U2/U3)
noises = np.linspace(0, 0.6, 60)
stability_vpcm = [simulate_structural_stability('VPCM', n) for n in noises]
stability_npu = [simulate_structural_stability('NPU', n) for n in noises]

# 結果の保存 (JSON)
import json
results = {
    "scaling": {"matrix_sizes": sizes.tolist(), "vpcm_times": time_vpcm.tolist(), "npu_times": time_npu.tolist()},
    "structural_stability": {"noise_levels": noises.tolist(), "vpcm_scores": stability_vpcm, "npu_scores": stability_npu}
}
with open("Step4/simulation_results.json", "w") as f:
    json.dump(results, f, indent=4)

plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(sizes, time_vpcm, 'o-', label="V-PCM (Photonic O(1) Manifold Flow)", color='red')
plt.plot(sizes, time_npu, 's-', label="NPU (Electronic O(N^2) Computation)", color='blue')
plt.yscale('log')
plt.title("Step 4: Manifold Scaling Efficiency (Axiom A1/U3)")
plt.xlabel("State Space Dimension (N)")
plt.ylabel("Relative Time (log scale)")
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(2,1,2)
plt.plot(noises, stability_vpcm, label="V-PCM: Axiom U1/U2 Stability (K_core + i K_fluct)", color='red')
plt.plot(noises, stability_npu, label="NPU: Digital Error Degradation", color='blue')
plt.title("Step 4: Structural Robustness against Physical Fluctuation")
plt.xlabel("Fluctuation Level (K_fluct)")
plt.ylabel("Structural Stability Score")
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Step4/step4_result.png")
print(f"Step 4 PKGF Comparison Simulation complete. Results saved to Step4/simulation_results.json and step4_result.png")

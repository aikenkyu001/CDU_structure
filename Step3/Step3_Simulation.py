import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================
# Step 3: Optical V-PCM 物理シミュレーション (PKGF Axiom U3 準拠)
# 目的：統一方程式 \nabla K = [\Omega, K] - \lambda D(K) の光学系での物理的再現
# ============================================

def calculate_effective_rank(K):
    """Axiom D3/U6: 簡易ランク推定 (Double Validation 用)"""
    return np.sum(K**2) / (np.max(K)**2 + 1e-12)

def simulate_step3_pkgf_flow(size=32, steps=400, lambda_param=0.1, sigma=1.2, noise_lvl=0.02):
    """
    Axiom U3: \nabla K = [\Omega, K] - \lambda D(K)
    size: 多様体 M の次元 (N x N)
    steps: ダイナミクスステップ数
    lambda_param: 散逸係数 \lambda
    sigma: 光学散逸作用素 D(K) のボケ幅 (PSF)
    """
    # Axiom A3: 初期並行鍵 K (ランダムな低ランク状態)
    K = np.random.rand(size, size)
    
    # Axiom A6: 意味ポテンシャル \Omega (ターゲットとなる構造の核)
    # ここでは中央に集約する構造を Omega とする
    Omega = np.zeros((size, size))
    Omega[size//4:3*size//4, size//4:3*size//4] = 1.0
    
    ranks = []
    structural_stability = []
    
    for t in range(steps):
        # 1. 構築項 [\Omega, K] (Axiom C1): 外部情報による構造へのガイド
        # 簡易的に Omega と K の相互作用を計算
        construction = (Omega @ K - K @ Omega) * 0.1
        
        # 2. 散逸項 - \lambda D(K) (Axiom D2): 光学的なボケによる次元崩壊
        # PSF を散逸作用素 D として扱う
        K_blurred = gaussian_filter(K, sigma=sigma)
        dissipation = -lambda_param * (K - K_blurred)
        
        # 3. 統一方程式 (Axiom U3) に基づく更新
        # \nabla K = [\Omega, K] - \lambda D(K)
        # 非線形活性化 (Axiom U4: ゲージ破れを誘発する非線形性)
        K_next = K + construction + dissipation
        K_next = np.exp(K_next * 2.5) # 非線形増幅
        K_next /= (np.max(K_next) + 1e-12) # 規格化
        
        # Axiom U1/U2: 複素的な揺らぎ K_fluct の付加 (ノイズを揺らぎとして統合)
        K_fluct = np.random.normal(0, noise_lvl, (size, size))
        K = K_next + K_fluct
        K = np.clip(K, 0, 1)
        
        # 秩序変数の記録
        r = calculate_effective_rank(K)
        ranks.append(r)
        
        # 構造安定性の評価 (Omega との相関)
        stability = np.corrcoef(K.flatten(), Omega.flatten())[0,1]
        structural_stability.append(stability)

    return ranks, structural_stability

# 実験実行
ranks, stability = simulate_step3_pkgf_flow(steps=300)

# 結果の保存 (JSON)
import json
results = {
    "initial_rank": float(ranks[0]),
    "final_rank": float(ranks[-1]),
    "max_rank": float(np.max(ranks)),
    "rank_jump_detected": bool(np.max(ranks) > ranks[0] * 1.5), # Axiom U6
    "final_stability": float(stability[-1])
}
with open("Step3/simulation_results.json", "w") as f:
    json.dump(results, f, indent=4)

# 可視化
plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(ranks, label="Effective Rank (Dynamic Dimension d_eff)", color='purple')
plt.axhline(ranks[0], color='gray', linestyle='--', alpha=0.5, label='Initial State')
plt.title("Step 3: PKGF Unified Flow Dynamics (Axiom U3/U6)")
plt.ylabel("Dimension (Rank)")
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(2,1,2)
plt.plot(stability, label="Structural Stability (Axiom U5: Emergent Sector)", color='green')
plt.title("Emergence of Stable Structure via Unified Equation")
plt.xlabel("PKGF Time Step (t)")
plt.ylabel("Stability Score")
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Step3/step3_result.png")
print(f"Step 3 PKGF Simulation complete. Results saved to Step3/simulation_results.json and step3_result.png")

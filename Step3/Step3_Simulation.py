import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# ============================================
# Step 3: Optical V-PCM 物理シミュレーション
# 目的：光学ボケ (PSF) を伴うダイナミクスでの構造生成 (rank jump) の検証
# ============================================

def calculate_effective_rank(K):
    """特異値分布のエントロピーから有効ランクを計算"""
    s = np.linalg.svd(K, compute_uv=False)
    s = s / np.sum(s)
    # Shannon entropy of singular value distribution
    entropy = -np.sum(s * np.log(s + 1e-12))
    return np.exp(entropy)

def simulate_step3_vpcm(size=32, steps=400, sigma=1.0, noise_lvl=0.01):
    """
    size: 行列サイズ (N x N)
    steps: ダイナミクスステップ数
    sigma: 光学カーネルAのボケ幅 (PSF)
    """
    # 初期状態 (ランダムな低ランク状態からの開始)
    K = np.random.rand(size, size)
    
    ranks = []
    entropies = []
    
    for t in range(steps):
        # 1. 光学的カーネル A の適用 (ボケ)
        K_opt = gaussian_filter(K, sigma=sigma)
        
        # 2. 内部ダイナミクス (非線形変換 + 散逸)
        # 簡易モデル: K = softmax(K_opt + feedback - decay)
        # ここでは「構造の先鋭化」を模倣する非線形写像を用いる
        K_next = np.exp(K_opt * 2.0) 
        K_next /= np.max(K_next)
        
        # 3. ノイズの付加
        K_next += np.random.normal(0, noise_lvl, (size, size))
        K_next = np.clip(K_next, 0, 1)
        
        K = K_next
        
        # 秩序変数の記録
        r = calculate_effective_rank(K)
        ranks.append(r)
        entropies.append(-np.sum( (K/np.sum(K)) * np.log(K/np.sum(K) + 1e-12) ))

    return ranks, entropies

# 実験
ranks, entropies = simulate_step3_vpcm(steps=200)

# 結果の保存 (JSON)
import json
results = {
    "initial_rank": float(ranks[0]),
    "final_rank": float(ranks[-1]),
    "max_rank": float(np.max(ranks)),
    "rank_jump": float(np.max(ranks) - ranks[0])
}
with open("Step3/simulation_results.json", "w") as f:
    json.dump(results, f, indent=4)

plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(ranks, label="Effective Rank (Dynamic Dimension)", color='purple')
plt.title("Step 3: V-PCM Structural Generation (Rank Jump)")
plt.ylabel("Dimension (Rank)")
plt.grid(True)
plt.legend()

plt.subplot(2,1,2)
plt.plot(entropies, label="Entropy (Structural Complexity)", color='blue')
plt.title("Information Entropy Transition")
plt.xlabel("Step")
plt.ylabel("Entropy")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("Step3/step3_result.png")
print(f"Step 3 Simulation complete. Results saved to Step3/simulation_results.json and step3_result.png")

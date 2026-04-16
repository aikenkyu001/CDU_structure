import numpy as np
import cv2
import json
import matplotlib.pyplot as plt
from scipy.linalg import svd
import os

# ============================================
# Step 3: 改訂版・生成型デジタル PKGF シミュレーション (修正版)
# 目的：パラメータスイープによる次元跳躍 (Rank Jump) の網羅的探索
# ============================================

# --- 定数・公理パラメータの初期値 ---
N = 100            # 多様体の解像度
ETA = 0.25         # 構築項の学習率 (Axiom C1)
STEPS_PER_SIM = 200

def get_effective_rank(K):
    """SVDに基づく有効ランク (d_eff) の計算: Axiom U6 の指標"""
    s = svd(K, compute_uv=False)
    p = (s**2) / (np.sum(s**2) + 1e-12)
    p = p[p > 0]
    return np.exp(-np.sum(p * np.log(p)))

def generate_stimulus(t, pattern_type='circle'):
    """動的な意味ポテンシャル Omega の生成"""
    img = np.zeros((N, N), dtype=np.float32)
    if pattern_type == 'circle':
        center = (int(50 + 25*np.cos(t/15)), int(50 + 25*np.sin(t/15)))
        cv2.circle(img, center, 12, 1.0, -1)
    elif pattern_type == 'grid':
        img[::20, :] = 0.6
        img[:, ::20] = 0.6
    return img

def apply_environment(img, blur_sigma, noise_level):
    """環境フィルター: 散逸 (D) と ゆらぎ (U1)"""
    if blur_sigma > 0:
        k_size = int(blur_sigma * 3) * 2 + 1
        img = cv2.GaussianBlur(img, (k_size, k_size), blur_sigma)
    noise = np.random.normal(0, noise_level, (N, N))
    return np.clip(img + noise, 0, 1)

def run_single_experiment(blur_sigma, noise_level, pattern='circle'):
    """特定のパラメータ条件下でのシミュレーション実行"""
    # 初期並行鍵 K (非常に低いランクから開始して構造生成を観測しやすくする)
    K = np.ones((N, N), dtype=np.float32) * 0.01
    history_rank = []
    
    for t in range(STEPS_PER_SIM):
        # 1. Generator & Environment
        raw_stim = generate_stimulus(t, pattern)
        Omega = apply_environment(raw_stim, blur_sigma, noise_level)
        
        # 2. PKGF Unified Flow (Axiom U3)
        # 内部散逸 (D)
        K_d = cv2.GaussianBlur(K, (5, 5), 0.8)
        # 構築 (C): [Omega, K]
        commutator = np.dot(Omega, K) - np.dot(K, Omega)
        K = K_d + ETA * commutator
        
        # ゲージ破れ (U4): 非線形増幅
        K = np.exp(K * 2.0)
        K = K / (np.linalg.norm(K, ord='fro') + 1e-12) * 10.0
        
        history_rank.append(get_effective_rank(K))
    
    # ランクの跳躍量 (初期と最終の差)
    rank_jump = history_rank[-1] - history_rank[0]
    return rank_jump, history_rank[-1]

def run_parameter_sweep():
    print("Starting Automated Parameter Sweep for Step 3...")
    
    # 探索範囲を広げる
    blurs = [0.5, 1.5, 3.0]
    noises = [0.01, 0.05, 0.15]
    
    sweep_results = []
    
    for b in blurs:
        for n in noises:
            jump, final_rank = run_single_experiment(b, n)
            sweep_results.append({
                "blur": b,
                "noise": n,
                "jump": float(jump),
                "final_rank": float(final_rank)
            })
            print(f"Blur: {b:.1f}, Noise: {n:.2f} -> Rank Jump: {jump:+.4f}")

    # 結果の保存
    with open("Step3/simulation_results.json", "w") as f:
        json.dump(sweep_results, f, indent=4)
    
    # 代表的なグラフの作成
    plt.figure(figsize=(10, 8))
    
    # Scatter plot for sweep
    for res in sweep_results:
        size = abs(res["jump"]) * 1000 + 10 # 最小サイズを保証
        color = 'red' if res["jump"] > 0 else 'blue'
        plt.scatter(res["blur"], res["noise"], s=size, alpha=0.6, 
                    c=color, edgecolors='black')
        plt.text(res["blur"], res["noise"] + 0.005, f"{res['jump']:+.3f}", 
                 ha='center', fontsize=9, fontweight='bold')

    plt.title("Step 3 Sweep: Rank Jump Intensity (Red: Increase, Blue: Decrease)")
    plt.xlabel("Dissipation (Blur Sigma)")
    plt.ylabel("Fluctuation (Noise Level)")
    plt.grid(True, alpha=0.3)
    plt.savefig("Step3/step3_result.png")
    print("Sweep complete. Results saved to Step3/simulation_results.json and step3_result.png")

if __name__ == "__main__":
    run_parameter_sweep()

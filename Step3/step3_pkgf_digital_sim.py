import numpy as np
import cv2
import time
import json
import os

# --- 1. 定数・公理パラメータの設定 ---
N = 100            # 多様体の解像度 (100x100)
ETA = 0.15         # 構築項の学習率 (Axiom C1)
LAMBDA_D = 0.08    # 散逸の強度 (Axiom D2)
NOISE_LEVEL = 0.02 # 複素ゆらぎの強度 (Axiom U1)

def get_effective_rank(K):
    """有効ランク (d_eff) の計算: Axiom U6 の指標"""
    s = np.linalg.svd(K, compute_uv=False)
    # 特異値分布のエントロピーから動的次元を算出
    p = (s**2) / np.sum(s**2 + 1e-10)
    return np.exp(-np.sum(p * np.log(p + 1e-10)))

# --- 2. 画像生成とフィルター (刺激と環境) ---
def generate_stimulus(t):
    """動的な意味ポテンシャル Omega の生成 (Axiom A6)"""
    img = np.zeros((N, N), dtype=np.float32)
    # ステップごとに変化する格子模様と円の干渉
    spacing = 10
    img[::spacing, :] = 0.5
    img[:, ::spacing] = 0.5
    center = (int(50 + 20*np.cos(t/10)), int(50 + 20*np.sin(t/10)))
    cv2.circle(img, center, 15, 1.0, -1)
    return img

def apply_physical_filter(img, sigma=1.2):
    """物理的な散逸（ボケ）とノイズの適用 (Axiom D1)"""
    # 散逸（光学的なボケをシミュレート）
    dissipated = cv2.GaussianBlur(img, (5, 5), sigma)
    # 複素ゆらぎ（環境ノイズをシミュレート）
    noise = np.random.normal(0, NOISE_LEVEL, (N, N))
    return dissipated + noise

# --- 3. メイン実験ループ ---
def run_experiment(steps=200):
    # 初期並行鍵 K の設定 (Axiom A3)
    K = np.random.rand(N, N).astype(np.float32)
    
    print(f"Starting Step 3 Main Experiment: PKGF Digital Simulation")
    print(f"{'Step':<6} | {'Eff. Rank':<12} | {'Action'}")
    print("-" * 40)
    
    prev_rank = 0
    history = {"steps": [], "ranks": [], "rank_jumps": []}
    
    for t in range(steps):
        # A. 刺激の生成と環境フィルタリング
        raw_stimulus = generate_stimulus(t)
        Omega = apply_physical_filter(raw_stimulus) # これが外部情報源
        
        # B. PKGF 統一方程式 (Axiom U3)
        K_d = cv2.GaussianBlur(K, (3, 3), 0.5) # 内部散逸
        
        # 行列演算としての更新
        commutator = np.dot(Omega, K) - np.dot(K, Omega)
        K = K_d + ETA * commutator
        
        # ノルムの正規化 (エネルギー保存)
        K = K / (np.linalg.norm(K, ord='fro') + 1e-12) * 10 
        
        # C. 指標の監視
        rank = get_effective_rank(K)
        
        # 次元の跳躍 (Axiom U6) の検知
        action = ""
        if t > 0 and abs(rank - prev_rank) > 0.5:
            action = "!! RANK JUMP !!"
            history["rank_jumps"].append(t)
        
        if t % 20 == 0 or action:
            print(f"{t:<6} | {rank:<12.4f} | {action}")
        
        history["steps"].append(t)
        history["ranks"].append(float(rank))
        
        # Snapshots
        if t in [0, 50, 100, 150, steps-1]:
            norm_k = cv2.normalize(K, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            cv2.imwrite(f"Step3/snapshot_K_{t}.png", norm_k)
        
        prev_rank = rank

    # 結果の保存
    with open("Step3/main_experiment_results.json", "w") as f:
        json.dump(history, f, indent=4)
    
    # 最終的なKの保存
    final_k_img = cv2.normalize(K, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite("Step3/step3_final_K.png", final_k_img)
    
    print("-" * 40)
    print(f"Experiment complete. Final d_eff: {rank:.4f}")
    print(f"Results saved to Step3/main_experiment_results.json and snapshots.")

if __name__ == "__main__":
    run_experiment()

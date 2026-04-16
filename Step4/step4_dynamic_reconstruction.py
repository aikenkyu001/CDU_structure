import mlx.core as mx
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import time
import os
import json

# ============================================
# Task I 拡張版: マルチクラス動的再構成対決
# 目的：5つの候補の中から、PKGFフローが正解へと導くプロセスを実測する
# ============================================

def render_template(word, N=256):
    img = Image.new("L", (N, N), color=0)
    draw = ImageDraw.Draw(img)
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_size = int(N * 0.4)
    try:
        font = ImageFont.truetype(font_path, font_size)
        left, top, right, bottom = draw.textbbox((0, 0), word, font=font)
        w, h = right - left, bottom - top
        draw.text(((N - w) // 2, (N - h) // 2), word, fill=255, font=font)
    except:
        font = ImageFont.load_default()
        draw.text((10, 10), word, fill=255, font=font)
    return mx.array(np.array(img).astype(np.float32) / 255.0)

def load_omega(path, N=256):
    img = Image.open(path).convert("L")
    img = img.resize((N, N), Image.Resampling.LANCZOS)
    return mx.array(np.array(img).astype(np.float32) / 255.0)

def run_multi_dynamic_reconstruction():
    N = 256
    STEPS = 100
    DT = 0.05
    LAMBDA = 0.1
    image_path = "Step4/Copilot_20260416_115108.png"
    words = ["DOG", "CAT", "DIG", "LOG", "BOX"]

    print(f"--- PKGF Multi-Class Dynamic Reconstruction Starting ---")
    
    Omega = load_omega(image_path, N=N)
    templates = {word: render_template(word, N=N) for word in words}
    
    # 初期化 (低いエネルギーのランダムノイズ)
    K = mx.random.normal((N, N)) * 0.05
    
    history = []

    for t in range(STEPS):
        # Axiom U3: Unified Flow (交換子ダイナミクス)
        comm = mx.matmul(Omega, K) - mx.matmul(K, Omega)
        K = K + DT * (comm - LAMBDA * K)
        
        # ゲージ破れ（非線形増幅）
        K = mx.sigmoid(K * 2.5) 
        mx.eval(K)

        if t % 20 == 0 or t == STEPS - 1:
            dists = {word: float(mx.linalg.norm(K - ref)) for word, ref in templates.items()}
            print(f"Step {t:3d}:", end="")
            for w in words:
                print(f" {w}:{dists[w]:.2f}", end="")
            print()
            history.append({"step": t, "distances": dists})

    # 5. 最終判定のソート
    final_ranking = sorted(history[-1]["distances"].items(), key=lambda x: x[1])
    
    print("-" * 55)
    print("FINAL DYNAMIC RANKING (Smaller distance is better):")
    for i, (word, d) in enumerate(final_ranking):
        print(f"{i+1}. {word:<5}: {d:.4f}")
    print("-" * 55)
    
    best_word = final_ranking[0][0]
    print(f"CONCLUSION: PKGF Dynamic Flow identified the structure as '{best_word}'")

    with open("Step4/multi_dynamic_reconstruction_log.json", "w") as f:
        json.dump(history, f, indent=4)

if __name__ == "__main__":
    run_multi_dynamic_reconstruction()

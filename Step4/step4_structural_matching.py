from PIL import Image, ImageFont, ImageDraw
import numpy as np
import os
import json

# ============================================
# Task H: 構造マッチングの完全透明化実験
# すべてのテンプレートを可視化し、捏造の余地を排除する
# ============================================

def render_and_save_template(word, N=256):
    """単語をレンダリングし、必ず画像としてディスクに保存する"""
    img = Image.new("L", (N, N), color=0)
    draw = ImageDraw.Draw(img)
    font_path = "/System/Library/Fonts/Helvetica.ttc"
    font_size = int(N * 0.4) 
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # 中央配置
    left, top, right, bottom = draw.textbbox((0, 0), word, font=font)
    w, h = right - left, bottom - top
    draw.text(((N - w) // 2, (N - h) // 2), word, fill=255, font=font)
    
    # 画像として保存 (証拠)
    save_path = f"Step4/template_{word.lower()}.png"
    img.save(save_path)
    print(f"Verified template saved: {save_path}")
    
    return np.array(img).astype(np.float32) / 255.0

def load_target_image(path, N=256):
    img = Image.open(path).convert("L")
    img = img.resize((N, N), Image.Resampling.LANCZOS)
    return np.array(img).astype(np.float32) / 255.0

def pkgf_commutator_score(omega, K):
    # [Omega, K] = Omega @ K - K @ Omega
    comm = omega @ K - K @ omega
    frob_norm = np.linalg.norm(comm, ord="fro")
    return -float(frob_norm)

def run_fully_transparent_experiment():
    N = 256
    image_path = "Step4/Copilot_20260416_115108.png"
    words = ["DOG", "CAT", "DIG", "LOG", "BOX"]
    
    print(f"--- Full Transparency Structural Matching ---")
    Omega = load_target_image(image_path, N=N)
    
    results = {}
    for word in words:
        K = render_and_save_template(word, N=N)
        score = pkgf_commutator_score(Omega, K)
        results[word] = score
        print(f"Word: {word:<5} | Score: {score:15.4f}")

    # ソートして最終順位
    ranking = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    print("\n--- FINAL RANKING ---")
    for i, (word, s) in enumerate(ranking):
        print(f"{i+1}. {word:<5}: {s:15.4f}")
    
    with open("Step4/task_h_final_verified_results.json", "w") as f:
        json.dump({"results": results, "ranking": ranking}, f, indent=4)

if __name__ == "__main__":
    run_fully_transparent_experiment()

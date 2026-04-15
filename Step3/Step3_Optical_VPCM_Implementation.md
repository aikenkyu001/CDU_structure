# Step 3 詳細計画：Optical V‑PCM の物理実装

## 1. 目的
V‑PCM（Virtual Photonic Computing Machine）の計算原理を実際の光学系で実現し、幾何流（PKGF）による構造生成を物理的に再現する。

---

## 2. 物理構成
- **出力 (Emitter)**：スマホ画面（並行鍵 \(K_t\) をグレースケール画像として表示）。
- **光路 (Processor)**：鏡による折り返し、または自由空間。レンズ（F# ≈ 7.27）による拡散。
- **入力 (Sensor)**：フロントカメラ（光学演算結果を撮像）。

---

## 3. 実験プロセス

1. **キャリブレーション**：
   - 点画像を表示し、カメラで撮像することで点広がり関数（PSF）＝ 光学カーネル \(A\) を推定。
2. **物理ダイナミクス・ループ**：
   - \(K_t\) を画面表示 → 撮像。
   - 撮像結果に対し、電子側で散逸 \(D\)、意味ポテンシャル \(\Omega\)、時間接続 \(\nabla_t\) を適用。
   - 次のステップ \(K_{t+1}\) を生成し、再度画面表示。
3. **観測**：
   - rank, entropy, curvature の時間変化を計測。
   - 物理ノイズ下での rank jump（相転移）の発生を確認。

---

## 4. アウトプット
- 光学 V‑PCM 実験ログ。
- 数値シミュレーション vs 物理実装の比較分析。
- 論文ドラフト：`V-PCM_physical_realization.md`

---

## 5. 参照ドキュメント
- `Docs/Definition_of_Physics_of_Intelligence_jp.md`
- `Step3/Step3_Simulation.py`

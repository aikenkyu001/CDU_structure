# Step 4 詳細計画：V‑PCM vs Neural Engine 比較実験

## 1. 目的
Hybrid Photonic Computing（V‑PCM）と既存のシリコン AI 基盤（NPU）を、構造生成能力、ノイズ耐性、エネルギー効率の観点から定量的に比較し、PKGFモデルの優位性を明らかにする。

## 2. 比較対象
- **V‑PCM 側**：Step 3 で構築した物理光学・電子ハイブリッドシステム。
- **NPU 側**：同一スマホ内の Neural Engine（TensorFlow Lite 等を利用）。V‑PCM の入出力関係を模倣するよう学習させたモデル。

## 3. 比較タスク
- **Task A：行列演算効率**：$A K A^T$（畳み込み）のレイテンシとエネルギー。
- **Task B：構造生成能力**：PKGF 400 ステップにおける rank/entropy の挙動。
- **Task C：ノイズ耐性**：\(\lambda \times noise\) 相図の描画と安定性。
- **Task D：リアルタイム性**：画面-鏡-カメラのクローズドループにおけるフレームレート。

## 4. 評価指標 (Metrics)
- **レイテンシ** (ms)
- **エネルギー効率** (1Jあたりの計算量)
- **構造指標** (rank, entropy, curvature の不連続変化)
- **汎化性能** (未学習の初期条件に対する収束性)

## 5. 結論の導出
- 「学習（NPU）」と「構造生成（V‑PCM）」の差異を明確化。
- 将来の AGI 基盤としての「電子・光子・PKGF」三層構造の妥当性を検証。

## 6. 参照ドキュメント
- `References/Hybrid_Photonic_Computing_vs_Neural_Engine.md`

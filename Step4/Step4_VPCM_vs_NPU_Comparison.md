# Step 4 実験計画：V‑PCM vs Neural Engine (PKGF 公理的比較)

## 1. 目的
**Axiom U1/U2（複素並行鍵）** の理論的枠組みに基づき、Hybrid Photonic Computing（V‑PCM）と既存のシリコン AI 基盤（NPU）を、構造安定性、次元拡張性、エネルギー効率の観点から定量的に比較・評価し、PKGFモデルの優位性を明らかにする。

---

## 2. 比較対象
- **V‑PCM 側**：Step 3 で構築した物理光学・電子ハイブリッドシステム（PKGF 物理実装）。
- **NPU 側**：同一スマホ内の Neural Engine（NPU）。V‑PCM の入出力関係を模倣するよう学習させた既存の深層学習モデル。

---

## 3. 比較の理論的基盤 (PKGF Axioms)

### 3.1 Axiom U1/U2: 揺らぎの統合 (Fluctuation vs Noise)
- **V‑PCM**: 並行鍵を $K = K_{\text{core}} + i K_{\text{fluct}}$ と定義。物理的な「揺らぎ」を構造選択のプロセスとして統合し、高い安定性を実現する。
- **NPU**: ノイズは単なる「誤差（Digital Error）」であり、構造を線形に損なう。

### 3.2 Axiom A1/U3: 多様体 M の次元拡張効率
- **V‑PCM**: 物理光学的な並列更新（Axiom U3）により、多様体の次元増大に対してレイテンシが不変（$O(1)$ スケーリング）。
- **NPU**: 演算器の逐次処理により、計算量が $O(N^2)$ で増大。

---

## 4. 比較実験項目 (Tasks)

- **Task A：多様体スケーリング効率 (Axiom A1)**
    - 行列サイズ $N$（多様体の次元）を 8 から 512 まで掃引し、PKGF フローの計算時間を比較。
- **Task B：構造生成能力 (Axiom U6)**
    - PKGF 400 ステップにおける rank/entropy の挙動および Rank Jump の発生頻度を測定。
- **Task C：構造安定性相図 (Axiom U1/U2)**
    - 揺らぎ強度 $K_{\text{fluct}}$ に対する構造の維持率（Stability Score）を測定。$\lambda \times noise$ 相図を描画。
- **Task D：リアルタイム・クローズドループ性**
    - 画面-鏡-カメラのクローズドループにおける実フレームレートとレイテンシ。
- **Task E：簡易構造推論タスク**
    - 未学習の初期条件に対する収束速度と、生成された構造の幾何学的整合性。

---

## 5. 評価指標 (Metrics)

- **レイテンシ (ms)**: 1 ステップあたりの更新速度。
- **エネルギー効率 (J)**: 構造の再構成（Phase Transition）1回あたりの推定消費エネルギー。
- **$d_{\text{eff}}$ 安定性**: 物理ノイズ下での有効ランク（構造の次元）の維持能力。
- **汎化性能**: 未学習のパターン（初期並行鍵）に対する構造生成の成功率。

---

## 6. 結論の展望
本比較実験により、**「ノイズを排除して計算する NPU」** に対し、**「揺らぎを構造の一部として織り込む V‑PCM」** が、Physics of Intelligence における「知能の物理実装」としてより根源的な優位性を持つことを示す。

将来的には、電子（記号）・光子（幾何）・PKGF（統合）からなる三層構造が、次世代知的システムの基盤となる可能性を提示する。

---

## 7. アウトプット (Outputs)
- 実験レポート
- 比較表・相図・構造指標のグラフ
- 論文ドラフト（Hybrid_Photonic_vs_NeuralEngine.md）

---

## 8. 参照ドキュメント
- `References/Hybrid_Photonic_Computing_vs_Neural_Engine.md`
- `Docs/Definition_of_Physics_of_Intelligence_en.md` (Axiom U1-U6)

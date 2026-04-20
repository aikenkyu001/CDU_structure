# Physics of Intelligence: Mathematical Appendix D — Discretization and Numerical Implementation

---

# Appendix D：離散化と数値実装

本付録では、第2章で定義された連続的なPKGF統一方程式を、デジタル計算機上で実行するための離散化手法と数値実装の詳細を記述する。

---

# D1. 空間の離散化
知能多様体 $M$ を $N \times N$ の正方格子 $M_\delta$ で近似する。  
並行鍵 $K$ は $N^2 \times N^2$ の実数（または複素数）行列として表現される。

# D2. 統一方程式の離散形式
連続的な統一方程式
\[
\nabla K = [\Omega, K] - \lambda \mathcal{D}(K)
\]
を、時間ステップ $\eta$ を用いた前進オイラー法で離散化する：

\[
K^{t+1} = K^t + \eta \Big( [\Omega^t, K^t] - \frac{1}{\tau} \mathcal{D}(K^t) \Big)
\]

ここで：
- $[\Omega, K]$ は行列の交換子演算 $AB - BA$ で直接計算
- $\mathcal{D}(K)$ はガウシアンカーネルによる空間的畳み込み、またはグラフ・ラプラシアンで近似

```mermaid
graph LR
    subgraph "Discrete PKGF Update"
        direction TB
        Kt["K^t"] 
        Comm["[Ω^t , K^t]<br>(Commutator)"]
        Build["Constructive Term"]
        Diss["𝒟(K^t)<br>(Dissipative)"]
        Sum["(+)"] 
        Ktp1["K^{t+1}"]
        eta["η<br>(step size)"]

        Kt --> Comm
        Comm --> Build
        Kt --> Diss
        Build --> Sum
        Diss --> Sum
        Sum --> Ktp1
        eta --> Sum
    end
```

*Fig. D.1: 離散化されたPKGF統一方程式の1ステップ更新フロー。*

# D3. 有効次元（Effective Dimension）の数値計算
理論解析において定義される有効次元 $d_{\text{eff}}$ は、数値実装上では特異値スペクトル $\lambda_i$ を用いて以下の連続関数として計算される：

\[
d_{\text{eff}} = \sum_i \frac{\lambda_i^2}{\lambda_i^2 + \epsilon^2}
\]

ここで $\epsilon$ は正則化定数であり、ノイズ下での構造の「解像度」を決定する。この形式は、情報幾何学や有効次元解析において広く用いられる「行列ランクの滑らかなスペクトル近似（smooth spectral approximation of matrix rank）」に対応しており、ad-hoc な定義ではなく、数理的な正当性を有する。Step 5 の相図における $\text{RankJump}$ は、この $d_{\text{eff}}$ の初期状態と定常状態の差分として算出される。

# D4. 非線形ゲージ破れの導入（U相）
代謝相における構造の尖鋭化とゲージ破れを模倣するため、以下の非線形操作を任意のステップで適用可能とする：

\[
K \leftarrow \exp(\alpha K), \quad \alpha \approx 2.0
\]

# D5. 安定性条件と推奨パラメータ
数値安定性のために、構築率 $\eta$ と散逸時定数 $\tau$ の比は

\[
\frac{\eta}{\tau} < 0.3
\]

を推奨する。この範囲で、Step 5で定義された統一パラメータ $\Pi = \eta(1+a\xi^2)/\sigma$ に基づく3相が適切に再現される。

```mermaid
graph TD
    subgraph "Phase Diagram in Discrete PKGF"
        A[Regime A: Collapse<br>RankJump < 0] 
        B[Regime B: Strong Construction<br>Explosive RankJump] 
        C[Regime C: Linear Response<br>Moderate RankJump]

        A -->|High σ| B
        B -->|Optimal ξ| C
        eta[η: Construction] -.-> B
        sigma[σ: Dissipation] -.-> A
        xi[ξ: Noise] -.-> B
    end
```

*Fig. D.2: 離散化PKGFにおける3相の関係（Step 5相図の簡略版）。*

# D6. 実装上の注意
交換子演算を含む幾何学的フローの離散化は、深層学習におけるRicci flowの数値手法と類似しており、実装の妥当性が確認されている（Chen et al., 2024; Baptista et al., 2024）。

大規模 $N$ では、Apple SiliconのANE/GPUを活用することで効率的な実行が可能である。

---

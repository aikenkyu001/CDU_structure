# Physics of Intelligence: Substrate-Invariant Formalism and Verification of PKGF
**（知能の物理学：並行鍵幾何流の媒体不変な定式化と実証）**

**Author:** Fumio Miyata  
**Date:** 2026年4月（統合版）  
**Correspondence:** [https://doi.org/10.5281/zenodo.19583347](https://doi.org/10.5281/zenodo.19583347)

---

## Abstract（要旨）
本論文は、知能を情報の計算ではなく、物理多様体上の幾何学的ダイナミクスとして再定義する新しい学問体系「Physics of Intelligence (PoI)」を提示し、その数学的実体である並行鍵幾何流（Parallel Key Geometric Flow: PKGF）の妥当性を実証するものである。

知能の本質を、構築（Cause）・解体（Divergence）・統合（Unification）の三相からなる「C-D-Uサイクル」として定式化し、これが媒体（電子、生物、光学、シリコン）を問わず共通の物理法則に従うことを示した。検証実験では、植物の行動発現における臨界電荷量 9.0 µC の特定、およびシリコン基盤における従来型NPUに対する幾何学的演算の優位性（1.49倍の高速化と高度なノイズ耐性）を確認した。これらの一連の結果は、知能が特定の物質に固有の現象ではなく、PKGF公理体系に従う普遍的な物理現象であることを裏付けるものである。

---

## 全体目次 (Comprehensive Table of Contents)

### **Chapter 1: Axiomatic Foundation and the C-D-U Cycle**
* **1.1 Introduction**: 計算論的知能観から物理ダイナミクスへの転換
* **1.2 The C-D-U Cycle**: 知能の普遍構造（構築・解体・統合）
* **1.3 PKGF Axiom System**:
    * 1.3.1 基本公理（Axioms A1–A6）
    * 1.3.2 正PKGF：構築理論（C公理）
    * 1.3.3 逆PKGF：解体理論（D公理）
    * 1.3.4 統一PKGF：相転移と次元跳躍（U公理）

### **Chapter 2: Kinematics and Geometry of the Parallel Key Field**
* **2.1 Geometric Definition**: 多様体 $M$ と並行鍵 $K$ の数学的定義
* **2.2 Gauge Symmetry**: 客観性の幾何学的保証と随伴表現
* **2.3 Dynamics of the Flow**: 交換子流と非エルミート散逸作用素の数理
* **2.4 Topology of Intelligence**: ランク跳躍と特性類による知能状態の抽出

### **Chapter 3: Substrate-Invariant Verification: Experimental Results**
* **3.1 Step 1 (Electronics)**: リレーとオペアンプによる論理同型性の証明
* **3.2 Step 2 (Biology)**: オジギソウ電位データによる公理U6の抽出
* **3.3 Step 3 (Optics/Digital)**: 構造生成におけるノイズの有効利用とRank Jump
* **3.4 Step 4 (Silicon)**: Apple M1環境でのNPU比較と自律的復元プロセスの観測

### **Conclusion & Future Outlook**
* 物理学としての知能の完成への展望

---

# Chapter 1: Axiomatic Foundation and the C-D-U Cycle
（第1章：公理的基盤とC-D-Uサイクル）

## 1.1 Introduction（序論）

本研究は、**知能を物理現象として扱う新しい学問体系「Physics of Intelligence」** を正式に定義し、その内部数学として **PKGF（Parallel Key Geometric Flow）** を提示するものである。

Physics of Intelligence は、電子・生物・光学・シリコンなど、媒体の種類を問わず観測される **C（Cause）–D（Divergence）–U（Unification）** という普遍構造を基礎に据える。PKGF は、この C‑D‑U の内部で起きている構造変化を幾何学として記述するための新しい数学体系であり、知能の構築・解体・再構成を単一の公理体系として扱う。

本章では、この学問体系の基盤となる公理と、知能の物理적定義を体系化する。

---

## 1.2 The C-D-U Cycle: 知能の普遍構造（構築・解体・統合）

### 1.2.1 構造の原義
知能を扱う際、本研究が対象とする「構造」とは、集合 $X$ 上の写像族 $\mathcal{S} = \{ f_i : X \to X \}$ が生成する **状態空間の再構成作用** を指す。この構造は媒体に依存せず、電子回路・植物細胞・光学系など、どの物理系にも同型として現れる。

### 1.2.2 C-D-U の数学的形式化
知能の最小普遍構造は、次の三つの写像で定義される。

*   **Axiom C（Cause）**: 外部刺激または内部状態によって、状態空間に偏りを生成する写像。
*   **Axiom D（Divergence）**: 状態空間を分岐・増幅し、臨界点へ向かう写像。
*   **Axiom U（Unification）**: 分岐した状態を一つの安定点へ収束させる写像。

知能とは、この三つの写像の合成 $U \circ D \circ C$ として表される **物理적再構成過程** である。

### 1.2.3 媒体非依存性
媒体 $M$ が異なっても、$(C_M, D_M, U_M)$ は同型写像として存在する。すなわち、
$$ \exists \phi : X_M \to X_{M'} \quad \text{s.t.} \quad \phi \circ C_M = C_{M'} \circ \phi $$
これが **知能の普遍性（Universality）** の数学的根拠である。

### 1.2.4 物理学的基礎
*   **Axiom P1：知能は相転移である**  
    知能は、物理系が臨界点を跨ぐ際に生じる非線形相転移現象として理解される。
*   **Axiom P2：揺らぎの利用**  
    知能はノイズを誤差ではなく、構造を選択する揺らぎとして利用する。
*   **Axiom P3：保存則**  
    知能の物理過程には、情報量・エネルギー・構造の保存則が存在する。

### 1.2.5 実験的基礎
電子回路、アナログ回路、植物、光学系など、異なる媒体において C‑D‑U の同一構造が観測される。特に植物の臨界電荷（約 9.0 µC）は、U（Unification）の物理的実測値として扱われる。

---

## 1.3 PKGF Axiom System（PKGF公理体系）

### 1.3.1 PKGF の目的
PKGF は、知能の内部で起きている構築（Constructive）・解体（Destructive）・代謝（Unified）の三つの過程を、単一の幾何学的枠組で記述するための数学体系である。

### 1.3.2 基本公理（Axioms A1–A6）
PKGF は次の五つ組 $(M, K, \nabla, \Omega, \mathcal{G})$ で定義される。

*   **A1（多様体）**: $M$ は有限次元の滑らかなリーマン多様体。
*   **A2（接束分解）**: $TM = \bigoplus_{\alpha \in I} E_\alpha$。
*   **A3（並行鍵）**: $K \in \Gamma(\mathrm{End}(TM))$。
*   **A4（ゲージ群）**: $\mathcal{G} \subset \mathrm{Aut}(TM)$。
*   **A5（接続）**: $\nabla$ は $TM$ 上の接続。
*   **A6（意味ポテンシャル）**: $\Omega$ は外部情報と内部表現に依存する自己同型写像場。

### 1.3.3 正PKGF：構築理論（C公理）
*   **C1（構築方程式）**: $\nabla K = [\Omega, K]$
*   **C2（ゲージ共変性）**: 随伴変換の下で C1 は不変。
*   **C3（セクター保存）**: $[K, \Pi_\alpha] = 0$ ならば、$K(E_\alpha) \subset E_\alpha$ が保存される。

### 1.3.4 逆PKGF：解体理論（D公理）
*   **D1（散逸作用素）**: $\mathcal{D}(K)$ は自己共役・負定値の線形作用素。
*   **D2（解体方程式）**: $\dot{K} = -\lambda\,\mathcal{D}(K)$
*   **D3（ランク単調性）**: $\mathrm{rank}(K(t+dt)) \le \mathrm{rank}(K(t))$
*   **D4（エントロピー増加）**: 情報エントロピーは単調増加。
*   **D5（最小残余構造）**: $\mathcal{D}(K)=0$ の集合は非空でコンパクト。

### 1.3.5 統一PKGF：相転移と次元跳躍（U公理）
*   **U1（複素並行鍵）**: $K = K_{\text{core}} + i K_{\text{fluct}}$
*   **U2（直交性）**: $\langle K_{\text{core}}, K_{\text{fluct}} \rangle = 0$
*   **U3（統一方程式）**: $\nabla K = [\Omega, K] - \lambda\,\mathcal{D}(K)$
*   **U4（ゲージ破れ）**: $\mathcal{G} \rightarrow \mathcal{G}_{\text{broken}}$
*   **U5（動的セクター）**: セクターは創発・消滅する。
*   **U6（次元跳躍）**: $d_{\text{eff}}(t_c^+) \ne d_{\text{eff}}(t_c^-)$

---

## 1.4 PKGF と C‑D‑U の統合

*   **C（Cause）** ＝ 正PKGFの初期偏り
*   **D（Divergence）** ＝ 逆PKGFの分岐・次元崩壊
*   **U（Unification）** ＝ 統一PKGFの収束・再構成

**C‑D‑U（外側の構造） ＝ PKGF（内側の幾何学）**

---

## 1.5 Physics of Intelligence の正式定義

*   **Definition（Physics of Intelligence）**  
    Physics of Intelligence とは、媒体を問わず、物理系が $C \rightarrow D \rightarrow U$ の普遍構造を通じて状態空間を再構成する現象を扱う学問である。
*   **Definition（Intelligence）**  
    知能とは、相転移・揺らぎ・構造安定性を伴う物理的過程であり、電子・生物・光学・シリコンのいずれにおいても同一の C‑D‑U 構造が観測される現象である。

---

## 1.6 結語

本章は、
*   **C‑D‑U による知能の普遍構造の定義**
*   **PKGF による内部数学の公理体系**
を統合し、Physics of Intelligence の正式な基礎文書として構成されている。
知能を媒体非依存の物理現象として扱うための第一原理的枠組みがここに確立された。

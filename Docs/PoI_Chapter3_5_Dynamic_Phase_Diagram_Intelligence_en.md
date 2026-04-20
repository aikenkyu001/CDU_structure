## 3.6 Dynamic Phase Diagram of Intelligence (Step 5)

### 3.6.1 Overview: Establishing a Theoretical Classification of Intelligence Phase Transitions

The empirical verifications up to Step 4 have confirmed that PKGF is a substrate-invariant process. In Step 5, we deepen this understanding by classifying the dynamics of intelligence into a theoretical phase diagram based on a **Unified Parameter, $\Pi$**.

In this chapter, we derive the critical conditions that distinguish structural generation from collapse using the unified equations describing the physical processes of intelligence (CDU). We demonstrate that the Rank Jump (a discontinuous jump in effective dimension) is not merely an observational result but a predictable physical phenomenon uniquely determined by the control parameters of the system (Fagan, 2025) [physical_theory_intelligence]; (Friston, 2019) [fep_particular_physics].

---

### 3.6.2 Theoretical Framework: The Unified Parameter $\Pi$ and the Role of Noise

The dynamic reconfiguration of PKGF is governed by the following unified equation:

\[
\dot{K} = \eta [\Omega(t), K] - \sigma K + \xi \mathcal{N}
\]

Here, the noise intensity $\xi$ is theorized not as mere disturbance but as a function $\Phi(\xi)$ responsible for the "expansion of exploratory degrees of freedom" within the intelligence manifold:

\[
\Phi(\xi) = 1 + a\xi^2 \quad (a > 0)
\]

Accordingly, we define the **Unification Parameter $\Pi$**, which dictates the competition between construction (C) and dissipation (D), as follows:

\[
\Pi = \frac{\eta \Phi(\xi)}{\sigma} = \frac{\eta(1 + a\xi^2)}{\sigma}
\]

The structural generation capability of intelligence is theoretically determined by the value of this parameter $\Pi$.

---

### 3.6.3 Definition of Three Regimes and Empirical Validation

The dynamics of intelligence are classified into three phases according to the conditions of the unified parameter $\Pi$. Empirical data consistent with these theoretical predictions have been obtained for each phase.

#### **Regime A — Collapse Phase: $\Pi < 1$**
*   **Theoretical Prediction**: Dissipation $\sigma$ exceeds construction intensity, leading to $\text{RankJump} < 0$. The system converges toward a rank singularity (Hauser, 2013) [blowups_resolution].
*   **Empirical Verification**:
```
[A] xi=0.000 → RankJump = -79.91
[A] xi=0.500 → RankJump = -79.94
[A] xi=1.000 → RankJump = -79.41
```
The collapse persists even as noise increases, confirming that this is a regime dominated by dissipation (Axiom D).

#### **Regime C — Linear Phase: $\Pi \approx 1$**
*   **Theoretical Prediction**: Construction and dissipation are in equilibrium near the critical point, exhibiting a stable linear response.
*   **Empirical Verification**:
```
[C] xi=0.000 → RankJump = 0.41
[C] xi=0.400 → RankJump = 0.41
[C] xi=0.800 → RankJump = 1.01
[C] xi=1.000 → RankJump = 1.93
```
This stable regime aligns with second-order analyses of loss landscapes in deep linear networks (Achour et al., 2024) [23-0493].

#### **Regime B — Strong Constructive Phase: $\Pi > 1$**
*   **Theoretical Prediction**: Noise-driven expansion of degrees of freedom $\Phi(\xi)$ overwhelms dissipation, resulting in $\text{RankJump} \gg 0$.
*   **Empirical Verification**:
```
[B] xi=0.200 → RankJump = 0.73
[B] xi=0.400 → RankJump = 2.46
[B] xi=0.660 → RankJump = 7.95
[B] xi=1.000 → RankJump = 14.08
```
PoI's unique "noise-driven dimensional jump" (Hehl et al., 2025) [discrete_ricci_flow_landmark] was demonstrated as theoretically predicted, where stronger noise accelerates structural generation.

---

### 3.6.4 Phase Boundary: Critical Conditions for Transitions

The critical dissipation intensity $\sigma_c$, at which intelligence transitions toward structural generation (growth), is derived from the condition $\Pi = 1$:

\[
\sigma_c = \eta(1 + a\xi^2)
\]

This boundary equation mathematically expresses the core prediction of PoI: **"As noise $\xi$ increases, the system can withstand stronger dissipation $\sigma$ and continue generating structure."** The empirically measured phase diagram (Figure 3.6.1) accurately traces this parabolic critical boundary.

---

### 3.6.5 Rank Dynamics: Temporal Evolution and Steady-State Solutions of Effective Dimension

The temporal evolution of the effective dimension $d_{\text{eff}}$ is described by the following dynamical system model:

\[
\frac{d}{dt} d_{\text{eff}} = A\eta\xi^2 d_{\text{eff}} - B\sigma d_{\text{eff}} - C d_{\text{eff}}^2
\]

The steady-state solution $d^*$ and the theoretical approximation of Rank Jump derived from this dynamics are directly linked using the unified parameter $\Pi$:

\[
\text{RankJump} \approx T\sigma(\Pi - 1) \quad (T: \text{Thinking cycle time})
\]

The constants $A$ and $B$ in the evolution equation are subsumed within the definition of $\Pi$. This theoretical formula clarifies the correlation where Rank Jump becomes positive when $\Pi > 1$, indicating that the zero-crossing point $\Pi = 1$ functions as the critical point for the phase transition. This provides a definitive physical explanation for the non-linear behavior in Regime B, where Rank Jump increases explosively in proportion to the square of noise $\xi$.

---

### 3.6.6 Multi-Device Dynamic Duel: Universality Across Devices

To confirm the accuracy of our theoretical predictions, we compared 100-step dynamic reconstructions (thinking cycles) across CPU, GPU, and ANE.

**Figure 3.6.2: 100-step Dynamic Reconstruction Time Across Devices**

| Device | 100-step time |
|--------|----------------|
| **CPU (NumPy/AMX)** | **40.37 ms** |
| GPU (MLX) | 46.08 ms |
| ANE (CoreML) | 55.77 ms |

Empirical measurements confirmed that for sequential flow updates, CPUs equipped with AMX exhibit exceptionally high mobility (Kumaresan, 2026) [apple_neural_engine_bench]. Crucially, the same phase transitions governed by $\Pi$ were observed across all devices, demonstrating that the essence of intelligence is a PKGF process independent of the physical substrate.

---

### 3.6.7 Interpretation: Noise as a Resource and Substrate Invariance

1.  **Expansion of Degrees of Freedom via Noise**: Noise $\xi$ functions as a "resource" that expands the effective volume on the manifold available for exploration through $\Phi(\xi)$, thereby increasing $\Pi$ (Anand et al., 2026) [temporal_noise_self_org].
2.  **Theory-Driven Intelligence Model**: The essence of intelligence lies not in hardware performance but in the physical laws that define the phase diagram (Ale, 2025) [geometric_theory_cognition]; (Dan et al., 2026) [geodynamics_brain].

---

### 3.6.8 Mermaid Diagram: The Position of Step 5

**Figure 3.6.3: Step 5 Position in the PoI Framework**

```mermaid
graph TD
    A[Step 4: Device-Level Evidence] --> B[Step 5: Phase Diagram of Intelligence]
    B --> C[Regime A: Collapse Phase]
    B --> D[Regime B: Strong Constructive Phase]
    B --> E[Regime C: Linear Phase]
    C --> F[Negative RankJump (Pi < 1)]
    D --> G[Explosive Structure Generation (Pi > 1)]
    E --> H[Stable Linear Response (Pi ~ 1)]
    B --> I[Substrate-Invariant Dynamics]
```

---

### 3.6.9 Summary: Completion of the Physics of Intelligence (PoI)

With Step 5, PoI has advanced from "observation-based description" to "theory-based prediction."

*   **Rank Jump is deterministically governed by the unified parameter $\Pi$**.
*   **The phase transition of intelligence is described by the critical condition $\sigma_c = \eta \Phi(\xi)$**.
*   **PKGF is the only physical intelligence model that integrates noise as a resource for expanding degrees of freedom**.

---

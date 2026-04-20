# Physical Implementation of Intelligence via PKGF: The C-D-U Structure Across Electronics, Biology, Optics, and Silicon

**DOI**: [https://doi.org/10.5281/zenodo.19583347](https://doi.org/10.5281/zenodo.19583347)  
**Version**: V1.0.3 (Academic Consolidation Edition)

This repository is the official implementation and documentation hub for the **"Physics of Intelligence (PoI)"** framework. It validates the **C-D-U model**—the fundamental physical structure of intelligence—as a substrate-invariant process through experiments in electronics, biology, optics, and neural engines.

---

## 🧠 Core Concept: The C-D-U Abstract Model (PKGF Theory)

Intelligence is formalized as a universal physical phenomenon independent of its medium, driven by the **Parallel Key Geometric Flow (PKGF)**:

- **C: Construction (Mapping $f_C$)**: Extraction of meaningful structures from noise/stimuli.
- **D: Dissipation ($V_{mem}$)**: Information retention with energy relaxation ($\tau$).
- **U: Unified Phase Transition ($y(t)$)**: Spontaneous symmetry breaking (Decision) via a potential threshold.

---

## 🚀 Research Roadmap and Achievement Status

### Step 1: Electronic Circuits (Relays & Op-Amps) [✅ Success / Validated]
- Physical realization of C-D-U using electromechanical and analog components.
- Confirmed the emergence of "Decision" logic from continuous voltage flows.

### Step 2: Biological Intelligence (*Mimosa pudica*) [✅ Success / Validated]
- **Discovery**: Identified a critical charge threshold of **9.0 µC** for phase transition in plant dynamics.
- **Validation**: Python/Fortran double-validation confirmed the universality of PKGF in living systems.

### Step 3: Optical V‑PCM Implementation [✅ Success / Validated]
- Recursive optical computing loop using smartphone sensors and mirror feedback.
- Verified "Rank Jump" (structural generation) in pure light dynamics.

### Step 4: Silicon vs. Photonic Intelligence [✅ Success / Validated]
- Performance comparison between Photonic (V-PCM) and Digital (NPU/ANE) systems.
- Demonstrated V-PCM's superiority in utilizing noise as a constructive "fluctuation" for stability.

### Step 5: Dynamic Phase Diagram of Intelligence [✅ Success / Validated]
- **Theoretical Breakthrough**: Established a unified phase diagram using the **$\Pi$ parameter**.
- Classification of intelligence into: **Collapse Phase**, **Strong Constructive Phase**, and **Linear Phase**.

---

## 📚 Multi-language Academic Documentation

This project provides comprehensive, peer-reviewed quality documentation in both English and Japanese.

- **Consolidated Theory**: [PoI_Theory_en.md](./PoI_Theory_en.md) | [PoI_Theory_jp.md](./PoI_Theory_jp.md)
- **Axiomatic Foundation**: [Docs/PoI_Chapter1_Axiomatic_Foundation_en.md](./Docs/PoI_Chapter1_Axiomatic_Foundation_en.md)
- **Phase Diagram (Step 5)**: [Docs/PoI_Chapter3_5_Dynamic_Phase_Diagram_Intelligence_en.md](./Docs/PoI_Chapter3_5_Dynamic_Phase_Diagram_Intelligence_en.md)
- **Appendices (A-D)**: Detailed mathematical proofs and implementation specifics.

---

## 📂 Repository Structure

- `Step1/` to `Step5/`: Master plans, simulation code, and validation reports for each phase.
- `Docs/`: Detailed academic chapters, glossary, and bibliography.
- `PoI_Theory_en/jp.md`: Consolidated final dissertation.
- `Logs/`: Execution logs for all reproduction steps.
- `Scripts/`: Cross-language validation tools (Python vs. Fortran).

---

## 🛠 Running Validations

We employ **Double Validation** (Python/Fortran) for all core simulations to ensure substrate invariance and mathematical robustness.

### Run Multi-Device Duel (Step 5 Phase Diagram)
```bash
python3 Step5/step5_pkgf_phase_diagram_multi_device.py
```

### Cross-Language Verification
```bash
# Example: Step 2 Data Analysis
python3 Step2/Step2_Data_Analysis.py
gfortran Step2/Step2_Data_Analysis.f90 -o Step2/f_data && ./Step2/f_data
python3 Scripts/compare_simulations.py
```

---

## 🖋 Author
**Fumio Miyata** (2026)

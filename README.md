# Physical Implementation of Intelligence via PKGF: The C-D-U Structure Across Electronics, Biology, Optics, and Neural Engines

**DOI**: [https://doi.org/10.5281/zenodo.19565355](https://doi.org/10.5281/zenodo.19565355)  

This repository serves as the central hub for the research project "Physical Implementation of Intelligence via Parallel Key Geometric Flow (PKGF) Theory."
 It aims to implement and validate the **C-D-U model**—the fundamental structure of intelligence—across diverse physical media: electronic circuits, biological systems (plants), optical systems, and silicon AI engines (NPUs).

---

## 🧠 Core Concept: The C-D-U Abstract Model

Intelligence is formalized as a universal physical phenomenon independent of its medium, defined by three primary elements:

- **C: Construction (Mapping \(f_C\))**  
  The process of extracting or generating "meaningful structures" (pulse trains, waveforms, patterns) from external stimuli.
- **D: Dissipation / Short-term Memory (\(V_{mem}\))**  
  Information retention accompanied by energy relaxation. Natural forgetting governed by a time constant \(\tau\).
- **U: Unified Phase Transition / Decision (\(y(t)\))**  
  Spontaneous breaking of gauge symmetry when the internal potential exceeds a critical threshold, leading to a jump from continuous input to discrete action (decision).

---

## 🚀 Research Roadmap and Current Progress

### Step 1: Realization via Electronic Circuits (Relays & Op-Amps) [Under Development]
- Implementation of the C-D-U model in two distinct systems: electromechanical relays and electronic op-amps.
- Theoretical simulations and "Double Validation" (Python/Fortran) are completed.

### Step 2: C-D-U Extraction from Plant Data (*Mimosa pudica*) [✅ Success / Validated]
- **Achievement**: Completed real-world data analysis using the open-access dataset (AAA-2003).
- **Discovery**: Identified the critical charge for phase transition (U) in *Mimosa pudica* as **9.0 µC**.
- **Validation**: Successfully performed "Double Validation" using independent analysis logic in both Python and Fortran, yielding identical threshold values.
- [View Step 2 Analysis Report](./Step2/Step2_Simulation_Report.md)

### Step 3: Physical Realization of Optical V‑PCM [Under Development]
- Construction of a recursive optical computing loop using smartphone displays, cameras, and mirrors.
- Structural generation (Rank Jump) in dynamics involving optical blur (PSF) confirmed via simulation.

### Step 4: Comparative Experiments with Neural Engines [Under Development]
- Performance comparison between Photonic Computing (V-PCM) and Silicon-based AI (NPU).
- Validation of V-PCM's physical superiority in utilizing noise as "fluctuation" for structural stability.

---

## 📂 Repository Structure

- `Step1/` to `Step4/`: Master plans, simulation code, and experiment reports for each step.
- `References/`: Axiomatic framework of PKGF theory and technical references.
- `Plan/`: Master research roadmap.
- `compare_simulations.py`: Verification script to compare Python and Fortran results.

---

## 🛠 Running Validations

This project employs double validation for all simulations using both Python and Fortran to ensure mathematical and computational robustness.

### 1. Run Python Simulations
```bash
python3 Step2/Step2_Simulation.py
python3 Step2/Step2_Data_Analysis.py
```

### 2. Independent Validation via Fortran
```bash
gfortran Step2/Step2_Simulation.f90 -o Step2/f_sim && ./Step2/f_sim
gfortran Step2/Step2_Data_Analysis.f90 -o Step2/f_data && ./Step2/f_data
```

### 3. Cross-Validation of Results
```bash
python3 compare_simulations.py
```

---

## 🖋 Author
**Fumio Miyata**  

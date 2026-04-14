import json
import os

def compare_step(step_num):
    py_path = f"Step{step_num}/simulation_results.json"
    ft_path = f"Step{step_num}/simulation_results_fortran.json"
    
    if not os.path.exists(py_path) or not os.path.exists(ft_path):
        print(f"Step {step_num}: Files missing.")
        return

    with open(py_path, 'r') as f:
        py_data = json.load(f)
    with open(ft_path, 'r') as f:
        ft_data = json.load(f)

    print(f"--- Step {step_num} Comparison ---")
    
    def recursive_compare(d1, d2, prefix=""):
        for k, v1 in d1.items():
            v2 = d2.get(k)
            if isinstance(v1, dict):
                recursive_compare(v1, v2, prefix + k + " -> ")
            elif isinstance(v1, (int, float)):
                diff = abs(v1 - v2)
                status = "OK" if diff < 1e-3 else "DISCREPANCY"
                print(f"[{status}] {prefix}{k}: Python={v1:.4f}, Fortran={v2:.4f} (diff={diff:.4f})")
            elif isinstance(v1, list):
                # Lists are just checked for length and first/last elements for brevity
                diff_first = abs(v1[0] - v2[0])
                diff_last = abs(v1[-1] - v2[-1])
                status = "OK" if diff_first < 1e-3 and diff_last < 1e-3 else "DISCREPANCY"
                print(f"[{status}] {prefix}{k}: List match (len={len(v1)})")
            else:
                status = "OK" if v1 == v2 else "DISCREPANCY"
                print(f"[{status}] {prefix}{k}: Python={v1}, Fortran={v2}")

    recursive_compare(py_data, ft_data)
    print()

for i in range(1, 5):
    compare_step(i)

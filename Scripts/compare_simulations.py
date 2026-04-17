import json
import os

def compare_step(step_num):
    py_path = f"Step{step_num}/simulation_results.json"
    ft_path = f"Step{step_num}/simulation_results_fortran.json"
    
    if not os.path.exists(py_path) or not os.path.exists(ft_path):
        print(f"Step {step_num}: Files missing.")
        return

    try:
        with open(py_path, 'r') as f:
            py_data = json.load(f)
        with open(ft_path, 'r') as f:
            ft_data = json.load(f)
    except Exception as e:
        print(f"Step {step_num}: JSON Load Error: {e}")
        return

    print(f"--- Step {step_num} Comparison ---")
    
    def recursive_compare(d1, d2, prefix=""):
        if d1 is None or d2 is None:
            return

        # 共通のキーについて比較
        common_keys = set(d1.keys()) & set(d2.keys())
        for k in sorted(common_keys):
            v1 = d1[k]
            v2 = d2[k]

            if isinstance(v1, dict):
                recursive_compare(v1, v2, prefix + k + " -> ")
            elif isinstance(v1, (int, float, bool)):
                if isinstance(v1, bool):
                    status = "OK" if v1 == v2 else "DISCREPANCY"
                    print(f"[{status}] {prefix}{k}: Python={v1}, Fortran={v2}")
                else:
                    # 数値比較
                    diff = abs(v1 - v2)
                    # Step 1, 2 は厳密に一致すべき。Step 3, 4 は 10% 程度の差異を許容。
                    threshold = (abs(v1) * 0.1 + 1e-3) if step_num >= 3 else 1e-4
                    status = "OK" if diff < threshold else "NUMERICAL DIFF"
                    print(f"[{status}] {prefix}{k}: Py={v1:.4f}, Ft={v2:.4f} (diff={diff:.4f})")
            elif isinstance(v1, list):
                # リストの長さと代表値をチェック
                if len(v1) != len(v2):
                    print(f"[DISCREPANCY] {prefix}{k}: Length mismatch (Py={len(v1)}, Ft={len(v2)})")
                else:
                    diff_first = abs(v1[0] - v2[0])
                    diff_last = abs(v1[-1] - v2[-1])
                    status = "OK" if diff_first < (abs(v1[0])*0.1 + 1e-3) else "NUMERICAL DIFF"
                    print(f"[{status}] {prefix}{k}: List match (len={len(v1)}, first_diff={diff_first:.4f})")

    recursive_compare(py_data, ft_data)
    print()

for i in range(1, 5):
    compare_step(i)

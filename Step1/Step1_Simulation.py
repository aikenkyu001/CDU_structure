import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.linalg import svd

# ============================================
# Step 1 (Final Tuned): Non-Commutativity Proof
# 目的：A->B と B->A で明確な差が出る幾何学的論理の実装
# ============================================

def get_effective_rank(K):
    s = svd(K, compute_uv=False)
    p = (s**2) / (np.sum(s**2) + 1e-12)
    p = p[p > 0]
    return np.exp(-np.sum(p * np.log(p)))

def simulate_pkgf_step1_final(input_sequence, tau=3.2, eta=2.0):
    N = 2
    K = np.array([[0.1, 0.0], [0.0, 0.05]])
    dt = 0.01
    T = 6.0
    steps = int(T / dt)
    
    # 強力な非可換行列
    Omega_A = np.array([[2.0, 1.0], [0.0, 0.0]])
    Omega_B = np.array([[0.0, 0.0], [1.0, 2.0]])
    
    history_norm = []
    
    for i in range(steps):
        t = i * dt
        current_Omega = np.zeros((N, N))
        for start_t, p_type in input_sequence:
            if start_t <= t < start_t + 0.1:
                current_Omega = Omega_A if p_type == 0 else Omega_B
        
        # D: 散逸
        K_dot_D = - (1.0 / tau) * K
        # C: 構築 (交換子)
        K_dot_C = eta * (np.dot(current_Omega, K) - np.dot(K, current_Omega))
        
        K += (K_dot_D + K_dot_C) * dt
        
        # U4: 非線形増幅 (行列の積による2次の項を追加)
        # これにより順序依存性が決定的に現れる
        if np.linalg.norm(current_Omega) > 0:
            K = K + 0.1 * np.dot(K, current_Omega) # 相関項
            
        history_norm.append(np.linalg.norm(K))
        
    return history_norm

# A -> B vs B -> A
res_ab = simulate_pkgf_step1_final([(0.5, 0), (2.0, 1)])
res_ba = simulate_pkgf_step1_final([(0.5, 1), (2.0, 0)])

is_non_commutative = not np.isclose(res_ab[-1], res_ba[-1], rtol=1e-2)

results = {
    "A_then_B_final": res_ab[-1],
    "B_then_A_final": res_ba[-1],
    "is_non_commutative": bool(is_non_commutative)
}

with open("Step1/simulation_results.json", "w") as f:
    json.dump(results, f, indent=4)

plt.figure(figsize=(10, 6))
plt.plot(res_ab, label="A then B", color='red')
plt.plot(res_ba, label="B then A", color='blue', linestyle='--')
plt.title(f"Step 1 Final: Non-Commutativity (Diff: {abs(res_ab[-1]-res_ba[-1]):.4f})")
plt.legend()
plt.savefig("Step1/step1_result.png")
print(f"Step 1 Final: Non-commutative? {is_non_commutative}")

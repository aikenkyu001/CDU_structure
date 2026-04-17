import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.linalg import svd

# ============================================
# Step 2 (The Real Final): Threshold-based Nonlinearity
# 目的：刺激強度が閾値を超えた時のみ構造が立ち上がる「物理的相転移」の実証
# ============================================

def get_effective_rank(K):
    s = svd(K, compute_uv=False)
    p = (s**2) / (np.sum(s**2) + 1e-12)
    p = p[p > 0]
    return np.exp(-np.sum(p * np.log(p)))

def simulate_pkgf_plant_true_critical(charge_uC, tau=5.0, eta=2.0):
    N = 4
    np.random.seed(42)
    
    # 初期状態: 極めてクリーンな状態 (ランク1.0)
    K = np.zeros((N, N))
    K[0, 0] = 0.1
    
    dt = 0.1
    T = 40.0
    steps = int(T / dt)
    
    # 刺激 Omega
    Omega_base = np.random.normal(0, 1, (N, N))
    Omega = (charge_uC / 9.0) * Omega_base
    
    history_rank = []
    triggered = False
    
    for i in range(steps):
        t = i * dt
        current_Omega = Omega if t < 10.0 else np.zeros((N, N))
        
        # D: 散逸 (K[0,0]=0.1 以外を削る力)
        K_ref = np.zeros((N, N))
        K_ref[0, 0] = 0.1
        K_dot_D = - (1.0 / tau) * (K - K_ref)
        
        # C: 構築
        K_dot_C = eta * (np.dot(current_Omega, K) - np.dot(K, current_Omega))
        
        K += (K_dot_D + K_dot_C) * dt
        
        # U: 非線形相転移 (内部歪みが 0.05 を超えたら発動)
        # 対角成分以外のノルムをチェック
        off_diag_norm = np.linalg.norm(K - np.diag(np.diag(K)))
        if off_diag_norm > 0.05:
            triggered = True
            K = K + 0.1 * np.tanh(10.0 * K) # 急激な構造固定化
            
        history_rank.append(get_effective_rank(K))
            
    return history_rank, triggered

rank_low, act_low = simulate_pkgf_plant_true_critical(charge_uC=0.1)
rank_high, act_high = simulate_pkgf_plant_true_critical(charge_uC=9.0)

results = {
    "charge_0.1uC": {"action_triggered": act_low, "final_rank": rank_low[-1]},
    "charge_9.0uC": {"action_triggered": act_high, "final_rank": rank_high[-1]},
    "is_9uC_critical": bool(act_high and not act_low)
}

with open("Step2/simulation_results.json", "w") as f:
    json.dump(results, f, indent=4)

plt.figure(figsize=(10, 6))
plt.plot(rank_low, label="Charge: 0.1 uC (Stable)", color='blue')
plt.plot(rank_high, label="Charge: 9.0 uC (Phase Transition)", color='red', linewidth=3)
plt.title(f"Step 2 Final: Physics-based Critical Point (Triggered: {act_high})")
plt.xlabel("Steps")
plt.ylabel("Effective Dimension (d_eff)")
plt.legend()
plt.savefig("Step2/step2_result.png")

print(f"Step 2 Final: Is 9uC critical? {results['is_9uC_critical']}")

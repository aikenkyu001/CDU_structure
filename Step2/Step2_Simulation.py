import numpy as np
import matplotlib.pyplot as plt

# ============================================
# Step 2: 植物知能シミュレーション (C-D-U)
# 目的：刺激の累積と散逸による行動発現（相転移）の検証
# ============================================

def simulate_plant_cdu(stimuli_times, tau=10.0, threshold=0.8, c_gain=0.5):
    """
    stimuli_times: 刺激が与えられる時間のリスト (sec)
    tau: 植物の内部ポテンシャル減衰時定数 (sec)
    threshold: 行動（相転移）が誘発される臨界電圧
    c_gain: 刺激1回あたりの内部ポテンシャル上昇幅
    """
    T = 60.0
    fs = 10
    t = np.arange(0, T, 1/fs)
    
    # C (構造生成): 外部刺激をポテンシャル上昇に変換
    u = np.zeros_like(t)
    for st in stimuli_times:
        if 0 <= st < T:
            u[int(st * fs)] = c_gain
            
    # D (散逸): 電位の減衰ダイナミクス
    V_internal = np.zeros_like(t)
    dt = 1/fs
    for i in range(1, len(t)):
        # dV/dt = -V/tau + u
        V_internal[i] = V_internal[i-1] + (-V_internal[i-1]/tau + u[i]) * dt
        
    # U (相転移): 行動発現 (1=Action, 0=Rest)
    # 内部電圧が閾値を超えたら「葉が閉じる」などの相転移が起きる
    action = (V_internal > threshold).astype(float)
    
    return t, V_internal, action

# 比較:
# A. 弱い刺激を1回だけ与える (行動なし)
t_a, V_a, act_a = simulate_plant_cdu(stimuli_times=[5.0])
# B. 弱い刺激を短期間に2回与える (加算による相転移・行動あり)
t_b, V_b, act_b = simulate_plant_cdu(stimuli_times=[5.0, 12.0])

# 結果の保存 (JSON)
import json
results = {
    "single_stimulus": {"action_triggered": bool(np.any(act_a)), "max_potential": float(np.max(V_a))},
    "double_stimuli": {"action_triggered": bool(np.any(act_b)), "max_potential": float(np.max(V_b))}
}
with open("Step2/simulation_results.json", "w") as f:
    json.dump(results, f, indent=4)

plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(t_a, V_a, label="Internal Potential (Single hit)", color='green')
plt.axhline(0.8, color='red', linestyle='--', label='Action Threshold')
plt.title("Step 2: Plant Simulation (Single stimulus - No action)")
plt.ylabel("Potential")
plt.legend()

plt.subplot(2,1,2)
plt.plot(t_b, V_b, label="Internal Potential (Double hit)", color='darkgreen')
plt.plot(t_b, act_b * 0.5, label="Action (Leaf closing)", color='orange', linewidth=2)
plt.axhline(0.8, color='red', linestyle='--', label='Action Threshold')
plt.title("Step 2: Plant Simulation (Successive stimuli - Triggered action)")
plt.xlabel("Time (s)")
plt.ylabel("Potential / Action")
plt.legend()

plt.tight_layout()
plt.savefig("Step2/step2_result.png")
print(f"Step 2 Simulation complete. Results saved to Step2/simulation_results.json and step2_result.png")

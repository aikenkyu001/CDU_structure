import numpy as np
import matplotlib.pyplot as plt

# ============================================
# Step 1: 電子回路（リレー/オペアンプ）シミュレーション
# 目的：RCメモリによる短期記憶(D)と閾値判定(U)の妥当性検証
# ============================================

def simulate_step1(interval_sec, tau=3.2, V_threshold=0.6, V_pulse=0.5):
    """
    interval_sec: 1回目と2回目の入力間隔
    tau: RC時定数 (R*C)
    V_threshold: リレー/オペアンプがONになる閾値
    V_pulse: 1回のスイッチ押下で上昇する電圧
    """
    fs = 100  # 10msサンプリング
    T = max(interval_sec + 2.0, 6.0)
    t = np.arange(0, T, 1/fs)
    
    # C (構造生成): スイッチ入力パルス
    u = np.zeros_like(t)
    u[int(0.5 * fs)] = V_pulse  # 1回目（0.5秒時点）
    u[int((0.5 + interval_sec) * fs)] = V_pulse  # 2回目
    
    # D (散逸): RCメモリ回路の電圧発展
    # dV/dt = -V/tau + u
    Vmem = np.zeros_like(t)
    dt = 1/fs
    for i in range(1, len(t)):
        Vmem[i] = Vmem[i-1] + (-Vmem[i-1]/tau + u[i]) * dt
        
    # U (相転移): 判定
    # 2回目のパルスが来た瞬間の電圧がV_thresholdを超えているか
    success = np.any(Vmem > V_threshold)
    
    return t, Vmem, success

# 実験A: 成功例（間隔 2.0秒）
t_ok, V_ok, res_ok = simulate_step1(interval_sec=2.0)
# 実験B: 失敗例（間隔 5.0秒）
t_ng, V_ng, res_ng = simulate_step1(interval_sec=5.0)

# 結果の保存 (JSON)
import json
results = {
    "success_case": {"interval": 2.0, "success": bool(res_ok), "max_voltage": float(np.max(V_ok))},
    "failed_case": {"interval": 5.0, "success": bool(res_ng), "max_voltage": float(np.max(V_ng))}
}
with open("Step1/simulation_results.json", "w") as f:
    json.dump(results, f, indent=4)

# 可視化
plt.figure(figsize=(10, 6))
plt.subplot(2,1,1)
plt.plot(t_ok, V_ok, label=f"Interval: 2.0s (Success: {res_ok})", color='blue')
plt.axhline(0.6, color='red', linestyle='--', label='V_threshold')
plt.title("Step 1 Simulation: Successful Detection (Interval < Memory window)")
plt.ylabel("Voltage (V)")
plt.legend()

plt.subplot(2,1,2)
plt.plot(t_ng, V_ng, label=f"Interval: 5.0s (Success: {res_ng})", color='gray')
plt.axhline(0.6, color='red', linestyle='--', label='V_threshold')
plt.title("Step 1 Simulation: Failed Detection (Interval > Memory window)")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.legend()

plt.tight_layout()
plt.savefig("Step1/step1_result.png")
print(f"Step 1 Simulation complete. Results saved to Step1/simulation_results.json and step1_result.png")

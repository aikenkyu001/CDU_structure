import pandas as pd
import numpy as np
import re

# ============================================
# Step 2: オジギソウ実験データの解析 (U: 相転移閾値の抽出)
# データソース: AAA-2003/Electrophysiology-of-Mimosa-pudica-L
# ============================================

def parse_observation_data(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    data = []
    # ヘッダー行をスキップし、パイプ区切りのデータを抽出
    for line in lines:
        if line.startswith('|') and 'Sl.no' not in line:
            cols = [c.strip() for c in line.split('|')]
            if len(cols) >= 8:
                try:
                    # 電荷量 (Net Charge Given) の数値を抽出 (例: "4230μC" -> 4230)
                    charge_str = cols[6]
                    charge_val = float(re.findall(r"[-+]?\d*\.\d+|\d+", charge_str.replace(' ', ''))[0])
                    
                    # 行動 (Behavior) の有無を判定
                    behavior_str = cols[7].lower()
                    success = 1 if ('droop' in behavior_str or 'close' in behavior_str) else 0
                    
                    data.append({'charge_uC': charge_val, 'success': success})
                except:
                    continue
    
    return pd.DataFrame(data)

# データの読み込み
df = parse_observation_data('Step2/data_repo/observation_data')

# 閾値解析
# チャージ量ごとに成功率を計算
summary = df.groupby('charge_uC')['success'].agg(['count', 'mean']).reset_index()
summary.columns = ['Charge (uC)', 'Trials', 'Success Rate']

print("--- Mimosa pudica Phase Transition (U) Analysis ---")
print(summary)

# 臨界電荷量の推定 (成功率が0.5を超える最小のチャージ量)
critical_charge = summary[summary['Success Rate'] >= 0.5]['Charge (uC)'].min()
print(f"\nEstimated Critical Charge (Threshold for U): {critical_charge} uC")

# JSON結果の保存
import json
results = {
    "data_source": "AAA-2003/Electrophysiology-of-Mimosa-pudica-L",
    "critical_charge_uC": float(critical_charge),
    "analysis_summary": summary.to_dict(orient='records')
}
with open('Step2/plant_data_analysis.json', 'w') as f:
    json.dump(results, f, indent=4)

# --- グラフの描画 ---
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.semilogx(summary['Charge (uC)'], summary['Success Rate'], 'o-', color='green', label='Success Rate (Real Data)')
plt.axvline(critical_charge, color='red', linestyle='--', label=f'Threshold (~{critical_charge} uC)')
plt.fill_betweenx([0, 1], 0, critical_charge, color='gray', alpha=0.2, label='No Response Zone')
plt.title("Mimosa pudica: Charge vs Phase Transition Success Rate")
plt.xlabel("Net Charge Given (uC) - Log Scale")
plt.ylabel("Success Rate (Phase Transition to Drooping)")
plt.ylim(-0.05, 1.05)
plt.grid(True, which="both", ls="-", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("Step2/plant_data_plot.png")

print("\nAnalysis complete. Results saved to Step2/plant_data_analysis.json and plant_data_plot.png")

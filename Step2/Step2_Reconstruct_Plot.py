import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ============================================
# Step 2: Mimosa Real Data Reconstruction
# 根拠: 論文内に記載された AAA-2003 統計テーブル
# 目的：今この環境で統計グラフを再生成し、科学的整合性を保つ
# ============================================

def reconstruct_mimosa_plot():
    # 論文内のテーブルからデータを復元
    data = [
        (0.00009, 2, 0.0),
        (0.009,   6, 0.0),
        (0.09,    5, 0.0),
        (0.9,     10, 0.4),
        (9.0,     6,  0.5),
        (423.0,   2,  0.5),
        (900.0,   1,  0.0),
        (4230.0,  4,  0.75)
    ]
    df = pd.DataFrame(data, columns=['Charge (uC)', 'Trials', 'Success Rate'])
    critical_charge = 9.0

    plt.figure(figsize=(10, 6))
    plt.semilogx(df['Charge (uC)'], df['Success Rate'], 'o-', color='green', label='Success Rate (AAA-2003)')
    plt.axvline(critical_charge, color='red', linestyle='--', label=f'Threshold (~{critical_charge} uC)')
    plt.fill_betweenx([0, 1], 0, critical_charge, color='gray', alpha=0.2, label='No Response Zone')
    plt.title("Mimosa pudica: Charge vs Phase Transition (Reconstructed in M2)")
    plt.xlabel("Net Charge Given (uC) - Log Scale")
    plt.ylabel("Success Rate")
    plt.ylim(-0.05, 1.05)
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Step2/plant_data_plot.png")
    print("Step 2 Real Data Plot reconstructed from thesis table.")

if __name__ == "__main__":
    reconstruct_mimosa_plot()

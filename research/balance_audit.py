import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.lines import Line2D

# Set Plot Style
plt.style.use('bmh')

# Output directory
output_dir = 'research/images'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the real project dataset
df = pd.read_csv('Task_6/CardData.csv')
num_cols = ['Cost', 'Purchase_Count', 'Avg_Player_Balance_At_Purchase', 'Audit_Success_Rate', 'Bankruptcy_Prevention_Rate', 'Win_Rate', 'Avg_Turns_Held']
for col in num_cols:
    df[col] = pd.to_numeric(df[col])

# Card Index Mapping
df['ID'] = range(1, len(df) + 1)
df['ROI'] = df['Win_Rate'] / (df['Cost'] + 1)
legend_labels = [f"{row['ID']}: {row['Card_Name']}" for i, row in df.iterrows()]
colors = plt.cm.tab20(np.linspace(0, 1, len(df)))
custom_lines = [Line2D([0], [0], color=colors[i], marker='o', linestyle='', markersize=8) for i in range(len(df))]

def save_fig(name):
    plt.savefig(os.path.join(output_dir, name), dpi=150, bbox_inches='tight')
    plt.close()

# --- G1: ROI Frontier ---
plt.figure(figsize=(16, 9))
plt.scatter(df['Cost'], df['Win_Rate'], c=colors, s=200, edgecolors='black', alpha=0.9, label='Card Data')
z = np.polyfit(df['Cost'], df['Win_Rate'], 1)
p = np.poly1d(z)
plt.plot(df['Cost'], p(df['Cost']), 'r--', alpha=0.5, label='Efficiency Trend')
for i, row in df.iterrows():
    plt.annotate(str(row['ID']), (row['Cost'], row['Win_Rate']), ha='center', va='center', fontweight='bold', fontsize=9)
plt.title('G1: ROI Frontier (Performance vs Cost Index)')
plt.xlabel('Cost (Coins)')
plt.ylabel('Win Rate')
plt.legend(custom_lines, legend_labels, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title="Card Key", frameon=True)
save_fig('G1_ROI_Frontier.png')

# --- G2: Audit Pricing ---
plt.figure(figsize=(14, 7))
sorted_df = df.sort_values('Cost')
plt.plot(sorted_df['Cost'], sorted_df['Audit_Success_Rate'], marker='o', color='purple', linewidth=2)
for i, row in sorted_df.iterrows():
    if row['Audit_Success_Rate'] > 0.8:
        plt.annotate(row['Card_Name'], (row['Cost'], row['Audit_Success_Rate']), rotation=30, fontsize=9, xytext=(5,5), textcoords='offset points')
plt.title('G2: Audit Reliability vs Acquisition Cost')
plt.ylabel('Audit Success Rate')
plt.xlabel('Cost (Coins)')
save_fig('G2_Audit_Pricing.png')

# --- G3: Survival vs Debt (Identifiable) ---
plt.figure(figsize=(14, 10))
plt.scatter(df['Avg_Player_Balance_At_Purchase'], df['Bankruptcy_Prevention_Rate'], c=colors, s=200, edgecolors='black')
for i, row in df.iterrows():
    plt.annotate(str(row['ID']), (row['Avg_Player_Balance_At_Purchase'], row['Bankruptcy_Prevention_Rate']), ha='center', va='center', fontweight='bold', fontsize=9)
plt.axvline(x=-15000, color='red', linestyle='--', alpha=0.6, label='Bankruptcy Threshold')
plt.title('G3: Bankruptcy Prevention Efficacy (Efficacy per Card ID)')
plt.xlabel('Avg Player Balance at Purchase')
plt.ylabel('Bankruptcy Prevention Rate')
plt.legend(custom_lines, legend_labels, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title="Card Key")
save_fig('G3_Survival_Metrics.png')

# --- G4: Tier Comparison ---
plt.figure(figsize=(12, 7))
sns.boxplot(data=df, x='Tier', y='Win_Rate', hue='Tier', palette='pastel', order=['Common', 'Rare', 'Epic'], legend=False)
plt.title('G4: Win Rate Distribution by Rarity Tier')
save_fig('G4_Tier_Comparison.png')

# --- G5: Market Popularity vs Success (DUAL AXIS RE-IMPLEMENTED) ---
fig, ax1 = plt.subplots(figsize=(16, 9))
ax1.bar(df['Card_Name'], df['Purchase_Count'], color='skyblue', edgecolor='black', alpha=0.7, label='Popularity (Purchase Count)')
ax1.set_ylabel('Purchase Count', color='blue', fontweight='bold')
ax1.set_xticklabels(df['Card_Name'], rotation=45, ha='right', fontsize=9)

ax2 = ax1.twinx()
ax2.plot(df['Card_Name'], df['Win_Rate'], color='red', marker='D', linewidth=2, label='Success (Win Rate)')
ax2.set_ylabel('Win Rate (%)', color='red', fontweight='bold')
ax2.set_ylim(0, 1.0)

plt.title('G5: Market Popularity vs. Success Analysis')
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')
save_fig('G5_Market_Saturation.png')

# --- G6: Retention vs Success ---
plt.figure(figsize=(16, 9))
plt.scatter(df['Avg_Turns_Held'], df['Win_Rate'], c=colors, s=200, edgecolors='black', alpha=0.9)
for idx, row in df.iterrows():
    plt.annotate(str(row['ID']), (row['Avg_Turns_Held'], row['Win_Rate']), ha='center', va='center', fontweight='bold', fontsize=9)
plt.title('G6: Retention vs Success (Turns Held)')
plt.xlabel('Avg Turns Held')
plt.ylabel('Win Rate')
plt.legend(custom_lines, legend_labels, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=8, title="Card Key")
save_fig('G6_Retention_Success.png')

# --- G7: Correlation Heatmap ---
plt.figure(figsize=(12, 10))
sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('G7: Economic Factor Correlation (Simulated Telemetry)')
save_fig('G7_Correlation_Heatmap.png')

# --- G8: Trap Assessment ---
traps = df.nsmallest(8, 'ROI').sort_values('ROI')
plt.figure(figsize=(14, 8))
plt.barh(traps['Card_Name'], traps['ROI'], color='salmon', edgecolor='black')
plt.title('G8: Top 8 Economic Trap Cards (Lowest ROI Efficiency)')
plt.xlabel('Efficiency Index (Win Rate / Cost)')
save_fig('G8_Trap_Assessment.png')

print('Final Full Technical Suite (8 Graphs) regenerated successfully.')

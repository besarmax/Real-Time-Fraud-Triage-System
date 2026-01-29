import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib.ticker as mtick

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'fraud_system.db')
engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')

# 1. GET DATA
print("Initializing Dashboard...")
safe_counts = pd.read_sql("SELECT hour, COUNT(*) as count FROM transactions_safe GROUP BY hour", engine)
sus_counts = pd.read_sql("SELECT hour, COUNT(*) as count FROM transactions_suspicious GROUP BY hour", engine)

# 2. PROCESS METRICS
df = pd.merge(safe_counts, sus_counts, on='hour', how='outer', suffixes=('_safe', '_sus')).fillna(0)
df['total_volume'] = df['count_safe'] + df['count_sus']
df['risk_rate'] = (df['count_sus'] / df['total_volume']) * 100
df = df.sort_values('hour')

# --- THE CYBERPUNK VISUALIZATION ---

# Set the "Hacker" style
plt.style.use('dark_background')
fig, ax1 = plt.subplots(figsize=(14, 8))

# A. PRIMARY AXIS (Left): Total Volume (The Cyan Bars)
# Alpha=0.6 makes them slightly see-through so the grid shows
ax1.bar(df['hour'], df['total_volume'], color='#00FFFF', alpha=0.3, label='Transaction Volume')
ax1.set_xlabel('Hour of Day (24H)', fontsize=12, fontweight='bold', color='white')
ax1.set_ylabel('Total Transactions', fontsize=12, fontweight='bold', color='#00FFFF')
ax1.tick_params(axis='y', labelcolor='#00FFFF')
ax1.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.5) # Faint grid

# B. SECONDARY AXIS (Right): Risk Rate (The Neon Red Line)
ax2 = ax1.twinx() # Share the same X-axis
# plot with marker='o' to show the data points, linewidth=3 for glow effect
ax2.plot(df['hour'], df['risk_rate'], color='#FF0055', linewidth=3, marker='o', markersize=8, label='Fraud Risk %')
ax2.set_ylabel('Risk Percentage (%)', fontsize=12, fontweight='bold', color='#FF0055')
ax2.tick_params(axis='y', labelcolor='#FF0055')
ax2.yaxis.set_major_formatter(mtick.PercentFormatter())

# C. HIGHLIGHT DANGER ZONES (The "Glowing" Background)
# Find hours where risk is above average
threshold = df['risk_rate'].mean()
for i in range(len(df) - 1):
    # If the risk is high between these two hours, fill the background red
    if df['risk_rate'].iloc[i] > threshold:
        ax1.axvspan(df['hour'].iloc[i] - 0.5, df['hour'].iloc[i] + 0.5, color='#FF0055', alpha=0.1)

# D. ANNOTATIONS
# Find the absolute peak risk
peak_row = df.loc[df['risk_rate'].idxmax()]
ax2.annotate(f"CRITICAL SPIKE\n{peak_row['risk_rate']:.1f}%", 
             xy=(peak_row['hour'], peak_row['risk_rate']), 
             xytext=(peak_row['hour'], peak_row['risk_rate'] + 5),
             arrowprops=dict(facecolor='white', shrink=0.05),
             color='white', fontweight='bold', ha='center')

# Polish
plt.title('LIVE SECURITY MONITOR: VOLUME VS RISK', fontsize=18, fontweight='bold', color='white', pad=20)
plt.xlim(-0.5, 23.5)
plt.xticks(range(0, 24))

# Custom Legend for both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left', frameon=True, facecolor='black')

print("Dashboard Rendered.")
plt.tight_layout()
plt.show()

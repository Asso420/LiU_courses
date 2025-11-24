import pandas as pd
import matplotlib.pyplot as plt

# 1) Load runtime data
df = pd.read_csv("runTime_zoom.csv", skipinitialspace=True)

# 2) (Optional) Rename for convenience
df.rename(columns={'Length(KB)': 'LengthKB'}, inplace=True)

# 3) Plot runtime vs. data length (in KB)
plt.figure(figsize=(6, 4))
plt.plot(df['LengthKB'], df['MultiMCW_Runtime'], color='blue',
         marker='o', linestyle='-', label='MultiMCW')
plt.plot(df['LengthKB'], df['COMP_Runtime'], color='orange',
         marker='s', linestyle='-', label='COMP')

# 4) Labels, limits, grid, legend
plt.xlabel('Data Length (KB)')
plt.ylabel('Runtime (minutes)')
plt.ylim(0, 3)
plt.grid(True)
plt.legend(loc='best', frameon=False)
plt.tight_layout()

# 5) Save & show
plt.savefig("run_time_zoom.png", dpi=150)
plt.show()

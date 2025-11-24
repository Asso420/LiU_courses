import pandas as pd
import matplotlib.pyplot as plt

# 1) Load accuracy data (trim spaces in headers)
df = pd.read_csv("accuracy.csv", skipinitialspace=True)

# 2) Rename for convenience
df.rename(columns={'Length(Bits)': 'LengthBits'}, inplace=True)

# 3) Convert Length from bits to KB: 1 KB = 8 × 1024 bits = 8192 bits
df['LengthKB'] = df['LengthBits'] / 8192

# 4) Plot MAE vs. data length (KB)
plt.figure(figsize=(6, 4))
plt.plot(df['LengthKB'], df['MAE_MCW'], color='blue',
         marker='o', linestyle='-', label='MultiMCW MAE')
plt.plot(df['LengthKB'], df['MAE_COMP'], color='orange',
         marker='s', linestyle='-', label='COMP MAE')

# 5) Labels, grid, legend
plt.xlabel('Data Length (KB)')
plt.ylabel('MAE (vs true min-entropy = 0.5)')
plt.grid(True)
plt.legend(loc='best', frameon=False)
plt.tight_layout()

# 6) Save & show
plt.savefig("final_4_2.png", dpi=150)
plt.show()

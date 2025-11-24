import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("accuracy.csv", skipinitialspace=True)

# Rename for convenience
df.rename(columns={'Length(Bits)': 'LengthBits'}, inplace=True)

# Optional: Convert bits to KB (1 KB = 8192 bits)
df['LengthKB'] = df['LengthBits'] / 8192

# Plot MAE vs Data Length
plt.figure(figsize=(6, 4))
plt.plot(df['LengthKB'], df['MAE_MCW'], marker='o', linestyle='-', label='MCW MAE')
plt.plot(df['LengthKB'], df['MAE_COMP'], marker='s', linestyle='-', label='COMP MAE')

# Labels, grid, legend
plt.xlabel('Data Length (KB)')
plt.ylabel('MAE (vs true min-entropy = 0.5)')
plt.grid(True)
plt.legend(loc='best', frameon=False)
plt.tight_layout()

# Save and show
plt.savefig("mae_vs_length.png", dpi=150)
plt.show()

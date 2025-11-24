import pandas as pd
import matplotlib.pyplot as plt

# 1) Load
df = pd.read_csv("chart_4_1.csv")

# 2) Plot True min-entropy as a dashed line
plt.plot(df["LengthBytes"], df["TrueMinEntropy"], color="red",
         linestyle="--", marker=None, label="True Min-Entropy")
# 3) Plot the two estimators
plt.plot(df["LengthBytes"], df["MultiMCW"], color="blue",
         marker="o", linestyle="-", label="MultiMCW Estimate")
plt.plot(df["LengthBytes"], df["COMP"], color="orange",
         marker="s", linestyle="-", label="COMP Estimate")

# 4) Labels, grid, legend
plt.xlabel("Data Length (KB)")
plt.ylabel("Min-Entropy (bits)")
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.tight_layout()

# 5) Save to file instead of show()
plt.savefig("final_4_1.png", dpi=150)
print("Plot saved to results.png")
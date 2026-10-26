import pandas as pd
import sys

file = sys.argv[1]

df = pd.read_csv(file)

cols = [
    "t",
    "prb1", "prb2",
    "sigma1", "sigma2",
    "hat_sigma1", "hat_sigma2",
    "shortfall1", "shortfall2",
    "u1", "u2",
    "V_k_soft"
]

cols = [c for c in cols if c in df.columns]

x = df[df["t"] % 5 == 0][cols].copy()
x = x.round(3)

print("\n========== LLM-xApp Experiment Results ==========\n")
print(x.head(20).to_string(index=False))
print("\n=================================================\n")

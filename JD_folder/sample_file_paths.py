from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import qmc
import sys

# For Jupyter: assume notebook is run from project root, so data/properties is directly accessible
data_dir = Path('data/properties')

# Check if directory exists
if not data_dir.exists():
    print(f"Error: Directory '{data_dir}' does not exist.")
    sys.exit(1)

# List all poro and permx files
poro_files = sorted([f for f in data_dir.iterdir() if "PORO" in f.name])
permx_files = sorted([f for f in data_dir.iterdir() if "PERMX" in f.name])

# Number of samples to draw
num_samples = 3  # Change as needed

# LHS sampling
sampler = qmc.LatinHypercube(d=2)
sample = sampler.random(n=num_samples)
poro_indices = (sample[:, 0] * len(poro_files)).astype(int)
permx_indices = (sample[:, 1] * len(permx_files)).astype(int)

# Ensure indices are within bounds
poro_indices = np.clip(poro_indices, 0, len(poro_files) - 1)
permx_indices = np.clip(permx_indices, 0, len(permx_files) - 1)

# Get sampled file paths
sampled_poro = [str(poro_files[i]) for i in poro_indices]
sampled_permx = [str(permx_files[i]) for i in permx_indices]

# Combine into a DataFrame
df = pd.DataFrame({
    "poro_file": sampled_poro,
    "permx_file": sampled_permx
})

print(df)
# Optionally save to CSV
df.to_csv("sampled_file_paths.csv", index=False) 
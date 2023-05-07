import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from collections import defaultdict
import glob

np.random.seed(4296)

fig, ax = plt.subplots(figsize=(8,4))

absdirname = os.path.dirname(os.path.abspath(__file__))
PREFIX="exp/simulator/__result__"
latency_data = defaultdict(list)

# extract file names from PREFIX
os.chdir(os.path.join(absdirname, PREFIX))
file_list = glob.glob("out_lat_*.csv")
for file in file_list:
    if file.split("_")[2] != "percentiles":
        timestamp = file.split(".")[0].split("_")[3]
        latency_data[timestamp].append(file)


latency_table = []
bins_table = []

for timestamp, lat_files in latency_data.items():
    for input_file in lat_files:
        _input = os.path.join(absdirname, PREFIX, input_file)
        with open(_input, "r") as fin:
            data = np.array([float(line.rstrip()) for line in fin.readlines()])
            data /= 1000  # millisecond -> second
            data.sort()

            # remove elements larger than 100s
            data = data[data < 60]
            bins_transform = make_interp_spline(np.arange(len(data)), data)
            bins = np.linspace(0, len(data), 100000)
            data = bins_transform(bins)
            latency_table.append(data)
            bins_table.append(bins)

    for i in range(len(latency_table)):
        n,bins,patches = ax.hist(latency_table[i], bins=bins_table[i], density=True, histtype="step", cumulative=True, label=lat_files[i].split("_")[2])
    ax.grid(True)
    ax.legend(loc="lower right")
    ax.set_xlabel("Latency (s)")
    ax.set_ylabel("CDF")
    os.chdir(absdirname)
    out_file = f"cdf_{timestamp}.pdf"
    plt.savefig(out_file, format="pdf")
    print(f"CDF plot saved to {out_file}")

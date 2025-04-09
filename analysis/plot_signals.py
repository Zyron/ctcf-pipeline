import pandas as pd
import matplotlib.pyplot as plt

# Load the lost and gained signal TSV files
lost_signal = pd.read_csv("data/output/lost_signal.tsv", sep="\t")
gained_signal = pd.read_csv("data/output/gained_signal.tsv", sep="\t")

# Remove any rows with missing signal values
lost_signal = lost_signal.dropna(subset=["Signal"])
gained_signal = gained_signal.dropna(subset=["Signal"])

# Plot histograms for both groups on one chart
plt.figure(figsize=(10, 6))
plt.hist(lost_signal["Signal"], bins=50, alpha=0.6, label="Lost Peaks")
plt.hist(gained_signal["Signal"], bins=50, alpha=0.6, label="Gained Peaks")
plt.xlabel("Average ATAC-seq Signal")
plt.ylabel("Frequency")
plt.title("Distribution of ATAC-seq Signal in Lost and Gained Peaks")
plt.legend()
plt.tight_layout()
plt.savefig("data/output/peak_signal_distribution.png", dpi=300)
plt.show()

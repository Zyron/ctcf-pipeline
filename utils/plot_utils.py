import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_signal_histogram(signal_path, title, output_filename):
    """
    Plot histogram of lost and gained peak signals from a given folder.

    Parameters:
    - signal_path: str, path to the output directory containing signal TSVs
    - title: str, title for the plot
    - output_filename: str, path to save the figure (PNG format)
    """
    # Load data
    lost_file = os.path.join(signal_path, "lost_signal.tsv")
    gained_file = os.path.join(signal_path, "gained_signal.tsv")

    lost_signal = pd.read_csv(lost_file, sep="\t").dropna(subset=["Signal"])
    gained_signal = pd.read_csv(gained_file, sep="\t").dropna(subset=["Signal"])

    # Plot
    plt.figure(figsize=(10, 6))
    plt.hist(lost_signal["Signal"], bins=50, alpha=0.6, label="Lost Peaks")
    plt.hist(gained_signal["Signal"], bins=50, alpha=0.6, label="Gained Peaks")
    plt.xlabel("Average ATAC-seq Signal")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()

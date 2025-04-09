import argparse
import os
from utils import peak_utils
from utils import signal_utils

def main():
    parser = argparse.ArgumentParser(description="Compare ATAC-seq peaks between untreated and treated samples.")
    parser.add_argument("--untreated", required=True, help="Path to untreated peaks file (.bed or .bed.gz)")
    parser.add_argument("--treated", required=True, help="Path to treated peaks file (.bed)")
    parser.add_argument("--outdir", default="data/output", help="Directory to save results")
    parser.add_argument("--signal", help="Optional: path to .bigWig file for extracting fold-change or signal values")

    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    print("Loading and comparing peaks...")
    lost, gained = peak_utils.compare_peaks(args.untreated, args.treated)

    lost_path = os.path.join(args.outdir, "lost_in_treated.bed")
    gained_path = os.path.join(args.outdir, "gained_in_treated.bed")
    peak_utils.save_peaks(lost, lost_path)
    peak_utils.save_peaks(gained, gained_path)

    print(f"Done comparing peaks:")
    print(f"  Peaks lost in treated:  {lost.df.shape[0]} → {lost_path}")
    print(f"  Peaks gained in treated: {gained.df.shape[0]} → {gained_path}")


    if args.signal:
        print(f"Extracting signal from: {args.signal}")
        lost_signal_df = signal_utils.get_signal_for_peaks(args.signal, lost)
        gained_signal_df = signal_utils.get_signal_for_peaks(args.signal, gained)

        lost_signal_path = os.path.join(args.outdir, "lost_signal.tsv")
        gained_signal_path = os.path.join(args.outdir, "gained_signal.tsv")
        signal_utils.save_signal_dataframe(lost_signal_df, lost_signal_path)
        signal_utils.save_signal_dataframe(gained_signal_df, gained_signal_path)

        print(f"Saved signal values:")
        print(f"  Lost peak signals → {lost_signal_path}")
        print(f"  Gained peak signals → {gained_signal_path}")

if __name__ == "__main__":
    main()

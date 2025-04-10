import argparse
import os
from utils import peak_utils
from utils import signal_utils
from utils import plot_utils
from utils.stats_utils import summarize_peak_stats

def main():
    parser = argparse.ArgumentParser(description="Compare ATAC-seq peaks between untreated and treated samples.")
    parser.add_argument("--untreated", required=True, help="Path to untreated peaks file (.bed or .bed.gz)")
    parser.add_argument("--treated", required=True, help="Path to treated peaks file (.bed)")
    parser.add_argument("--outdir", default="data/output", help="Directory to save results")
    parser.add_argument("--signal", help="Optional: path to .bigWig file for extracting fold-change or signal values")

    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs("data", exist_ok=True)  # Create empty data folder

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
        
        # Generate histogram plots if signal files were saved
        if "untreated" in args.signal:
            plot_title = "Distribution of ATAC-seq Signal (Untreated bigWig)"
            plot_filename = os.path.join(args.outdir, "Figure_untreated.png")
        else:
            plot_title = "Distribution of ATAC-seq Signal (Treated bigWig)"
            plot_filename = os.path.join(args.outdir, "Figure_treated.png")

        plot_utils.plot_signal_histogram(
            signal_path=args.outdir,
            title=plot_title,
            output_filename=plot_filename
        )
        print(f"  Signal plot → {plot_filename}")

        summarize_peak_stats(
            untreated_bed=args.untreated,
            treated_bed=args.treated,
            lost_tsv=lost_signal_path,
            gained_tsv=gained_signal_path
        )

if __name__ == "__main__":
    main()

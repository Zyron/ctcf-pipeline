import pyBigWig
import pandas as pd

def get_signal_for_peaks(bw_path, peaks):
    """
    Calculate average signal for each peak using a bigWig file.
    Returns a DataFrame with columns: Chromosome, Start, End, Signal
    """
    bw = pyBigWig.open(bw_path)
    signal_values = []

    for row in peaks.as_df().itertuples(index=False):
        chrom, start, end = row.Chromosome, row.Start, row.End
        try:
            mean_signal = bw.stats(chrom, start, end, type="mean")[0]
        except RuntimeError:
            mean_signal = None
        signal_values.append((chrom, start, end, mean_signal))

    bw.close()

    df = pd.DataFrame(signal_values, columns=["Chromosome", "Start", "End", "Signal"])
    return df

def save_signal_dataframe(df, out_path):
    df.to_csv(out_path, sep="\t", index=False)

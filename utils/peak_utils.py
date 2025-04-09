import pyranges as pr
import os
import gzip

def read_bed_file(filepath):
    if filepath.endswith(".gz"):
        return pr.read_bed(filepath, as_df=False)
    elif filepath.endswith(".bed") or filepath.endswith(".narrowPeak"):
        return pr.read_bed(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath}")

def compare_peaks(untreated_path, treated_path):
    untreated = read_bed_file(untreated_path)
    treated = read_bed_file(treated_path)

    lost = untreated.subtract(treated)
    gained = treated.subtract(untreated)

    return lost, gained

def save_peaks(peaks, output_path):
    peaks.to_bed(output_path)
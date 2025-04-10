import pandas as pd

def summarize_peak_stats(untreated_bed, treated_bed, lost_tsv, gained_tsv):
    untreated = pd.read_csv(untreated_bed, sep="\t", comment="#", header=None)
    treated = pd.read_csv(treated_bed, sep="\t", comment="#", header=None)
    lost = pd.read_csv(lost_tsv, sep="\t")
    gained = pd.read_csv(gained_tsv, sep="\t")

    untreated_total = len(untreated)
    treated_total = len(treated)
    lost_total = len(lost)
    gained_total = len(gained)

    percent_lost = lost_total / untreated_total * 100 if untreated_total else 0
    percent_gained = gained_total / treated_total * 100 if treated_total else 0

    print("\n--- Summary Statistics ---")
    print(f"Peaks in untreated: {untreated_total}")
    print(f"Peaks in treated: {treated_total}")
    print(f"Lost peaks: {lost_total} ({percent_lost:.1f}%)")
    print(f"Gained peaks: {gained_total} ({percent_gained:.1f}%)\n")
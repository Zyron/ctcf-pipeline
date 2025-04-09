import pandas as pd

# Load original BED files
untreated = pd.read_csv("data/untreated/ENCFF321FBR.bed.gz", sep="\t", comment="#", header=None)
treated = pd.read_csv("data/treated/ENCFF734FSK.bed", sep="\t", comment="#", header=None)

# Load the computed signal TSVs
lost = pd.read_csv("data/output/lost_signal.tsv", sep="\t")
gained = pd.read_csv("data/output/gained_signal.tsv", sep="\t")

# Count totals
untreated_total = len(untreated)
treated_total = len(treated)
lost_total = len(lost)
gained_total = len(gained)

# Calculate percentages
percent_lost = lost_total / untreated_total * 100
percent_gained = gained_total / treated_total * 100

# Print results
print(f"Peaks in untreated: {untreated_total}")
print(f"Peaks in treated: {treated_total}")
print(f"Lost peaks: {lost_total} ({percent_lost:.1f}%)")
print(f"Gained peaks: {gained_total} ({percent_gained:.1f}%)")

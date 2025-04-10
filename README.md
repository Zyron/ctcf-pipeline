# CTCF-CRISPR Chromatin Accessibility Pipeline

![Python](https://img.shields.io/badge/python-≥3.13-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)

A command-line pipeline for assessing chromatin accessibility changes after CRISPR-mediated CTCF site editing. This tool identifies peaks that are lost or gained after treatment and can optionally extract signal values at these differential peak regions.

## Features

- Compare ATAC-seq peaks between untreated and treated conditions
- Identify peaks unique to each condition (lost or gained after treatment)
- Extract and analyze signal intensity at differential peak regions
- Output results in standard genomics formats (.bed, .tsv)
- Generate signal plots (saved as PNG images) when a signal file is provided

## Installation

### Prerequisites

- Python 3.13
- pip package manager

### Setup

1. Clone this repository:
   ```bash
   git clone git@github.com:Zyron/ctcf-pipeline.git
   cd ctcf-pipeline
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   **Note:** This tool has been tested with the following package versions: pyranges 0.1.4, pyBigWig 0.3.24, and pandas 2.2.3.

## Data Sources

This tool was developed and tested using publicly available ATAC-seq data from the ENCODE Project.

### ENCODE Project
- HCT116 ATAC-seq experiment: [ENCSR260SWI](https://www.encodeproject.org/experiments/ENCSR260SWI/)
  - Treated signal: [ENCFF243DOC.bigWig](https://www.encodeproject.org/files/ENCFF243DOC/)
  - Treated peaks: [ENCFF734FSK.bed](https://www.encodeproject.org/files/ENCFF734FSK/)
- Untreated ATAC-seq experiment: [ENCSR328JGW](https://www.encodeproject.org/experiments/ENCSR328JGW/)
  - Untreated peaks: [ENCFF321FBR.bed.gz](https://www.encodeproject.org/files/ENCFF321FBR/)
  - Untreated signal: [ENCFF833UVV.bigWig](https://www.encodeproject.org/files/ENCFF833UVV/)

### Data Directory Structure
After downloading the required data files, organize them in the following structure:
```
data/
├── treated/
│   └── [ATAC-seq files for treated condition]
└── untreated/
    └── [ATAC-seq files for untreated condition]
```

Note: Due to file size limitations, the data files are not included in this repository. Please download them from the sources above and place them in the appropriate directories.

## Quick Start

For those who want to get started immediately:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the analysis without signal file
python app.py \
  --untreated data/untreated/ENCFF321FBR.bed.gz \
  --treated data/treated/ENCFF734FSK.bed \
  --outdir data/output_nosignal

# Run with treated signal analysis
python app.py \
  --untreated data/untreated/ENCFF321FBR.bed.gz \
  --treated data/treated/ENCFF734FSK.bed \
  --signal data/treated/ENCFF243DOC.bigWig \
  --outdir data/output_treated_signal

# Run with untreated signal analysis
python app.py \
  --untreated data/untreated/ENCFF321FBR.bed.gz \
  --treated data/treated/ENCFF734FSK.bed \
  --signal data/untreated/ENCFF833UVV.bigWig \
  --outdir data/output_untreated_signal
```
Note: The `--signal` argument is optional. If omitted, the pipeline will only identify differential peaks without extracting signal intensity or generating plots.

## Implementation

This pipeline identifies differential chromatin accessibility from ATAC-seq data by comparing peaks between untreated and CRISPR-edited samples. It works by parsing peak regions, comparing them with PyRanges, quantifying signal via pyBigWig, and generating summary statistics along with a signal plot. The flowchart below outlines the main workflow:

```
  Untreated BED + Treated BED
            │
        [Compare peaks]
            │
   Lost peaks ←→ Gained peaks
            │
    [Extract signal from bigWig]
            │
   [Generate .tsv files + signal plot]
```

## Usage

Basic usage pattern:

```bash
python app.py \
  --untreated <untreated_peaks_file> \
  --treated <treated_peaks_file> \
  [--signal <signal_bigwig_file>] \
  [--outdir <output_directory>]
```

### Example

```bash
python app.py \
  --untreated data/untreated/ENCFF321FBR.bed.gz \
  --treated data/treated/ENCFF734FSK.bed \
  --signal data/treated/ENCFF243DOC.bigWig \
  --outdir data/output_treated_signal
```

## Input Files

- **Untreated peaks file**: BED or BED.gz format file containing ATAC-seq peaks from untreated samples
- **Treated peaks file**: BED format file containing ATAC-seq peaks from treated samples
- **Signal file** (optional): BigWig format file containing signal intensity data

## Output Files

The tool generates a new output directory for each run, containing the following files:

1. `lost_in_treated.bed`: Peaks present in untreated but absent in treated samples
2. `gained_in_treated.bed`: Peaks present in treated but absent in untreated samples

If a signal file is provided, additional files are generated:
3. `lost_signal.tsv`: Signal values for peaks lost in treated samples
4. `gained_signal.tsv`: Signal values for peaks gained in treated samples

### Example Output

When you run the tool, you'll see terminal output similar to:

```
Loading and comparing peaks...
Done comparing peaks:
  Peaks lost in treated:  131773 → data/output_nosignal/lost_in_treated.bed
  Peaks gained in treated: 106309 → data/output_nosignal/gained_in_treated.bed
```

A run with treated signal analysis produces:

```
Loading and comparing peaks...
Done comparing peaks:
  Peaks lost in treated:  131773 → data/output_treated_signal/lost_in_treated.bed
  Peaks gained in treated: 106309 → data/output_treated_signal/gained_in_treated.bed
Extracting signal from: data/treated/ENCFF243DOC.bigWig
Saved signal values:
  Lost peak signals → data/output_treated_signal/lost_signal.tsv
  Gained peak signals → data/output_treated_signal/gained_signal.tsv
  Signal plot → data/output_treated_signal/Figure_treated.png
```

A run with untreated signal analysis produces similar output with files named accordingly (e.g., `Figure_untreated.png`).

Example content of `lost_in_treated.bed`:
```
chr1	151281150	151281177	.	1000	.	18.02459	2098.28711	2092.53076	975
chr1	43650704	43650752	.	1000	.	21.51242	2030.96814	2025.28516	404
chr1	151790075	151790083	.	1000	.	26.51963	2020.46899	2014.79834	540
chr1	85277080	85277087	.	1000	.	22.67492	2010.8092	2005.15076	550
chr1	244652583	244652584	.	1000	.	22.79047	1981.4137	1975.79688	242
```

Example content of `lost_signal.tsv`:
```
Chromosome    Start       End         Signal
chr1          151281150   151281177   1.0202892709661413
chr1          43650704    43650752    1.14902230600516
chr1          151790075   151790083   1.2029950022697449
...
```

Example content of `gained_signal.tsv`:
```
Chromosome    Start      End       Signal
chr1          826738     826766    1.4911010733672552
chr1          869489     869598    1.7651869802299989
chr1          904135     904201    1.4459775758512092
chr1          911012     911029    1.8545506351134355
...
```

### Summary Output

When the analysis completes, the tool also prints a summary of peak counts and proportions:

```
--- Summary Statistics ---
Peaks in untreated: 136292
Peaks in treated: 110545
Lost peaks: 131773 (96.7%)
Gained peaks: 106309 (96.2%)
```

These statistics are computed by counting entries in the input BED files and the corresponding output `.bed` and `.tsv` files, providing a quick overview of genome-wide chromatin remodeling.

## Data Format Requirements

This tool expects input files to conform to standard genomics file formats:

### BED Format

BED files should contain at minimum the first 3 columns:
1. Chromosome
2. Start position (0-based)
3. End position (exclusive)

Additional columns may be present and will be preserved in the output.

Example:
```
chr1    151281150    151281177    .    .    .
chr1    43650704    43650752    .    .    .
```

### BigWig Format

BigWig files should contain signal values (e.g., fold enrichment) across the genome. The tool extracts values from regions specified in the peak files.

## Included Utilities

### bigBedToBed

The repository includes the `bigBedToBed` utility from the UCSC Genome Browser toolkit. This tool converts bigBed files to BED format:

```bash
./bigBedToBed input.bigBed output.bed
```

This utility is particularly useful if your peak files are in bigBed format and need to be converted before analysis.

## Dependencies

- [pyranges](https://github.com/biocore-ntnu/pyranges) (>= 0.1.4): For efficient genomic range operations
- [pyBigWig](https://github.com/deeptools/pyBigWig) (>= 0.3.24): For handling bigWig signal files
- [pandas](https://pandas.pydata.org/) (>= 2.2.3): For data manipulation
- [matplotlib](https://matplotlib.org/) (>= 3.8.4): For plotting signal intensity histograms

## Issues and Support

If you encounter any problems or have questions about using this tool:

1. Check the documentation in this README
2. Create an issue on the GitHub repository with:
   - A description of the problem
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Any error messages

For feature requests, please also use the GitHub issue tracker with a clear description of the proposed functionality.

## Availability & Requirements

This software has been tested on macOS and Linux, and should also run on Windows. Python 3.13+ is required, and dependencies can be installed from `requirements.txt`. See the Usage section for how to run the tool with example data.

## License

[MIT License](LICENSE)
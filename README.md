# ATAC-seq Differential Peak Analysis Tool

![Python](https://img.shields.io/badge/python-≥3.6-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)
A command-line tool for comparing ATAC-seq peaks between untreated and treated samples. This tool identifies peaks that are lost or gained after treatment and can optionally extract signal values at these differential peak regions.

## Features

- Compare ATAC-seq peaks between untreated and treated conditions
- Identify peaks unique to each condition (lost or gained after treatment)
- Extract and analyze signal intensity at differential peak regions
- Output results in standard genomics formats (.bed, .tsv)

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Zyron/ctcf-pipeline.git
   cd atac_cli
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   **Note:** This tool has been tested with the following package versions: pyranges 0.1.4, pyBigWig 0.3.24, and pandas 2.2.3.

## Data Sources

This tool was developed and tested using ATAC-seq data from the following sources:

### ENCODE Project
- HCT116 ATAC-seq experiments: [ENCODE Search Results](https://www.encodeproject.org/search/?type=Experiment&assay_title=ATAC-seq&biosample_ontology.term_name=HCT116)
- Specific experiment: [ENCSR260SWI](https://www.encodeproject.org/experiments/ENCSR260SWI/)

### GEO Database
- Additional datasets: [GSE187210](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE187210)

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

# Run the analysis with example data
python app.py \
  --untreated data/untreated/ENCFF321FBR.bed.gz \
  --treated data/treated/ENCFF734FSK.bed \
  --outdir data/output

# Run with signal analysis
python app.py \
  --untreated data/untreated/ENCFF321FBR.bed.gz \
  --treated data/treated/ENCFF734FSK.bed \
  --signal data/treated/ENCFF243DOC.bigWig \
  --outdir data/output
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
  --outdir data/output
```

## Input Files

- **Untreated peaks file**: BED or BED.gz format file containing ATAC-seq peaks from untreated samples
- **Treated peaks file**: BED format file containing ATAC-seq peaks from treated samples
- **Signal file** (optional): BigWig format file containing signal intensity data

## Output Files

The tool generates the following output files:

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
  Peaks lost in treated:  1253 → data/output/lost_in_treated.bed
  Peaks gained in treated: 879 → data/output/gained_in_treated.bed
Extracting signal from: data/treated/ENCFF243DOC.bigWig
Saved signal values:
  Lost peak signals → data/output/lost_signal.tsv
  Gained peak signals → data/output/gained_signal.tsv
```

Example content of `lost_in_treated.bed`:
```
chr1    565480    565750    peak_1    .    .
chr1    569480    570000    peak_2    .    .
chr2    781200    781500    peak_3    .    .
```

Example content of `lost_signal.tsv`:
```
chrom    start    end    name    signal_mean    signal_max
chr1    565480    565750    peak_1    4.23    7.85
chr1    569480    570000    peak_2    3.17    5.62
chr2    781200    781500    peak_3    5.89    9.14
```

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
chr1    565480    565750    .    .    .
chr1    566480    567000    .    .    .
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

## Issues and Support

If you encounter any problems or have questions about using this tool:

1. Check the documentation in this README
2. Create an issue on the GitHub repository with:
   - A description of the problem
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Any error messages

For feature requests, please also use the GitHub issue tracker with a clear description of the proposed functionality.

## License

[MIT License](LICENSE)

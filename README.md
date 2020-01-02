# DUEL tools

**Utilities to work with the DUEL dataset (Hough et al. 2016)**

## Installation

```bash
$ pip install git+https://github.com/nagasaki45/duel-tools.git
```

## Convert logging data to CSVs

### Command line

```bash
$ python -m convert_duel_logging_to_csv path_to_duel_logging_data path_to_output_dir
```

### In code

```
import convert_duel_logging_to_csv

convert_duel_logging_to_csv.main('path/to/duel/logging', 'output/path')
```

import sys
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import pybel

TSV_PATH = Path('homo_sapiens.tsv')
BELNS_PATH = Path('homo_sapiens.belns')

# TODO: download the TSV if missing; use functions like in export_belns.py

# TODO: load the BELNS? only if required to make the graph

# TODO: populate the graph with links from the TSV

# TODO: output the BEL graph (as BEL?)


def main() -> Optional[int]:
    with open(TSV_PATH, 'r') as f:
        f.seek(1)  # skip the leading '#' in the file
        complex_data = pd.read_table(f)
    graph = pybel.BELGraph()


if __name__ == '__main__':
    sys.exit(main())

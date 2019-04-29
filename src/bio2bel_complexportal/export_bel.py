# -*- coding: utf-8 -*-

"""Export Complex Portal as BEL."""

import sys
from hashlib import sha256
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import pybel

from bio2bel_complexportal.constants import NAMESPACE_URL, TSV_PATH
from bio2bel_complexportal.parser import df_getter

CHUNKSIZE = 2 ** 20  # 1 megabyte


def hash_file(path: Union[str, Path]) -> str:
    """Determine the SHA256 hash of the contents of the file at `path`.

    :param path: path to the file to be hashed

    :returns: the hexdigest of the SHA256 hash of the contents of the file
    """
    with open(path, 'rb') as f:
        hasher = sha256()
        chunk = f.read(CHUNKSIZE)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(CHUNKSIZE)

    return hasher.hexdigest()


def is_version_string_equal_to_digest(
        path: Union[str, Path], digest: Optional[str]
) -> bool:
    """Check if the digest stored in the VersionString of the BEL file at `path` is the same as the passed-in digest string.

    If the digest string is `None`, always returns False.

    :param path: path to the BEL that is being compared
    :param digest: hexdigest of the data that the BEL may be based on

    :returns: True if the digests match, False otherwise
    """
    # TODO: implement loading of BEL file
    return False


def build_graph() -> pybel.BELGraph:
    return _build_graph_from_df(df_getter())


def _build_graph_from_df(df: pd.DataFrame) -> pybel.BELGraph:
    raise NotImplementedError


def main() -> Optional[int]:
    assert (
            len(sys.argv) == 1 or len(sys.argv) == 2
    ), 'requires 0 or 1 arguments: [output filename]'

    output_file = sys.argv[1] if len(sys.argv) == 2 else None
    if output_file and output_file.strip() == '-':  # handle '-' for stdout output
        output_file = None

    try:
        digest = hash_file(TSV_PATH)
    except FileNotFoundError:
        print(f'no cached data at `{TSV_PATH}`; unable to continue', file=sys.stderr)
        return 1

    if output_file:
        if is_version_string_equal_to_digest(output_file, digest):
            print(f'`{NAMESPACE_URL}` has not changed; exiting', file=sys.stderr)
            print(
                f'delete or rename `{output_file}` to force a re-run', file=sys.stderr
            )
            return

    # TODO: populate the graph with links from the TSV
    # TODO: graph metadata
    graph = build_graph()
    # TODO: output the BEL graph (as BEL?)
    pybel.to_bel(graph, file=output_file)


if __name__ == '__main__':
    sys.exit(main())

import os
import sys
from hashlib import sha256
from pathlib import Path
from typing import Optional, Union
from urllib.request import URLError, urlopen
from warnings import warn

import pandas as pd
import pybel

CHUNKSIZE = 2 ** 20  # 1 megabyte

NAMESPACE_URL = 'ftp://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/homo_sapiens.tsv'

TSV_PATH = Path('homo_sapiens.tsv')
# BELNS_PATH = Path('homo_sapiens.belns')


def retrieve_and_cache(uri: str, output_name: Union[str, Path]) -> None:
    """Retrieve a remote URI and save it, saving a backup of a previous file with the same name if present.

    If there is a file matching `output_name` already existing, it is moved to `output_name.bak`. A previous `output_name.bak` is overwritten.

    :param uri: URI to be retrieved
    :param output_name: the location to store the retrieved file; passed directly to `open()`
    """
    with urlopen(uri) as remote_f:
        try:
            os.replace(output_name, f'{output_name}.bak')
        except FileNotFoundError:
            pass

        with open(output_name, 'wb') as output_f:
            chunk = remote_f.read(CHUNKSIZE)
            while chunk:
                output_f.write(chunk)
                chunk = remote_f.read(CHUNKSIZE)


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


def main() -> Optional[int]:
    assert (
        len(sys.argv) == 1 or len(sys.argv) == 2
    ), 'requires 0 or 1 arguments: [output filename]'

    output_file = sys.argv[1] if len(sys.argv) == 2 else None
    if output_file and output_file.strip() == '-':  # handle '-' for stdout output
        output_file = None

    try:
        retrieve_and_cache(NAMESPACE_URL, TSV_PATH)
    except URLError:
        warn(f'could not retrieve `{NAMESPACE_URL}`, will try with cached version')

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
    with open(TSV_PATH, 'r') as f:
        f.seek(1)  # skip the leading '#' in the file
        complex_data = pd.read_table(f)
    # TODO: graph metadata
    graph = pybel.BELGraph()

    # TODO: output the BEL graph (as BEL?)
    pybel.to_bel(graph, file=output_file)


if __name__ == '__main__':
    sys.exit(main())

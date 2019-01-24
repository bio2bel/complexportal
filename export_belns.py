import csv
import os
import sys
from hashlib import sha256
from pathlib import Path
from typing import Optional, Union
from urllib.request import URLError, urlopen
from warnings import warn

from bel_resources import parse_bel_resource, write_namespace

CHUNKSIZE = 2 ** 20  # 1 megabyte

NAMESPACE_URL = 'ftp://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/homo_sapiens.tsv'

TSV_PATH = Path('homo_sapiens.tsv')

NAMESPACE_NAME = 'Complex Portal'
NAMESPACE_KEYWORD = 'complexportal'


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
    """Check if the digest stored in the VersionString of the BELNS at `path` is the same as the passed-in digest string.

    If the digest string is `None`, always returns False.

    :param path: path to the BELNS that is being compared
    :param digest: hexdigest of the data that the BELNS may be based on

    :returns: True if the digests match, False otherwise
    """
    if not digest:
        return False

    try:
        with open(path, 'r') as belns:
            resource = parse_bel_resource(belns)
        if resource.get('Namespace', {}).get('VersionString') == digest:
            return True
    except FileNotFoundError:
        pass

    return False


def tsv_to_belns(
    tsv_path: Union[str, Path],
    belns_path: Optional[Union[str, Path]],
    digest: Optional[str] = None,
) -> None:
    """Create a BELNS file from the TSV data.

    If `belns_path` is None, the namespace will be printed to STDOUT.

    :param tsv_path: path to the input TSV
    :param belns_path: path to the output BELNS
    :param digest: SHA256 hexdigest of the input TSV for versioning the BELNS
    """
    with open(tsv_path, 'r') as tsv:
        header = tsv.readline().lstrip('#')
        fieldnames = header.split('\t')

        reader = csv.DictReader(tsv, fieldnames=fieldnames, dialect='excel-tab')
        complexnames = (row['Complex ac'] for row in reader)

        try:
            if belns_path is not None:
                belns = open(belns_path, 'w')
            else:
                belns = None

            write_namespace(
                values={complexname: 'C' for complexname in complexnames},
                namespace_name=NAMESPACE_NAME,
                namespace_keyword=NAMESPACE_KEYWORD,
                namespace_version=digest,
                file=belns,
            )
        finally:
            if belns is not None:
                belns.close()


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

    # check if the new tsv is different from what we have
    if output_file:
        if is_version_string_equal_to_digest(output_file, digest):
            print(f'`{NAMESPACE_URL}` has not changed; exiting', file=sys.stderr)
            print(
                f'delete or rename `{output_file}` to force a re-run', file=sys.stderr
            )
            return

    # the output file doesn't exist, is STDOUT, or the TSV data is newer
    # so we write a new BELNS
    tsv_to_belns(TSV_PATH, output_file, digest)


if __name__ == '__main__':
    sys.exit(main())

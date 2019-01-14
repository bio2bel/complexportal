import csv
import os
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any, IO, Optional, Union
from urllib.request import urlopen, URLError
from warnings import warn

from bel_resources import parse_bel_resource, write_namespace

CHUNKSIZE = 2 ** 20  # 1 megabyte

NAMESPACE_URL = 'ftp://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/homo_sapiens.tsv'

TSV_PATH = Path('homo_sapiens.tsv')

NAMESPACE_NAME = 'Complex Portal'
NAMESPACE_KEYWORD = 'complexportal'


def retrieve_and_cache(uri: str, output_name: Union[str, Path]) -> str:
    hasher = sha256()
    with urlopen(uri) as remote_f:
        try:
            os.replace(output_name, f'{output_name}.bak')
        except FileNotFoundError:
            pass
        with open(output_name, 'wb') as output_f:
            chunk = remote_f.read(CHUNKSIZE)
            while chunk:
                hasher.update(chunk)
                output_f.write(chunk)
                chunk = remote_f.read(CHUNKSIZE)

        return hasher.hexdigest()


def compare_tsv_to_belns(path: Union[str, Path], digest: str) -> bool:
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
    bel_path: Optional[Union[str, Path]],
    digest: Optional[str] = None,
) -> None:
    with open(tsv_path, 'r') as tsv:
        header = tsv.readline().lstrip('#')
        fieldnames = header.split('\t')

        reader = csv.DictReader(tsv, fieldnames=fieldnames, dialect='excel-tab')
        complexnames = (row['Complex ac'] for row in reader)

        try:
            if bel_path is not None:
                belns = open(bel_path, 'w')
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

    try:
        digest = retrieve_and_cache(NAMESPACE_URL, TSV_PATH)
    except URLError:
        # TODO this breaks if the file can't be retrieved because digest isn't set
        warn(f'could not retrieve `{NAMESPACE_URL}`, will try with cached version')

    if output_file:
        if compare_tsv_to_belns(output_file, digest):
            print(f'`{NAMESPACE_URL}` has not changed; exiting', file=sys.stderr)
            print(
                f'delete or rename `{output_file}` to force a re-run', file=sys.stderr
            )
            return

    tsv_to_belns(TSV_PATH, output_file, digest)


if __name__ == '__main__':
    sys.exit(main())

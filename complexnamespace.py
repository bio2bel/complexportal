import csv
import sys
from hashlib import sha256
from typing import Optional

from bel_resources import write_namespace

CHUNKSIZE = 1024


def main() -> Optional[int]:
    assert len(sys.argv) == 3, 'requires two arguments: input and output files'

    with open(sys.argv[1], 'rb') as tsv, open(sys.argv[2], 'w') as bel:
        hasher = sha256()
        chunk = tsv.read(CHUNKSIZE)
        while chunk:
            hasher.update(chunk)
            chunk = tsv.read(CHUNKSIZE)
        digest = hasher.hexdigest()

        tsv.seek(0)

        header = tsv.readline().decode('UTF-8').lstrip('#')
        fieldnames = header.split('\t')

        tsv_decoded = (l.decode('UTF-8') for l in tsv)
        reader = csv.DictReader(tsv_decoded, fieldnames=fieldnames, dialect='excel-tab')
        complexnames = (row['Complex ac'] for row in reader)

        write_namespace(
            values={complexname: 'C' for complexname in complexnames},
            namespace_name='Complex Portal',
            namespace_keyword='complexportal',
            namespace_version=digest,
            file=bel,
        )


if __name__ == '__main__':
    sys.exit(main())

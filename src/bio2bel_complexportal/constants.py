# -*- coding: utf-8 -*-

"""Constants for Bio2BEL Complex Portal."""

from bio2bel import get_data_dir
import os
__all__ = [
    'VERSION',
    'MODULE_NAME',
    'DATA_DIR',
    'get_version',
    'NAMESPACE_URL',
]

VERSION = '0.0.1-dev'
MODULE_NAME = 'complexportal'
DATA_DIR = get_data_dir(MODULE_NAME)

NAMESPACE_URL = 'ftp://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/homo_sapiens.tsv'
TSV_PATH = os.path.join(DATA_DIR, 'homo_sapiens.tsv')


def get_version() -> str:
    """Get the software version."""
    return VERSION

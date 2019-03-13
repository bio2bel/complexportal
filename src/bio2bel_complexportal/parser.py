# -*- coding: utf-8 -*-

"""Parsers and downloaders for Bio2BEL Complex Portal."""

from bio2bel.downloading import make_df_getter

from bio2bel_complexportal.constants import NAMESPACE_URL, TSV_PATH

__all__ = [
    'df_getter',
]

df_getter = make_df_getter(NAMESPACE_URL, TSV_PATH, sep='\t')

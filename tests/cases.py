# -*- coding: utf-8 -*-

"""Test cases for Bio2BEL Complex Portal."""

import os

from bio2bel.testing import AbstractTemporaryCacheClassMixin
from bio2bel_complexportal import Manager

__all__ = [
    'TemporaryCacheClass',
]

class TemporaryCacheClass(AbstractTemporaryCacheClassMixin):
    """A test case containing a temporary database and a Bio2BEL Complex Portal manager."""

    Manager = Manager
    manager: Manager

    @classmethod
    def populate(cls):
        """Populate the Bio2BEL Complex Portal database with test data."""
        # cls.manager.populate(url=...)
        raise NotImplementedError

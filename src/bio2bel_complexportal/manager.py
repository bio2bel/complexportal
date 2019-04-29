# -*- coding: utf-8 -*-

"""Manager for Bio2BEL Complex Portal."""

from typing import Mapping

from bio2bel import AbstractManager
from pybel import BELGraph

from .constants import MODULE_NAME
from .export_bel import build_graph
from .models import Base

__all__ = [
    'Manager',
]


class Manager(AbstractManager):
    """Manages the Bio2BEL Complex Portal database."""

    module_name = MODULE_NAME
    _base = Base

    def __init__(self, *args, **kwargs):
        self._graph = None

    @property
    def graph(self) -> BELGraph:
        if self._graph is None:
            self._graph = build_graph()
        return self._graph

    def is_populated(self) -> bool:
        """Check if the Bio2BEL Complex Portal database is populated."""
        return True

    def summarize(self) -> Mapping[str, int]:
        """Summarize the contents of the Bio2BEL Complex Portal database."""
        raise NotImplementedError

    def populate(self) -> None:
        """Populate the Bio2BEL Complex Portal database."""
        raise NotImplementedError

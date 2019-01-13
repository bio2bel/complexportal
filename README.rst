Bio2BEL Complex Portal
======================
Download data from ftp://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/homo_sapiens.tsv

The first line contains the header of:

- Complex ac
- Recommended name
- Aliases for complex
- Taxonomy identifier
- Identifiers (and stoichiometry) of molecules in complex
- Confidence
- Experimental evidence
- Go Annotations
- Cross references
- Description
- Complex properties
- Complex assembly
- Ligand
- Disease
- Agonist
- Antagonist
- Comment
- Source

Goal 1: Generate BEL namespace file using `bel_resources.write_namespace <https://github.com/cthoyt/bel-resources/blob/master/src/bel_resources/write_namespace.py>`_.

Arguments to this function:

- ``values`` should be a dictionary from keys as entries from ``Complex ac``  and the values as ``'C'``, which 
  represents complexes in BEL namespace files
- ``namespace_name`` should be ``'Complex Portal'``
- ``namespace_keyword`` should be ``'complexportal'``.

Goal 2: Create an instance of `pybel.BELGraph <https://pybel.readthedocs.io/en/latest/datamodel.html#pybel.BELGraph>`_
and populate it with links from complexes to their constituent entities (in ``Identifiers (and stoichiometry) of molecules in complex``) using `pybel.BELGraph.add_part_of <https://pybel.readthedocs.io/en/latest/datamodel.html#pybel.BELGraph.add_part_of>`_.

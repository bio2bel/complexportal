.PHONY: clean

%.bel: %.tsv
	python complexnamespace.py $< $@

%.tsv:
	wget ftp://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/$@

clean:
	-rm *.bel *.tsv


# Makefile for snub24_z3.tex
# Build chain: pdflatex -> bibtex -> pdflatex -> pdflatex

TEX      = pdflatex
BIB      = bibtex
SRC      = snub24_z3
PDF      = $(SRC).pdf

.PHONY: all clean

all: $(PDF)

$(PDF): $(SRC).tex $(SRC).bib
	$(TEX) $(SRC)
	$(BIB) $(SRC)
	$(TEX) $(SRC)
	$(TEX) $(SRC)

clean:
	rm -f $(SRC).aux $(SRC).bbl $(SRC).blg $(SRC).log
	rm -f $(SRC).out $(SRC).toc $(SRC).fdb_latexmk $(SRC).synctex.gz

distclean: clean
	rm -f $(PDF)

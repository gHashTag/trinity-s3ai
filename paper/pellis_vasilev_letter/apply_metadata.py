#!/usr/bin/env python3
"""Re-apply PDF metadata after every tectonic compile (tectonic wipes it).
Author MUST be 'Perplexity Computer'; Title is the full descriptive title."""
from pypdf import PdfReader, PdfWriter

SRC = "pellis_vasilev_letter.pdf"
TITLE = ("A Constrained Symbolic Search for phi-Structured Physical Constants: "
         "A Report, an Independent Numerical Audit, and a Roadmap for the "
         "Vasilev-Pellis-Olsen Programme")
AUTHOR = "Perplexity Computer"

r = PdfReader(SRC)
w = PdfWriter()
for p in r.pages:
    w.add_page(p)
w.add_metadata({"/Title": TITLE, "/Author": AUTHOR})
with open(SRC, "wb") as fh:
    w.write(fh)
print("metadata set")

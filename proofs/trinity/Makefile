# =============================================================================
# Trinity S3AI Proof Base v3.3 — Makefile
# =============================================================================
# Targets:
#   make / make all   — compile all .v files with coqc
#   make test         — run Coq compilation + Python regression tests
#   make stats        — print theorem/QED/Admitted counts
#   make clean        — remove generated files
# =============================================================================

COQFLAGS := -Q . Trinity
COQC     := coqc $(COQFLAGS)
COQDEP   := coqdep $(COQFLAGS)

# Source files (ordered by dependency)
VFILES := \
	TrinityCore.v \
	TrinityConstants.v \
	TrinityFormula_Q01.v \
	TrinityFormula_Q02.v \
	TrinityFormula_Q03.v \
	TrinityFormula_Q04.v \
	TrinityFormula_Q05.v \
	TrinityFormula_Q06.v \
	TrinityFormula_Q07.v \
	TrinityFormula_Q08.v \
	TrinityFormula_Q09.v \
	TrinityFormula_Q10.v \
	TrinityFormula_Q11.v \
	TrinityFormula_Q12.v \
	TrinityFormula_Q13.v \
	TrinityFormula_Q14.v \
	TrinityFormula_Q15.v \
	TrinityFormula_Q16.v \
	TrinityFormula_Q17.v \
	TrinityFormula_L01.v \
	TrinityFormula_L02.v \
	TrinityFormula_L03.v \
	TrinityFormula_P01.v \
	TrinityFormula_P02.v \
	TrinityFormula_P03.v \
	TrinityFormula_P04.v \
	TrinityPredicates.v \
	TrinityMain.v

VOFILES := $(VFILES:.v=.vo)
GLOBFILES := $(VFILES:.v=.glob)
AUXFILES := $(VFILES:.v=.vok) $(VFILES:.v=.vos)

# Default target: compile all .v files
.PHONY: all test stats clean

all: $(VOFILES)

# Compile .v files using coqc
%.vo: %.v
	$(COQC) $<

# Generate dependency file
coqdepend: $(VFILES)
	$(COQDEP) $(VFILES) > .coqdeps 2>/dev/null || true

# Run Coq compilation + Python regression tests
test: all
	@echo "======================================================================"
	@echo "  Trinity S3AI v3.3 — Full Test Suite"
	@echo "======================================================================"
	@echo "[1/2] Coq compilation: DONE"
	@echo "[2/2] Running Python regression tests..."
	@python3 test_formulas.py

# Print theorem count, QED count, and Admitted count
stats:
	@echo "======================================================================"
	@echo "  Trinity S3AI v3.3 — Proof Statistics"
	@echo "======================================================================"
	@echo ""
	@echo "  Source files:    $(words $(VFILES))"
	@if [ -f TrinityMain.vo ]; then \
		echo "  Compile status:  SUCCESS (all .vo present)"; \
	else \
		echo "  Compile status:  NOT COMPILED (run 'make' first)"; \
	fi
	@echo ""
	@echo "--- Theorem counts ---"
	@grep -rh "Theorem " $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Theorem:    {}"
	@grep -rh "Lemma " $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Lemma:      {}"
	@grep -rh "Qed." $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Qed:        {}"
	@grep -rh "Admitted." $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Admitted:   {}"
	@grep -rh "Defined." $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Defined:    {}"
	@echo ""
	@echo "--- Formula definitions ---"
	@grep -rh "Definition .*theoretical" $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Theoretical formulas: {}"
	@grep -rh "Definition .*experimental" $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Experimental anchors: {}"
	@echo ""
	@echo "--- Proof status ---"
	@TOTAL=$$(grep -rh "Theorem \|Lemma " $(VFILES) 2>/dev/null | wc -l); \
	ADMIT=$$(grep -rh "Admitted." $(VFILES) 2>/dev/null | wc -l); \
	COMPLETE=$$((TOTAL - ADMIT)); \
	if [ $$TOTAL -gt 0 ]; then \
		PCT=$$(awk "BEGIN {printf \"%.1f\", $$COMPLETE/$$TOTAL*100}"); \
		echo "  Complete:   $$COMPLETE / $$TOTAL ($$PCT%)"; \
	else \
		echo "  Complete:   N/A (no proofs found)"; \
	fi
	@echo ""

# Remove generated files
clean:
	rm -f $(VOFILES) $(GLOBFILES) $(AUXFILES)
	rm -f .coqdeps
	rm -f *.cmi *.cmx *.o
	@echo "  Cleaned generated files."

# Full reset (including python cache)
distclean: clean
	rm -rf __pycache__ .pytest_cache
	@echo "  Full clean complete."

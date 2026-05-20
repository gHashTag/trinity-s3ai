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

# Source files (ordered by dependency — CorePhi.v must be FIRST)
VFILES := \
	CorePhi.v \
	H4Derivations.v \
	Bounds_LeptonMasses.v \
	Bounds_Mixing.v \
	Unitarity.v \
	Catalog42.v \
	Koide.v \
	H4GaugeEmbedding.v \
	Predictions.v \
	H4Lagrangian.v \
	SpectralAction600Cell.v \
	HiggsPrediction.v \
	OptimizerInvariants.v \
	UniquenessTheorem.v \
	HonestPValue.v \
	E6vsH4.v

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
	@if [ -f CorePhi.vo ]; then \
		echo "  CorePhi.vo:      COMPILED (foundation ready)"; \
	else \
		echo "  CorePhi.vo:      MISSING (foundation fails)"; \
	fi
	@echo ""
	@echo "--- Theorem counts ---"
	@grep -rh "Theorem " $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Theorem:    {}"
	@grep -rh "Lemma " $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Lemma:      {}"
	@grep -rh "Qed." $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Qed:        {}"
	@grep -rh "Admitted." $(VFILES) 2>/dev/null | wc -l | xargs -I{} echo "  Admitted:   {}"
	@echo ""
	@echo "--- Proof status ---"
	@COMPILED=$$(ls *.vo 2>/dev/null | wc -l); \
	echo "  .vo files:  $$COMPILED / $(words $(VFILES))"
	@echo ""

# Remove generated files
clean:
	rm -f $(VOFILES) $(GLOBFILES) $(AUXFILES)
	rm -f .coqdeps
	@echo "  Cleaned generated files."

# Full reset (including python cache)
distclean: clean
	rm -rf __pycache__ .pytest_cache
	@echo "  Full clean complete."

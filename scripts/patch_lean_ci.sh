#!/bin/bash
# patch_lean_ci.sh — manual patch for .github/workflows/lean.yml
# Run this script from the repo root to apply the CI fix.
# Scope-gate forbidden for direct agent edit; must be run by human.

set -euo pipefail

WORKFLOW=".github/workflows/lean.yml"

if [ ! -f "$WORKFLOW" ]; then
  echo "ERROR: $WORKFLOW not found" >&2
  exit 1
fi

# Backup
cp "$WORKFLOW" "$WORKFLOW.bak"

# Apply patch using sed/awk approach
cat > /tmp/lean_ci_patch.txt <<'PATCH_EOF'
--- a/.github/workflows/lean.yml
+++ b/.github/workflows/lean.yml
@@ -28,8 +28,10 @@ jobs:
         with:
           path: |
             derivations/lean_port/TrinityLean/.lake/packages
             derivations/lean_port/TrinityLean/.lake/build
+            proofs/lean/.lake/packages
+            proofs/lean/.lake/build
           key: lean-mathlib-${{ runner.os }}-v4.13.0-${{ hashFiles('derivations/lean_port/TrinityLean/lakefile.lean', 'derivations/lean_port/TrinityLean/lean-toolchain', 'proofs/lean/lakefile.lean', 'proofs/lean/lean-toolchain') }}
           restore-keys: |
             lean-mathlib-${{ runner.os }}-v4.13.0-
@@ -43,9 +45,21 @@ jobs:
           lake exe cache get || true
           lake build

+      - name: Build proofs/lean
+        run: |
+          cd proofs/lean
+          lake update -R
+          lake exe cache get || true
+          lake build
+
       - name: Report build status
         if: always()
         run: |
           echo "=== LEAN BUILD STATUS ==="
           if [ -d derivations/lean_port/TrinityLean/.lake/build/lib ]; then
             echo "TrinityLean: BUILT"
           else
             echo "TrinityLean: NOT BUILT"
           fi
+          if [ -d proofs/lean/.lake/build/lib ]; then
+            echo "proofs/lean: BUILT"
+          else
+            echo "proofs/lean: NOT BUILT"
+          fi
PATCH_EOF

echo "Patch instructions written to /tmp/lean_ci_patch.txt"
echo "Apply manually with: patch -p1 < /tmp/lean_ci_patch.txt"
echo "Or edit $WORKFLOW by hand using the diff above."

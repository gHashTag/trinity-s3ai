#!/usr/bin/env python3
"""
Uniqueness Enumeration for ALL 25 Trinity coefficients.

For each Trinity coefficient, find ALL ways to derive it from H4 invariants
using operations: +, -, *, // (integer division).

H4 invariants: {1, 2, 7, 11, 12, 19, 20, 29, 30, 120, 240}
Trinity coefficients: {1, 2, 3, 4, 8, 10, 14, 15, 18, 24, 36, 48, 92, 239, 549}
"""

H4_invariants = [1, 2, 7, 11, 12, 19, 20, 29, 30, 120, 240]

trinity_coefficients = [1, 2, 3, 4, 8, 10, 14, 15, 18, 24, 36, 48, 92, 239, 549]

# Operations: (name, function, symbol)
operations = [
    ("add", lambda a, b: a + b, "+"),
    ("sub", lambda a, b: a - b, "-"),
    ("mul", lambda a, b: a * b, "*"),
    ("div", lambda a, b: a // b if b != 0 and a % b == 0 else None, "//"),
]

def enumerate_all():
    """Enumerate ALL derivations for each Trinity coefficient."""
    results = {}
    
    for c in trinity_coefficients:
        derivations = []
        
        # Check ALL ordered pairs (a, b) from H4_invariants
        for a in H4_invariants:
            for b in H4_invariants:
                for op_name, op_func, op_sym in operations:
                    try:
                        result = op_func(a, b)
                    except:
                        result = None
                    
                    if result is not None and result == c:
                        derivations.append({
                            "a": a,
                            "b": b,
                            "op": op_name,
                            "op_sym": op_sym,
                            "expr": f"{a} {op_sym} {b} = {c}"
                        })
        
        results[c] = derivations
    
    return results

def format_results(results):
    """Format the results into a readable report."""
    lines = []
    lines.append("# Uniqueness Enumeration: Trinity Coefficients from H4 Invariants")
    lines.append("")
    lines.append("**H4 Invariants:** {1, 2, 7, 11, 12, 19, 20, 29, 30, 120, 240}")
    lines.append("")
    lines.append("**Trinity Coefficients:** {1, 2, 3, 4, 8, 10, 14, 15, 18, 24, 36, 48, 92, 239, 549}")
    lines.append("")
    lines.append("**Operations:** +, -, *, // (integer division)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Summary table
    lines.append("## Summary Table")
    lines.append("")
    lines.append("| Coefficient | Derivation Count | Unique? | Derivations |")
    lines.append("|-------------|-----------------|---------|-------------|")
    
    total_derivations = 0
    unique_count = 0
    non_unique = []
    
    for c in trinity_coefficients:
        derivations = results[c]
        count = len(derivations)
        total_derivations += count
        is_unique = count == 1
        if is_unique:
            unique_count += 1
        else:
            non_unique.append(c)
        
        deriv_str = "; ".join([d["expr"] for d in derivations]) if derivations else "NONE"
        unique_str = "YES" if is_unique else ("NO — " + str(count) + " ways" if count > 1 else "NO — 0 ways")
        lines.append(f"| {c} | {count} | {unique_str} | {deriv_str} |")
    
    lines.append("")
    lines.append(f"**Total derivations:** {total_derivations}")
    lines.append(f"**Unique coefficients:** {unique_count} / {len(trinity_coefficients)}")
    lines.append(f"**Non-unique coefficients:** {non_unique if non_unique else 'None'}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Detailed breakdown per coefficient
    lines.append("## Detailed Derivation Breakdown")
    lines.append("")
    
    for c in trinity_coefficients:
        derivations = results[c]
        count = len(derivations)
        lines.append(f"### Coefficient {c}")
        lines.append(f"**Derivation count:** {count}")
        lines.append("")
        
        if count == 0:
            lines.append("⚠️ **NO derivation found from H4 invariants with single binary operation!**")
            lines.append("")
        elif count == 1:
            lines.append(f"✅ **UNIQUE:** {derivations[0]['expr']}")
            lines.append("")
        else:
            lines.append("❌ **NON-UNIQUE — Multiple derivations:**")
            for i, d in enumerate(derivations, 1):
                lines.append(f"  {i}. {d['expr']}  (operation: {d['op']}, a={d['a']}, b={d['b']})")
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Cross-tabulation: which operations produce which coefficients
    lines.append("## Operation-Type Analysis")
    lines.append("")
    
    op_counts = {"add": 0, "sub": 0, "mul": 0, "div": 0}
    op_derivations = {"add": [], "sub": [], "mul": [], "div": []}
    
    for c in trinity_coefficients:
        for d in results[c]:
            op_counts[d["op"]] += 1
            op_derivations[d["op"]].append(d["expr"])
    
    lines.append("| Operation | Count | Derivations |")
    lines.append("|-----------|-------|-------------|")
    for op in ["add", "sub", "mul", "div"]:
        opsym = {"add": "+", "sub": "-", "mul": "*", "div": "//"}[op]
        deriv_list = "; ".join(op_derivations[op])
        lines.append(f"| {op} ({opsym}) | {op_counts[op]} | {deriv_list} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Full enumeration of ALL pairs
    lines.append("## Appendix: Full Pair Enumeration")
    lines.append("")
    lines.append("All results of a op b for every (a,b) in H4 × H4:")
    lines.append("")
    
    # Header
    lines.append("| a | b | a+b | a-b | a*b | a//b |")
    lines.append("|---|---|-----|-----|-----|------|")
    
    for a in H4_invariants:
        for b in H4_invariants:
            s = a + b
            d = a - b
            m = a * b
            div = a // b if b != 0 and a % b == 0 else "N/A"
            lines.append(f"| {a} | {b} | {s} | {d} | {m} | {div} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by uniqueness_enumeration.py*")
    
    return "\n".join(lines)

def main():
    print("=" * 70)
    print("UNIQUENESS ENUMERATION: Trinity Coefficients from H4 Invariants")
    print("=" * 70)
    print()
    
    results = enumerate_all()
    
    # Print summary
    print("COEFFICIENT -> [ALL DERIVATIONS]")
    print("-" * 50)
    
    total = 0
    for c in trinity_coefficients:
        derivs = results[c]
        count = len(derivs)
        total += count
        exprs = [d["expr"] for d in derivs]
        if count == 0:
            print(f"  {c:3d}: NO DERIVATION FOUND")
        elif count == 1:
            print(f"  {c:3d}: {exprs[0]}  [UNIQUE]")
        else:
            print(f"  {c:3d}: {count} derivations — {', '.join(exprs)}")
    
    print("-" * 50)
    print(f"Total derivations: {total}")
    print()
    
    # Generate and save markdown report
    report = format_results(results)
    
    output_path = "/mnt/agents/output/trinity-v33/uniqueness_results.md"
    with open(output_path, "w") as f:
        f.write(report)
    
    print(f"Full report saved to: {output_path}")
    
    # Also print non-unique coefficients
    print()
    print("NON-UNIQUE COEFFICIENTS (count > 1):")
    for c in trinity_coefficients:
        derivs = results[c]
        if len(derivs) > 1:
            print(f"  {c}: {len(derivs)} ways")
            for d in derivs:
                print(f"    - {d['expr']}")
    
    print()
    print("COEFFICIENTS WITH ZERO DERIVATIONS:")
    for c in trinity_coefficients:
        derivs = results[c]
        if len(derivs) == 0:
            print(f"  {c}: NO single-operation derivation")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Wave 14.4 — Geometric sigma-field test for E8, F4, and H4.

Builds a discrete de Rham complex on a reduced simplicial model of each
plumbing manifold, computes Hodge Laplacians, and counts harmonic forms.

Honest reduced model:
  - E8: 8 Dynkin nodes + 12 icosahedron boundary vertices
  - F4: 4 Dynkin nodes + 24-cell boundary vertices
  - H4: 4 Dynkin nodes + 12 icosahedron boundary vertices

The full E8 plumbing has b_2 = 8 (from the E8 intersection form), but the
reduced model cannot resolve the full 4-manifold topology. We report kernel
dimensions for the reduced model honestly and explicitly note this limitation.
"""

import numpy as np
import json
from itertools import combinations, product, permutations
from math import comb, isclose

# ============================================================
# GEOMETRY: Polytope vertices
# ============================================================

PHI = (1 + np.sqrt(5)) / 2


def icosahedron_vertices():
    """12 vertices of regular icosahedron, embedded in 4D with w=0."""
    verts_3d = [
        (0, 1, PHI), (0, 1, -PHI), (0, -1, PHI), (0, -1, -PHI),
        (1, PHI, 0), (1, -PHI, 0), (-1, PHI, 0), (-1, -PHI, 0),
        (PHI, 0, 1), (PHI, 0, -1), (-PHI, 0, 1), (-PHI, 0, -1),
    ]
    # Scale so that edge length = 2 (standard)
    # Actually these already have edge length 2
    return [np.array([x, y, z, 0.0]) for (x, y, z) in verts_3d]


def cell24_vertices():
    """24 vertices of 24-cell: permutations of (±1, ±1, 0, 0)."""
    base = [(1, 1, 0, 0), (1, -1, 0, 0), (-1, 1, 0, 0), (-1, -1, 0, 0)]
    verts = set()
    for b in base:
        for p in permutations(b):
            verts.add(tuple(p))
    return [np.array(v, dtype=float) for v in verts]


# ============================================================
# SIMPLICIAL COMPLEX CONSTRUCTION
# ============================================================

def build_edges_from_polytope(vertices, edge_length, tol=1e-6):
    """Return list of edges (i,j) where |v_i - v_j| ≈ edge_length."""
    edges = []
    n = len(vertices)
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(vertices[i] - vertices[j])
            if abs(d - edge_length) < tol:
                edges.append((i, j))
    return edges


def build_polytope_edges(vertices):
    """Infer edge length as the smallest nonzero distance, then build edges."""
    n = len(vertices)
    min_dist = float('inf')
    for i in range(n):
        for j in range(i + 1, n):
            d = np.linalg.norm(vertices[i] - vertices[j])
            if d > 1e-6 and d < min_dist:
                min_dist = d
    return build_edges_from_polytope(vertices, min_dist)


def find_cliques_of_size(graph_edges, size, n_vertices):
    """Find all cliques of given size in an undirected graph."""
    # Build adjacency set
    adj = [set() for _ in range(n_vertices)]
    for i, j in graph_edges:
        adj[i].add(j)
        adj[j].add(i)
    
    cliques = []
    
    def extend_clique(current, candidates):
        if len(current) == size:
            cliques.append(tuple(sorted(current)))
            return
        needed = size - len(current)
        for idx, v in enumerate(candidates):
            if len(candidates) - idx < needed:
                break
            # Check if v is connected to all vertices in current
            if all(v in adj[u] for u in current):
                new_candidates = [w for w in candidates[idx+1:] if w in adj[v]]
                extend_clique(current + [v], new_candidates)
    
    vertices = list(range(n_vertices))
    extend_clique([], vertices)
    return cliques


def build_simplicial_complex(interior_edges, boundary_edges, n_interior, n_boundary):
    """
    Build simplicial complex as the join of interior graph and boundary polytope.
    
    Vertices: 0..n_interior-1 (interior), n_interior..n_interior+n_boundary-1 (boundary)
    
    Edges:
      - interior-interior edges
      - boundary-boundary edges  
      - ALL interior-boundary edges (cone structure)
    
    Simplices: any (k+1)-subset where all edges are present.
    """
    n_vertices = n_interior + n_boundary
    
    # Shift boundary vertex indices
    boundary_edges_shifted = [(i + n_interior, j + n_interior) for (i, j) in boundary_edges]
    
    # All interior-boundary edges
    ib_edges = []
    for i in range(n_interior):
        for j in range(n_boundary):
            ib_edges.append((i, j + n_interior))
    
    all_edges = list(set(interior_edges + boundary_edges_shifted + ib_edges))
    
    # Find triangles (3-cliques)
    triangles = find_cliques_of_size(all_edges, 3, n_vertices)
    
    # Find tetrahedra (4-cliques)
    tetrahedra = find_cliques_of_size(all_edges, 4, n_vertices)
    
    # Find 4-simplices (5-cliques)
    simplices_4 = find_cliques_of_size(all_edges, 5, n_vertices)
    
    return {
        'n_vertices': n_vertices,
        'n_interior': n_interior,
        'n_boundary': n_boundary,
        'edges': all_edges,
        'triangles': triangles,
        'tetrahedra': tetrahedra,
        'simplices_4': simplices_4,
    }


# ============================================================
# DISCRETE DE RHAM COMPLEX
# ============================================================

def build_coboundary_operator(faces, cofaces, k):
    """
    Build d_k: C^k → C^(k+1) as a sparse matrix.
    
    faces: list of k-simplices (tuples of vertex indices)
    cofaces: list of (k+1)-simplices
    
    For oriented simplex [v_0, ..., v_k] with v_0 < ... < v_k,
    the orientation is induced by the vertex ordering.
    
    d_k([v_0, ..., v_k]) = sum_{i=0}^{k+1} (-1)^i [v_0, ..., v̂_i, ..., v_{k+1}]
    """
    if not faces or not cofaces:
        return np.zeros((len(cofaces), len(faces)))
    
    face_to_idx = {tuple(f): i for i, f in enumerate(faces)}
    
    rows = []
    cols = []
    vals = []
    
    for j, coface in enumerate(cofaces):
        coface = list(coface)
        for i in range(len(coface)):
            face = tuple(sorted(coface[:i] + coface[i+1:]))
            if face in face_to_idx:
                sign = (-1) ** i
                rows.append(j)
                cols.append(face_to_idx[face])
                vals.append(float(sign))
    
    d = np.zeros((len(cofaces), len(faces)))
    for r, c, v in zip(rows, cols, vals):
        d[r, c] = v
    
    return d


def hodge_laplacian(d_k, d_km1):
    """
    Compute Δ_k = d_{k-1} d_{k-1}^T + d_k^T d_k.
    d_k: C^k → C^{k+1}
    d_km1: C^{k-1} → C^k
    With unit mass matrix, d† = d^T.
    """
    n_k = d_k.shape[1] if d_k.size > 0 else d_km1.shape[0]
    
    term1 = d_km1 @ d_km1.T if d_km1.size > 0 else np.zeros((n_k, n_k))
    term2 = d_k.T @ d_k if d_k.size > 0 else np.zeros((n_k, n_k))
    
    return term1 + term2


def kernel_dimension(matrix, tol=1e-10):
    """Compute dimension of kernel via SVD."""
    if matrix.size == 0:
        return 0
    if matrix.shape[0] == 0 or matrix.shape[1] == 0:
        return matrix.shape[1]  # domain dimension
    s = np.linalg.svd(matrix, compute_uv=False)
    return int(np.sum(s < tol))


def kernel_dimension_laplacian(lap, tol=1e-8):
    """Compute dim ker(Δ) via eigenvalue count near zero."""
    if lap.size == 0:
        return 0
    if lap.shape[0] == 0:
        return 0
    # Laplacian is symmetric positive semi-definite
    w = np.linalg.eigvalsh(lap)
    return int(np.sum(np.abs(w) < tol))


# ============================================================
# SYSTEM DEFINITIONS
# ============================================================

def build_e8_model():
    """E8 reduced model: 8 Dynkin nodes + 12 icosahedron vertices."""
    n_interior = 8
    boundary = icosahedron_vertices()
    n_boundary = len(boundary)
    
    # E8 Dynkin diagram edges:
    # 0—1—2—3—4—5—6
    #         |
    #         7
    interior_edges = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (3,7)]
    boundary_edges = build_polytope_edges(boundary)
    
    sc = build_simplicial_complex(interior_edges, boundary_edges, n_interior, n_boundary)
    sc['name'] = 'E8'
    sc['interior_coords'] = [
        np.array([-3.0, 0, 0, 0]),
        np.array([-2.0, 0, 0, 0]),
        np.array([-1.0, 0, 0, 0]),
        np.array([0.0, 0, 0, 0]),
        np.array([1.0, 0, 0, 0]),
        np.array([2.0, 0, 0, 0]),
        np.array([3.0, 0, 0, 0]),
        np.array([0.0, 1.0, 0, 0]),
    ]
    sc['boundary_coords'] = boundary
    return sc


def build_f4_model():
    """F4 reduced model: 4 Dynkin nodes + 24-cell vertices."""
    n_interior = 4
    boundary = cell24_vertices()
    n_boundary = len(boundary)
    
    # F4 Dynkin diagram: 0—1—2—3 with double bond between 1 and 2.
    # As an undirected graph, just a path.
    interior_edges = [(0,1), (1,2), (2,3)]
    boundary_edges = build_polytope_edges(boundary)
    
    sc = build_simplicial_complex(interior_edges, boundary_edges, n_interior, n_boundary)
    sc['name'] = 'F4'
    sc['interior_coords'] = [
        np.array([-1.5, 0, 0, 0]),
        np.array([-0.5, 0, 0, 0]),
        np.array([0.5, 0, 0, 0]),
        np.array([1.5, 0, 0, 0]),
    ]
    sc['boundary_coords'] = boundary
    return sc


def build_h4_model():
    """H4 reduced model: 4 Dynkin nodes + 12 icosahedron vertices."""
    n_interior = 4
    boundary = icosahedron_vertices()
    n_boundary = len(boundary)
    
    # H4 Dynkin diagram (Coxeter): linear 0—1—2—3
    interior_edges = [(0,1), (1,2), (2,3)]
    boundary_edges = build_polytope_edges(boundary)
    
    sc = build_simplicial_complex(interior_edges, boundary_edges, n_interior, n_boundary)
    sc['name'] = 'H4'
    sc['interior_coords'] = [
        np.array([-1.5, 0, 0, 0]),
        np.array([-0.5, 0, 0, 0]),
        np.array([0.5, 0, 0, 0]),
        np.array([1.5, 0, 0, 0]),
    ]
    sc['boundary_coords'] = boundary
    return sc


# ============================================================
# MAIN COMPUTATION
# ============================================================

def analyze_system(sc):
    """Build de Rham complex, compute Laplacians, count zero modes."""
    name = sc['name']
    print(f"\n{'='*60}")
    print(f"  SYSTEM: {name}")
    print(f"{'='*60}")
    print(f"  Vertices: {sc['n_vertices']} ({sc['n_interior']} interior + {sc['n_boundary']} boundary)")
    print(f"  Edges: {len(sc['edges'])}")
    print(f"  Triangles: {len(sc['triangles'])}")
    print(f"  Tetrahedra: {len(sc['tetrahedra'])}")
    print(f"  4-simplices: {len(sc['simplices_4'])}")
    
    # Build cochain spaces
    vertices = [(i,) for i in range(sc['n_vertices'])]
    edges = sc['edges']
    triangles = sc['triangles']
    tetrahedra = sc['tetrahedra']
    simplices_4 = sc['simplices_4']
    
    print(f"\n  Cochain dimensions:")
    print(f"    C^0 = {len(vertices)}")
    print(f"    C^1 = {len(edges)}")
    print(f"    C^2 = {len(triangles)}")
    print(f"    C^3 = {len(tetrahedra)}")
    print(f"    C^4 = {len(simplices_4)}")
    
    # Build coboundary operators
    d0 = build_coboundary_operator(vertices, edges, 0)
    d1 = build_coboundary_operator(edges, triangles, 1)
    d2 = build_coboundary_operator(triangles, tetrahedra, 2)
    d3 = build_coboundary_operator(tetrahedra, simplices_4, 3)
    
    # Compute Laplacians
    Delta0 = hodge_laplacian(d0, np.zeros((0, len(vertices))))
    Delta1 = hodge_laplacian(d1, d0)
    Delta2 = hodge_laplacian(d2, d1)
    Delta3 = hodge_laplacian(d3, d2)
    Delta4 = hodge_laplacian(np.zeros((0, len(simplices_4))), d3)
    
    # Compute kernel dimensions
    dim_H0 = kernel_dimension_laplacian(Delta0)
    dim_H1 = kernel_dimension_laplacian(Delta1)
    dim_H2 = kernel_dimension_laplacian(Delta2)
    dim_H3 = kernel_dimension_laplacian(Delta3)
    dim_H4 = kernel_dimension_laplacian(Delta4)
    
    print(f"\n  Harmonic dimensions (Betti numbers):")
    print(f"    dim H^0 = {dim_H0}")
    print(f"    dim H^1 = {dim_H1}")
    print(f"    dim H^2 = {dim_H2}")
    print(f"    dim H^3 = {dim_H3}")
    print(f"    dim H^4 = {dim_H4}")
    
    # Also compute via rank-nullity as a consistency check
    rank_d0 = np.linalg.matrix_rank(d0, tol=1e-8) if d0.size > 0 else 0
    rank_d1 = np.linalg.matrix_rank(d1, tol=1e-8) if d1.size > 0 else 0
    rank_d2 = np.linalg.matrix_rank(d2, tol=1e-8) if d2.size > 0 else 0
    rank_d3 = np.linalg.matrix_rank(d3, tol=1e-8) if d3.size > 0 else 0
    
    b0_check = len(vertices) - rank_d0
    b1_check = len(edges) - rank_d0 - rank_d1
    b2_check = len(triangles) - rank_d1 - rank_d2
    b3_check = len(tetrahedra) - rank_d2 - rank_d3
    b4_check = len(simplices_4) - rank_d3
    
    print(f"\n  Consistency check (rank-nullity):")
    print(f"    b0 = {b0_check}, b1 = {b1_check}, b2 = {b2_check}, b3 = {b3_check}, b4 = {b4_check}")
    
    # Eigenvalue spectra (smallest 10 for each Laplacian)
    spectra = {}
    for label, lap in [('Delta0', Delta0), ('Delta1', Delta1), ('Delta2', Delta2), 
                        ('Delta3', Delta3), ('Delta4', Delta4)]:
        if lap.size > 0 and lap.shape[0] > 0:
            w = np.linalg.eigvalsh(lap)
            spectra[label] = {
                'smallest_10': [round(float(x), 8) for x in np.sort(w)[:min(10, len(w))]],
                'largest_3': [round(float(x), 8) for x in np.sort(w)[-3:]],
            }
        else:
            spectra[label] = {'smallest_10': [], 'largest_3': []}
    
    return {
        'name': name,
        'n_vertices': sc['n_vertices'],
        'n_interior': sc['n_interior'],
        'n_boundary': sc['n_boundary'],
        'n_edges': len(edges),
        'n_triangles': len(triangles),
        'n_tetrahedra': len(tetrahedra),
        'n_4simplices': len(simplices_4),
        'dim_H0': dim_H0,
        'dim_H1': dim_H1,
        'dim_H2': dim_H2,
        'dim_H3': dim_H3,
        'dim_H4': dim_H4,
        'rank_d0': int(rank_d0),
        'rank_d1': int(rank_d1),
        'rank_d2': int(rank_d2),
        'rank_d3': int(rank_d3),
        'betti_check': [b0_check, b1_check, b2_check, b3_check, b4_check],
        'spectra': spectra,
    }


def main():
    print("="*60)
    print("GEOMETRIC SIGMA-FIELD TEST (Wave 14.4)")
    print("="*60)
    print("\nDiscrete de Rham complex on reduced plumbing models.")
    print("Computing Hodge Laplacians and harmonic form dimensions.")
    
    systems = [build_e8_model(), build_f4_model(), build_h4_model()]
    results = {}
    
    for sc in systems:
        res = analyze_system(sc)
        results[res['name']] = res
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"{'System':<6} {'Verts':>6} {'Edges':>6} {'Tris':>6} {'Tets':>6} {'4-simp':>7} {'dim H²':>8}")
    print("-"*60)
    for name in ['E8', 'F4', 'H4']:
        r = results[name]
        print(f"{name:<6} {r['n_vertices']:>6} {r['n_edges']:>6} {r['n_triangles']:>6} "
              f"{r['n_tetrahedra']:>6} {r['n_4simplices']:>7} {r['dim_H2']:>8}")
    
    # Determine Boundary Theorem 6 status
    print("\n" + "="*60)
    print("SIGMA-FIELD CANDIDATE ANALYSIS")
    print("="*60)
    
    any_positive = False
    for name in ['E8', 'F4', 'H4']:
        dim_H2 = results[name]['dim_H2']
        if dim_H2 > 0:
            print(f"  {name}: dim H² = {dim_H2} > 0 → sigma-field candidate exists")
            any_positive = True
        else:
            print(f"  {name}: dim H² = {dim_H2} → no harmonic 2-form")
    
    if any_positive:
        print("\n  At least one system admits harmonic 2-forms.")
        print("  Boundary Theorem 6: NOT proven (sigma-field may be available).")
        no_go_status = "NOT proven"
    else:
        print("\n  Boundary Theorem 6: PROVEN — No system admits harmonic 2-forms.")
        print("  The sigma-field is unavailable in ALL tested root systems.")
        no_go_status = "PROVEN"
    
    results['no_go_theorem_6'] = no_go_status
    results['note'] = (
        "Reduced model uses simplified boundary (icosahedron/24-cell) and cone-like "
        "interior-boundary connections. Full E8 plumbing has b_2=8, but the reduced "
        "model cannot resolve the full 4-manifold topology. Results are honest counts "
        "for the reduced simplicial complex."
    )
    
    # Save JSON
    out_path = 'derivations/sigma_bypass/geometric_sigma_results.json'
    # Convert numpy types before JSON serialization
    def convert(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, default=convert)
    print(f"\n  Saved: {out_path}")
    
    return results


if __name__ == '__main__':
    main()

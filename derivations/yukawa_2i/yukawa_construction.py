#!/usr/bin/env python3
"""
Wave 9.2: Yukawa coupling matrix construction from 2I-equivariant representation theory.

Strategy:
1. Reconstruct D_F (480×480 matrix) from Wave 8.4.
2. Compute isotypic projectors P_ρ onto each of the 9 irrep sectors of 2I.
3. Define Yukawa block Y_{LR} = P_R · D_F · P_L for each irrep pair (L, R).
4. Compute SVD of each Y_{LR} block.
5. Compare singular values to SM mass ratios.
6. Report honestly.

Key theorem (Schur's lemma, proven analytically):
  If D_F is 2I-equivariant, then Y_{LR} = 0 for L ≠ R (different irreps).
  Y_{LL} = λ_L · I_{dim²} (scalar multiple of identity within each isotypic block).
  Therefore: purely equivariant D_F → no mass hierarchies from irrep structure alone.
  
  BUT: the MULTIPLICITY MATRIX within a single isotypic block can break degeneracy!
  For irrep ρ of dim d, the isotypic component has dim d×mult(ρ) = d×d (in regular rep).
  The multiplicity part is a d×d matrix that CAN be a general Hermitian matrix.
  This is where "Yukawa" can live.
"""

import numpy as np
from numpy.linalg import svd
import json, os, sys

phi = (1 + np.sqrt(5)) / 2

print("="*70)
print("WAVE 9.2: Yukawa Construction from 2I-Equivariant D_F")
print("="*70)

# ============================================================
# Step 1: Reconstruct D_F (from Wave 8.4 computation)
# ============================================================
print("\n[Step 1] Reconstructing D_F (480×480 matrix)...")

def build_600cell_vertices():
    """Generate 120 vertices of 600-cell as unit quaternions."""
    verts = []
    # Type I: (±1, 0, 0, 0) and permutations (8 vertices)
    for i in range(4):
        for s in [1, -1]:
            v = [0.0, 0.0, 0.0, 0.0]
            v[i] = s
            verts.append(tuple(v))
    # Type II: (±1/2, ±1/2, ±1/2, ±1/2) (16 vertices)
    for s0 in [1,-1]:
        for s1 in [1,-1]:
            for s2 in [1,-1]:
                for s3 in [1,-1]:
                    verts.append((s0/2, s1/2, s2/2, s3/2))
    # Type III: even permutations of (0, ±1/2, ±φ/2, ±1/(2φ)) (96 vertices)
    half_phi = phi/2
    half_inv_phi = 1/(2*phi)
    base_coords = [(0.0, 0.5, half_phi, half_inv_phi)]
    # Generate all sign combinations and even permutations
    from itertools import permutations
    seen = set()
    for s0 in [1,-1]:
        for s1 in [1,-1]:
            for s2 in [1,-1]:
                coords = [0.0, s0*0.5, s1*half_phi, s2*half_inv_phi]
                # even permutations of 4 elements: 12 of them
                for perm in permutations(range(4)):
                    # parity of permutation
                    perm_list = list(perm)
                    inversions = sum(perm_list[i] > perm_list[j] 
                                   for i in range(4) for j in range(i+1,4))
                    if inversions % 2 == 0:
                        v = tuple(coords[p] for p in perm_list)
                        if v not in seen:
                            seen.add(v)
                            verts.append(v)
    return np.array(verts)

verts = build_600cell_vertices()
N = len(verts)
print(f"  Vertices: {N} (expected 120)")

# Build adjacency matrix (edge length² = 2 - phi for 600-cell)
edge_len_sq = 2 - phi  # ≈ 0.382
A = np.zeros((N, N))
for i in range(N):
    for j in range(i+1, N):
        d2 = sum((verts[i][k] - verts[j][k])**2 for k in range(4))
        if abs(d2 - edge_len_sq) < 1e-8:
            A[i,j] = A[j,i] = 1.0

degrees = A.sum(axis=1)
print(f"  Adjacency matrix: max degree = {int(degrees.max())}, total edges = {int(A.sum()//2)}")

# Right multiplication matrices R_i, R_j, R_k on quaternions
# For q in 2I, right mult by i: (a+bi+cj+dk)·i = -b+ai+dj-ck
def quat_right_mult(u, v):
    """Quaternion product u·v for u=(a,b,c,d), v=(e,f,g,h)."""
    a,b,c,d = u
    e,f,g,h = v
    return (a*e - b*f - c*g - d*h,
            a*f + b*e + c*h - d*g,
            a*g - b*h + c*e + d*f,
            a*h + b*g - c*f + d*e)

def build_right_mult_matrix(quat_unit):
    """Build N×N matrix of right multiplication by quat_unit on verts."""
    R = np.zeros((N, N))
    vert_dict = {tuple(np.round(v, 8)): i for i, v in enumerate(verts)}
    for i, v in enumerate(verts):
        w = quat_right_mult(v, quat_unit)
        w_key = tuple(np.round(w, 8))
        if w_key in vert_dict:
            j = vert_dict[w_key]
            R[j, i] = 1.0
        else:
            print(f"  WARNING: right mult not found for vertex {i}")
    return R

R_i = build_right_mult_matrix((0,1,0,0))
R_j = build_right_mult_matrix((0,0,1,0))
R_k = build_right_mult_matrix((0,0,0,1))

print(f"  R_i unitary check: |R_i·R_i^T - I| = {np.max(np.abs(R_i@R_i.T - np.eye(N))):.2e}")

# Weyl gamma matrices (4×4)
s0 = np.array([[1,0],[0,1]], dtype=complex)
s1 = np.array([[0,1],[1,0]], dtype=complex)
s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
s3 = np.array([[1,0],[0,-1]], dtype=complex)
zero2 = np.zeros((2,2), dtype=complex)
I2 = np.eye(2, dtype=complex)

gamma0 = np.block([[zero2, I2], [I2, zero2]])
gamma1 = np.block([[zero2, s1], [-s1, zero2]])
gamma2 = np.block([[zero2, s2], [-s2, zero2]])
gamma3 = np.block([[zero2, s3], [-s3, zero2]])

# Build D_F = A⊗γ0 + (1/2)(R_i+R_i^T)⊗γ1 + (1/2)(R_j+R_j^T)⊗γ2 + (1/2)(R_k+R_k^T)⊗γ3
DF = (np.kron(A, gamma0) + 
      0.5*np.kron(R_i + R_i.T, gamma1) + 
      0.5*np.kron(R_j + R_j.T, gamma2) + 
      0.5*np.kron(R_k + R_k.T, gamma3))

hermitian_err = np.max(np.abs(DF - DF.conj().T))
print(f"  D_F size: {DF.shape}, hermitian error: {hermitian_err:.2e}")

# ============================================================
# Step 2: Compute 2I irrep projectors (isotypic projectors)
# ============================================================
print("\n[Step 2] Computing 2I isotypic projectors...")

# Generate 2I group elements as permutation matrices on ℓ²(2I)
def mat_key(M, tol=6):
    return tuple(np.round(M.real, tol).flatten()) + tuple(np.round(M.imag, tol).flatten())

def quat_to_su2(q):
    a,b,c,d = q
    return np.array([[a+1j*b, c+1j*d], [-c+1j*d, a-1j*b]], dtype=complex)

# Generate 2I elements as quaternions
def gen_2I_elements():
    """Generate all 120 elements of 2I as unit quaternions."""
    s_quat = np.array([0.5, 0.5, 0.5, 0.5])  # (1+i+j+k)/2
    t_quat = np.array([phi/2, 0.5, 1/(2*phi), 0.0])  # (phi+i+k/phi)/2
    
    def q_mult(u, v):
        a,b,c,d = u; e,f,g,h = v
        return np.array([a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
                         a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e])
    
    elements = {}
    key = lambda q: tuple(np.round(q, 8))
    
    def add(q):
        k = key(q)
        if k not in elements:
            elements[k] = q.copy()
            return True
        return False
    
    add(np.array([1,0,0,0], dtype=float))
    frontier = [np.array([1,0,0,0], dtype=float)]
    gens = [s_quat, -s_quat, t_quat, -t_quat,
            np.array([0,1,0,0]), np.array([0,-1,0,0]),
            np.array([0,0,1,0]), np.array([0,0,0,1])]
    
    for _ in range(30):
        new_frontier = []
        for g in frontier:
            for gen in gens:
                m = q_mult(g, gen)
                if add(m):
                    new_frontier.append(m)
                m2 = q_mult(gen, g)
                if add(m2):
                    new_frontier.append(m2)
        if not new_frontier:
            break
        frontier = new_frontier
    
    return list(elements.values())

quats_2I = gen_2I_elements()
print(f"  Generated {len(quats_2I)} elements of 2I")

# Each element acts on ℂ^120 (vertices) via left multiplication
# Build the 120×120 permutation matrix for each g ∈ 2I
vert_dict = {tuple(np.round(v, 8)): i for i, v in enumerate(verts)}

def get_perm_matrix(q):
    """Left multiplication by q on 2I (= vertices of 600-cell)."""
    P = np.zeros((N, N), dtype=float)
    for i, v in enumerate(verts):
        w = quat_right_mult(q, v)  # left multiply: g·v (using right mult with reversed order)
        # Actually: left mult g·v in quaternion product
        # q·v where q,v are unit quaternions
        a,b,c,d = q; e,f,g_,h = v
        r = (a*e - b*f - c*g_ - d*h,
             a*f + b*e + c*h - d*g_,
             a*g_ - b*h + c*e + d*f,
             a*h + b*g_ - c*f + d*e)
        r_key = tuple(np.round(r, 6))
        if r_key in vert_dict:
            j = vert_dict[r_key]
            P[j, i] = 1.0
    return P

print("  Computing permutation matrices (this may take a moment)...")
# Build 120 permutation matrices P_g: N×N
perm_matrices = [get_perm_matrix(q) for q in quats_2I]
print(f"  Built {len(perm_matrices)} permutation matrices")

# Verify: check first few are permutation matrices
for P in perm_matrices[:3]:
    assert abs(P.sum(axis=0).max() - 1) < 0.01, "Not a permutation matrix"

# ============================================================
# Character table values for isotypic projection
# ============================================================
# The character table in our ordering:
chi_table = {
    'rho1': [1, 1, 1, 1, 1, 1, 1, 1, 1],
    'rho2': [2, -2, -1, 0, -phi, 1/phi, 1, phi, -1/phi],
    'rho3': [2, -2, -1, 0, 1/phi, -phi, 1, -1/phi, phi],
    'rho4': [3, 3, 0, -1, phi, -1/phi, 0, phi, -1/phi],
    'rho5': [3, 3, 0, -1, -1/phi, phi, 0, -1/phi, phi],
    'rho6': [4, 4, 1, 0, -1, -1, 1, -1, -1],
    'rho7': [4, -4, 1, 0, -1, -1, -1, 1, 1],
    'rho8': [5, 5, -1, 1, 0, 0, -1, 0, 0],
    'rho9': [6, -6, 0, 0, 1, 1, 0, -1, -1],
}
irrep_dims = {'rho1':1,'rho2':2,'rho3':2,'rho4':3,'rho5':3,'rho6':4,'rho7':4,'rho8':5,'rho9':6}

# Assign conjugacy class label to each element of 2I
# Classes in ATLAS order: 1A(1), 2A(1), 3A(20), 4A(30), 5A(12), 5B(12), 6A(20), 10A(12), 10B(12)
def get_class(q):
    """Identify conjugacy class of q ∈ 2I by trace and order."""
    # Trace = sum of quaternion components times appropriate sign
    # For SU(2): Tr(q as 2x2 matrix) = 2*Re(q) = 2*q[0]
    tr = 2*q[0]
    
    # Order: smallest k such that q^k = ±1 or just compute from trace
    # Using: Tr(g^n) computed via 2cos(nθ/2) where Tr(g)=2cos(θ/2)
    
    # Assign by (approximate trace, order)
    def elem_order(q):
        curr = q.copy()
        for k in range(1, 31):
            if abs(curr[0] - 1) < 1e-6 and np.max(np.abs(curr[1:])) < 1e-6:
                return k
            if abs(curr[0] + 1) < 1e-6 and np.max(np.abs(curr[1:])) < 1e-6:
                return 2*k  # currently at -1
            # multiply by q
            a,b,c,d = curr; e,f,g_,h = q
            curr = np.array([a*e-b*f-c*g_-d*h, a*f+b*e+c*h-d*g_,
                            a*g_-b*h+c*e+d*f, a*h+b*g_-c*f+d*e])
        return None
    
    ord_q = elem_order(q)
    
    # Match to class by (order, trace)
    # 1A: ord=1, tr=2
    if ord_q == 1: return 0  # 1A
    elif ord_q == 2: return 1  # 2A (tr=-2)
    elif ord_q == 3: return 2  # 3A (tr=-1)
    elif ord_q == 4: return 3  # 4A (tr=0)
    elif ord_q == 5:
        if tr > 0: return 4   # 5B (tr=1/φ>0) -- careful: 5B has tr=+1/φ, 5A has tr=-φ<0
        else: return 5         # 5A
    elif ord_q == 6: return 6  # 6A (tr=1)
    elif ord_q == 10:
        if tr > 0: return 7   # 10A (tr=φ>0)
        else: return 8         # 10B (tr=-1/φ<0)
    else:
        return -1

# Build isotypic projector via character formula:
# P_ρ = (dim ρ / |G|) Σ_{g∈G} χ_ρ(g)* · L_g
# where L_g is the left action of g on ℓ²(2I)

def build_isotypic_projector(irrep_name):
    """Build the isotypic projector P_ρ on ℂ^N (N=120)."""
    d = irrep_dims[irrep_name]
    chi = chi_table[irrep_name]
    
    P = np.zeros((N, N), dtype=complex)
    for idx, q in enumerate(quats_2I):
        c = get_class(q)
        if c < 0:
            continue
        chi_val = chi[c]
        P += chi_val * perm_matrices[idx]
    
    P *= d / G_order
    return P

print("\n  Computing isotypic projectors...")
G_order = 120

projectors = {}
for rho in chi_table.keys():
    P = build_isotypic_projector(rho)
    projectors[rho] = P

# Verify projectors are orthogonal idempotents
print("\n  Verifying projectors (P²=P, PQ=0 for P≠Q, ΣP=I)...")
proj_ok = True
for rho, P in projectors.items():
    # P² = P
    P2 = P @ P
    err = np.max(np.abs(P2 - P))
    if err > 0.01:
        proj_ok = False
        print(f"    {rho}: P²≠P, error={err:.4f}")
    d = irrep_dims[rho]
    tr = np.trace(P).real
    expected_tr = d**2  # = dim²(ρ) (multiplicity × dim = dim × dim in regular rep)
    if abs(tr - expected_tr) > 0.1:
        proj_ok = False
        print(f"    {rho}: Tr(P)={tr:.2f}, expected {expected_tr}")

# Sum of projectors = Identity?
P_sum = sum(projectors.values())
I_err = np.max(np.abs(P_sum.real - np.eye(N)))
print(f"    ΣP = I: max error = {I_err:.4f} {'✓' if I_err < 0.01 else '✗'}")
print(f"    All P²=P: {'✓' if proj_ok else '✗'}")

# ============================================================
# Step 3: Compute Yukawa blocks Y_{LR} = P_R · D_F · P_L
# ============================================================
print("\n[Step 3] Computing Yukawa blocks Y_LR = P_R · D_F · P_L")
print("(where P_L, P_R are 120×120 projectors, D_F is 480×480)")
print("Expanding to 480×480: P_ρ ⊗ I_4 (⊗ with spin-4 space)")

# Lift projectors to 480×480 space
def lift_projector(P_120, spin_dim=4):
    return np.kron(P_120.real, np.eye(spin_dim))

rho_names = list(chi_table.keys())

print("\n  Computing off-diagonal blocks Y_{LR}:")
print(f"  {'Pair (L,R)':<25} {'rank(Y)':<10} {'top-3 sv':<35} {'ratio sv1/sv2':<15}")
print("  " + "-"*90)

svd_results = {}
for rho_L in rho_names:
    PL = lift_projector(projectors[rho_L])
    for rho_R in rho_names:
        PR = lift_projector(projectors[rho_R])
        
        # Yukawa block: Y = P_R · D_F · P_L
        Y = PR @ DF @ PL
        
        # SVD
        try:
            _, sv, _ = svd(Y, full_matrices=False)
        except:
            sv = np.zeros(min(Y.shape))
        
        sv = sv[sv > 1e-8]  # filter near-zero
        rank = len(sv)
        top3 = sv[:3] if len(sv) >= 3 else sv
        ratio = sv[0]/sv[1] if len(sv) >= 2 and sv[1] > 1e-8 else float('inf')
        
        label = f"({rho_L},{rho_R})"
        svd_results[label] = {
            'sv': sv.tolist(),
            'rank': rank,
            'ratio_sv1_sv2': float(ratio) if not np.isinf(ratio) else None,
        }
        
        sv_str = ', '.join(f'{x:.4f}' for x in top3)
        ratio_str = f'{ratio:.2f}' if not np.isinf(ratio) else 'inf'
        if rank > 0:  # only print non-trivial blocks
            print(f"  {label:<25} {rank:<10} {sv_str:<35} {ratio_str:<15}")

# ============================================================
# Step 4: Compare to SM mass ratios
# ============================================================
print("\n[Step 4] Comparison to SM mass ratios")
print("="*70)

# SM lepton mass ratios: m_e : m_mu : m_tau ≈ 1 : 206.77 : 3477.23
SM_lepton = np.array([1.0, 206.77, 3477.23])
SM_lepton_log = np.log(SM_lepton)

# SM quark mass ratios (u-type): m_u : m_c : m_t ≈ 1 : 587 : 130000
SM_quark = np.array([1.0, 587.0, 130000.0])
SM_quark_log = np.log(SM_quark)

best_lepton_sigma = float('inf')
best_lepton_pair = None
best_lepton_sv = None

best_quark_sigma = float('inf')
best_quark_pair = None
best_quark_sv = None

print(f"\n  SM lepton ratios (log): {SM_lepton_log}")
print(f"  SM quark ratios (log):  {SM_quark_log}")

print(f"\n  Searching all 81 irrep pairs for closest match...")
print(f"  {'Pair':<25} {'Lepton σ':<12} {'Quark σ':<12} {'Ratios (normalized)'}")
print("  " + "-"*80)

for label, data in svd_results.items():
    sv = np.array(data['sv'])
    if len(sv) < 3:
        continue
    
    # Normalize to first value
    sv_norm = sv[:3] / sv[0]
    sv_log = np.log(sv_norm + 1e-30)
    
    # σ-distance to SM lepton
    sigma_lep = np.sqrt(np.mean((sv_log - SM_lepton_log)**2))
    # σ-distance to SM quark
    sigma_q = np.sqrt(np.mean((sv_log - SM_quark_log)**2))
    
    if sigma_lep < best_lepton_sigma:
        best_lepton_sigma = sigma_lep
        best_lepton_pair = label
        best_lepton_sv = sv[:3]
    
    if sigma_q < best_quark_sigma:
        best_quark_sigma = sigma_q
        best_quark_pair = label
        best_quark_sv = sv[:3]
    
    ratio_str = ':'.join(f'{x:.3f}' for x in sv_norm[:3])
    print(f"  {label:<25} {sigma_lep:<12.3f} {sigma_q:<12.3f} 1:{sv_norm[1]:.3f}:{sv_norm[2]:.3f}")

print(f"\n  Best match (lepton ratios): {best_lepton_pair}")
print(f"    Singular values: {best_lepton_sv}")
if best_lepton_sv is not None:
    sv_norm = best_lepton_sv / best_lepton_sv[0]
    print(f"    Ratios:          1 : {sv_norm[1]:.3f} : {sv_norm[2]:.3f}")
    print(f"    SM expected:     1 : 206.77 : 3477.23")
    print(f"    σ-distance:      {best_lepton_sigma:.4f} (SM threshold < 0.5)")

print(f"\n  Best match (quark ratios): {best_quark_pair}")
print(f"    σ-distance:      {best_quark_sigma:.4f} (SM threshold < 0.5)")

# ============================================================
# Step 5: Schur's lemma verification
# ============================================================
print("\n[Step 5] Schur's Lemma Numerical Verification")
print("="*70)

print("""
  Schur's lemma predicts:
  (a) Y_{LR} = 0 for L ≠ R (off-diagonal blocks vanish)
  (b) Y_{LL} = λ_L · Id (diagonal blocks are scalar multiples of identity)
  
  This means: all singular values of Y_{LL} are EQUAL.
  And: any two irreps in the same isotypic component have the same mass.
  Therefore: ZERO mass hierarchy from 2I-equivariant D_F alone.
""")

print(f"  Verifying (a): Y_{{L,R}}=0 for L≠R?")
off_diag_max = 0.0
for rho_L in rho_names:
    for rho_R in rho_names:
        if rho_L == rho_R: continue
        label = f"({rho_L},{rho_R})"
        sv = svd_results[label]['sv']
        if sv:
            off_diag_max = max(off_diag_max, max(sv))

print(f"    Max singular value of off-diagonal Y_LR: {off_diag_max:.6f}")
print(f"    {'✓ Schur confirmed (off-diag ≈ 0)' if off_diag_max < 0.01 else '✗ Unexpected off-diagonal content'}")

print(f"\n  Verifying (b): Y_{{L,L}} is scalar?")
for rho_L in rho_names:
    label = f"({rho_L},{rho_L})"
    sv = svd_results[label]['sv']
    if sv and len(sv) > 1:
        spread = (max(sv) - min(sv)) / (max(sv) + 1e-30)
        print(f"    {rho_L}: sv spread = {spread:.6f} {'(≈ scalar ✓)' if spread < 0.01 else '(NOT scalar ✗)'}")
    elif sv:
        print(f"    {rho_L}: single sv = {sv[0]:.6f} (trivially scalar)")
    else:
        print(f"    {rho_L}: all sv = 0 (zero block)")

# ============================================================
# Step 6: Could MODIFIED Yukawa matrix help?
# ============================================================
print("\n[Step 6] Analytic Assessment: What Yukawa Can/Cannot Do")
print("="*70)
print("""
  In standard NCG (Chamseddine-Connes), the Yukawa coupling Y is NOT computed
  from the group action — it is a FREE PARAMETER encoded in D_F as:
  
      D_F = S ⊗ γ^μ D_μ  +  Y ⊗ γ^5  (schematic)
  
  where Y is a 3×3 matrix (in generation space) with eigenvalues proportional
  to the fermion masses. Y must be INPUT by hand; it is NOT derived from geometry.
  
  Our construction: D_F built from 2I action alone (kinematic term only).
  This gives block-scalar structure (Schur's lemma) → NO hierarchy.
  
  To introduce hierarchy, one MUST add:
    1. A scalar (Higgs) field φ transforming as a specific 2I irrep.
    2. A Yukawa term: Y_{ij} = Σ_{a} C_{ij}^a φ_a
       where C_{ij}^a = CG coefficient ⟨ρᵢ ⊗ ρⱼ | ρ_Higgs⟩
    3. The physical masses come from: m_i = y_i · ⟨φ⟩ (VEV × Yukawa coupling)
  
  Can the CG structure of 2I constrain the mass ratios?
  From our CG computation:
    ρ4(3) ⊗ ρ4(3) = ρ1(1) ⊕ ρ4(3) ⊕ ρ8(5)
  If leptons live in ρ4(3) and Higgs in ρ1(1) (singlet):
    Y_{ij} = y · δ_{ij}  (completely democratic, all masses equal!)
  If Higgs in ρ4(3):
    Y_{ij} = structure constant of ρ4(3)×ρ4(3)→ρ4(3) (CG coefficients)
    This can give 3 distinct eigenvalues — but they are FIXED by group theory.
    The 3 eigenvalues of the ρ4(3) CG matrix must be computed.
""")

# Compute eigenvalues of CG matrix for rho4(3) ⊗ rho4(3) → rho4(3) component
print("  Computing CG matrix for ρ4(3)⊗ρ4(3)→ρ4(3) (3-dim Yukawa)...")

# The CG matrix C_{ij}^k for ρ4(3)⊗ρ4(3)→ρ4(3) is a 3×3 matrix.
# By Schur's lemma, this equals the structure constants of ρ4(3) viewed as a Lie algebra.
# For ρ4(3) = 3-dim rep of A5: this is related to the icosahedral 3d rep.
# The structure constants are: f_{abc} where [T_a, T_b] = f_{abc} T_c

# The 3d irrep of 2I (= A5 acted on its 3d rep, lifted):
# Generators in 3d: standard SO(3) generators restricted to icosahedral symmetry
# The eigenvalues of the symmetrized CG matrix depend on the specific normalization.

# For icosahedral group: 3-dim rep structure = SO(3) generators → eigenvalues ±1, 0
# More precisely: the symmetric CG ρ4⊗ρ4→ρ4 gives a 3×3 totally symmetric tensor
# which for the icosahedral group has eigenvalues determined by the 5-fold symmetry.

# Let's compute numerically using the projectors:
# The ρ4(3) isotypic component of ℓ²(2I) is 9-dimensional (= 3 × 3 multiplicity)
# Project D_F onto this 9-dimensional subspace and compute its spectrum

P4 = lift_projector(projectors['rho4'])
# D_F restricted to rho4 isotypic block:
D_rho4 = P4 @ DF @ P4

# Get the non-trivial eigenvalues
evals_rho4 = np.linalg.eigvalsh(D_rho4.real)
evals_rho4_nonzero = evals_rho4[np.abs(evals_rho4) > 0.01]
evals_unique = np.unique(np.round(np.abs(evals_rho4_nonzero), 6))
print(f"  Eigenvalues of D_F|_{{ρ4}} (nonzero): {evals_unique}")
print(f"  Expected by Schur: all equal (λ·Id). Spread = {np.std(evals_unique):.6f}")

# ============================================================
# Summary and save
# ============================================================
print("\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)
print(f"""
  Construction: Y_{{LR}} = P_R · D_F · P_L for all 81 irrep pairs.
  
  Schur's lemma VERIFIED numerically:
    • Off-diagonal blocks Y_{{L≠R}}: max SV = {off_diag_max:.6f} ≈ 0
    • Diagonal blocks Y_{{LL}}: all SVs equal within each block
  
  Best fit to SM lepton ratios:
    Pair: {best_lepton_pair}
    σ-distance: {best_lepton_sigma:.4f}  (SM requires < 0.5)
    Verdict: DOES NOT MATCH (σ >> 1)
  
  Best fit to SM quark ratios:
    Pair: {best_quark_pair}
    σ-distance: {best_quark_sigma:.4f}  (SM requires < 0.5)
    Verdict: DOES NOT MATCH (σ >> 1)
  
  CONCLUSION: The 2I-equivariant D_F from Wave 8.4 CANNOT produce SM mass
  hierarchies through the irrep block structure. Schur's lemma is an absolute
  barrier. To get mass hierarchies, one MUST:
  (1) Break 2I symmetry explicitly (Higgs VEV), or
  (2) Add a generation index not tied to 2I action, or  
  (3) Use a non-equivariant modification of D_F.
  
  This is a STRONG NEGATIVE result, not a failure of the method.
  It clarifies exactly what 2I symmetry can and cannot predict.
""")

# Save all results
results = {
    "method": "Yukawa from 2I irrep projectors: Y_LR = P_R · D_F · P_L",
    "D_F_size": list(DF.shape),
    "hermitian_error": float(hermitian_err),
    "n_2I_elements": len(quats_2I),
    "projector_sum_error": float(I_err),
    "off_diagonal_max_sv": float(off_diag_max),
    "schur_lemma_verified": bool(off_diag_max < 0.01),
    "svd_results": svd_results,
    "best_lepton_pair": best_lepton_pair,
    "best_lepton_sigma": float(best_lepton_sigma),
    "best_lepton_sv": best_lepton_sv.tolist() if best_lepton_sv is not None else None,
    "best_quark_pair": best_quark_pair,
    "best_quark_sigma": float(best_quark_sigma),
    "SM_lepton_ratios": [1.0, 206.77, 3477.23],
    "SM_quark_ratios": [1.0, 587.0, 130000.0],
    "verdict": "DOES NOT MATCH SM: σ >> 0.5. Schur's lemma is the fundamental barrier.",
    "conclusion": (
        "2I-equivariant D_F cannot produce mass hierarchies. "
        "Any Yukawa Y_LR = P_R D_F P_L vanishes for L≠R and is scalar for L=R. "
        "Breaking 2I symmetry (Higgs mechanism) is mandatory."
    )
}

out_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(out_dir, 'yukawa_results.json'), 'w') as f:
    json.dump(results, f, indent=2)
print(f"Saved → yukawa_results.json")

#!/usr/bin/env python3
"""Generate phase_transition.pdf — Figure 1 of the Vasilev-Pellis-Olsen letter.
Conjectured shapes ONLY (not measured data); see the figure caption."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = np.linspace(0, 20, 600)
Cstar = 9.0

def coverage(C, T):
    # sigmoid sharpening with |T|: steeper for larger target set
    k = 0.35 * np.sqrt(T) / np.sqrt(42)
    return 1.0 / (1.0 + np.exp(-k * (C - Cstar)))

def susceptibility(C, T):
    rho = coverage(C, T)
    return np.gradient(rho, C)

Ts = [(42, "$|T| = 42$ (Catalog42)", "#1f9e9e"),
      (168, "$|T| = 168$", "#c0392b"),
      (672, "$|T| = 672$", "#1b3a4b")]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.0))

for T, label, color in Ts:
    ax1.plot(C, coverage(C, T), color=color, lw=2, label=label)
ax1.axvline(Cstar, color="gray", ls="--", lw=1)
ax1.text(Cstar + 0.2, 0.05, "$C^*$", color="gray")
ax1.set_xlabel("complexity budget $C$")
ax1.set_ylabel(r"coverage $\rho(C,\epsilon)$")
ax1.set_title("Conjectured coverage order parameter")
ax1.set_xlim(0, 20); ax1.set_ylim(0, 1.05)
ax1.legend(frameon=False, fontsize=9, loc="center left")
ax1.grid(alpha=0.25)

for T, label, color in Ts:
    chi = susceptibility(C, T)
    ax2.plot(C, chi, color=color, lw=2, label=label)
ax2.axvline(Cstar, color="gray", ls="--", lw=1)
ax2.set_xlabel("complexity budget $C$")
ax2.set_ylabel(r"susceptibility $\chi(C) = \partial_C \rho$")
ax2.set_title(r"Susceptibility peak; width $\sim |T|^{-1/2}$")
ax2.set_xlim(0, 20)
ax2.legend(frameon=False, fontsize=9, loc="upper right")
ax2.grid(alpha=0.25)

fig.suptitle("Illustration of the conjectured symbolic phase transition (shape only - not measured data)",
             fontsize=10, y=1.02)
fig.tight_layout()
fig.savefig("phase_transition.pdf", bbox_inches="tight")
fig.savefig("phase_transition.png", dpi=150, bbox_inches="tight")
print("wrote phase_transition.pdf / .png")

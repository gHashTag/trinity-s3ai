//! Trinity S³AI v5.0 — H4 Coxeter Group → Standard Model
//!
//! Complete Rust implementation of the Trinity framework:
//! - Algebraic rings (Q(√5) with phi-structure)
//! - H4 Coxeter group and reflection subgroups
//! - Spectral triple and spectral action
//! - 0 of 26 core formulas are rigorous derivations from H4 invariants; 3 of 13 Lagrangian sectors formally proven
//! - Validation against experimental data
//!
//! Usage: cargo run --release

mod export;
mod coq_bridge;
mod spectral_numeric;
mod json_schema;
use export::export_json;
use json_schema::generate_arxiv_json;
mod biology;
mod cosmology;
mod formulas;
mod gauge;
mod h4;
mod higgs;
mod mixing;
mod ml_params;
mod rg;
mod ring;
mod spectral;
mod stages;
mod validation;
mod yukawa;

use stages::run_full_derivation;
use validation::ValidationReport;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let json_mode = args.iter().any(|a| a == "--json");
    let arxiv_mode = args.iter().any(|a| a == "--arxiv");

    if arxiv_mode {
        println!("{}", generate_arxiv_json());
        return;
    }

    if json_mode {
        println!("{}", export_json());
        return;
    }

    println!("\n");
    println!("╔══════════════════════════════════════════════════════════════════════╗");
    println!("║                                                                      ║");
    println!("║     𝒵_TRINITY  S³AI  v5.0                                            ║");
    println!("║     H4 Coxeter Group → Standard Model Lagrangian                     ║");
    println!("║                                                                      ║");
    println!("║     φ² + 1/φ² = 3                                                    ║");
    println!("║                                                                      ║");
    println!("╚══════════════════════════════════════════════════════════════════════╝");

    run_full_derivation();

    println!("\n");
    let report = ValidationReport::generate();
    report.print();

    println!("\n");
    println!("╔══════════════════════════════════════════════════════════════════════╗");
    println!("║  FINAL STATUS                                                        ║");
    println!("╠══════════════════════════════════════════════════════════════════════╣");
    println!("║  79 Coq files (partial compilation) |  1325 Qed / 123 unproven       ║");
    println!("║  3/13 Lagrangian sectors formally proven |  44 SG-class fitted coincidences ║");
    println!("║  5 Boundary Theorems QED           |  NOT submitted to arXiv        ║");
    println!("╚══════════════════════════════════════════════════════════════════════╝");

    if report.is_success() {
        println!("\n✅ ALL VALIDATIONS PASSED — H4 → SM numerical coincidences are consistent.\n");
    } else {
        println!("\n⚠️  Some validations failed — review failures above.\n");
    }
}

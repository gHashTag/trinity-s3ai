//! Coq Bridge — parse and verify Coq proofs from Rust
//!
//! Connects the Trinity S³AI Rust codebase with the Coq proof base
//! located at `../proofs/trinity/`.

use regex::Regex;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

/// Compilation status of a Coq theorem
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum CoqStatus {
    Qed,
    Admitted,
    Proven,
    Open,
}

/// Parsed Coq theorem/lemma/definition
#[derive(Clone, Debug)]
pub struct CoqFormula {
    pub file: String,
    pub theorem: String,
    pub statement: String,
    pub status: CoqStatus,
}

/// Parser for Coq `.v` files (regex-based, not a full Coq parser)
pub struct CoqParser;

impl CoqParser {
    /// Parse a single `.v` file and return all discovered items
    pub fn parse_file(path: &Path) -> Vec<CoqFormula> {
        let content = fs::read_to_string(path).unwrap_or_default();
        let file_name = path
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("unknown")
            .to_string();

        let decl_re =
            Regex::new(r"(?m)^\s*(Theorem|Lemma|Definition|Corollary)\s+([A-Za-z0-9_]+)").unwrap();
        let mut formulas = Vec::new();

        let matches: Vec<_> = decl_re.find_iter(&content).collect();

        for (idx, mat) in matches.iter().enumerate() {
            let caps = decl_re.captures(mat.as_str()).unwrap();
            let _kind = caps.get(1).unwrap().as_str();
            let name = caps.get(2).unwrap().as_str();

            let start = mat.start();
            let end = if idx + 1 < matches.len() {
                matches[idx + 1].start()
            } else {
                content.len()
            };

            let region = &content[start..end];

            // Determine status by looking for terminal keywords in the region
            let region_trimmed = region.trim();
            let status = if region_trimmed.contains("Qed.") {
                CoqStatus::Qed
            } else if region_trimmed.contains("Admitted.") {
                CoqStatus::Admitted
            } else if region_trimmed.contains("Proof.") {
                CoqStatus::Open
            } else {
                CoqStatus::Proven
            };

            // Extract statement: text between ':' and 'Proof.' / 'Qed.' / 'Admitted.' / next decl
            let after_decl = &content[mat.end()..end];
            let statement = if let Some(colon_idx) = after_decl.find(':') {
                let after_colon = &after_decl[colon_idx + 1..];
                let mut stmt = String::new();
                for line in after_colon.lines() {
                    let trimmed = line.trim();
                    if trimmed.starts_with("Proof.")
                        || trimmed.starts_with("Qed.")
                        || trimmed.starts_with("Admitted.")
                        || trimmed.starts_with("Defined.")
                    {
                        break;
                    }
                    stmt.push_str(trimmed);
                    stmt.push(' ');
                    // heuristic: statement usually ends at first standalone '.'
                    if trimmed.ends_with('.')
                        && !trimmed.ends_with("..")
                        && !trimmed.starts_with("(*")
                        && !trimmed.starts_with("Require")
                        && !trimmed.starts_with("From")
                        && !trimmed.starts_with("Open")
                        && !trimmed.starts_with("Close")
                        && !trimmed.starts_with("Section")
                        && !trimmed.starts_with("End")
                        && !trimmed.starts_with("Parameter")
                        && !trimmed.starts_with("Hypothesis")
                    {
                        break;
                    }
                }
                stmt.trim().to_string()
            } else {
                String::new()
            };

            formulas.push(CoqFormula {
                file: file_name.clone(),
                theorem: name.to_string(),
                statement,
                status,
            });
        }

        formulas
    }

    /// Parse all `.v` files in `../proofs/trinity`
    pub fn parse_all() -> Vec<CoqFormula> {
        let proofs_dir = Path::new("../proofs/trinity");
        let mut all = Vec::new();

        if let Ok(entries) = fs::read_dir(proofs_dir) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.extension().and_then(|e| e.to_str()) == Some("v") {
                    all.extend(Self::parse_file(&path));
                }
            }
        }

        all
    }

    /// Parse the four key files explicitly requested
    pub fn parse_key_files() -> Vec<CoqFormula> {
        let files = [
            "CorePhi.v",
            "H4Derivations.v",
            "SpectralAction600Cell.v",
            "HiggsPotentialCorrected.v",
        ];
        let proofs_dir = Path::new("../proofs/trinity");
        let mut all = Vec::new();
        for file in &files {
            let path = proofs_dir.join(file);
            if path.exists() {
                all.extend(Self::parse_file(&path));
            }
        }
        all
    }
}

/// Verify a single Coq theorem by name.
///
/// 1. Locates the `.v` file containing the theorem.
/// 2. If the corresponding `.vo` exists and is newer, returns `true`.
/// 3. Otherwise attempts to compile with `coqc`.
pub fn verify_coq_theorem(name: &str) -> bool {
    let proofs_dir = Path::new("../proofs/trinity");
    let decl_re = match Regex::new(&format!(
        r"(?m)^\s*(Theorem|Lemma|Definition|Corollary)\s+{}",
        regex::escape(name)
    )) {
        Ok(re) => re,
        Err(_) => return false,
    };

    let target_file = fs::read_dir(proofs_dir).ok().and_then(|entries| {
        for entry in entries.flatten() {
            let path = entry.path();
            if path.extension().and_then(|e| e.to_str()) == Some("v") {
                if let Ok(content) = fs::read_to_string(&path) {
                    if decl_re.is_match(&content) {
                        return Some(path);
                    }
                }
            }
        }
        None
    });

    let file_path = match target_file {
        Some(p) => p,
        None => return false,
    };

    let vo_path = file_path.with_extension("vo");

    // Check if .vo is up-to-date
    if vo_path.exists() && file_path.exists() {
        if let (Ok(vo_meta), Ok(v_meta)) = (fs::metadata(&vo_path), fs::metadata(&file_path)) {
            if let (Ok(vo_time), Ok(v_time)) = (vo_meta.modified(), v_meta.modified()) {
                if vo_time >= v_time {
                    return true;
                }
            }
        }
    }

    // Determine project root (parent of trinity_rust if we're inside it)
    let current_dir = std::env::current_dir().unwrap_or_else(|_| PathBuf::from("."));
    let project_root = if current_dir.file_name().and_then(|f| f.to_str()) == Some("trinity_rust") {
        current_dir.parent().unwrap_or(&current_dir).to_path_buf()
    } else {
        current_dir
    };

    let file_name = file_path.file_name().and_then(|f| f.to_str()).unwrap_or("");
    let v_rel = format!("proofs/trinity/{}", file_name);

    let output = Command::new("coqc")
        .args(&["-Q", "proofs/trinity", "Trinity"])
        .arg(&v_rel)
        .current_dir(&project_root)
        .output();

    match output {
        Ok(out) => out.status.success(),
        Err(_) => false,
    }
}

/// Compare Rust formula catalog with Coq theorems and print mismatches
pub fn sync_with_formulas() {
    let coq_theorems = CoqParser::parse_all();
    let rust_formulas: Vec<_> = crate::formulas::tier1_formulas()
        .into_iter()
        .chain(crate::formulas::tier2_formulas().into_iter())
        .collect();

    println!("=== Coq ↔ Rust Formula Sync ===");
    println!("Coq theorems/lemmas/definitions: {}", coq_theorems.len());
    println!("Rust formulas: {}", rust_formulas.len());

    let mut mismatches = Vec::new();

    for formula in &rust_formulas {
        let id = formula.id;
        let mut found = false;
        for coq in &coq_theorems {
            // Heuristic 1: theorem name starts with formula ID
            if coq.theorem.starts_with(id) {
                found = true;
                break;
            }
            // Heuristic 2: formula name appears in theorem name (case-insensitive, spaces→_)
            let norm_formula = formula.name.to_lowercase().replace(' ', "_");
            let norm_theorem = coq.theorem.to_lowercase();
            if norm_theorem.contains(&norm_formula) {
                found = true;
                break;
            }
        }
        if !found {
            mismatches.push((id, formula.name));
            println!(
                "MISMATCH: Rust formula '{}' ({}) has no Coq counterpart",
                id, formula.name
            );
        }
    }

    if mismatches.is_empty() {
        println!("All Rust formulas have Coq counterparts.");
    } else {
        println!("Total mismatches: {}/{}", mismatches.len(), rust_formulas.len());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_core_phi_proven() {
        let formulas = CoqParser::parse_key_files();
        let phi_sq = formulas.iter().find(|f| f.theorem == "phi_sq");
        assert!(phi_sq.is_some(), "phi_sq theorem not found in CorePhi.v");
        let phi_sq = phi_sq.unwrap();
        assert_eq!(
            phi_sq.status,
            CoqStatus::Qed,
            "phi_sq should have Qed status"
        );
        assert!(
            phi_sq.statement.contains("phi * phi = phi + 1")
                || phi_sq.statement.contains("phi * phi"),
            "phi_sq statement mismatch: {}",
            phi_sq.statement
        );
    }

    #[test]
    fn test_coq_files_exist() {
        let proofs_dir = Path::new("../proofs/trinity");
        let vo_count = fs::read_dir(proofs_dir)
            .unwrap()
            .filter_map(|e| e.ok())
            .filter(|e| e.path().extension().and_then(|e| e.to_str()) == Some("vo"))
            .count();
        assert!(
            vo_count >= 26,
            "Expected at least 26 .vo files, found {}",
            vo_count
        );
    }
}

// Dependency-direction guard.
//
// The ring architecture is only meaningful if dependencies point INWARD:
//
//     ring0_core   <-  ring1_constraints  <-  ring2_search  <-  ring3_adapters  <-  app
//
// In particular:
//   * ring 0 must not depend on any other ring crate, nor on serde_json or fs.
//   * ring 1 must depend on ring 0 only.
//   * ring 2 must depend on ring 0 + ring 1 only.
//   * ring 3 may add serde_json (it is the IO boundary).
//
// This test reads each crate's Cargo.toml as plain text (no toml parser
// dependency) and asserts the relevant invariants. If you add a new crate
// to the workspace, extend this file.

use std::fs;
use std::path::PathBuf;

fn manifest(name: &str) -> String {
    let mut p = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    // CARGO_MANIFEST_DIR points at crates/app; go up to the workspace root.
    p.pop();
    p.pop();
    p.push("crates");
    p.push(name);
    p.push("Cargo.toml");
    fs::read_to_string(&p).unwrap_or_else(|e| panic!("missing {}: {}", p.display(), e))
}

fn deps_block(manifest_str: &str) -> &str {
    // Find the [dependencies] block. Stops at next top-level [section] or EOF.
    let start = manifest_str
        .find("[dependencies]")
        .expect("no [dependencies] block");
    let rest = &manifest_str[start + "[dependencies]".len()..];
    let end = rest.find("\n[").unwrap_or(rest.len());
    &rest[..end]
}

fn declares(manifest_str: &str, dep: &str) -> bool {
    deps_block(manifest_str)
        .lines()
        .any(|l| l.trim_start().starts_with(&format!("{} ", dep))
            || l.trim_start().starts_with(&format!("{}=", dep)))
}

#[test]
fn ring0_has_no_ring_dependencies() {
    let m = manifest("ring0_core");
    for forbidden in [
        "ring1_constraints",
        "ring2_search",
        "ring3_adapters",
        "trinity_fold_app",
        "serde_json", // ring 0 is the type layer; no JSON here
    ] {
        assert!(
            !declares(&m, forbidden),
            "ring0_core must not depend on `{}` — found in its [dependencies]",
            forbidden
        );
    }
}

#[test]
fn ring1_depends_on_ring0_only() {
    let m = manifest("ring1_constraints");
    assert!(declares(&m, "ring0_core"), "ring1_constraints must depend on ring0_core");
    for forbidden in ["ring2_search", "ring3_adapters", "trinity_fold_app", "serde_json"] {
        assert!(
            !declares(&m, forbidden),
            "ring1_constraints must not depend on `{}`",
            forbidden
        );
    }
}

#[test]
fn ring2_depends_on_ring0_and_ring1_only() {
    let m = manifest("ring2_search");
    assert!(declares(&m, "ring0_core"));
    assert!(declares(&m, "ring1_constraints"));
    for forbidden in ["ring3_adapters", "trinity_fold_app", "serde", "serde_json"] {
        assert!(
            !declares(&m, forbidden),
            "ring2_search must not depend on `{}`",
            forbidden
        );
    }
}

#[test]
fn ring3_may_depend_on_lower_rings_and_is_the_io_boundary() {
    let m = manifest("ring3_adapters");
    assert!(declares(&m, "ring0_core"));
    assert!(declares(&m, "ring1_constraints"));
    assert!(declares(&m, "ring2_search"));
    // serde_json is allowed here (this is the JSON boundary).
    assert!(declares(&m, "serde_json"));
    assert!(
        !declares(&m, "trinity_fold_app"),
        "ring3_adapters must not depend on the outer app crate"
    );
}

#[test]
fn ring0_source_is_io_and_rng_free() {
    // Lightweight grep over the ring 0 source. Catches anyone who adds fs/IO
    // back into the core by accident. Keeping this list short and explicit.
    let mut p = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    p.pop();
    p.pop();
    p.push("crates/ring0_core/src");
    for entry in fs::read_dir(&p).expect("ring0 src dir") {
        let entry = entry.expect("entry");
        let path = entry.path();
        if path.extension().and_then(|s| s.to_str()) != Some("rs") {
            continue;
        }
        let src = fs::read_to_string(&path).expect("read");
        for forbidden in ["std::fs", "std::net", "std::process", "std::thread::sleep"] {
            assert!(
                !src.contains(forbidden),
                "ring0_core/{} contains forbidden API `{}`",
                path.file_name().unwrap().to_string_lossy(),
                forbidden
            );
        }
    }
}

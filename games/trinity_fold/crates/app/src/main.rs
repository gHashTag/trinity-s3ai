// Trinity Fold CLI — orchestration ring.
//
// This binary is the outermost ring. It composes ring 0 (types), ring 1
// (scoring), ring 2 (search), and ring 3 (adapters) but holds no logic of
// its own beyond argument parsing and presentation.
//
// Subcommands:
//   score      — score a board (list of node ids, comma-separated)
//   search     — run hill climbing or simulated annealing from an initial board
//   export     — dump the default catalog as JSON (used by the web UI)
//   benchmark  — like `score`, but hides the held-out observables
//
// Honesty caveat: this binary reports numbers. None of those numbers should
// be cited as evidence for or against any unification claim. See
// games/trinity_fold/README.md.

use std::env;
use std::process::ExitCode;

use ring0_core::{Board, Catalog};
use ring1_constraints::{
    ScoreBreakdown, ScoreWeights, score_board, score_board_with, tower_counts,
};
use ring2_search::{anneal, hill_climb};
use ring3_adapters::{benchmark_holdout_ids, default_catalog, save_catalog};

fn main() -> ExitCode {
    let args: Vec<String> = env::args().collect();
    let cmd = args.get(1).map(String::as_str).unwrap_or("help");

    match cmd {
        "score" => cmd_score(&args[2..], false),
        "benchmark" => cmd_score(&args[2..], true),
        "search" => cmd_search(&args[2..]),
        "export" => cmd_export(&args[2..]),
        "help" | "--help" | "-h" => {
            print_help();
            ExitCode::SUCCESS
        }
        _ => {
            eprintln!("unknown command: {cmd}");
            print_help();
            ExitCode::from(2)
        }
    }
}

fn print_help() {
    println!(
        "Trinity Fold — puzzle prototype for candidate unification structures.

Ring architecture: ring0_core (types) <- ring1_constraints (scoring) <-
ring2_search (AI) <- ring3_adapters (IO) <- this binary (orchestration).

This tool does NOT prove a Theory of Everything. Every score is gated by a
claim-status tag. Read games/trinity_fold/README.md before drawing conclusions.

USAGE:
  trinity-fold score   <id1,id2,...>
  trinity-fold benchmark <id1,id2,...>   # hides held-out observables
  trinity-fold search [--anneal] [--seed N] [--iters N] [--start id,...]
  trinity-fold export <path/to/catalog.json>
  trinity-fold help
"
    );
}

fn parse_ids(s: &str) -> Vec<String> {
    s.split(',')
        .map(|x| x.trim())
        .filter(|x| !x.is_empty())
        .map(String::from)
        .collect()
}

fn cmd_score(args: &[String], benchmark: bool) -> ExitCode {
    let mut catalog = default_catalog();
    if benchmark {
        for id in benchmark_holdout_ids() {
            if let Some(n) = catalog.nodes.iter_mut().find(|n| n.id == *id) {
                n.value = None;
                n.uncertainty = None;
            }
        }
    }
    let ids = args.first().map(|s| parse_ids(s)).unwrap_or_default();
    let board = Board::from_ids(ids);
    let report = score_board(&catalog, &board);
    print_report(&catalog, &board, &report);
    ExitCode::SUCCESS
}

fn cmd_search(args: &[String]) -> ExitCode {
    let mut use_anneal = false;
    let mut seed: u64 = 0xC0FFEE;
    let mut iters: usize = 2000;
    let mut start_ids: Vec<String> = Vec::new();
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--anneal" => use_anneal = true,
            "--seed" => {
                i += 1;
                if let Some(v) = args.get(i) {
                    seed = v.parse().unwrap_or(seed);
                }
            }
            "--iters" => {
                i += 1;
                if let Some(v) = args.get(i) {
                    iters = v.parse().unwrap_or(iters);
                }
            }
            "--start" => {
                i += 1;
                if let Some(v) = args.get(i) {
                    start_ids = parse_ids(v);
                }
            }
            other => {
                eprintln!("ignoring unknown flag: {other}");
            }
        }
        i += 1;
    }
    let catalog = default_catalog();
    let start = Board::from_ids(start_ids);
    let weights = ScoreWeights::default();
    let report = if use_anneal {
        anneal(&catalog, start, &weights, iters, seed, 0.25, 0.999)
    } else {
        hill_climb(&catalog, start, &weights, iters)
    };
    println!(
        "search: iterations={} accepted={} (mode={})",
        report.iterations,
        report.accepted_moves,
        if use_anneal { "anneal" } else { "hill" }
    );
    let final_score = score_board_with(&catalog, &report.best_board, &weights);
    print_report(&catalog, &report.best_board, &final_score);
    ExitCode::SUCCESS
}

fn cmd_export(args: &[String]) -> ExitCode {
    let path = match args.first() {
        Some(p) => p,
        None => {
            eprintln!("export requires a path");
            return ExitCode::from(2);
        }
    };
    let catalog = default_catalog();
    match save_catalog(&catalog, path) {
        Ok(()) => {
            println!("wrote {path}");
            ExitCode::SUCCESS
        }
        Err(e) => {
            eprintln!("export failed: {e}");
            ExitCode::from(1)
        }
    }
}

fn print_report(catalog: &Catalog, board: &Board, report: &ScoreBreakdown) {
    let (data_n, geom_n) = tower_counts(catalog, board);
    println!(
        "board: {} tiles (data={}, geometry={})",
        board.len(),
        data_n,
        geom_n
    );
    for id in board.ids() {
        if let Some(n) = catalog.by_id(id) {
            println!(
                "  - {:<24} [{:<13}] {}",
                n.id,
                n.claim.label(),
                n.name
            );
        } else {
            println!("  - {:<24} [UNKNOWN_ID]", id);
        }
    }
    println!();
    println!("score breakdown:");
    println!("  consistency           {:.3}", report.consistency);
    println!("  dimensional_sanity    {:.3}", report.dimensional_sanity);
    println!("  observable_fit        {:.3}", report.observable_fit);
    println!("  simplicity            {:.3}", report.simplicity);
    println!("  symmetry_coherence    {:.3}", report.symmetry_coherence);
    println!("  reproducibility       {:.3}", report.reproducibility);
    println!("  proof_debt_penalty    {:.3}", report.proof_debt_penalty);
    println!("  falsification_penalty {:.3}", report.falsification_penalty);
    println!("  ---");
    println!("  TOTAL                 {:.3}", report.total);
    println!("  worst claim status    {}", report.worst_claim.label());
    if !report.notes.is_empty() {
        println!("notes:");
        for n in &report.notes {
            println!("  * {}", n);
        }
    }
    println!();
    println!(
        "DISCLAIMER: A high TOTAL is not evidence of a unified theory. It only
indicates the board passes more consistency checks than alternatives in this
illustrative catalog. See games/trinity_fold/README.md."
    );
}

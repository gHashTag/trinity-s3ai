// Claim cards generated from docs/claims.yaml.
//
// The single source of truth lives at `docs/claims.yaml` at the repo root.
// `scripts/generate_claims.py` materialises it into
// `games/trinity_fold/fixtures/generated_claim_cards.json`, which we embed at
// compile time so the wasm build does not need filesystem access.
//
// IMPORTANT: do not edit the JSON file by hand. Edit the YAML, then run
// `python3 scripts/generate_claims.py`.

use ring0_core::ClaimStatus;
use serde::{Deserialize, Serialize};

const GENERATED_CARDS_JSON: &str =
    include_str!("../../../fixtures/generated_claim_cards.json");

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct GeneratedClaimCard {
    pub id: String,
    pub kind: String,
    pub name: String,
    pub description: String,
    pub claim: ClaimStatus,
    pub layer: String,
    pub evidence: String,
    pub owner_file: String,
    pub blocking_gap: String,
    #[serde(default)]
    pub tags: Vec<String>,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct GeneratedClaimDeck {
    pub version: u32,
    pub source: String,
    pub generator: String,
    pub cards: Vec<GeneratedClaimCard>,
}

/// Parse the embedded generated card JSON. Panics on malformed input because
/// this represents a build-time SSOT contract, not user input.
pub fn embedded_claim_deck() -> GeneratedClaimDeck {
    serde_json::from_str(GENERATED_CARDS_JSON)
        .expect("generated_claim_cards.json is malformed; regenerate via scripts/generate_claims.py")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn embedded_deck_parses() {
        let deck = embedded_claim_deck();
        assert!(!deck.cards.is_empty(), "claim deck should be non-empty");
        assert_eq!(deck.source, "docs/claims.yaml");
        assert_eq!(deck.generator, "scripts/generate_claims.py");
    }

    #[test]
    fn embedded_deck_has_unique_ids() {
        let deck = embedded_claim_deck();
        let mut ids: Vec<&str> = deck.cards.iter().map(|c| c.id.as_str()).collect();
        ids.sort();
        let original_len = ids.len();
        ids.dedup();
        assert_eq!(ids.len(), original_len, "duplicate card ids in generated deck");
    }

    #[test]
    fn at_least_one_falsified_card_present() {
        // The SSOT must always carry at least one falsified/refuted entry so
        // the GOLDEN BRIDGE honesty floor has something to demonstrate.
        let deck = embedded_claim_deck();
        assert!(
            deck.cards
                .iter()
                .any(|c| c.claim == ClaimStatus::HighRiskOrFalsified),
            "expected at least one HighRiskOrFalsified card in the ledger"
        );
    }
}

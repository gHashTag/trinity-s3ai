// Recipes — community-curated build strategies for the GOLDEN CHAIN.
//
// A `Recipe` is a *named list of catalog ids* paired with a short rationale.
// Loading a recipe replays its tile placements via `UiEvent::ToggleTile`, so
// the resulting board is fully reproducible from ring 0+1 alone.
//
// The point of recipes is **not** to ship privileged solutions. It is to let
// the UI host illustrative or community-contributed starting points without
// hard-coding them into the catalog. A recipe whose tiles include any
// `HighRiskOrFalsified` node will trip the honesty floor exactly like any
// other board — recipes are not exempt.
//
// This module ships a small built-in set (`builtin_recipes()`); future work
// can replace it with a `ring3_adapters` JSON loader. The API is intentionally
// thin so that ring 1 / ring 2 never need to know recipes exist.

use ring0_core::Catalog;

#[derive(Clone, Debug)]
pub struct Recipe {
    pub id: String,
    pub title: String,
    pub rationale: String,
    pub tile_ids: Vec<String>,
}

impl Recipe {
    /// Drop tile ids that do not exist in the given catalog. Returns the
    /// number of unknown ids removed so the UI can surface a warning.
    pub fn rebind_to(&mut self, catalog: &Catalog) -> usize {
        let before = self.tile_ids.len();
        self.tile_ids.retain(|id| catalog.by_id(id).is_some());
        before - self.tile_ids.len()
    }
}

/// Built-in starter recipes. These are illustrative; none of them is a
/// claim about physics.
pub fn builtin_recipes() -> Vec<Recipe> {
    vec![
        Recipe {
            id: "sm_core".into(),
            title: "Standard-Model core".into(),
            rationale: "Place the three gauge symmetries plus the Higgs and fermion fields. \
                        Establishes the baseline data/geometry coverage before any geometric ansatz."
                .into(),
            tile_ids: vec![
                "s_su2".into(),
                "s_u1".into(),
                "s_su3".into(),
                "f_higgs".into(),
                "f_fermions".into(),
            ],
        },
        Recipe {
            id: "h4_geometry".into(),
            title: "H4 / 600-cell geometry pier".into(),
            rationale: "Loads the geometric building blocks (H4 root system, 600-cell, \
                        Clifford algebra) as a Geometry-pier anchor. Does NOT assert that this \
                        ansatz reproduces the Standard Model; that question lives in the proofs/ \
                        directory and remains open."
                .into(),
            tile_ids: vec![
                "s_h4".into(),
                "g_600cell".into(),
                "g_cl8".into(),
                "g_ncg_triple".into(),
            ],
        },
        Recipe {
            id: "anomaly_audit".into(),
            title: "Anomaly-cancellation audit".into(),
            rationale: "Pairs the SU(2)/U(1) gauge tiles with the anomaly-cancellation constraint \
                        so the consistency term has something to check against. Useful as a \
                        diagnostic when investigating proposed extensions."
                .into(),
            tile_ids: vec![
                "s_su2".into(),
                "s_u1".into(),
                "f_fermions".into(),
                "cn_anomaly".into(),
            ],
        },
    ]
}

#[cfg(test)]
mod tests {
    use super::*;
    use ring3_adapters::default_catalog;

    #[test]
    fn builtin_recipes_are_non_empty() {
        let r = builtin_recipes();
        assert!(!r.is_empty());
        for recipe in &r {
            assert!(!recipe.id.is_empty());
            assert!(!recipe.title.is_empty());
            assert!(!recipe.tile_ids.is_empty(), "recipe `{}` has no tiles", recipe.id);
        }
    }

    #[test]
    fn rebind_drops_unknown_ids() {
        let cat = default_catalog();
        let mut r = Recipe {
            id: "test".into(),
            title: "".into(),
            rationale: "".into(),
            tile_ids: vec!["s_su2".into(), "definitely_not_a_real_tile".into()],
        };
        let dropped = r.rebind_to(&cat);
        assert_eq!(dropped, 1);
        assert_eq!(r.tile_ids, vec!["s_su2".to_string()]);
    }

    #[test]
    fn builtin_recipes_rebind_cleanly_against_default_catalog() {
        let cat = default_catalog();
        for mut recipe in builtin_recipes() {
            let dropped = recipe.rebind_to(&cat);
            // We do not enforce zero (the illustrative catalog may evolve)
            // but every built-in recipe must keep at least one tile.
            assert!(
                !recipe.tile_ids.is_empty(),
                "recipe `{}` lost all tiles after rebind (dropped {})",
                recipe.id,
                dropped
            );
        }
    }
}

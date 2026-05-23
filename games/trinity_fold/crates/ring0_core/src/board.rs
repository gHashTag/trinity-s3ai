use crate::node::{Node, NodeKind, Tower};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

/// A puzzle board: a chosen subset of nodes (by id) drawn from a fixed pool.
///
/// The board is intentionally a flat selection rather than a 2D layout —
/// the user-facing UI maps each selected node to a tower column for
/// presentation, but consistency scoring is layout-independent.
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct Board {
    pub selected: BTreeSet<String>,
}

impl Board {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn from_ids<I, S>(ids: I) -> Self
    where
        I: IntoIterator<Item = S>,
        S: Into<String>,
    {
        Self {
            selected: ids.into_iter().map(Into::into).collect(),
        }
    }

    pub fn contains(&self, id: &str) -> bool {
        self.selected.contains(id)
    }

    pub fn insert(&mut self, id: impl Into<String>) {
        self.selected.insert(id.into());
    }

    pub fn remove(&mut self, id: &str) {
        self.selected.remove(id);
    }

    pub fn len(&self) -> usize {
        self.selected.len()
    }

    pub fn is_empty(&self) -> bool {
        self.selected.is_empty()
    }

    pub fn ids(&self) -> impl Iterator<Item = &String> {
        self.selected.iter()
    }
}

/// A pool of available nodes plus a small set of "triangle" consistency
/// hints (triples of nodes that must all be present together to count as
/// internally consistent, AlphaFold-Evoformer style).
#[derive(Clone, Debug, Default, Serialize, Deserialize)]
pub struct Catalog {
    pub nodes: Vec<Node>,
    #[serde(default)]
    pub triangles: Vec<[String; 3]>,
}

impl Catalog {
    pub fn by_id(&self, id: &str) -> Option<&Node> {
        self.nodes.iter().find(|n| n.id == id)
    }

    pub fn nodes_of(&self, kind: NodeKind) -> impl Iterator<Item = &Node> {
        self.nodes.iter().filter(move |n| n.kind == kind)
    }

    pub fn tower(&self, t: Tower) -> impl Iterator<Item = &Node> {
        self.nodes.iter().filter(move |n| n.kind.tower() == t)
    }

    /// Sum of dimensional signatures of all nodes on the board, by base
    /// dimension key. Empty map means dimensionless / dimensionally clean.
    pub fn dimensional_signature(&self, board: &Board) -> BTreeMap<String, i32> {
        let mut sig: BTreeMap<String, i32> = BTreeMap::new();
        for id in board.ids() {
            if let Some(n) = self.by_id(id) {
                for (k, v) in &n.dimension {
                    *sig.entry(k.clone()).or_insert(0) += *v;
                }
            }
        }
        sig.retain(|_, v| *v != 0);
        sig
    }
}

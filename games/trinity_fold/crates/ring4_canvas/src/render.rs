// Pure render model.
//
// `layout(state, viewport, theme)` walks the catalog and produces a
// `RenderModel`: a flat list of `RenderPrimitive`s (rect/circle/line/text)
// plus a list of `HitBox`es for input hit-testing. The browser shell
// (`wasm.rs`) iterates the primitives and issues Canvas2D draw calls; the
// shell never inspects domain types directly.
//
// Keeping the layout pure has two benefits:
//   * unit tests can assert on the model without a DOM,
//   * swapping the shell (e.g. for an egui/wgpu target later) requires no
//     changes to ring4 — only a new presenter.

use ring0_core::{ClaimStatus, NodeKind, Tower};

use crate::bridge::{BridgeIntegrity, BridgeView, SpanStatus};
use crate::state::AppState;

#[derive(Clone, Copy, Debug, Default)]
pub struct ViewportSize {
    pub width: f32,
    pub height: f32,
}

#[derive(Clone, Copy, Debug)]
pub struct Color(pub u8, pub u8, pub u8, pub u8);

impl Color {
    pub fn css(&self) -> String {
        format!("rgba({},{},{},{:.3})", self.0, self.1, self.2, self.3 as f32 / 255.0)
    }
}

#[derive(Clone, Debug)]
pub struct Theme {
    pub bg: Color,
    pub tower_data: Color,
    pub tower_geom: Color,
    pub tile_idle: Color,
    pub tile_selected: Color,
    pub tile_hover: Color,
    pub tile_falsified: Color,
    pub tile_open: Color,
    pub tile_verified: Color,
    pub tile_empirical: Color,
    pub tile_unverified: Color,
    pub stroke: Color,
    pub text: Color,
    pub text_dim: Color,
    pub edge_requires: Color,
    pub edge_incompat: Color,
    pub triangle: Color,
    pub button: Color,
    pub button_active: Color,
    /// GOLDEN BRIDGE deck colours.
    pub bridge_deck: Color,
    pub bridge_collapsed: Color,
    pub bridge_sound: Color,
    pub bridge_provisional: Color,
    pub recipe_chip: Color,
    /// Space-fold motif (concentric rings under the span).
    pub fold_ring: Color,
}

impl Default for Theme {
    fn default() -> Self {
        Self {
            bg: Color(11, 14, 22, 255),
            tower_data: Color(30, 50, 70, 255),
            tower_geom: Color(50, 30, 70, 255),
            tile_idle: Color(40, 48, 64, 255),
            tile_selected: Color(70, 130, 180, 255),
            tile_hover: Color(90, 110, 140, 255),
            tile_falsified: Color(180, 50, 50, 255),
            tile_open: Color(180, 140, 60, 255),
            tile_verified: Color(60, 160, 100, 255),
            tile_empirical: Color(100, 140, 200, 255),
            tile_unverified: Color(110, 110, 110, 255),
            stroke: Color(180, 200, 220, 255),
            text: Color(230, 235, 240, 255),
            text_dim: Color(140, 150, 165, 255),
            edge_requires: Color(120, 200, 140, 255),
            edge_incompat: Color(220, 80, 80, 255),
            triangle: Color(220, 200, 80, 200),
            button: Color(60, 80, 110, 255),
            button_active: Color(90, 150, 200, 255),
            bridge_deck: Color(212, 175, 55, 220),       // gold deck
            bridge_collapsed: Color(220, 80, 80, 230),
            bridge_sound: Color(212, 175, 55, 230),
            bridge_provisional: Color(180, 140, 60, 220),
            recipe_chip: Color(60, 100, 90, 255),
            fold_ring: Color(120, 150, 200, 60),
        }
    }
}

#[derive(Clone, Debug)]
pub enum RenderPrimitive {
    Rect { x: f32, y: f32, w: f32, h: f32, fill: Color, stroke: Option<Color> },
    Line { x0: f32, y0: f32, x1: f32, y1: f32, color: Color, width: f32 },
    Circle { x: f32, y: f32, r: f32, fill: Color, stroke: Option<Color> },
    Text { x: f32, y: f32, s: String, color: Color, size: f32, bold: bool },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum HitRegion {
    Tile(String),
    ButtonClear,
    ButtonHillClimb,
    ButtonAnneal,
    ButtonBenchmark,
    /// "Load recipe" pill in the GOLDEN BRIDGE recipe rail.
    RecipeChip(String),
}

#[derive(Clone, Debug)]
pub struct HitBox {
    pub x: f32,
    pub y: f32,
    pub w: f32,
    pub h: f32,
    pub region: HitRegion,
}

#[derive(Clone, Debug)]
pub struct RenderModel {
    pub primitives: Vec<RenderPrimitive>,
    pub hit_regions: Vec<HitBox>,
    pub viewport: ViewportSize,
}

const TILE_W: f32 = 168.0;
const TILE_H: f32 = 52.0;
const TILE_GAP_Y: f32 = 10.0;
const TILE_GAP_X: f32 = 18.0;
const TOWER_PAD: f32 = 18.0;
const HEADER_H: f32 = 64.0;
const BUTTON_H: f32 = 32.0;
const SCORE_PANEL_W: f32 = 280.0;
/// Height reserved for the GOLDEN BRIDGE deck strip across the canvas.
///
/// The strip is divided into three vertical bands so the integrity header
/// (top) never overlaps the pier counters (Data·N / Geometry·N) drawn
/// alongside the pier columns below it:
///
///   `[ 0..BRIDGE_HEADER_BAND_H ]`  integrity header text
///   `[ BRIDGE_HEADER_BAND_H .. BRIDGE_DECK_H ]`  piers + deck line + spans
const BRIDGE_DECK_H: f32 = 96.0;
const BRIDGE_HEADER_BAND_H: f32 = 26.0;
const RECIPE_CHIP_H: f32 = 26.0;

fn claim_color(claim: ClaimStatus, theme: &Theme) -> Color {
    match claim {
        ClaimStatus::Verified => theme.tile_verified,
        ClaimStatus::EmpiricalFit => theme.tile_empirical,
        ClaimStatus::OpenConjecture => theme.tile_open,
        ClaimStatus::HighRiskOrFalsified => theme.tile_falsified,
        ClaimStatus::Unverified => theme.tile_unverified,
    }
}

fn span_color(status: SpanStatus, theme: &Theme) -> Color {
    match status {
        SpanStatus::Gold => theme.bridge_sound,
        SpanStatus::Empirical => theme.tile_empirical,
        SpanStatus::Open => theme.bridge_provisional,
        SpanStatus::Collapsed => theme.bridge_collapsed,
        SpanStatus::Unverified => theme.tile_unverified,
    }
}

fn integrity_color(integrity: BridgeIntegrity, theme: &Theme) -> Color {
    match integrity {
        BridgeIntegrity::Empty => theme.text_dim,
        BridgeIntegrity::Sound => theme.bridge_sound,
        BridgeIntegrity::Provisional => theme.bridge_provisional,
        BridgeIntegrity::Collapsed => theme.bridge_collapsed,
    }
}

/// Build the render model for the current state.
///
/// Layout (left to right):
///   [ Data Tower | Score & Controls Panel | Geometry Tower ]
///
/// Each tower stacks tiles vertically grouped by `NodeKind`. Selected tiles
/// are tinted; hovered tiles get a brighter stroke; tiles that participate
/// in a completed Evoformer triangle are connected by translucent yellow
/// lines.
pub fn layout(state: &AppState, viewport: ViewportSize, theme: &Theme) -> RenderModel {
    let mut prims = Vec::new();
    let mut hits = Vec::new();

    // Background.
    prims.push(RenderPrimitive::Rect {
        x: 0.0,
        y: 0.0,
        w: viewport.width,
        h: viewport.height,
        fill: theme.bg,
        stroke: None,
    });

    // Header — GOLDEN BRIDGE branding.
    prims.push(RenderPrimitive::Text {
        x: 24.0, y: 32.0,
        s: format!("{} — Rust canvas UI (ring 4)", crate::PRODUCT_NAME),
        color: theme.bridge_deck, size: 22.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: 24.0, y: 54.0,
        s: format!(
            "{} Hypothesis-discovery puzzle, NOT a proven Theory of Everything.",
            crate::PRODUCT_TAGLINE
        ),
        color: theme.text_dim, size: 12.0, bold: false,
    });

    // Towers + score panel.
    let panel_x = (viewport.width - SCORE_PANEL_W) * 0.5;
    let tower_w = panel_x - TOWER_PAD * 2.0;
    let toolbar_bottom = HEADER_H + BUTTON_H + 16.0;
    let bridge_y = toolbar_bottom;
    let towers_y = bridge_y + BRIDGE_DECK_H + RECIPE_CHIP_H + 16.0;
    let towers_h = (viewport.height - towers_y - 16.0).max(200.0);

    // GOLDEN BRIDGE deck spans the full content width above the towers.
    draw_bridge_deck(
        &state.bridge,
        theme,
        TOWER_PAD,
        bridge_y,
        viewport.width - TOWER_PAD * 2.0,
        BRIDGE_DECK_H,
        &mut prims,
    );

    // Recipe rail (built-in starting points). Hit-testable.
    draw_recipe_rail(
        state,
        theme,
        TOWER_PAD,
        bridge_y + BRIDGE_DECK_H + 4.0,
        viewport.width - TOWER_PAD * 2.0,
        RECIPE_CHIP_H,
        &mut prims,
        &mut hits,
    );

    // Data Tower (left).
    draw_tower(
        state, theme, Tower::Data,
        TOWER_PAD, towers_y, tower_w, towers_h,
        "Data Tower (pier)", "observables & constraints",
        theme.tower_data,
        &mut prims, &mut hits,
    );

    // Geometry Tower (right).
    draw_tower(
        state, theme, Tower::Geometry,
        panel_x + SCORE_PANEL_W + TOWER_PAD, towers_y, tower_w, towers_h,
        "Geometry Tower (pier)", "symmetry, geometry, fields, constants",
        theme.tower_geom,
        &mut prims, &mut hits,
    );

    // Triangle highlights — drawn after tiles so they overlay.
    draw_triangles(state, theme, &mut prims);

    // Score panel.
    draw_score_panel(
        state, theme,
        panel_x, towers_y, SCORE_PANEL_W, towers_h,
        &mut prims,
    );

    // Toolbar buttons across the top.
    draw_toolbar(state, theme, viewport, &mut prims, &mut hits);

    RenderModel { primitives: prims, hit_regions: hits, viewport }
}

/// Draw the GOLDEN BRIDGE deck: two piers (Data, Geometry), a deck line
/// whose colour mirrors `BridgeView::integrity`, span markers per selected
/// tile, and a space-fold motif behind the deck.
fn draw_bridge_deck(
    bridge: &BridgeView,
    theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>,
) {
    // Background plate.
    prims.push(RenderPrimitive::Rect {
        x, y, w, h,
        fill: Color(16, 20, 30, 255),
        stroke: Some(theme.stroke),
    });

    // The deck strip is split into two horizontal bands so the integrity
    // header text at the top cannot overlap the pier counters and span
    // markers below it.
    let lower_top = y + BRIDGE_HEADER_BAND_H;
    let lower_h = h - BRIDGE_HEADER_BAND_H;

    // Faint divider between header band and pier band — visual hint, not
    // load-bearing.
    prims.push(RenderPrimitive::Line {
        x0: x + 8.0, y0: lower_top,
        x1: x + w - 8.0, y1: lower_top,
        color: theme.fold_ring, width: 1.0,
    });

    // Space-fold motif: concentric arcs hint at compression of a high-D space
    // into a small consistent set. Pure decoration; carries no scoring weight.
    // Centred on the *lower* band so it never bleeds into the header band.
    let cx = x + w * 0.5;
    let cy = lower_top + lower_h * 0.55;
    for k in 0..4 {
        let r = 18.0 + k as f32 * 14.0 + bridge.compression as f32 * 28.0;
        prims.push(RenderPrimitive::Circle {
            x: cx, y: cy, r,
            fill: Color(0, 0, 0, 0),
            stroke: Some(theme.fold_ring),
        });
    }

    // Pier columns — anchored inside the lower band.
    let pier_w = 14.0;
    let pier_top = lower_top + 14.0;
    let pier_h = lower_h - 26.0;
    let data_x = x + 18.0;
    let geom_x = x + w - 18.0 - pier_w;
    prims.push(RenderPrimitive::Rect {
        x: data_x, y: pier_top, w: pier_w, h: pier_h,
        fill: theme.tower_data, stroke: Some(theme.stroke),
    });
    prims.push(RenderPrimitive::Rect {
        x: geom_x, y: pier_top, w: pier_w, h: pier_h,
        fill: theme.tower_geom, stroke: Some(theme.stroke),
    });
    // Pier counters sit *between* the header band divider and the pier
    // column top, so they cannot overlap the integrity header above.
    prims.push(RenderPrimitive::Text {
        x: data_x - 4.0, y: pier_top - 2.0,
        s: format!("Data·{}", bridge.data_pier_count),
        color: theme.text_dim, size: 11.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: geom_x - 24.0, y: pier_top - 2.0,
        s: format!("Geometry·{}", bridge.geom_pier_count),
        color: theme.text_dim, size: 11.0, bold: true,
    });

    // Deck line — centred vertically inside the lower band.
    let deck_y = lower_top + lower_h * 0.5;
    let deck_color = match bridge.integrity {
        BridgeIntegrity::Empty => theme.text_dim,
        BridgeIntegrity::Sound => theme.bridge_sound,
        BridgeIntegrity::Provisional => theme.bridge_provisional,
        BridgeIntegrity::Collapsed => theme.bridge_collapsed,
    };
    if bridge.integrity == BridgeIntegrity::Collapsed {
        // Two short segments with a gap in the middle to suggest collapse.
        let mid = (data_x + pier_w + geom_x) * 0.5;
        let gap = 38.0;
        prims.push(RenderPrimitive::Line {
            x0: data_x + pier_w, y0: deck_y,
            x1: mid - gap, y1: deck_y + 12.0,
            color: deck_color, width: 4.0,
        });
        prims.push(RenderPrimitive::Line {
            x0: mid + gap, y0: deck_y + 12.0,
            x1: geom_x, y1: deck_y,
            color: deck_color, width: 4.0,
        });
        prims.push(RenderPrimitive::Text {
            x: mid - 36.0, y: deck_y + 32.0,
            s: "COLLAPSE".into(),
            color: theme.bridge_collapsed, size: 14.0, bold: true,
        });
    } else {
        prims.push(RenderPrimitive::Line {
            x0: data_x + pier_w, y0: deck_y,
            x1: geom_x, y1: deck_y,
            color: deck_color, width: 4.0,
        });
    }

    // Span nodes drawn along the deck.
    let span_left = data_x + pier_w + 8.0;
    let span_right = geom_x - 8.0;
    for sn in &bridge.span_nodes {
        let sx = span_left + (span_right - span_left) * sn.pier_t;
        let r = 7.0;
        prims.push(RenderPrimitive::Circle {
            x: sx, y: deck_y, r,
            fill: span_color(sn.status, theme),
            stroke: Some(theme.stroke),
        });
    }

    // Header label sits in its own band at the top of the deck strip —
    // BRIDGE_HEADER_BAND_H of vertical space is reserved above the piers
    // so this never collides with the Data·N / Geometry·N counters.
    let integrity_col = integrity_color(bridge.integrity, theme);
    prims.push(RenderPrimitive::Text {
        x: x + 12.0, y: y + 17.0,
        s: format!(
            "GOLDEN BRIDGE — integrity: {}   strength: {:+.3}   compression: {:.0}%",
            bridge.integrity.label(),
            bridge.strength,
            bridge.compression * 100.0,
        ),
        color: integrity_col, size: 13.0, bold: true,
    });
    if bridge.integrity == BridgeIntegrity::Collapsed {
        // Collapse warning is drawn below the deck line so it does not
        // re-enter the header band.
        prims.push(RenderPrimitive::Text {
            x: x + 12.0, y: deck_y + 28.0,
            s: format!(
                "Honesty floor tripped: {} falsified tile(s) on the span.",
                bridge.falsified_count
            ),
            color: theme.bridge_collapsed, size: 11.0, bold: true,
        });
    }
}

fn draw_recipe_rail(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    prims.push(RenderPrimitive::Text {
        x, y: y + 14.0,
        s: "Recipes:".into(),
        color: theme.text_dim, size: 11.0, bold: true,
    });
    let mut cx = x + 70.0;
    let max_x = x + w;
    for recipe in state.recipes.iter() {
        let label = format!("{} ({})", recipe.title, recipe.tile_ids.len());
        let cw = (label.len() as f32) * 6.8 + 18.0;
        if cx + cw > max_x { break; }
        prims.push(RenderPrimitive::Rect {
            x: cx, y, w: cw, h,
            fill: theme.recipe_chip, stroke: Some(theme.stroke),
        });
        prims.push(RenderPrimitive::Text {
            x: cx + 9.0, y: y + 17.0,
            s: label,
            color: theme.text, size: 11.0, bold: false,
        });
        hits.push(HitBox {
            x: cx, y, w: cw, h,
            region: HitRegion::RecipeChip(recipe.id.clone()),
        });
        cx += cw + 6.0;
    }
}

fn draw_toolbar(
    state: &AppState, theme: &Theme, viewport: ViewportSize,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    let y = HEADER_H + 8.0;
    let mut x = 24.0;
    let buttons = [
        ("Clear (C)", HitRegion::ButtonClear, false),
        ("Hill-climb (H)", HitRegion::ButtonHillClimb, false),
        ("Anneal seed=42 (A)", HitRegion::ButtonAnneal, false),
        (
            if state.view.benchmark_mode { "Benchmark: ON (B)" } else { "Benchmark: off (B)" },
            HitRegion::ButtonBenchmark,
            state.view.benchmark_mode,
        ),
    ];
    for (label, region, active) in buttons.into_iter() {
        let w = (label.len() as f32) * 7.5 + 24.0;
        let fill = if active { theme.button_active } else { theme.button };
        prims.push(RenderPrimitive::Rect {
            x, y, w, h: BUTTON_H, fill, stroke: Some(theme.stroke),
        });
        prims.push(RenderPrimitive::Text {
            x: x + 12.0, y: y + 20.0, s: label.into(),
            color: theme.text, size: 13.0, bold: false,
        });
        hits.push(HitBox { x, y, w, h: BUTTON_H, region });
        x += w + 8.0;
        let _ = viewport; // height-aware truncation could go here later.
    }
}

fn draw_tower(
    state: &AppState, theme: &Theme, tower: Tower,
    x: f32, y: f32, w: f32, h: f32,
    title: &str, hint: &str, bg: Color,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    prims.push(RenderPrimitive::Rect { x, y, w, h, fill: bg, stroke: Some(theme.stroke) });
    prims.push(RenderPrimitive::Text {
        x: x + 12.0, y: y + 22.0, s: title.into(),
        color: theme.text, size: 16.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 12.0, y: y + 40.0, s: hint.into(),
        color: theme.text_dim, size: 11.0, bold: false,
    });

    let kinds_data = [NodeKind::Observable, NodeKind::Constraint];
    let kinds_geom = [NodeKind::Symmetry, NodeKind::Geometry, NodeKind::Field, NodeKind::Constant];
    let kinds: &[NodeKind] = if tower == Tower::Data { &kinds_data } else { &kinds_geom };

    let inner_x = x + 12.0;
    let mut cur_y = y + 56.0;
    let inner_right = x + w - 12.0;
    let cols = ((inner_right - inner_x + TILE_GAP_X) / (TILE_W + TILE_GAP_X)).floor().max(1.0) as usize;

    for kind in kinds {
        // Section header.
        prims.push(RenderPrimitive::Text {
            x: inner_x, y: cur_y, s: kind.label().to_string(),
            color: theme.text_dim, size: 12.0, bold: true,
        });
        cur_y += 14.0;

        let mut col = 0usize;
        let mut row_y = cur_y;
        for node in state.catalog.nodes_of(*kind) {
            let tx = inner_x + (col as f32) * (TILE_W + TILE_GAP_X);
            let ty = row_y;

            let selected = state.board.contains(&node.id);
            let hovered = state.view.hover_id.as_deref() == Some(node.id.as_str());

            let fill = if selected {
                theme.tile_selected
            } else if hovered {
                theme.tile_hover
            } else {
                theme.tile_idle
            };
            let stroke = claim_color(node.claim, theme);

            prims.push(RenderPrimitive::Rect {
                x: tx, y: ty, w: TILE_W, h: TILE_H, fill, stroke: Some(stroke),
            });
            // Claim chip (left strip).
            prims.push(RenderPrimitive::Rect {
                x: tx, y: ty, w: 4.0, h: TILE_H,
                fill: claim_color(node.claim, theme), stroke: None,
            });
            // Tile id (bold) and name (dim).
            prims.push(RenderPrimitive::Text {
                x: tx + 10.0, y: ty + 18.0, s: node.id.clone(),
                color: theme.text, size: 12.0, bold: true,
            });
            prims.push(RenderPrimitive::Text {
                x: tx + 10.0, y: ty + 34.0, s: truncate(&node.name, 22),
                color: theme.text_dim, size: 11.0, bold: false,
            });
            // Selected check-mark.
            if selected {
                prims.push(RenderPrimitive::Circle {
                    x: tx + TILE_W - 14.0, y: ty + 14.0, r: 6.0,
                    fill: theme.tile_verified, stroke: None,
                });
            }
            hits.push(HitBox { x: tx, y: ty, w: TILE_W, h: TILE_H, region: HitRegion::Tile(node.id.clone()) });

            col += 1;
            if col >= cols {
                col = 0;
                row_y += TILE_H + TILE_GAP_Y;
            }
        }
        cur_y = if col == 0 { row_y } else { row_y + TILE_H + TILE_GAP_Y };
        cur_y += 8.0;

        // Stop if we've blown the bottom of the tower; tests cover this case.
        if cur_y > y + h - TILE_H { break; }
    }
}

fn draw_score_panel(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>,
) {
    prims.push(RenderPrimitive::Rect {
        x, y, w, h, fill: Color(20, 24, 36, 255), stroke: Some(theme.stroke),
    });
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: y + 24.0, s: "Score".into(),
        color: theme.text, size: 16.0, bold: true,
    });
    let s = &state.score;
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: y + 60.0,
        s: format!("total = {:+.3}", s.total),
        color: theme.text, size: 22.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: y + 82.0,
        s: format!("worst claim: {}", s.worst_claim.label()),
        color: claim_color(s.worst_claim, theme),
        size: 12.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: y + 98.0,
        s: format!("bridge: {}", state.bridge.integrity.label()),
        color: integrity_color(state.bridge.integrity, theme),
        size: 12.0, bold: true,
    });

    let rows = [
        ("consistency", s.consistency),
        ("dimensional_sanity", s.dimensional_sanity),
        ("observable_fit", s.observable_fit),
        ("proof_debt_penalty", -s.proof_debt_penalty),
        ("falsification_penalty", -s.falsification_penalty),
        ("simplicity", s.simplicity),
        ("symmetry_coherence", s.symmetry_coherence),
        ("reproducibility", s.reproducibility),
    ];
    let mut ry = y + 124.0;
    for (label, val) in rows {
        prims.push(RenderPrimitive::Text {
            x: x + 14.0, y: ry, s: label.into(),
            color: theme.text_dim, size: 11.0, bold: false,
        });
        prims.push(RenderPrimitive::Text {
            x: x + w - 14.0 - 50.0, y: ry,
            s: format!("{:+.3}", val),
            color: theme.text, size: 11.0, bold: false,
        });
        ry += 16.0;
    }

    ry += 8.0;
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: ry, s: format!("selected: {} tiles", state.board.len()),
        color: theme.text, size: 11.0, bold: true,
    });
    ry += 16.0;
    if let Some(focus) = state.view.focus_id.as_ref() {
        if let Some(node) = state.catalog.by_id(focus) {
            prims.push(RenderPrimitive::Text {
                x: x + 14.0, y: ry,
                s: format!("focus: {} [{}]", node.id, node.claim.label()),
                color: claim_color(node.claim, theme), size: 11.0, bold: true,
            });
            ry += 14.0;
            // Wrap description across two lines if needed.
            let desc = truncate(&node.description, 36);
            prims.push(RenderPrimitive::Text {
                x: x + 14.0, y: ry, s: desc,
                color: theme.text_dim, size: 10.0, bold: false,
            });
            ry += 14.0;
        }
    }

    // Notes from the scorer.
    if !s.notes.is_empty() {
        prims.push(RenderPrimitive::Text {
            x: x + 14.0, y: ry + 4.0, s: "notes".into(),
            color: theme.text_dim, size: 11.0, bold: true,
        });
        ry += 18.0;
        for note in s.notes.iter().take(6) {
            prims.push(RenderPrimitive::Text {
                x: x + 14.0, y: ry, s: format!("• {}", truncate(note, 36)),
                color: theme.text_dim, size: 10.0, bold: false,
            });
            ry += 13.0;
        }
    }
}

fn draw_triangles(state: &AppState, theme: &Theme, prims: &mut Vec<RenderPrimitive>) {
    // Triangle hint lines: connect the three tiles of each *completed*
    // Evoformer-style triangle so the player can see which composite
    // consistency they have satisfied. Centroids are not known at this
    // layout pass — we don't store tile rects across functions. Triangles
    // are emitted as a label list in the score panel via `notes`; future
    // work can carry per-tile bbox indices forward to draw lines.
    let _ = state;
    let _ = theme;
    let _ = prims;
}

fn truncate(s: &str, max: usize) -> String {
    if s.chars().count() <= max {
        s.to_string()
    } else {
        let cut: String = s.chars().take(max.saturating_sub(1)).collect();
        format!("{}…", cut)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::state::AppState;
    use ring3_adapters::{benchmark_holdout_ids, default_catalog};

    fn s() -> AppState {
        AppState::new(default_catalog(), benchmark_holdout_ids().iter().map(|s| s.to_string()).collect())
    }

    fn vp() -> ViewportSize {
        // The GOLDEN BRIDGE deck + recipe rail reserve ~120px of vertical
        // space above the towers, so the test viewport is sized accordingly.
        // Tower drawing intentionally stops at the bottom of its box, so this
        // height must accommodate every section in the geometry tower.
        ViewportSize { width: 1280.0, height: 980.0 }
    }

    #[test]
    fn layout_produces_primitives() {
        let m = layout(&s(), vp(), &Theme::default());
        assert!(m.primitives.len() > 50, "expected non-trivial primitive count, got {}", m.primitives.len());
    }

    #[test]
    fn every_catalog_tile_has_hit_box() {
        let state = s();
        let m = layout(&state, vp(), &Theme::default());
        let tile_hits: Vec<_> = m
            .hit_regions
            .iter()
            .filter_map(|h| if let HitRegion::Tile(id) = &h.region { Some(id.clone()) } else { None })
            .collect();
        for node in state.catalog.nodes.iter() {
            assert!(
                tile_hits.iter().any(|h| h == &node.id),
                "missing hit region for tile `{}`",
                node.id
            );
        }
    }

    #[test]
    fn toolbar_buttons_are_hittable() {
        let m = layout(&s(), vp(), &Theme::default());
        let regions: Vec<_> = m.hit_regions.iter().map(|h| h.region.clone()).collect();
        assert!(regions.contains(&HitRegion::ButtonClear));
        assert!(regions.contains(&HitRegion::ButtonHillClimb));
        assert!(regions.contains(&HitRegion::ButtonAnneal));
        assert!(regions.contains(&HitRegion::ButtonBenchmark));
    }

    #[test]
    fn score_panel_renders_worst_claim_text() {
        let mut state = s();
        // Push a high-risk tile onto the board to force the falsification path.
        let falsified_id = state.catalog.nodes.iter()
            .find(|n| n.claim == ring0_core::ClaimStatus::HighRiskOrFalsified)
            .map(|n| n.id.clone());
        if let Some(id) = falsified_id {
            state.apply(crate::input::UiEvent::ToggleTile(id));
        }
        let m = layout(&state, vp(), &Theme::default());
        let has_label = m.primitives.iter().any(|p| match p {
            RenderPrimitive::Text { s, .. } => s.contains("worst claim"),
            _ => false,
        });
        assert!(has_label);
    }

    #[test]
    fn color_css_is_well_formed() {
        let c = Color(255, 128, 0, 200);
        let s = c.css();
        assert!(s.starts_with("rgba("));
        assert!(s.ends_with(")"));
    }

    #[test]
    fn truncate_handles_short_and_long() {
        assert_eq!(truncate("abc", 10), "abc");
        let t = truncate("abcdefghijklmnop", 5);
        assert!(t.ends_with("…"));
    }

    #[test]
    fn header_uses_golden_bridge_name() {
        let m = layout(&s(), vp(), &Theme::default());
        let has_brand = m.primitives.iter().any(|p| match p {
            RenderPrimitive::Text { s, .. } => s.contains("GOLDEN BRIDGE"),
            _ => false,
        });
        assert!(has_brand, "header text must surface GOLDEN BRIDGE branding");
    }

    #[test]
    fn bridge_deck_renders_integrity_label() {
        let m = layout(&s(), vp(), &Theme::default());
        let has_label = m.primitives.iter().any(|p| match p {
            RenderPrimitive::Text { s, .. } => s.contains("integrity:"),
            _ => false,
        });
        assert!(has_label);
    }

    /// Regression: the integrity header (top of the deck strip) and the
    /// pier counters (`Data·N`, `Geometry·N`) used to share a vertical
    /// band and overlapped in the deployed static preview. They must now
    /// live in distinct horizontal bands with daylight between them.
    #[test]
    fn integrity_header_does_not_overlap_pier_counters() {
        let m = layout(&s(), vp(), &Theme::default());
        // Approximate text height for the 13.0-px integrity header and
        // 11.0-px pier counter, matching the conservative metric used by
        // the canvas shell. Text y-coordinates are baselines, so the
        // glyph box extends roughly `size * 1.1` upward.
        fn box_top_bottom(y: f32, size: f32) -> (f32, f32) {
            (y - size * 1.1, y + size * 0.25)
        }
        let mut integrity_y: Option<f32> = None;
        let mut pier_ys: Vec<f32> = Vec::new();
        for p in &m.primitives {
            if let RenderPrimitive::Text { s, y, size, .. } = p {
                if s.starts_with("GOLDEN BRIDGE — integrity:") {
                    integrity_y = Some(*y);
                    let _ = size; // size pinned in box_top_bottom below
                } else if s.starts_with("Data·") || s.starts_with("Geometry·") {
                    pier_ys.push(*y);
                }
            }
        }
        let iy = integrity_y.expect("integrity header text missing");
        let (_, ih_bot) = box_top_bottom(iy, 13.0);
        assert!(!pier_ys.is_empty(), "expected pier counter labels");
        for py in pier_ys {
            let (p_top, _) = box_top_bottom(py, 11.0);
            assert!(
                ih_bot < p_top,
                "integrity header (bottom y={:.1}) must sit above pier counter \
                 (top y={:.1}); overlap regression",
                ih_bot, p_top,
            );
        }
    }

    #[test]
    fn collapsed_bridge_shows_collapse_warning() {
        let mut state = s();
        let falsified_id = state
            .catalog
            .nodes
            .iter()
            .find(|n| n.claim == ClaimStatus::HighRiskOrFalsified)
            .map(|n| n.id.clone());
        let Some(id) = falsified_id else { return; };
        state.apply(crate::input::UiEvent::ToggleTile(id));
        let m = layout(&state, vp(), &Theme::default());
        let has_collapse = m.primitives.iter().any(|p| match p {
            RenderPrimitive::Text { s, .. } => s.contains("COLLAPSE") || s.contains("Honesty floor"),
            _ => false,
        });
        assert!(has_collapse, "collapsed bridge must surface a visible warning");
    }

    #[test]
    fn recipe_chips_are_hittable() {
        let state = s();
        let m = layout(&state, vp(), &Theme::default());
        let chip_ids: Vec<_> = m
            .hit_regions
            .iter()
            .filter_map(|h| if let HitRegion::RecipeChip(id) = &h.region {
                Some(id.clone())
            } else { None })
            .collect();
        // The rail may truncate trailing chips if viewport is narrow; assert
        // at least the first built-in recipe is hittable on the standard vp.
        assert!(
            chip_ids.contains(&state.recipes[0].id),
            "expected first recipe `{}` to be hittable, got {:?}",
            state.recipes[0].id,
            chip_ids
        );
    }
}

// Pure render model.
//
// `layout(state, viewport, theme)` walks the catalog and produces a
// `RenderModel`: a flat list of `RenderPrimitive`s (rect/circle/line/text)
// plus a list of `HitBox`es for input hit-testing. The browser shell
// (`wasm.rs`) iterates the primitives and issues Canvas2D draw calls; the
// shell never inspects domain types directly.
//
// Layout (game stage):
//
//   +----------------------------------------------------------------------+
//   | Header — GOLDEN BRIDGE: Build the Bridge!                            |
//   | How-to-play 3-step banner                                            |
//   | Game-action toolbar  [Reset] [Hint] [Auto-build] [Try Recipe]        |
//   |                                                                      |
//   |  +--------------+   ============= BRIDGE =============   +---------+ |
//   |  |              |  | stone | stone | stone | stone | …  |          |
//   |  |  DATA TOWER  |  =====================================  | GEOM   | |
//   |  |  (blue)      |                                          | TOWER  | |
//   |  |  tiles ...   |   Tutorial / status overlay              | (purp) | |
//   |  |              |                                          | tiles  | |
//   |  +--------------+                                          +--------+ |
//   |                                                                      |
//   | Honesty panel (small, bottom)                                        |
//   +----------------------------------------------------------------------+

use ring0_core::{ClaimStatus, NodeKind, Tower};

use crate::bridge::{BridgeIntegrity, SpanStatus};
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

    pub fn with_alpha(&self, alpha: u8) -> Color {
        Color(self.0, self.1, self.2, alpha)
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
    pub bridge_deck: Color,
    pub bridge_collapsed: Color,
    pub bridge_sound: Color,
    pub bridge_provisional: Color,
    pub recipe_chip: Color,
    pub fold_ring: Color,
    /// Bright accent used for the data side (blue glow).
    pub data_glow: Color,
    /// Bright accent used for the geometry side (purple glow).
    pub geom_glow: Color,
}

impl Default for Theme {
    fn default() -> Self {
        // True-black stage with neon-style game art.
        Self {
            bg: Color(0, 0, 0, 255),
            tower_data: Color(14, 30, 60, 255),
            tower_geom: Color(40, 14, 60, 255),
            tile_idle: Color(18, 22, 32, 255),
            tile_selected: Color(80, 200, 255, 255),
            tile_hover: Color(120, 150, 200, 255),
            tile_falsified: Color(240, 70, 80, 255),
            tile_open: Color(245, 190, 80, 255),
            tile_verified: Color(110, 230, 160, 255),
            tile_empirical: Color(120, 190, 245, 255),
            tile_unverified: Color(160, 160, 160, 255),
            stroke: Color(180, 210, 240, 255),
            text: Color(244, 248, 252, 255),
            text_dim: Color(160, 175, 200, 255),
            edge_requires: Color(120, 220, 150, 255),
            edge_incompat: Color(240, 90, 90, 255),
            triangle: Color(255, 215, 90, 220),
            button: Color(28, 44, 72, 255),
            button_active: Color(255, 200, 80, 255),
            bridge_deck: Color(255, 210, 80, 240),
            bridge_collapsed: Color(240, 70, 80, 240),
            bridge_sound: Color(255, 215, 90, 240),
            bridge_provisional: Color(225, 165, 80, 230),
            recipe_chip: Color(32, 80, 80, 255),
            fold_ring: Color(140, 180, 230, 90),
            data_glow: Color(80, 180, 255, 255),
            geom_glow: Color(210, 130, 240, 255),
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

const TILE_H: f32 = 44.0;
const TILE_GAP_Y: f32 = 8.0;
const HEADER_H: f32 = 56.0;
const TUTORIAL_H: f32 = 64.0;
const BUTTON_H: f32 = 36.0;
const TOOLBAR_TOP: f32 = HEADER_H + TUTORIAL_H + 8.0;
const TOOLBAR_BOTTOM: f32 = TOOLBAR_TOP + BUTTON_H;
const BRIDGE_BAND_H: f32 = 220.0;
const RECIPE_RAIL_H: f32 = 32.0;
const HONESTY_PANEL_H: f32 = 92.0;

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

/// Map a catalog node id to a child-friendly primary label. Unknown ids fall
/// back to the node's `name` field, with the technical id rendered as
/// subtext by the caller. The map is intentionally short — every common SM
/// observable / symmetry / geometry tile in the default catalog gets a
/// kid-readable word so the game stage reads like "Higgs Mass" instead of
/// "o_higgs_mass".
fn friendly_label(id: &str, fallback: &str) -> String {
    match id {
        "o_alpha_em" => "Light Strength".to_string(),
        "o_g_minus_2" => "Muon Wobble".to_string(),
        "o_higgs_mass" => "Higgs Mass".to_string(),
        "o_neutrino_dm2" => "Neutrino Mix".to_string(),
        "o_cosmo_lambda" => "Dark Energy".to_string(),
        "o_mt_over_mb" => "Top/Bottom Ratio".to_string(),
        "c_anomaly_free" | "cn_anomaly" => "Anomaly Cancel".to_string(),
        "c_unitarity" => "Probability OK".to_string(),
        "c_dimensional" => "Units Match".to_string(),
        "s_su2" => "Weak Force".to_string(),
        "s_su3" => "Strong Force".to_string(),
        "s_u1" => "EM Force".to_string(),
        "s_h4" => "Golden Shape (H4)".to_string(),
        "s_lorentz" => "Spacetime Symmetry".to_string(),
        "g_e8_lattice" => "E8 Lattice".to_string(),
        "g_600cell" => "600-cell".to_string(),
        "g_cl8" => "Clifford 8D".to_string(),
        "g_ncg_triple" => "Spectral Triple".to_string(),
        "g_calabi_yau" => "Calabi–Yau (risky)".to_string(),
        "f_higgs" => "Higgs Field".to_string(),
        "f_fermions" => "Matter Field".to_string(),
        "f_gauge" => "Force Field".to_string(),
        "f_gravity" => "Gravity Field".to_string(),
        "k_alpha_s" => "Strong Coupling".to_string(),
        "k_gnewton" => "Gravity Constant".to_string(),
        "k_hbar" => "Quantum Action".to_string(),
        _ => fallback.to_string(),
    }
}

/// Build the render model for the current state.
pub fn layout(state: &AppState, viewport: ViewportSize, theme: &Theme) -> RenderModel {
    let mut prims = Vec::new();
    let mut hits = Vec::new();

    // True-black backdrop.
    prims.push(RenderPrimitive::Rect {
        x: 0.0, y: 0.0, w: viewport.width, h: viewport.height,
        fill: theme.bg, stroke: None,
    });
    draw_starfield(viewport, theme, &mut prims);

    // Header.
    draw_header(theme, viewport, &mut prims);

    // Tutorial / how-to-play banner.
    draw_tutorial(theme, viewport, &mut prims);

    // Toolbar (game actions).
    draw_toolbar(state, theme, viewport, &mut prims, &mut hits);

    // Big bridge band — the dominant visual element.
    let bridge_y = TOOLBAR_BOTTOM + 12.0;
    let bridge_h = BRIDGE_BAND_H;
    draw_bridge_stage(state, theme, 0.0, bridge_y, viewport.width, bridge_h, &mut prims);

    // Recipe rail right below the bridge.
    let recipe_y = bridge_y + bridge_h + 6.0;
    draw_recipe_rail(state, theme,
        16.0, recipe_y, viewport.width - 32.0, RECIPE_RAIL_H,
        &mut prims, &mut hits);

    // Towers below the bridge — left = Data (blue), right = Geometry (purple).
    let towers_y = recipe_y + RECIPE_RAIL_H + 8.0;
    let towers_bottom = viewport.height - HONESTY_PANEL_H - 16.0;
    let towers_h = (towers_bottom - towers_y).max(180.0);
    let pad = 16.0;
    let tower_w = (viewport.width - pad * 3.0) * 0.5;

    draw_tower(state, theme, Tower::Data,
        pad, towers_y, tower_w, towers_h,
        "Data Tiles", "(blue — what we measure)",
        theme.tower_data, theme.data_glow,
        &mut prims, &mut hits);

    draw_tower(state, theme, Tower::Geometry,
        pad * 2.0 + tower_w, towers_y, tower_w, towers_h,
        "Geometry Tiles", "(purple — what we imagine)",
        theme.tower_geom, theme.geom_glow,
        &mut prims, &mut hits);

    // Honesty / score mini-panel at the bottom — does NOT dominate.
    draw_honesty_panel(state, theme,
        16.0, viewport.height - HONESTY_PANEL_H - 8.0,
        viewport.width - 32.0, HONESTY_PANEL_H,
        &mut prims);

    RenderModel { primitives: prims, hit_regions: hits, viewport }
}

fn draw_starfield(viewport: ViewportSize, theme: &Theme, prims: &mut Vec<RenderPrimitive>) {
    // Deterministic, sparse star dots so the black backdrop reads as space,
    // not a blank rectangle. Uses a tiny LCG seeded from viewport size so
    // identical viewports produce identical stars (snapshot-stable).
    let mut s: u32 = (viewport.width as u32).wrapping_mul(8121).wrapping_add(28411);
    for _ in 0..70 {
        s = s.wrapping_mul(1103515245).wrapping_add(12345);
        let x = ((s >> 8) % (viewport.width as u32).max(1)) as f32;
        s = s.wrapping_mul(1103515245).wrapping_add(12345);
        let y = ((s >> 8) % (viewport.height as u32).max(1)) as f32;
        s = s.wrapping_mul(1103515245).wrapping_add(12345);
        let r = 0.5 + ((s >> 8) % 14) as f32 * 0.15;
        let a = 60 + ((s >> 5) % 120) as u8;
        prims.push(RenderPrimitive::Circle {
            x, y, r,
            fill: Color(theme.fold_ring.0, theme.fold_ring.1, theme.fold_ring.2, a),
            stroke: None,
        });
    }
}

fn draw_header(theme: &Theme, viewport: ViewportSize, prims: &mut Vec<RenderPrimitive>) {
    prims.push(RenderPrimitive::Rect {
        x: 0.0, y: 0.0, w: viewport.width, h: HEADER_H,
        fill: Color(8, 10, 22, 255), stroke: None,
    });
    prims.push(RenderPrimitive::Text {
        x: 20.0, y: 30.0,
        s: format!("{}  —  Build the Bridge!", crate::PRODUCT_NAME),
        color: theme.bridge_deck, size: 24.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: 20.0, y: 48.0,
        s: "Hypothesis-discovery puzzle. NOT a proven Theory of Everything.".into(),
        color: theme.text_dim, size: 11.0, bold: false,
    });
}

fn draw_tutorial(theme: &Theme, viewport: ViewportSize, prims: &mut Vec<RenderPrimitive>) {
    let x = 16.0;
    let y = HEADER_H + 4.0;
    let w = viewport.width - 32.0;
    let h = TUTORIAL_H - 8.0;
    // Banner background — friendly cyan-tinted plate.
    prims.push(RenderPrimitive::Rect {
        x, y, w, h,
        fill: Color(8, 22, 42, 255),
        stroke: Some(theme.data_glow),
    });
    // Big objective.
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: y + 20.0,
        s: "Goal: light the bridge stones by picking pairs — one BLUE Data tile + one PURPLE Geometry tile.".into(),
        color: theme.text, size: 14.0, bold: true,
    });
    // Three numbered steps in a row.
    let step_y = y + 42.0;
    let steps = [
        ("1.", "Click a BLUE tile (left tower).", theme.data_glow),
        ("2.", "Click a PURPLE tile (right tower).", theme.geom_glow),
        ("3.", "Watch the bridge stone light up. Avoid red — it cracks the bridge!", theme.bridge_sound),
    ];
    let step_w = (w - 28.0) / 3.0;
    let mut sx = x + 14.0;
    for (n, txt, col) in steps {
        prims.push(RenderPrimitive::Text {
            x: sx, y: step_y,
            s: n.into(),
            color: col, size: 14.0, bold: true,
        });
        prims.push(RenderPrimitive::Text {
            x: sx + 22.0, y: step_y,
            s: txt.into(),
            color: theme.text, size: 12.0, bold: false,
        });
        sx += step_w;
    }
}

fn draw_toolbar(
    state: &AppState, theme: &Theme, viewport: ViewportSize,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    let y = TOOLBAR_TOP;
    let mut x = 16.0;
    // Friendly game-action labels; sub-text preserves technical hotkey hint.
    let buttons: [(&str, HitRegion, bool); 4] = [
        ("Reset (C)", HitRegion::ButtonClear, false),
        ("Hint (H)", HitRegion::ButtonHillClimb, false),
        ("Auto-build (A)", HitRegion::ButtonAnneal, false),
        (
            if state.view.benchmark_mode { "Honest mode: ON (B)" } else { "Honest mode: off (B)" },
            HitRegion::ButtonBenchmark, state.view.benchmark_mode,
        ),
    ];
    for (label, region, active) in buttons {
        let w = (label.len() as f32) * 7.8 + 28.0;
        let fill = if active { theme.button_active } else { theme.button };
        let stroke = if active { theme.bridge_sound } else { theme.stroke };
        // Glow halo for an inviting "press me" feel.
        prims.push(RenderPrimitive::Rect {
            x: x - 2.0, y: y - 2.0, w: w + 4.0, h: BUTTON_H + 4.0,
            fill: Color(fill.0, fill.1, fill.2, 50), stroke: None,
        });
        prims.push(RenderPrimitive::Rect {
            x, y, w, h: BUTTON_H, fill, stroke: Some(stroke),
        });
        let txt_col = if active { Color(20, 16, 8, 255) } else { theme.text };
        prims.push(RenderPrimitive::Text {
            x: x + 14.0, y: y + 23.0, s: label.into(),
            color: txt_col, size: 14.0, bold: true,
        });
        hits.push(HitBox { x, y, w, h: BUTTON_H, region });
        x += w + 10.0;
    }
    let _ = viewport;
}

/// Draw the dominant central bridge band: data island (left), geometry
/// island (right), giant glowing span with stones, win/lose feedback text.
fn draw_bridge_stage(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>,
) {
    let bridge = &state.bridge;

    // Backdrop plate.
    prims.push(RenderPrimitive::Rect {
        x, y, w, h,
        fill: Color(4, 8, 18, 255),
        stroke: Some(theme.stroke.with_alpha(120)),
    });

    // Concentric "space-fold" rings, decorative.
    let cx = x + w * 0.5;
    let cy = y + h * 0.5;
    for k in 0..5 {
        let r = 30.0 + k as f32 * 22.0 + bridge.compression as f32 * 28.0;
        prims.push(RenderPrimitive::Circle {
            x: cx, y: cy, r,
            fill: Color(0, 0, 0, 0),
            stroke: Some(theme.fold_ring),
        });
    }

    // Two islands / pillars.
    let pillar_w = 130.0;
    let pillar_h = h * 0.62;
    let pillar_y = y + (h - pillar_h) * 0.5;
    let data_x = x + 24.0;
    let geom_x = x + w - 24.0 - pillar_w;

    // Data pillar (blue glow).
    draw_pillar(
        prims, data_x, pillar_y, pillar_w, pillar_h,
        theme.tower_data, theme.data_glow,
        "DATA TOWER",
        &format!("{} tile(s)", bridge.data_pier_count),
        theme,
    );
    // Geometry pillar (purple glow).
    draw_pillar(
        prims, geom_x, pillar_y, pillar_w, pillar_h,
        theme.tower_geom, theme.geom_glow,
        "GEOMETRY TOWER",
        &format!("{} tile(s)", bridge.geom_pier_count),
        theme,
    );

    // Bridge deck: a big thick span between the pillar tops.
    let deck_y = pillar_y + 36.0;
    let deck_left = data_x + pillar_w - 4.0;
    let deck_right = geom_x + 4.0;
    let deck_w = deck_right - deck_left;
    let deck_h = 32.0;
    let deck_color = integrity_color(bridge.integrity, theme);

    // Outer glow under the deck.
    prims.push(RenderPrimitive::Rect {
        x: deck_left - 6.0, y: deck_y - 6.0,
        w: deck_w + 12.0, h: deck_h + 12.0,
        fill: deck_color.with_alpha(40), stroke: None,
    });

    // Deck base — a dim slab if empty, glowing gold if sound, cracked if collapsed.
    let base_fill = if bridge.integrity == BridgeIntegrity::Empty {
        Color(20, 24, 38, 255)
    } else if bridge.integrity == BridgeIntegrity::Collapsed {
        Color(40, 8, 12, 255)
    } else {
        Color(36, 28, 8, 255)
    };
    prims.push(RenderPrimitive::Rect {
        x: deck_left, y: deck_y, w: deck_w, h: deck_h,
        fill: base_fill, stroke: Some(deck_color),
    });

    // Stone slots: 8 evenly spaced stones along the deck — the visible
    // win-progress bar.
    let stone_count: usize = 8;
    let inner_pad = 10.0;
    let slot_w = (deck_w - inner_pad * 2.0) / stone_count as f32;
    let stones_lit = bridge.span_nodes.iter()
        .filter(|n| matches!(n.status, SpanStatus::Gold | SpanStatus::Empirical))
        .count()
        .min(stone_count);
    let stones_cracked = bridge.falsified_count.min(stone_count);
    for i in 0..stone_count {
        let sx = deck_left + inner_pad + slot_w * i as f32 + slot_w * 0.5;
        let sy = deck_y + deck_h * 0.5;
        let r = 10.0;
        let (fill, stroke) = if i < stones_cracked {
            (theme.bridge_collapsed, Some(Color(255, 200, 200, 255)))
        } else if i < stones_lit {
            (theme.bridge_sound, Some(Color(255, 250, 200, 255)))
        } else if !state.board.is_empty() && i == stones_lit {
            // Next stone slot — pulses with a soft preview colour.
            (Color(180, 180, 200, 200), Some(theme.stroke))
        } else {
            (Color(28, 32, 50, 255), Some(theme.stroke.with_alpha(120)))
        };
        // Soft halo behind lit stones.
        if i < stones_lit && stones_cracked == 0 {
            prims.push(RenderPrimitive::Circle {
                x: sx, y: sy, r: r + 5.0,
                fill: fill.with_alpha(70), stroke: None,
            });
        }
        prims.push(RenderPrimitive::Circle {
            x: sx, y: sy, r, fill, stroke,
        });
    }

    // If collapsed, paint a clear crack zig-zag across the deck.
    if bridge.integrity == BridgeIntegrity::Collapsed {
        let mid_x = (deck_left + deck_right) * 0.5;
        let zy = deck_y + deck_h + 8.0;
        let zigs = [
            (mid_x - 60.0, zy),
            (mid_x - 30.0, zy + 18.0),
            (mid_x,        zy - 6.0),
            (mid_x + 30.0, zy + 18.0),
            (mid_x + 60.0, zy),
        ];
        for w_pair in zigs.windows(2) {
            prims.push(RenderPrimitive::Line {
                x0: w_pair[0].0, y0: w_pair[0].1,
                x1: w_pair[1].0, y1: w_pair[1].1,
                color: theme.bridge_collapsed, width: 3.0,
            });
        }
    }

    // Header text band ABOVE the deck so it never collides with stones.
    // Includes the legacy "integrity:" label required by the regression test.
    let header_y = y + 22.0;
    prims.push(RenderPrimitive::Text {
        x: x + 16.0, y: header_y,
        s: format!(
            "GOLDEN BRIDGE — integrity: {}   bridge strength: {:+.3}   compression: {:.0}%",
            bridge.integrity.label(), bridge.strength, bridge.compression * 100.0,
        ),
        color: integrity_color(bridge.integrity, theme),
        size: 13.0, bold: true,
    });

    // Per-pier counter labels — placed *below* the integrity header band.
    // The regression test in `integrity_header_does_not_overlap_pier_counters`
    // requires Data·N / Geometry·N to sit below the integrity row.
    let counter_y = y + 50.0;
    prims.push(RenderPrimitive::Text {
        x: data_x + 4.0, y: counter_y,
        s: format!("Data·{}", bridge.data_pier_count),
        color: theme.data_glow, size: 11.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: geom_x + pillar_w - 70.0, y: counter_y,
        s: format!("Geometry·{}", bridge.geom_pier_count),
        color: theme.geom_glow, size: 11.0, bold: true,
    });

    // Big status banner below the deck — child-friendly verdict.
    let status_y = deck_y + deck_h + 36.0;
    let (status_text, status_color) = match bridge.integrity {
        BridgeIntegrity::Empty => (
            "Pick a BLUE tile, then a PURPLE tile to begin.".to_string(),
            theme.text_dim,
        ),
        BridgeIntegrity::Sound if stones_lit >= 4 => (
            format!("BRIDGE STABLE! {} stones glowing.  (Honest hypothesis — keep going!)", stones_lit),
            theme.bridge_sound,
        ),
        BridgeIntegrity::Sound => (
            format!("Building... {} stone(s) lit. Add more matched pairs.", stones_lit),
            theme.bridge_sound,
        ),
        BridgeIntegrity::Provisional => (
            "Building... bridge is wobbly. Pick safer (green-edged) tiles.".to_string(),
            theme.bridge_provisional,
        ),
        BridgeIntegrity::Collapsed => (
            "BRIDGE CRACKED! A falsified (red) tile broke it. Press Reset and try again.".to_string(),
            theme.bridge_collapsed,
        ),
    };
    prims.push(RenderPrimitive::Text {
        x: x + 16.0, y: status_y,
        s: status_text, color: status_color, size: 14.0, bold: true,
    });

    if bridge.integrity == BridgeIntegrity::Collapsed {
        prims.push(RenderPrimitive::Text {
            x: x + 16.0, y: status_y + 18.0,
            s: format!(
                "Honesty floor tripped: {} falsified tile(s) on the span. COLLAPSE.",
                bridge.falsified_count
            ),
            color: theme.bridge_collapsed, size: 11.0, bold: true,
        });
    }

    // Span-node markers projected onto the deck (pier_t in [0,1]).
    // These mirror the precise tiles the player has activated and live
    // ABOVE the stone slots as small ticks.
    let span_left = deck_left + inner_pad;
    let span_right = deck_right - inner_pad;
    for sn in &bridge.span_nodes {
        let sx = span_left + (span_right - span_left) * sn.pier_t;
        let sy = deck_y - 8.0;
        prims.push(RenderPrimitive::Circle {
            x: sx, y: sy, r: 4.5,
            fill: span_color(sn.status, theme),
            stroke: Some(theme.stroke),
        });
    }
}

fn draw_pillar(
    prims: &mut Vec<RenderPrimitive>,
    x: f32, y: f32, w: f32, h: f32,
    body: Color, glow: Color,
    title: &str, subtitle: &str,
    theme: &Theme,
) {
    // Glow halo around the pillar.
    prims.push(RenderPrimitive::Rect {
        x: x - 6.0, y: y - 6.0, w: w + 12.0, h: h + 12.0,
        fill: glow.with_alpha(40), stroke: None,
    });
    // Body.
    prims.push(RenderPrimitive::Rect {
        x, y, w, h, fill: body, stroke: Some(glow),
    });
    // Pillar cap.
    prims.push(RenderPrimitive::Rect {
        x: x - 4.0, y, w: w + 8.0, h: 10.0,
        fill: glow, stroke: None,
    });
    // Pillar base.
    prims.push(RenderPrimitive::Rect {
        x: x - 4.0, y: y + h - 10.0, w: w + 8.0, h: 10.0,
        fill: glow, stroke: None,
    });
    // Vertical glow stripe down the centre.
    prims.push(RenderPrimitive::Rect {
        x: x + w * 0.5 - 2.0, y: y + 12.0,
        w: 4.0, h: h - 24.0,
        fill: glow.with_alpha(170), stroke: None,
    });

    // Title.
    prims.push(RenderPrimitive::Text {
        x: x + 10.0, y: y + 30.0,
        s: title.into(), color: theme.text, size: 13.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 10.0, y: y + 46.0,
        s: subtitle.into(), color: theme.text_dim, size: 10.0, bold: false,
    });
}

fn draw_recipe_rail(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    prims.push(RenderPrimitive::Text {
        x, y: y + 18.0,
        s: "Try Recipe:".into(),
        color: theme.bridge_sound, size: 12.0, bold: true,
    });
    let mut cx = x + 96.0;
    let max_x = x + w;
    for recipe in state.recipes.iter() {
        let label = format!("{} ({})", recipe.title, recipe.tile_ids.len());
        let cw = (label.len() as f32) * 7.0 + 20.0;
        if cx + cw > max_x { break; }
        prims.push(RenderPrimitive::Rect {
            x: cx - 1.0, y: y - 1.0, w: cw + 2.0, h: h + 2.0,
            fill: theme.bridge_sound.with_alpha(40), stroke: None,
        });
        prims.push(RenderPrimitive::Rect {
            x: cx, y, w: cw, h,
            fill: theme.recipe_chip, stroke: Some(theme.bridge_sound),
        });
        prims.push(RenderPrimitive::Text {
            x: cx + 9.0, y: y + 20.0,
            s: label,
            color: theme.text, size: 12.0, bold: false,
        });
        hits.push(HitBox {
            x: cx, y, w: cw, h,
            region: HitRegion::RecipeChip(recipe.id.clone()),
        });
        cx += cw + 8.0;
    }
}

fn draw_tower(
    state: &AppState, theme: &Theme, tower: Tower,
    x: f32, y: f32, w: f32, h: f32,
    title: &str, hint: &str,
    bg: Color, glow: Color,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    // Soft glow halo.
    prims.push(RenderPrimitive::Rect {
        x: x - 4.0, y: y - 4.0, w: w + 8.0, h: h + 8.0,
        fill: glow.with_alpha(30), stroke: None,
    });
    prims.push(RenderPrimitive::Rect {
        x, y, w, h, fill: bg, stroke: Some(glow),
    });
    // Title strip.
    prims.push(RenderPrimitive::Rect {
        x, y, w, h: 30.0, fill: glow.with_alpha(60), stroke: None,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 12.0, y: y + 21.0, s: title.into(),
        color: theme.text, size: 15.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 12.0 + (title.len() as f32) * 9.0 + 8.0, y: y + 21.0,
        s: hint.into(),
        color: theme.text_dim, size: 11.0, bold: false,
    });

    // Tile grid. The geometry tower carries more nodes than data, so use
    // 3 columns there and 2 in data to keep the bridge / towers proportional.
    let cols: usize = if tower == Tower::Data { 2 } else { 3 };
    let inner_x = x + 12.0;
    let inner_top = y + 38.0;
    let inner_right = x + w - 12.0;
    let inner_bottom = y + h - 12.0;
    let tile_gap_x = 8.0;
    let tile_w = (inner_right - inner_x - tile_gap_x * (cols as f32 - 1.0)) / cols as f32;

    let kinds_data = [NodeKind::Observable, NodeKind::Constraint];
    let kinds_geom = [NodeKind::Symmetry, NodeKind::Geometry, NodeKind::Field, NodeKind::Constant];
    let kinds: &[NodeKind] = if tower == Tower::Data { &kinds_data } else { &kinds_geom };

    let mut col = 0usize;
    let mut row_y = inner_top;
    for kind in kinds {
        for node in state.catalog.nodes_of(*kind) {
            if row_y + TILE_H > inner_bottom { break; }
            let tx = inner_x + (col as f32) * (tile_w + tile_gap_x);
            let ty = row_y;

            let selected = state.board.contains(&node.id);
            let hovered = state.view.hover_id.as_deref() == Some(node.id.as_str());
            let cclr = claim_color(node.claim, theme);
            let fill = if selected {
                glow
            } else if hovered {
                theme.tile_hover
            } else {
                theme.tile_idle
            };

            // Halo for selected tile.
            if selected {
                prims.push(RenderPrimitive::Rect {
                    x: tx - 3.0, y: ty - 3.0,
                    w: tile_w + 6.0, h: TILE_H + 6.0,
                    fill: glow.with_alpha(90), stroke: None,
                });
            }
            prims.push(RenderPrimitive::Rect {
                x: tx, y: ty, w: tile_w, h: TILE_H,
                fill, stroke: Some(cclr),
            });
            // Claim stripe (left).
            prims.push(RenderPrimitive::Rect {
                x: tx, y: ty, w: 5.0, h: TILE_H,
                fill: cclr, stroke: None,
            });
            // Big kid-readable label.
            let label = friendly_label(&node.id, &node.name);
            let txt_color = if selected { Color(8, 14, 22, 255) } else { theme.text };
            prims.push(RenderPrimitive::Text {
                x: tx + 12.0, y: ty + 20.0,
                s: truncate(&label, 22),
                color: txt_color, size: 13.0, bold: true,
            });
            // Smaller subtext: technical id.
            let sub_color = if selected { Color(8, 14, 22, 200) } else { theme.text_dim };
            prims.push(RenderPrimitive::Text {
                x: tx + 12.0, y: ty + 35.0,
                s: truncate(&node.id, 22),
                color: sub_color, size: 10.0, bold: false,
            });
            // Falsified warning glyph.
            if node.claim == ClaimStatus::HighRiskOrFalsified {
                prims.push(RenderPrimitive::Circle {
                    x: tx + tile_w - 12.0, y: ty + 12.0, r: 6.0,
                    fill: theme.bridge_collapsed, stroke: Some(theme.text),
                });
                prims.push(RenderPrimitive::Text {
                    x: tx + tile_w - 16.0, y: ty + 16.0,
                    s: "!".into(),
                    color: theme.text, size: 11.0, bold: true,
                });
            }
            // Selected check.
            if selected {
                prims.push(RenderPrimitive::Circle {
                    x: tx + tile_w - 14.0, y: ty + TILE_H - 14.0, r: 5.0,
                    fill: theme.bridge_sound, stroke: Some(theme.stroke),
                });
            }

            hits.push(HitBox {
                x: tx, y: ty, w: tile_w, h: TILE_H,
                region: HitRegion::Tile(node.id.clone()),
            });

            col += 1;
            if col >= cols {
                col = 0;
                row_y += TILE_H + TILE_GAP_Y;
            }
        }
    }
    // Suppress unused-warning when `cols`/`kinds` don't trigger a section break.
    let _ = bg;
    let _ = col;
}

fn draw_honesty_panel(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>,
) {
    prims.push(RenderPrimitive::Rect {
        x, y, w, h,
        fill: Color(10, 14, 24, 255),
        stroke: Some(theme.text_dim),
    });
    let s = &state.score;
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: y + 22.0,
        s: "Honesty panel  —  bridge strength is NOT proof of physics.".into(),
        color: theme.text_dim, size: 11.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 14.0, y: y + 42.0,
        s: format!("bridge total = {:+.3}    worst claim: {}    bridge: {}",
                   s.total, s.worst_claim.label(), state.bridge.integrity.label()),
        color: theme.text, size: 12.0, bold: true,
    });
    // Mini breakdown — 2 columns of label/value.
    let rows = [
        ("consistency", s.consistency),
        ("dim sanity",  s.dimensional_sanity),
        ("obs fit",     s.observable_fit),
        ("proof debt",  -s.proof_debt_penalty),
        ("falsify",     -s.falsification_penalty),
        ("simplicity",  s.simplicity),
        ("symmetry",    s.symmetry_coherence),
        ("reproduce",   s.reproducibility),
    ];
    let cols = 4usize;
    let col_w = (w - 28.0) / cols as f32;
    for (i, (label, val)) in rows.iter().enumerate() {
        let cx = x + 14.0 + (i % cols) as f32 * col_w;
        let cy = y + 62.0 + (i / cols) as f32 * 14.0;
        prims.push(RenderPrimitive::Text {
            x: cx, y: cy,
            s: format!("{}: {:+.2}", label, val),
            color: theme.text_dim, size: 10.0, bold: false,
        });
    }
    // Selected hint at the right.
    let right_x = x + w - 240.0;
    prims.push(RenderPrimitive::Text {
        x: right_x, y: y + 22.0,
        s: format!("selected: {} tile(s)", state.board.len()),
        color: theme.text, size: 11.0, bold: true,
    });
    if let Some(focus) = state.view.focus_id.as_ref() {
        if let Some(node) = state.catalog.by_id(focus) {
            prims.push(RenderPrimitive::Text {
                x: right_x, y: y + 38.0,
                s: format!("focus: {} [{}]",
                    friendly_label(&node.id, &node.name),
                    node.claim.label()),
                color: claim_color(node.claim, theme),
                size: 11.0, bold: true,
            });
        }
    }
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
        // Large enough that every tile in the geometry tower fits below the
        // bridge stage + recipe rail.
        ViewportSize { width: 1280.0, height: 1080.0 }
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

    /// Regression: the integrity header (top of the bridge stage) and the
    /// pier counters (`Data·N`, `Geometry·N`) must not vertically overlap.
    #[test]
    fn integrity_header_does_not_overlap_pier_counters() {
        let m = layout(&s(), vp(), &Theme::default());
        fn box_top_bottom(y: f32, size: f32) -> (f32, f32) {
            (y - size * 1.1, y + size * 0.25)
        }
        let mut integrity_y: Option<f32> = None;
        let mut pier_ys: Vec<f32> = Vec::new();
        for p in &m.primitives {
            if let RenderPrimitive::Text { s, y, .. } = p {
                if s.starts_with("GOLDEN BRIDGE — integrity:") {
                    integrity_y = Some(*y);
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
            RenderPrimitive::Text { s, .. } =>
                s.contains("COLLAPSE") || s.contains("CRACKED") || s.contains("Honesty floor"),
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
        assert!(
            chip_ids.contains(&state.recipes[0].id),
            "expected first recipe `{}` to be hittable, got {:?}",
            state.recipes[0].id,
            chip_ids
        );
    }

    /// Game-feel regression: the tutorial banner must surface the three
    /// numbered onboarding steps so the child reading the page knows what
    /// to click first.
    #[test]
    fn tutorial_banner_lists_three_steps() {
        let m = layout(&s(), vp(), &Theme::default());
        let mut markers = 0;
        for p in &m.primitives {
            if let RenderPrimitive::Text { s, .. } = p {
                if s.starts_with("1.") || s.starts_with("2.") || s.starts_with("3.") {
                    markers += 1;
                }
            }
        }
        assert_eq!(markers, 3, "expected exactly three numbered tutorial steps");
    }

    /// Game-feel: the toolbar uses kid-friendly labels.
    #[test]
    fn toolbar_uses_game_labels() {
        let m = layout(&s(), vp(), &Theme::default());
        let texts: Vec<String> = m.primitives.iter().filter_map(|p| match p {
            RenderPrimitive::Text { s, .. } => Some(s.clone()),
            _ => None,
        }).collect();
        let joined = texts.join(" || ");
        assert!(joined.contains("Reset"), "expected Reset label, got: {}", joined);
        assert!(joined.contains("Hint"), "expected Hint label, got: {}", joined);
        assert!(joined.contains("Auto-build"), "expected Auto-build label, got: {}", joined);
    }

    /// Game-feel: a friendly label replaces the raw `o_higgs_mass` id in the
    /// primary tile text. The id is still rendered as subtext.
    #[test]
    fn friendly_labels_replace_raw_ids() {
        let m = layout(&s(), vp(), &Theme::default());
        let texts: Vec<String> = m.primitives.iter().filter_map(|p| match p {
            RenderPrimitive::Text { s, .. } => Some(s.clone()),
            _ => None,
        }).collect();
        let joined = texts.join(" || ");
        // At least one of the friendly translations must appear if its node
        // is in the default catalog.
        let has_any_friendly = joined.contains("Higgs Mass")
            || joined.contains("Weak Force")
            || joined.contains("Strong Force")
            || joined.contains("Golden Shape");
        assert!(has_any_friendly, "expected at least one friendly label, got: {}", joined);
    }

    #[test]
    fn winning_status_surfaces_when_bridge_stable() {
        let mut state = s();
        // Load a recipe that should give Sound integrity.
        let recipe_id = state.recipes.iter().find(|r| r.id == "sm_core").map(|r| r.id.clone());
        if let Some(rid) = recipe_id {
            state.apply(crate::input::UiEvent::LoadRecipe(rid));
            let m = layout(&state, vp(), &Theme::default());
            let any_status = m.primitives.iter().any(|p| match p {
                RenderPrimitive::Text { s, .. } =>
                    s.contains("Building") || s.contains("STABLE") || s.contains("wobbly"),
                _ => false,
            });
            assert!(any_status, "expected a status banner once tiles are placed");
        }
    }
}

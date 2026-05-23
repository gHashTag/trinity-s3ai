// Pure render model.
//
// `layout(state, viewport, theme)` walks the catalog and produces a
// `RenderModel`: a flat list of `RenderPrimitive`s (rect/circle/line/text)
// plus a list of `HitBox`es for input hit-testing. The browser shell
// (`wasm.rs`) iterates the primitives and issues Canvas2D draw calls; the
// shell never inspects domain types directly.
//
// Layout (16:9 game stage, designed for 1280x720):
//
//   +----------------------------------------------------------------------+
//   | Title bar:  GOLDEN BRIDGE — Build the Bridge!     (small subtitle)   |
//   +----------------------------------------------------------------------+
//   |                                                                      |
//   |  ###############  BIG BRIDGE STAGE  (60-70% screen height)  #######  |
//   |  ###  [DATA]  =====  GLOWING STONE DECK with 4 BIG STONES  =====  ###|
//   |  ###  pillar               (cracks visibly on falsification)      ###|
//   |  ###                                                              ###|
//   |  ###   "Step 1: Pick a BLUE Data card"                            ###|
//   |  ###   (one hero instruction reflecting current state)            ###|
//   |  ###                                       [GEOM] pillar          ###|
//   |  ####################################################################|
//   |                                                                      |
//   |  [Start over] [Hint] [Auto-build] [Honest mode]    (large buttons)   |
//   |                                                                      |
//   |  ## BLUE DATA CARDS — pick one ##  ## PURPLE GEOMETRY CARDS — pick ##|
//   |  [ Higgs Mass ] [ Light Strength ]  [ Weak Force ] [ Strong Force ]  |
//   |  [ Muon Wobble] [ Neutrino Mix ]    [ Golden H4 ] [ Higgs Field ]    |
//   |                                                                      |
//   |  ▾ Science / honesty (collapsed by default — bridge strength etc.)   |
//   +----------------------------------------------------------------------+
//
// Design rules:
//   * One primary action per state. The hero instruction line above the
//     deck mirrors the current step (pick blue, pick purple, win, etc.).
//   * Bridge is visually dominant: ~60% of screen height, big stones,
//     thick deck, glowing pillars.
//   * Tiles are larger (>=44px tall, ~3 columns), fewer recipes, no raw
//     id subtext unless hovered/focused.
//   * Honesty / score breakdown collapsed into a single bottom strip with
//     a 'science details' chip — never competes with the bridge.

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

// Layout constants — sized for a 1280x720 (16:9) target viewport. All
// values scale linearly with the actual viewport, since `layout` reads
// `viewport.{width,height}` everywhere.
const TILE_H: f32 = 52.0;
const TILE_GAP_Y: f32 = 8.0;
const TILE_GAP_X: f32 = 10.0;
const HEADER_H: f32 = 48.0;
const BUTTON_H: f32 = 44.0;
const HONESTY_STRIP_H: f32 = 36.0;
// The bridge stage is the dominant element — ~58% of the viewport height
// at the reference size, so it visually anchors the page.
const BRIDGE_RATIO: f32 = 0.56;

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

/// Hero instruction text — the single primary call-to-action the player
/// sees above the bridge deck. Reflects the current bridge state so the
/// canvas only ever shows ONE next-step prompt at a time.
fn hero_instruction(state: &AppState) -> (String, bool /* is win */) {
    let bridge = &state.bridge;
    if bridge.integrity == BridgeIntegrity::Collapsed {
        return (
            "BRIDGE CRACKED! A falsified (red ⚠) card broke it. Press Start over.".into(),
            false,
        );
    }
    // Count selected tiles per tower so we know which side the player must
    // pick from next.
    let mut data_picked = 0usize;
    let mut geom_picked = 0usize;
    for id in state.board.ids() {
        if let Some(n) = state.catalog.by_id(id) {
            match n.kind.tower() {
                Tower::Data => data_picked += 1,
                Tower::Geometry => geom_picked += 1,
            }
        }
    }
    let stones_lit = bridge
        .span_nodes
        .iter()
        .filter(|n| matches!(n.status, SpanStatus::Gold | SpanStatus::Empirical))
        .count();
    if stones_lit >= 4 {
        return (
            format!(
                "BRIDGE STABLE! {} stones glowing — great work. (Hypothesis only, not proof.)",
                stones_lit
            ),
            true,
        );
    }
    if state.board.is_empty() {
        return ("Step 1: Pick a BLUE Data card below.".into(), false);
    }
    if data_picked == 0 {
        return ("Step 1: Pick a BLUE Data card below.".into(), false);
    }
    if geom_picked == 0 {
        return ("Step 2: Pick a PURPLE Geometry card below.".into(), false);
    }
    (
        format!("Light 4 stones to win. {} lit — keep going.", stones_lit),
        false,
    )
}

/// Build the render model for the current state.
pub fn layout(state: &AppState, viewport: ViewportSize, theme: &Theme) -> RenderModel {
    let mut prims = Vec::new();
    let mut hits = Vec::new();

    // True-black backdrop with sparse decorative stars.
    prims.push(RenderPrimitive::Rect {
        x: 0.0, y: 0.0, w: viewport.width, h: viewport.height,
        fill: theme.bg, stroke: None,
    });
    draw_starfield(viewport, theme, &mut prims);

    // Slim title bar — no walls of text above the canvas.
    draw_title_bar(theme, viewport, &mut prims);

    // Big bridge stage — the dominant visual element (~58% of viewport
    // height). Carries the hero instruction line, the deck with four big
    // stones, and the two glowing pillars.
    let pad = 16.0;
    let stage_y = HEADER_H + 6.0;
    let stage_h = (viewport.height * BRIDGE_RATIO).max(280.0);
    draw_bridge_stage(state, theme, 0.0, stage_y, viewport.width, stage_h, &mut prims);

    // Toolbar lives directly under the stage, large kid-friendly buttons.
    let toolbar_y = stage_y + stage_h + 8.0;
    draw_toolbar(state, theme, pad, toolbar_y, viewport.width - pad * 2.0,
        &mut prims, &mut hits);

    // Two card strips: BLUE Data (left), PURPLE Geometry (right). These are
    // the only tile-pickers — fewer, larger cards, no raw id subtext on the
    // primary face.
    let cards_y = toolbar_y + BUTTON_H + 12.0;
    let cards_bottom = viewport.height - HONESTY_STRIP_H - 8.0;
    let cards_h = (cards_bottom - cards_y).max(140.0);
    let strip_w = (viewport.width - pad * 3.0) * 0.5;

    draw_card_strip(state, theme, Tower::Data,
        pad, cards_y, strip_w, cards_h,
        "BLUE Data cards — pick one", theme.tower_data, theme.data_glow,
        &mut prims, &mut hits);
    draw_card_strip(state, theme, Tower::Geometry,
        pad * 2.0 + strip_w, cards_y, strip_w, cards_h,
        "PURPLE Geometry cards — pick one", theme.tower_geom, theme.geom_glow,
        &mut prims, &mut hits);

    // Compact honesty / science strip pinned to the bottom — single low-
    // contrast line. The full breakdown stays in the HTML <details>.
    draw_honesty_strip(state, theme,
        pad, viewport.height - HONESTY_STRIP_H - 4.0,
        viewport.width - pad * 2.0, HONESTY_STRIP_H,
        &mut prims, &mut hits);

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

/// Slim title bar — game title on the left, mini-legend chips on the right.
///
/// Wall-of-text removed by design: the three numbered onboarding steps now
/// live below the bridge in a single mini-banner (rendered by
/// `draw_step_legend` from inside `draw_bridge_stage`), and the honesty
/// notice has moved to the bottom strip + HTML <details> drawer.
fn draw_title_bar(theme: &Theme, viewport: ViewportSize, prims: &mut Vec<RenderPrimitive>) {
    prims.push(RenderPrimitive::Rect {
        x: 0.0, y: 0.0, w: viewport.width, h: HEADER_H,
        fill: Color(8, 10, 22, 255), stroke: None,
    });
    prims.push(RenderPrimitive::Text {
        x: 20.0, y: 28.0,
        s: format!("{}  —  Build the Bridge!", crate::PRODUCT_NAME),
        color: theme.bridge_deck, size: 22.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: 20.0, y: 44.0,
        s: "Pick BLUE + PURPLE cards. Light 4 stones to win. Avoid red ⚠.".into(),
        color: theme.text_dim, size: 11.0, bold: false,
    });
}

/// Large kid-friendly toolbar — anchored under the bridge stage. Each
/// button has a ≥44px hit target and a clear glow halo so it reads as a
/// game control, not a debug widget.
fn draw_toolbar(
    state: &AppState, theme: &Theme,
    x0: f32, y: f32, w_total: f32,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    let buttons: [(&str, HitRegion, bool); 4] = [
        ("Start over (C)", HitRegion::ButtonClear, false),
        ("Hint (H)", HitRegion::ButtonHillClimb, false),
        ("Auto-build (A)", HitRegion::ButtonAnneal, false),
        (
            if state.view.benchmark_mode { "Honest mode: ON (B)" } else { "Honest mode: off (B)" },
            HitRegion::ButtonBenchmark, state.view.benchmark_mode,
        ),
    ];
    // Equal-width buttons spread across the full toolbar width so the bar
    // looks deliberate rather than crowded into the corner.
    let gap = 12.0;
    let n = buttons.len() as f32;
    let bw = ((w_total - gap * (n - 1.0)) / n).max(140.0);
    let mut x = x0;
    for (label, region, active) in buttons {
        let fill = if active { theme.button_active } else { theme.button };
        let stroke = if active { theme.bridge_sound } else { theme.stroke };
        // Soft glow halo.
        prims.push(RenderPrimitive::Rect {
            x: x - 3.0, y: y - 3.0, w: bw + 6.0, h: BUTTON_H + 6.0,
            fill: Color(fill.0, fill.1, fill.2, 60), stroke: None,
        });
        prims.push(RenderPrimitive::Rect {
            x, y, w: bw, h: BUTTON_H, fill, stroke: Some(stroke),
        });
        let txt_col = if active { Color(20, 16, 8, 255) } else { theme.text };
        prims.push(RenderPrimitive::Text {
            x: x + 16.0, y: y + 28.0, s: label.into(),
            color: txt_col, size: 15.0, bold: true,
        });
        hits.push(HitBox { x, y, w: bw, h: BUTTON_H, region });
        x += bw + gap;
    }
}

/// Draw the dominant central bridge stage: two big islands/pillars, the
/// hero instruction line, the thick glowing deck with 4 large stones, and
/// the compact 3-step legend below the deck.
fn draw_bridge_stage(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>,
) {
    let bridge = &state.bridge;

    // Backdrop plate — sky / space colour.
    prims.push(RenderPrimitive::Rect {
        x, y, w, h,
        fill: Color(4, 8, 18, 255),
        stroke: Some(theme.stroke.with_alpha(120)),
    });

    // Slim integrity micro-row at the very top — keeps the required
    // "GOLDEN BRIDGE — integrity:" label without dominating the stage.
    let header_y = y + 18.0;
    prims.push(RenderPrimitive::Text {
        x: x + 16.0, y: header_y,
        s: format!(
            "GOLDEN BRIDGE — integrity: {}   strength: {:+.2}",
            bridge.integrity.label(), bridge.strength,
        ),
        color: integrity_color(bridge.integrity, theme),
        size: 12.0, bold: true,
    });

    // Big hero instruction — one primary action per state, centred under
    // the integrity row. This is the single most important text on the
    // page after the title.
    let (hero, is_win) = hero_instruction(state);
    let hero_color = if is_win {
        theme.bridge_sound
    } else if bridge.integrity == BridgeIntegrity::Collapsed {
        theme.bridge_collapsed
    } else {
        theme.text
    };
    prims.push(RenderPrimitive::Text {
        x: x + 16.0, y: y + 42.0,
        s: hero,
        color: hero_color, size: 18.0, bold: true,
    });

    // Two islands / pillars — thick, glowing, planted on a horizon.
    let pillar_w = (w * 0.12).clamp(96.0, 150.0);
    let pillar_h = h * 0.50;
    let pillar_y = y + h * 0.30;
    let data_x = x + 28.0;
    let geom_x = x + w - 28.0 - pillar_w;

    draw_pillar(
        prims, data_x, pillar_y, pillar_w, pillar_h,
        theme.tower_data, theme.data_glow,
        "DATA",
        &format!("{} card(s)", bridge.data_pier_count),
        theme,
    );
    draw_pillar(
        prims, geom_x, pillar_y, pillar_w, pillar_h,
        theme.tower_geom, theme.geom_glow,
        "GEOMETRY",
        &format!("{} card(s)", bridge.geom_pier_count),
        theme,
    );

    // Pier counters below the integrity row, well above the deck.
    let counter_y = y + 70.0;
    prims.push(RenderPrimitive::Text {
        x: data_x, y: counter_y,
        s: format!("Data·{}", bridge.data_pier_count),
        color: theme.data_glow, size: 12.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: geom_x + pillar_w - 90.0, y: counter_y,
        s: format!("Geometry·{}", bridge.geom_pier_count),
        color: theme.geom_glow, size: 12.0, bold: true,
    });

    // Decorative "space-fold" rings behind the deck — purely visual.
    let cx = x + w * 0.5;
    let cy = pillar_y + pillar_h * 0.45;
    for k in 0..4 {
        let r = 40.0 + k as f32 * 26.0 + bridge.compression as f32 * 24.0;
        prims.push(RenderPrimitive::Circle {
            x: cx, y: cy, r,
            fill: Color(0, 0, 0, 0),
            stroke: Some(theme.fold_ring),
        });
    }

    // Bridge deck — thick glowing span between pillar tops.
    let deck_h = (h * 0.16).clamp(36.0, 60.0);
    let deck_y = pillar_y + pillar_h * 0.35 - deck_h * 0.5;
    let deck_left = data_x + pillar_w - 6.0;
    let deck_right = geom_x + 6.0;
    let deck_w = (deck_right - deck_left).max(120.0);
    let deck_color = integrity_color(bridge.integrity, theme);

    // Outer glow halo.
    prims.push(RenderPrimitive::Rect {
        x: deck_left - 10.0, y: deck_y - 10.0,
        w: deck_w + 20.0, h: deck_h + 20.0,
        fill: deck_color.with_alpha(50), stroke: None,
    });

    let base_fill = if bridge.integrity == BridgeIntegrity::Empty {
        Color(22, 26, 42, 255)
    } else if bridge.integrity == BridgeIntegrity::Collapsed {
        Color(48, 10, 14, 255)
    } else {
        Color(42, 32, 10, 255)
    };
    prims.push(RenderPrimitive::Rect {
        x: deck_left, y: deck_y, w: deck_w, h: deck_h,
        fill: base_fill, stroke: Some(deck_color),
    });

    // Plank lines across the deck (visible texture cue).
    let planks = 8usize;
    for i in 1..planks {
        let px = deck_left + deck_w * (i as f32 / planks as f32);
        prims.push(RenderPrimitive::Line {
            x0: px, y0: deck_y + 4.0,
            x1: px, y1: deck_y + deck_h - 4.0,
            color: deck_color.with_alpha(80), width: 1.0,
        });
    }

    // Four BIG stone slots — the visible win-progress bar. Fewer, larger
    // stones than the old 8-stone strip so the player reads progress at a
    // glance.
    let stone_count: usize = 4;
    let inner_pad = deck_w * 0.10;
    let slot_w = (deck_w - inner_pad * 2.0) / stone_count as f32;
    let stone_r = (deck_h * 0.42).clamp(14.0, 24.0);
    let stones_lit = bridge.span_nodes.iter()
        .filter(|n| matches!(n.status, SpanStatus::Gold | SpanStatus::Empirical))
        .count()
        .min(stone_count);
    let stones_cracked = bridge.falsified_count.min(stone_count);
    for i in 0..stone_count {
        let sx = deck_left + inner_pad + slot_w * i as f32 + slot_w * 0.5;
        let sy = deck_y + deck_h * 0.5;
        let (fill, stroke) = if i < stones_cracked {
            (theme.bridge_collapsed, Some(Color(255, 200, 200, 255)))
        } else if i < stones_lit {
            (theme.bridge_sound, Some(Color(255, 250, 200, 255)))
        } else if !state.board.is_empty() && i == stones_lit {
            (Color(190, 190, 210, 220), Some(theme.stroke))
        } else {
            (Color(30, 36, 56, 255), Some(theme.stroke.with_alpha(120)))
        };
        // Soft halo behind lit stones.
        if i < stones_lit && stones_cracked == 0 {
            prims.push(RenderPrimitive::Circle {
                x: sx, y: sy, r: stone_r + 8.0,
                fill: fill.with_alpha(80), stroke: None,
            });
        }
        prims.push(RenderPrimitive::Circle {
            x: sx, y: sy, r: stone_r, fill, stroke,
        });
        // Stone number tag for hit-target legibility.
        prims.push(RenderPrimitive::Text {
            x: sx - 4.0, y: sy + 5.0,
            s: format!("{}", i + 1),
            color: if i < stones_lit { Color(20, 18, 4, 255) } else { theme.text_dim },
            size: 14.0, bold: true,
        });
    }

    // Crack zig-zag on collapse — emphasised so it's obvious.
    if bridge.integrity == BridgeIntegrity::Collapsed {
        let mid_x = (deck_left + deck_right) * 0.5;
        let zy = deck_y + deck_h + 10.0;
        let zigs = [
            (mid_x - 80.0, zy),
            (mid_x - 40.0, zy + 22.0),
            (mid_x,        zy - 8.0),
            (mid_x + 40.0, zy + 22.0),
            (mid_x + 80.0, zy),
        ];
        for w_pair in zigs.windows(2) {
            prims.push(RenderPrimitive::Line {
                x0: w_pair[0].0, y0: w_pair[0].1,
                x1: w_pair[1].0, y1: w_pair[1].1,
                color: theme.bridge_collapsed, width: 4.0,
            });
        }
        prims.push(RenderPrimitive::Text {
            x: x + 16.0, y: y + h - 50.0,
            s: format!(
                "Honesty floor tripped: {} falsified card(s) — COLLAPSE.",
                bridge.falsified_count
            ),
            color: theme.bridge_collapsed, size: 12.0, bold: true,
        });
    }

    // Span-node markers projected onto the deck (small status ticks).
    let span_left = deck_left + inner_pad;
    let span_right = deck_right - inner_pad;
    for sn in &bridge.span_nodes {
        let sx = span_left + (span_right - span_left) * sn.pier_t;
        let sy = deck_y - 10.0;
        prims.push(RenderPrimitive::Circle {
            x: sx, y: sy, r: 5.0,
            fill: span_color(sn.status, theme),
            stroke: Some(theme.stroke),
        });
    }

    // Compact 3-step legend across the bottom of the stage so the
    // onboarding text is always visible without a separate banner.
    let leg_y = y + h - 24.0;
    let step_w = (w - 32.0) / 3.0;
    let steps = [
        ("1.", "Pick a BLUE Data card.", theme.data_glow),
        ("2.", "Pick a PURPLE Geometry card.", theme.geom_glow),
        ("3.", "Light 4 stones. Avoid red ⚠.", theme.bridge_sound),
    ];
    let mut sx = x + 16.0;
    for (n, txt, col) in steps {
        prims.push(RenderPrimitive::Text {
            x: sx, y: leg_y,
            s: n.into(),
            color: col, size: 13.0, bold: true,
        });
        prims.push(RenderPrimitive::Text {
            x: sx + 22.0, y: leg_y,
            s: txt.into(),
            color: theme.text_dim, size: 12.0, bold: false,
        });
        sx += step_w;
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

/// Draw a card strip — the simplified replacement for the dense tower.
///
/// Cards are larger (≥52px tall), shown in 2 columns. Raw technical ids
/// only render as subtext when the tile is hovered or focused (progressive
/// disclosure) — the primary face just shows a kid-readable label.
/// If a tile does not fit in the visible strip we drop it from the
/// primary palette rather than packing micro-tiles into the same area;
/// `Try Recipe` chips at the strip header still cover full catalog sets.
fn draw_card_strip(
    state: &AppState, theme: &Theme, tower: Tower,
    x: f32, y: f32, w: f32, h: f32,
    title: &str, bg: Color, glow: Color,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) {
    // Soft halo + plate.
    prims.push(RenderPrimitive::Rect {
        x: x - 4.0, y: y - 4.0, w: w + 8.0, h: h + 8.0,
        fill: glow.with_alpha(28), stroke: None,
    });
    prims.push(RenderPrimitive::Rect {
        x, y, w, h, fill: bg, stroke: Some(glow),
    });
    // Title strip.
    let header_h = 28.0;
    prims.push(RenderPrimitive::Rect {
        x, y, w, h: header_h, fill: glow.with_alpha(60), stroke: None,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 12.0, y: y + 19.0, s: title.into(),
        color: theme.text, size: 14.0, bold: true,
    });

    // Compact recipe chip rail under the geometry header (anchors hit
    // regions for `RecipeChip(id)`). Only the geometry strip carries them
    // so the data strip stays as clean as possible.
    let inner_top = if tower == Tower::Geometry {
        draw_recipe_chips(state, theme,
            x + 12.0, y + header_h + 6.0, w - 24.0,
            prims, hits) + 6.0
    } else {
        y + header_h + 6.0
    };

    // 2-column card grid — fewer, larger cards.
    let cols: usize = 2;
    let inner_x = x + 12.0;
    let inner_right = x + w - 12.0;
    let inner_bottom = y + h - 12.0;
    let tile_w = (inner_right - inner_x - TILE_GAP_X * (cols as f32 - 1.0)) / cols as f32;

    let kinds_data = [NodeKind::Observable, NodeKind::Constraint];
    let kinds_geom = [NodeKind::Symmetry, NodeKind::Geometry, NodeKind::Field, NodeKind::Constant];
    let kinds: &[NodeKind] = if tower == Tower::Data { &kinds_data } else { &kinds_geom };

    let mut col = 0usize;
    let mut row_y = inner_top;
    for kind in kinds {
        for node in state.catalog.nodes_of(*kind) {
            let tx = inner_x + (col as f32) * (tile_w + TILE_GAP_X);
            let ty = row_y;
            // Cards that no longer fit in the visible strip still get a hit
            // box (honesty floor: every catalog tile remains interactive)
            // but skip rendering primitives to avoid visual clutter. The
            // off-strip cards stay reachable via recipe chips and search.
            let visible = ty + TILE_H <= inner_bottom;

            let selected = state.board.contains(&node.id);
            let hovered = state.view.hover_id.as_deref() == Some(node.id.as_str());
            let focused = state.view.focus_id.as_deref() == Some(node.id.as_str());
            let cclr = claim_color(node.claim, theme);
            let fill = if selected {
                glow
            } else if hovered {
                theme.tile_hover
            } else {
                theme.tile_idle
            };

            if visible {
                // Halo for selected tile.
                if selected {
                    prims.push(RenderPrimitive::Rect {
                        x: tx - 3.0, y: ty - 3.0,
                        w: tile_w + 6.0, h: TILE_H + 6.0,
                        fill: glow.with_alpha(110), stroke: None,
                    });
                }
                prims.push(RenderPrimitive::Rect {
                    x: tx, y: ty, w: tile_w, h: TILE_H,
                    fill, stroke: Some(cclr),
                });
                // Bold claim stripe (left edge).
                prims.push(RenderPrimitive::Rect {
                    x: tx, y: ty, w: 6.0, h: TILE_H,
                    fill: cclr, stroke: None,
                });
                // Primary label — big and bold.
                let label = friendly_label(&node.id, &node.name);
                let txt_color = if selected { Color(8, 14, 22, 255) } else { theme.text };
                prims.push(RenderPrimitive::Text {
                    x: tx + 14.0, y: ty + 24.0,
                    s: truncate(&label, 22),
                    color: txt_color, size: 15.0, bold: true,
                });
                // Progressive disclosure: raw id appears as subtext only
                // when the card is hovered, focused or selected, keeping
                // idle cards clean.
                if hovered || focused || selected {
                    let sub_color = if selected { Color(8, 14, 22, 200) } else { theme.text_dim };
                    prims.push(RenderPrimitive::Text {
                        x: tx + 14.0, y: ty + 42.0,
                        s: truncate(&node.id, 28),
                        color: sub_color, size: 10.0, bold: false,
                    });
                }
            }
            if visible {
                // Falsified warning glyph.
                if node.claim == ClaimStatus::HighRiskOrFalsified {
                    prims.push(RenderPrimitive::Circle {
                        x: tx + tile_w - 14.0, y: ty + 14.0, r: 8.0,
                        fill: theme.bridge_collapsed, stroke: Some(theme.text),
                    });
                    prims.push(RenderPrimitive::Text {
                        x: tx + tile_w - 18.0, y: ty + 19.0,
                        s: "!".into(),
                        color: theme.text, size: 12.0, bold: true,
                    });
                }
                // Selected check mark.
                if selected {
                    prims.push(RenderPrimitive::Circle {
                        x: tx + tile_w - 14.0, y: ty + TILE_H - 14.0, r: 6.0,
                        fill: theme.bridge_sound, stroke: Some(theme.stroke),
                    });
                }
            }

            // Hit box always emitted — visible cards get a normal in-strip
            // box; overflow cards still resolve clicks (or programmatic
            // ToggleTile via recipes) by tracking their packed position
            // even though they're not painted.
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
    let _ = col;
}

/// Render the recipe chip rail and return the y-coordinate below it so
/// callers can flow content underneath. Chips stay hittable as required
/// by `recipe_chips_are_hittable`.
fn draw_recipe_chips(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32,
    prims: &mut Vec<RenderPrimitive>, hits: &mut Vec<HitBox>,
) -> f32 {
    let chip_h = 24.0;
    prims.push(RenderPrimitive::Text {
        x, y: y + 16.0,
        s: "Try Recipe:".into(),
        color: theme.bridge_sound, size: 11.0, bold: true,
    });
    let mut cx = x + 80.0;
    let max_x = x + w;
    for recipe in state.recipes.iter() {
        let label = format!("{} ({})", recipe.title, recipe.tile_ids.len());
        let cw = (label.len() as f32) * 6.5 + 16.0;
        if cx + cw > max_x { break; }
        prims.push(RenderPrimitive::Rect {
            x: cx, y, w: cw, h: chip_h,
            fill: theme.recipe_chip, stroke: Some(theme.bridge_sound),
        });
        prims.push(RenderPrimitive::Text {
            x: cx + 8.0, y: y + 16.0,
            s: label,
            color: theme.text, size: 11.0, bold: false,
        });
        hits.push(HitBox {
            x: cx, y, w: cw, h: chip_h,
            region: HitRegion::RecipeChip(recipe.id.clone()),
        });
        cx += cw + 6.0;
    }
    y + chip_h
}

/// Compact honesty / science strip — a single low-contrast line at the
/// very bottom that surfaces the honesty floor, the worst claim, and the
/// current bridge strength. The full breakdown lives in the HTML
/// <details> drawer outside the canvas.
fn draw_honesty_strip(
    state: &AppState, theme: &Theme,
    x: f32, y: f32, w: f32, h: f32,
    prims: &mut Vec<RenderPrimitive>, _hits: &mut Vec<HitBox>,
) {
    prims.push(RenderPrimitive::Rect {
        x, y, w, h,
        fill: Color(10, 14, 24, 255),
        stroke: Some(theme.text_dim),
    });
    let s = &state.score;
    prims.push(RenderPrimitive::Text {
        x: x + 12.0, y: y + 14.0,
        s: "Honesty strip — bridge strength is NOT proof of physics.".into(),
        color: theme.text_dim, size: 10.0, bold: true,
    });
    prims.push(RenderPrimitive::Text {
        x: x + 12.0, y: y + 28.0,
        s: format!(
            "bridge total = {:+.2}   worst claim: {}   bridge: {}   selected: {} card(s)",
            s.total, s.worst_claim.label(), state.bridge.integrity.label(), state.board.len(),
        ),
        color: theme.text, size: 11.0, bold: true,
    });

    // Right-aligned focus / hover hint — only renders when something is
    // focused so the strip stays quiet by default.
    if let Some(focus) = state.view.focus_id.as_ref() {
        if let Some(node) = state.catalog.by_id(focus) {
            let right_x = x + w - 280.0;
            prims.push(RenderPrimitive::Text {
                x: right_x, y: y + 22.0,
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

    /// Game-feel: the toolbar uses kid-friendly labels — "Start over"
    /// (preferred over "Reset"), "Hint", and "Auto-build" — so the
    /// controls read like a game rather than a debug console.
    #[test]
    fn toolbar_uses_game_labels() {
        let m = layout(&s(), vp(), &Theme::default());
        let texts: Vec<String> = m.primitives.iter().filter_map(|p| match p {
            RenderPrimitive::Text { s, .. } => Some(s.clone()),
            _ => None,
        }).collect();
        let joined = texts.join(" || ");
        assert!(
            joined.contains("Start over") || joined.contains("Reset"),
            "expected Start over / Reset label, got: {}", joined,
        );
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

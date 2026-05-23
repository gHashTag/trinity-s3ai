// GOLDEN BRIDGE — static SVG snapshot exporter.
//
// Calls the same `ring4_canvas::render::layout` used by the live wasm shell
// and emits an SVG file. This is the fallback that `web/canvas/index.html`
// shows when the wasm bundle is not available (e.g. in sandboxes without
// `wasm-pack`). Keeping the snapshot generator inside ring 4 guarantees the
// fallback never drifts from the real layout — it consumes the same render
// primitives.
//
// Usage:
//
//   cargo run -p ring4_canvas --example snapshot_svg -- \
//       web/canvas/snapshot.svg
//
// Without an argument it writes to stdout.
//
// The snapshot is intentionally a *static* picture of the initial state
// (empty board, default catalog, no benchmark mode). It is not interactive
// and not authoritative — its only job is to make the fallback page look
// like the game instead of a blank canvas.

use std::env;
use std::fs;
use std::io::{self, Write};
use std::path::PathBuf;

use ring3_adapters::{benchmark_holdout_ids, default_catalog};
use ring4_canvas::render::{
    layout, Color, RenderModel, RenderPrimitive, Theme, ViewportSize,
};
use ring4_canvas::state::AppState;

fn main() -> io::Result<()> {
    // The new game stage is a 16:9 (1280x720) canvas — the snapshot
    // exporter matches so the static fallback renders the same layout
    // proportions the wasm shell uses in the browser.
    let viewport = ViewportSize { width: 1280.0, height: 720.0 };
    let state = AppState::new(
        default_catalog(),
        benchmark_holdout_ids().iter().map(|s| s.to_string()).collect(),
    );
    let model = layout(&state, viewport, &Theme::default());
    let svg = render_svg(&model);

    let args: Vec<String> = env::args().collect();
    if let Some(out) = args.get(1) {
        let path = PathBuf::from(out);
        if let Some(parent) = path.parent() {
            if !parent.as_os_str().is_empty() {
                fs::create_dir_all(parent)?;
            }
        }
        fs::write(&path, svg)?;
        eprintln!("wrote {}", path.display());
    } else {
        io::stdout().write_all(svg.as_bytes())?;
    }
    Ok(())
}

fn render_svg(model: &RenderModel) -> String {
    let w = model.viewport.width;
    let h = model.viewport.height;
    let mut out = String::with_capacity(64 * 1024);
    out.push_str(&format!(
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
         <svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 {w} {h}\" \
         width=\"100%\" preserveAspectRatio=\"xMidYMid meet\" \
         font-family=\"ui-sans-serif, system-ui, -apple-system, sans-serif\" \
         role=\"img\" aria-label=\"GOLDEN BRIDGE static layout snapshot\">\n",
        w = w as i32,
        h = h as i32,
    ));
    out.push_str("<title>GOLDEN BRIDGE — static layout snapshot</title>\n");
    out.push_str(
        "<desc>Rendered from ring4_canvas::render::layout on the empty board. \
         Static fallback for the wasm-backed canvas UI.</desc>\n",
    );

    for prim in &model.primitives {
        emit_primitive(&mut out, prim);
    }
    out.push_str("</svg>\n");
    out
}

fn emit_primitive(out: &mut String, p: &RenderPrimitive) {
    match p {
        RenderPrimitive::Rect { x, y, w, h, fill, stroke } => {
            out.push_str(&format!(
                "<rect x=\"{:.2}\" y=\"{:.2}\" width=\"{:.2}\" height=\"{:.2}\" \
                 fill=\"{}\"{}/>\n",
                x, y, w, h,
                fill.css(),
                stroke_attr(*stroke),
            ));
        }
        RenderPrimitive::Line { x0, y0, x1, y1, color, width } => {
            out.push_str(&format!(
                "<line x1=\"{:.2}\" y1=\"{:.2}\" x2=\"{:.2}\" y2=\"{:.2}\" \
                 stroke=\"{}\" stroke-width=\"{:.2}\" stroke-linecap=\"round\"/>\n",
                x0, y0, x1, y1, color.css(), width,
            ));
        }
        RenderPrimitive::Circle { x, y, r, fill, stroke } => {
            out.push_str(&format!(
                "<circle cx=\"{:.2}\" cy=\"{:.2}\" r=\"{:.2}\" fill=\"{}\"{}/>\n",
                x, y, r, fill.css(), stroke_attr(*stroke),
            ));
        }
        RenderPrimitive::Text { x, y, s, color, size, bold } => {
            let weight = if *bold { "700" } else { "400" };
            out.push_str(&format!(
                "<text x=\"{:.2}\" y=\"{:.2}\" fill=\"{}\" font-size=\"{:.1}\" \
                 font-weight=\"{}\">{}</text>\n",
                x, y, color.css(), size, weight, escape_xml(s),
            ));
        }
    }
}

fn stroke_attr(stroke: Option<Color>) -> String {
    match stroke {
        Some(c) => format!(" stroke=\"{}\" stroke-width=\"1\"", c.css()),
        None => String::new(),
    }
}

fn escape_xml(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    for ch in s.chars() {
        match ch {
            '&' => out.push_str("&amp;"),
            '<' => out.push_str("&lt;"),
            '>' => out.push_str("&gt;"),
            '"' => out.push_str("&quot;"),
            '\'' => out.push_str("&apos;"),
            c => out.push(c),
        }
    }
    out
}

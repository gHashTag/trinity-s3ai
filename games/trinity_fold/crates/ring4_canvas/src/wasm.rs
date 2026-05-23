// Browser shell: wires the pure render model into Canvas2D and routes DOM
// events through `input::resolve` into the state machine. The entire game
// loop is owned by `TrinityFoldApp` — JavaScript only forwards events.
//
// Build with:
//
//   wasm-pack build games/trinity_fold/crates/ring4_canvas \
//       --target web --features wasm
//
// Then serve `games/trinity_fold/web/canvas/index.html` over HTTP and the
// bootstrap script will pull the generated `ring4_canvas_bg.wasm`.
//
// Limitation: this module is only compiled for `target_arch = "wasm32"`. On
// native targets the lib still compiles fine — all wasm dependencies are
// `optional = true` in Cargo.toml.

#![cfg(all(target_arch = "wasm32", feature = "wasm"))]

use std::cell::RefCell;
use std::rc::Rc;

use ring3_adapters::{benchmark_holdout_ids, default_catalog};
use wasm_bindgen::prelude::*;
use wasm_bindgen::JsCast;
use web_sys::{CanvasRenderingContext2d, HtmlCanvasElement, KeyboardEvent, MouseEvent};

use crate::input::{InputAction, KeyCode, UiEvent, resolve};
use crate::render::{RenderModel, RenderPrimitive, Theme, ViewportSize, layout};
use crate::state::AppState;

#[wasm_bindgen]
pub struct TrinityFoldApp {
    state: Rc<RefCell<AppState>>,
    canvas: HtmlCanvasElement,
    ctx: CanvasRenderingContext2d,
    theme: Theme,
}

#[wasm_bindgen]
impl TrinityFoldApp {
    /// Construct the app, attach it to the given canvas element, and render
    /// the initial frame. Call once from JS; keep the returned handle alive.
    #[wasm_bindgen(constructor)]
    pub fn new(canvas_id: &str) -> Result<TrinityFoldApp, JsValue> {
        console_error_panic_hook::set_once();

        let win = web_sys::window().ok_or_else(|| JsValue::from_str("no window"))?;
        let doc = win
            .document()
            .ok_or_else(|| JsValue::from_str("no document"))?;
        let canvas = doc
            .get_element_by_id(canvas_id)
            .ok_or_else(|| JsValue::from_str(&format!("no canvas `{}`", canvas_id)))?
            .dyn_into::<HtmlCanvasElement>()?;
        let ctx = canvas
            .get_context("2d")?
            .ok_or_else(|| JsValue::from_str("no 2d context"))?
            .dyn_into::<CanvasRenderingContext2d>()?;

        let holdout = benchmark_holdout_ids().iter().map(|s| s.to_string()).collect();
        let state = Rc::new(RefCell::new(AppState::new(default_catalog(), holdout)));
        let theme = Theme::default();

        let app = TrinityFoldApp { state: state.clone(), canvas: canvas.clone(), ctx, theme: theme.clone() };
        app.render();

        // Mouse click.
        {
            let state = state.clone();
            let canvas2 = canvas.clone();
            let theme = theme.clone();
            let cb = Closure::<dyn FnMut(MouseEvent)>::new(move |ev: MouseEvent| {
                let rect = canvas2.get_bounding_client_rect();
                let x = (ev.client_x() as f64 - rect.left()) as f32;
                let y = (ev.client_y() as f64 - rect.top()) as f32;
                let model = layout(
                    &state.borrow(),
                    ViewportSize { width: canvas2.width() as f32, height: canvas2.height() as f32 },
                    &theme,
                );
                if let Some(ev) = resolve(&model, InputAction::Click { x, y }) {
                    if state.borrow_mut().apply(ev) {
                        redraw(&state.borrow(), &canvas2, &theme);
                    }
                }
            });
            canvas
                .add_event_listener_with_callback("click", cb.as_ref().unchecked_ref())?;
            cb.forget();
        }

        // Mouse move (hover).
        {
            let state = state.clone();
            let canvas2 = canvas.clone();
            let theme = theme.clone();
            let cb = Closure::<dyn FnMut(MouseEvent)>::new(move |ev: MouseEvent| {
                let rect = canvas2.get_bounding_client_rect();
                let x = (ev.client_x() as f64 - rect.left()) as f32;
                let y = (ev.client_y() as f64 - rect.top()) as f32;
                let model = layout(
                    &state.borrow(),
                    ViewportSize { width: canvas2.width() as f32, height: canvas2.height() as f32 },
                    &theme,
                );
                if let Some(ev) = resolve(&model, InputAction::Hover { x, y }) {
                    if state.borrow_mut().apply(ev) {
                        redraw(&state.borrow(), &canvas2, &theme);
                    }
                }
            });
            canvas
                .add_event_listener_with_callback("mousemove", cb.as_ref().unchecked_ref())?;
            cb.forget();
        }

        // Keyboard (document-level so the canvas does not need focus).
        {
            let state = state.clone();
            let canvas2 = canvas.clone();
            let theme = theme.clone();
            let cb = Closure::<dyn FnMut(KeyboardEvent)>::new(move |ev: KeyboardEvent| {
                if let Some(k) = KeyCode::from_dom_key(&ev.key()) {
                    let model = layout(
                        &state.borrow(),
                        ViewportSize { width: canvas2.width() as f32, height: canvas2.height() as f32 },
                        &theme,
                    );
                    if let Some(ui_ev) = resolve(&model, InputAction::Key(k)) {
                        if state.borrow_mut().apply(ui_ev) {
                            redraw(&state.borrow(), &canvas2, &theme);
                        }
                    }
                }
            });
            doc.add_event_listener_with_callback("keydown", cb.as_ref().unchecked_ref())?;
            cb.forget();
        }

        Ok(app)
    }

    pub fn render(&self) {
        let model = layout(
            &self.state.borrow(),
            ViewportSize {
                width: self.canvas.width() as f32,
                height: self.canvas.height() as f32,
            },
            &self.theme,
        );
        paint(&self.ctx, &model);

    }

    /// Programmatic hook for headless tests / debug consoles.
    pub fn apply_event(&self, name: &str) -> bool {
        let ev = match name {
            "clear" => UiEvent::ClearBoard,
            "hill_climb" => UiEvent::RunHillClimb,
            "anneal" => UiEvent::RunAnneal { seed: 42, iters: 500 },
            "benchmark" => UiEvent::ToggleBenchmark,
            "undo" => UiEvent::UndoLast,

            _ => return false,
        };
        let changed = self.state.borrow_mut().apply(ev);
        if changed {
            self.render();
        }
        changed
    }
}

fn redraw(state: &AppState, canvas: &HtmlCanvasElement, theme: &Theme) {
    let ctx = canvas
        .get_context("2d")
        .unwrap()
        .unwrap()
        .dyn_into::<CanvasRenderingContext2d>()
        .unwrap();
    let model = layout(
        state,
        ViewportSize { width: canvas.width() as f32, height: canvas.height() as f32 },
        theme,
    );
    paint(&ctx, &model);
}

fn paint(ctx: &CanvasRenderingContext2d, model: &RenderModel) {
    // Clear once via the background rect emitted by `layout`.
    for p in &model.primitives {
        match p {
            RenderPrimitive::Rect { x, y, w, h, fill, stroke } => {
                ctx.set_fill_style_str(&fill.css());
                ctx.fill_rect(*x as f64, *y as f64, *w as f64, *h as f64);
                if let Some(s) = stroke {
                    ctx.set_stroke_style_str(&s.css());

                    ctx.set_line_width(1.0);
                    ctx.stroke_rect(*x as f64, *y as f64, *w as f64, *h as f64);
                }
            }
            RenderPrimitive::Line { x0, y0, x1, y1, color, width } => {
                ctx.set_stroke_style_str(&color.css());

                ctx.set_line_width(*width as f64);
                ctx.begin_path();
                ctx.move_to(*x0 as f64, *y0 as f64);
                ctx.line_to(*x1 as f64, *y1 as f64);
                ctx.stroke();
            }
            RenderPrimitive::Circle { x, y, r, fill, stroke } => {
                ctx.set_fill_style_str(&fill.css());

                ctx.begin_path();
                let _ = ctx.arc(*x as f64, *y as f64, *r as f64, 0.0, std::f64::consts::TAU);
                ctx.fill();
                if let Some(s) = stroke {
                    ctx.set_stroke_style_str(&s.css());

                    ctx.stroke();
                }
            }
            RenderPrimitive::Text { x, y, s, color, size, bold } => {
                ctx.set_fill_style_str(&color.css());

                let weight = if *bold { "700" } else { "400" };
                ctx.set_font(&format!(
                    "{} {}px ui-sans-serif, system-ui, -apple-system, sans-serif",
                    weight, size
                ));
                let _ = ctx.fill_text(s, *x as f64, *y as f64);
            }
        }
    }
}

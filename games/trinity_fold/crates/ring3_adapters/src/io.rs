use ring0_core::Catalog;
use std::fs;
use std::path::Path;

pub fn load_catalog(path: impl AsRef<Path>) -> Result<Catalog, String> {
    let data = fs::read_to_string(path.as_ref())
        .map_err(|e| format!("cannot read {}: {}", path.as_ref().display(), e))?;
    serde_json::from_str(&data).map_err(|e| format!("invalid catalog JSON: {}", e))
}

pub fn save_catalog(catalog: &Catalog, path: impl AsRef<Path>) -> Result<(), String> {
    let s = serde_json::to_string_pretty(catalog).map_err(|e| e.to_string())?;
    fs::write(path.as_ref(), s).map_err(|e| e.to_string())
}

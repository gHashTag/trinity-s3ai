//! JSON Export for Trinity Formula Results

use crate::formulas::{Formula, FormulaClass, tier1_formulas, tier2_formulas, tier3_formulas, tier4_formulas, tier6_formulas};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct FormulaRecord {
    pub id: String,
    pub name: String,
    pub formula: String,
    pub predicted: f64,
    pub experimental: f64,
    pub unit: String,
    pub error_percent: f64,
    pub class: String,
    pub passed: bool,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct TrinityExport {
    pub version: String,
    pub total: usize,
    pub passed: usize,
    pub failed: usize,
    pub formulas: Vec<FormulaRecord>,
}

pub fn export_json() -> String {
    let all: Vec<Formula> = tier1_formulas()
        .into_iter()
        .chain(tier2_formulas().into_iter())
        .chain(tier3_formulas().into_iter())
        .chain(tier4_formulas().into_iter())
        .chain(tier6_formulas().into_iter())
        .collect();

    let mut records = Vec::new();
    let mut passed = 0;
    let mut failed = 0;

    for f in &all {
        let err = if f.experimental == 0.0 {
            0.0
        } else {
            (f.predicted - f.experimental).abs() / f.experimental * 100.0
        };
        let ok = match f.class {
            FormulaClass::SacredGeometry => err < 0.01,
            FormulaClass::Verified => err < 0.1,
            FormulaClass::Pass => err < 1.0,
            _ => true,
        };
        if ok {
            passed += 1;
        } else {
            failed += 1;
        }

        records.push(FormulaRecord {
            id: f.id.to_string(),
            name: f.name.to_string(),
            formula: f.formula.to_string(),
            predicted: f.predicted,
            experimental: f.experimental,
            unit: f.unit.to_string(),
            error_percent: err,
            class: f.class.symbol().to_string(),
            passed: ok,
        });
    }

    let export = TrinityExport {
        version: "5.0.0".to_string(),
        total: all.len(),
        passed,
        failed,
        formulas: records,
    };

    serde_json::to_string_pretty(&export).unwrap_or_else(|_| "{}".to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_export() {
        let json = export_json();
        assert!(json.contains("version"));
        assert!(json.contains("5.0.0"));
    }
}

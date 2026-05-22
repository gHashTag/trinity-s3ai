use criterion::{Criterion, black_box, criterion_group, criterion_main};

use trinity_h4_sm::gauge::GaugeCouplings;
use trinity_h4_sm::h4::generate_h4_roots;
use trinity_h4_sm::higgs::HiggsTrinity;
use trinity_h4_sm::ring::phi_pow;

fn bench_phi_pow(c: &mut Criterion) {
    let mut group = c.benchmark_group("phi_pow");
    for n in 1..=30 {
        group.bench_with_input(format!("n={}", n), &n, |b, &n| {
            b.iter(|| phi_pow(black_box(n)))
        });
    }
    group.finish();
}

fn bench_inv_alpha(c: &mut Criterion) {
    c.bench_function("GaugeCouplings::inv_alpha", |b| {
        b.iter(|| GaugeCouplings::inv_alpha())
    });
}

fn bench_m_higgs(c: &mut Criterion) {
    c.bench_function("HiggsTrinity::m_higgs", |b| {
        b.iter(|| HiggsTrinity::m_higgs())
    });
}

fn bench_generate_h4_roots(c: &mut Criterion) {
    c.bench_function("generate_h4_roots", |b| b.iter(|| generate_h4_roots()));
}

criterion_group!(
    benches,
    bench_phi_pow,
    bench_inv_alpha,
    bench_m_higgs,
    bench_generate_h4_roots
);
criterion_main!(benches);


use criterion::{black_box, criterion_group, criterion_main, Criterion};
use laa_core::SkiRental;

fn ski_rental_benchmark(c: &mut Criterion) {
    let ski_rental = SkiRental::new(100.0);
    c.bench_function("ski_rental_decide", |b| {
        b.iter(|| {
            ski_rental.decide(black_box(1), black_box(120.0), black_box(0.5));
        })
    });
}

criterion_group!(benches, ski_rental_benchmark);
criterion_main!(benches);

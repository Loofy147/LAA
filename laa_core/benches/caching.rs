
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use laa_core::Caching;
use std::collections::HashMap;

fn caching_benchmark(c: &mut Criterion) {
    let mut predictions = HashMap::new();
    predictions.insert(1, 10);
    predictions.insert(2, 5);
    predictions.insert(3, 12);
    let caching = Caching::new(2, predictions);
    let cache = vec![1, 2];
    c.bench_function("caching_decide", |b| {
        b.iter(|| {
            caching.decide(black_box(3), black_box(cache.clone()));
        })
    });
}

criterion_group!(benches, caching_benchmark);
criterion_main!(benches);

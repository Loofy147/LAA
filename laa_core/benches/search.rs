
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use laa_core::Search;

fn search_benchmark(c: &mut Criterion) {
    let search = Search::new(100);
    let values = vec![10, 5, 12, 50, 99];
    let prediction = 4;
    c.bench_function("search_decide", |b| {
        b.iter(|| {
            search.decide(black_box(values.clone()), black_box(prediction));
        })
    });
}

criterion_group!(benches, search_benchmark);
criterion_main!(benches);

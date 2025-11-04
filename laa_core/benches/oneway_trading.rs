
use criterion::{black_box, criterion_group, criterion_main, Criterion};
use laa_core::OnewayTrading;

fn oneway_trading_benchmark(c: &mut Criterion) {
    let oneway_trading = OnewayTrading::new(100.0);
    c.bench_function("oneway_trading_decide", |b| {
        b.iter(|| {
            oneway_trading.decide(black_box(110.0), black_box(120.0), black_box(0.5));
        })
    });
}

criterion_group!(benches, oneway_trading_benchmark);
criterion_main!(benches);


use criterion::{black_box, criterion_group, criterion_main, Criterion};
use laa_core::Scheduling;

fn scheduling_benchmark(c: &mut Criterion) {
    let scheduling = Scheduling::new(2);
    let job_lengths = vec![10, 5, 12];
    let predictions = vec![5, 10, 12];
    c.bench_function("scheduling_decide", |b| {
        b.iter(|| {
            scheduling.decide(black_box(job_lengths.clone()), black_box(predictions.clone()));
        })
    });
}

criterion_group!(benches, scheduling_benchmark);
criterion_main!(benches);

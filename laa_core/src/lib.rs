
use pyo3::prelude::*;
use std::collections::HashMap;

#[pyclass]
pub struct SkiRental {
    buy_cost: f64,
}

#[pymethods]
impl SkiRental {
    #[new]
    pub fn new(buy_cost: f64) -> Self {
        SkiRental { buy_cost }
    }

    pub fn decide(&self, day: u32, prediction: f64, trust: f64) -> bool {
        let threshold = (1.0 - trust) * self.buy_cost + trust * prediction.min(self.buy_cost);
        day as f64 >= threshold
    }
}

#[pyclass]
pub struct Caching {
    cache_size: usize,
    predictions: HashMap<u32, u32>,
}

#[pymethods]
impl Caching {
    #[new]
    pub fn new(cache_size: usize, predictions: HashMap<u32, u32>) -> Self {
        Caching {
            cache_size,
            predictions,
        }
    }

    pub fn decide(&self, item: u32, cache: Vec<u32>) -> (bool, Vec<u32>) {
        let mut new_cache = cache.clone();
        if new_cache.contains(&item) {
            return (true, new_cache);
        }

        if new_cache.len() < self.cache_size {
            new_cache.push(item);
            return (true, new_cache);
        }

        let mut evict_item = 0;
        let mut max_prediction = 0;
        for i in 0..new_cache.len() {
            let prediction = self.predictions.get(&new_cache[i]).unwrap_or(&0);
            if *prediction > max_prediction {
                max_prediction = *prediction;
                evict_item = i;
            }
        }
        new_cache.remove(evict_item);
        new_cache.push(item);
        (false, new_cache)
    }
}

#[pyclass]
pub struct OnewayTrading {
    buy_price: f64,
}

#[pymethods]
impl OnewayTrading {
    #[new]
    pub fn new(buy_price: f64) -> Self {
        OnewayTrading { buy_price }
    }

    pub fn decide(&self, current_price: f64, prediction: f64, trust: f64) -> bool {
        let threshold = (1.0 - trust) * self.buy_price + trust * prediction;
        current_price >= threshold
    }
}

#[pymodule]
fn laa_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<SkiRental>()?;
    m.add_class::<Caching>()?;
    m.add_class::<OnewayTrading>()?;
    Ok(())
}

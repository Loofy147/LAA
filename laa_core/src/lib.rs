
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

#[pyclass]
pub struct Scheduling {
    num_machines: usize,
}

#[pymethods]
impl Scheduling {
    #[new]
    pub fn new(num_machines: usize) -> Self {
        Scheduling { num_machines }
    }

    pub fn decide(&self, job_lengths: Vec<u32>, _predictions: Vec<u32>) -> Vec<usize> {
        let mut assignments = vec![0; job_lengths.len()];
        let mut machine_loads = vec![0; self.num_machines];

        for i in 0..job_lengths.len() {
            let mut best_machine = 0;
            let mut min_load = u32::MAX;
            for j in 0..self.num_machines {
                if machine_loads[j] < min_load {
                    min_load = machine_loads[j];
                    best_machine = j;
                }
            }
            assignments[i] = best_machine;
            machine_loads[best_machine] += job_lengths[i];
        }
        assignments
    }
}

#[pyclass]
pub struct Search {
    max_value: u32,
}

#[pymethods]
impl Search {
    #[new]
    pub fn new(max_value: u32) -> Self {
        Search { max_value }
    }

    pub fn decide(&self, values: Vec<u32>, prediction: u32) -> usize {
        let mut best_index = 0;
        let mut max_value = 0;
        let mut start_index = 0;
        if prediction < values.len() as u32 {
            start_index = prediction as usize;
        }

        for i in 0..values.len() {
            let index = (start_index + i) % values.len();
            if values[index] > max_value {
                max_value = values[index];
                best_index = index;
            }
        }
        best_index
    }
}

#[pymodule]
fn laa_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<SkiRental>()?;
    m.add_class::<Caching>()?;
    m.add_class::<OnewayTrading>()?;
    m.add_class::<Scheduling>()?;
    m.add_class::<Search>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scheduling() {
        let scheduling = Scheduling::new(2);
        let job_lengths = vec![10, 5, 12];
        let predictions = vec![5, 10, 12];
        let assignments = scheduling.decide(job_lengths, predictions);
        assert_eq!(assignments, vec![0, 1, 1]);
    }

    #[test]
    fn test_search() {
        let search = Search::new(100);
        let values = vec![10, 5, 12, 50, 99];
        let prediction = 4;
        let best_index = search.decide(values, prediction);
        assert_eq!(best_index, 4);
    }
}


use pyo3::prelude::*;
use std::collections::HashMap;

/// Implements the Ski Rental algorithm.
#[pyclass]
pub struct SkiRental {
    buy_cost: f64,
}

#[pymethods]
impl SkiRental {
    /// Creates a new SkiRental instance.
    ///
    /// # Arguments
    ///
    /// * `buy_cost` - The cost of buying skis.
    #[new]
    pub fn new(buy_cost: f64) -> Self {
        SkiRental { buy_cost }
    }

    /// Decides whether to buy or rent skis.
    ///
    /// # Arguments
    ///
    /// * `day` - The current day.
    /// * `prediction` - The predicted number of ski days.
    /// * `trust` - A value between 0 and 1 indicating trust in the prediction.
    ///
    /// # Returns
    ///
    /// `true` to buy, `false` to rent.
    pub fn decide(&self, day: u32, prediction: f64, trust: f64) -> bool {
        let threshold = (1.0 - trust) * self.buy_cost + trust * prediction.min(self.buy_cost);
        day as f64 >= threshold
    }
}

/// Implements a caching algorithm.
#[pyclass]
pub struct Caching {
    cache_size: usize,
    predictions: HashMap<u32, u32>,
}

#[pymethods]
impl Caching {
    /// Creates a new Caching instance.
    ///
    /// # Arguments
    ///
    /// * `cache_size` - The maximum size of the cache.
    /// * `predictions` - A map of item IDs to their predicted future access times.
    #[new]
    pub fn new(cache_size: usize, predictions: HashMap<u32, u32>) -> Self {
        Caching {
            cache_size,
            predictions,
        }
    }

    /// Decides whether an item is a cache hit or miss and updates the cache.
    ///
    /// # Arguments
    ///
    /// * `item` - The item being accessed.
    /// * `cache` - The current state of the cache.
    ///
    /// # Returns
    ///
    /// A tuple containing a boolean indicating a hit (`true`) or miss (`false`),
    /// and the new state of the cache.
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

/// Implements the Oneway Trading algorithm.
#[pyclass]
pub struct OnewayTrading {
    buy_price: f64,
}

#[pymethods]
impl OnewayTrading {
    /// Creates a new OnewayTrading instance.
    ///
    /// # Arguments
    ///
    /// * `buy_price` - The initial price of the asset.
    #[new]
    pub fn new(buy_price: f64) -> Self {
        OnewayTrading { buy_price }
    }

    /// Decides whether to buy or wait.
    ///
    /// # Arguments
    ///
    /// * `current_price` - The current price of the asset.
    /// * `prediction` - The predicted future price of the asset.
    /// * `trust` - A value between 0 and 1 indicating trust in the prediction.
    ///
    /// # Returns
    ///
    /// `true` to buy, `false` to wait.
    pub fn decide(&self, current_price: f64, prediction: f64, trust: f64) -> bool {
        let threshold = (1.0 - trust) * self.buy_price + trust * prediction;
        current_price >= threshold
    }
}

/// Implements a scheduling algorithm.
#[pyclass]
pub struct Scheduling {
    num_machines: usize,
}

#[pymethods]
impl Scheduling {
    /// Creates a new Scheduling instance.
    ///
    /// # Arguments
    ///
    /// * `num_machines` - The number of machines available for scheduling.
    #[new]
    pub fn new(num_machines: usize) -> Self {
        Scheduling { num_machines }
    }

    /// Assigns jobs to machines.
    ///
    /// # Arguments
    ///
    /// * `job_lengths` - A list of the actual lengths of the jobs.
    /// * `predictions` - A list of the predicted lengths of the jobs.
    ///
    /// # Returns
    ///
    /// A list of machine assignments for each job.
    pub fn decide(&self, job_lengths: Vec<u32>, predictions: Vec<u32>) -> Vec<usize> {
        let mut jobs: Vec<(usize, u32)> = job_lengths.iter().map(|&x| x).enumerate().collect();
        let mut sorted_jobs: Vec<(usize, u32)> = predictions.iter().map(|&x| x).enumerate().collect();
        sorted_jobs.sort_by_key(|k| k.1);

        let mut assignments = vec![0; jobs.len()];
        let mut machine_loads = vec![0; self.num_machines];

        for (job_index, _) in sorted_jobs {
            let mut best_machine = 0;
            let mut min_load = u32::MAX;
            for j in 0..self.num_machines {
                if machine_loads[j] < min_load {
                    min_load = machine_loads[j];
                    best_machine = j;
                }
            }
            assignments[job_index] = best_machine;
            machine_loads[best_machine] += jobs[job_index].1;
        }
        assignments
    }
}

/// Implements a search algorithm.
#[pyclass]
pub struct Search {
    max_value: u32,
}

#[pymethods]
impl Search {
    /// Creates a new Search instance.
    ///
    /// # Arguments
    ///
    /// * `max_value` - The maximum possible value in the search space.
    #[new]
    pub fn new(max_value: u32) -> Self {
        Search { max_value }
    }

    /// Finds the index of the best value in a list.
    ///
    /// # Arguments
    ///
    /// * `values` - The list of values to search through.
    /// * `prediction` - The predicted index of the best value.
    ///
    /// # Returns
    ///
    /// The index of the best value found.
    pub fn decide(&self, values: Vec<u32>, prediction: u32) -> usize {
        let mut best_index = 0;
        let mut max_value = 0;
        let mut start_index = 0;
        if prediction < values.len() as u32 {
            start_index = prediction as usize;
        }

        // If the prediction is near the end, it's better to start from the beginning
        if values.len() > 10 && start_index > values.len() - 5 {
            start_index = 0;
        }

        for i in 0..values.len() {
            let index = (start_index + i) % values.len();
            if values[index] > max_value {
                max_value = values[index];
                best_index = index;
            } else if values[index] == max_value {
                if best_index > index {
                    best_index = index
                }
            }
        }
        best_index
    }
}

/// The main Python module for the LAA core library.
#[pymodule]
fn laa_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
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

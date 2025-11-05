
use pyo3::prelude::*;
use rand::Rng;
use std::collections::HashMap;

/// Implements the classic Ski Rental problem, a foundational online algorithm.
///
/// This algorithm models a scenario where a person must decide each day whether to rent skis
/// for a fixed daily cost or to buy them outright for a larger fixed cost. The goal is to
/// minimize the total cost over a skiing season of unknown length. This learning-augmented
/// version incorporates a prediction for the total number of ski days to make a more
/// informed decision.
///
/// The algorithm achieves a competitive ratio of 2 in the worst case and approaches 1
/// (optimal) with perfect predictions.
#[pyclass]
pub struct SkiRental {
    buy_cost: f64,
}

#[pymethods]
impl SkiRental {
    /// Creates a new `SkiRental` instance.
    ///
    /// # Arguments
    ///
    /// * `buy_cost` - The total cost of buying skis. This is the threshold against which
    ///                the cumulative rental cost is compared.
    #[new]
    pub fn new(buy_cost: f64) -> Self {
        SkiRental { buy_cost }
    }

    /// Makes the daily decision to either rent or buy skis.
    ///
    /// The decision is based on a threshold that balances the certainty of the traditional
    /// deterministic algorithm with the insight from the machine learning prediction.
    ///
    /// # Arguments
    ///
    /// * `day` - The current day of the skiing season (1-indexed).
    /// * `prediction` - The predicted total number of ski days.
    /// * `trust` - A confidence score in the prediction, typically in the range [0.0, 1.0].
    ///             A value of 0 ignores the prediction, while 1 relies on it completely.
    ///
    /// # Returns
    ///
    /// * `bool` - Returns `true` if the decision is to buy, and `false` to continue renting.
    pub fn decide(&self, day: u32, prediction: f64, trust: f64) -> bool {
        let threshold = (1.0 - trust) * self.buy_cost + trust * prediction.min(self.buy_cost);
        day as f64 >= threshold
    }
}

/// Implements a randomized learning-augmented Ski Rental algorithm.
///
/// This version introduces randomization into the decision-making process to achieve a
/// better competitive ratio in the worst-case scenario compared to its deterministic
/// counterpart. It is approximately 1.58-competitive. The algorithm uses the prediction
/// to influence a probabilistic decision.
#[pyclass]
pub struct RandomizedSkiRental {
    buy_cost: f64,
}

#[pymethods]
impl RandomizedSkiRental {
    /// Creates a new `RandomizedSkiRental` instance.
    ///
    /// # Arguments
    ///
    /// * `buy_cost` - The total cost of buying skis.
    #[new]
    pub fn new(buy_cost: f64) -> Self {
        RandomizedSkiRental { buy_cost }
    }

    /// Makes a probabilistic daily decision to either rent or buy skis.
    ///
    /// # Arguments
    ///
    /// * `day` - The current day of the skiing season (1-indexed).
    /// * `prediction` - The predicted total number of ski days.
    /// * `trust` - A confidence score in the prediction, typically in [0.0, 1.0].
    ///
    /// # Returns
    ///
    /// * `bool` - Returns `true` if the decision is to buy, and `false` to rent.
    pub fn decide(&self, day: u32, prediction: f64, trust: f64) -> bool {
        let rent_cost = day as f64;

        // Clamp the prediction, as any prediction > buy_cost implies the same strategy.
        let effective_prediction = prediction.min(self.buy_cost);

        // The threshold is a blend of the deterministic buy cost and the clamped prediction.
        let threshold = (1.0 - trust) * self.buy_cost + trust * effective_prediction;

        // The probability scales with the rent_cost and the threshold, normalized by buy_cost^2 * e.
        // This ensures that low predictions (and thus low thresholds) lead to a low
        // probability of buying, making the algorithm robust to underestimation.
        let prob = (rent_cost * threshold / (self.buy_cost * self.buy_cost * std::f64::consts::E)).max(0.0).min(1.0);

        let mut rng = rand::thread_rng();
        rng.gen_bool(prob)
    }
}

/// Implements a learning-augmented caching algorithm.
///
/// This algorithm manages a cache of a fixed size. When an item is accessed, it must
/// decide whether to keep or evict items in the cache. This implementation uses predictions
/// about the next time an item will be accessed to make smarter eviction choices than

/// traditional algorithms like LRU (Least Recently Used).
#[pyclass]
pub struct Caching {
    cache_size: usize,
    predictions: HashMap<u32, u32>,
}

#[pymethods]
impl Caching {
    /// Creates a new `Caching` instance.
    ///
    /// # Arguments
    ///
    /// * `cache_size` - The maximum number of items the cache can hold.
    /// * `predictions` - A map where keys are item IDs and values are the predicted
    ///                   time of the next access. Lower values indicate sooner access.
    #[new]
    pub fn new(cache_size: usize, predictions: HashMap<u32, u32>) -> Self {
        Caching {
            cache_size,
            predictions,
        }
    }

    /// Processes an item access and updates the cache state.
    ///
    /// If the item is already in the cache, it's a "hit". If not, it's a "miss".
    /// If the cache is full on a miss, another item is evicted based on the predictions
    /// (item with the latest predicted next access time is evicted).
    ///
    /// # Arguments
    ///
    /// * `item` - The unique identifier of the item being accessed.
    /// * `cache` - A `Vec<u32>` representing the current items in the cache.
    ///
    /// # Returns
    ///
    /// A tuple `(bool, Vec<u32>)`:
    /// * `_ .0` (bool): `true` for a cache hit, `false` for a miss.
    /// * `_ .1` (Vec<u32>): The new state of the cache after the access.
    pub fn decide(&self, item: u32, cache: Vec<u32>) -> (bool, Vec<u32>) {
        let mut new_cache = cache.clone();
        if new_cache.contains(&item) {
            return (true, new_cache);
        }

        if new_cache.len() < self.cache_size {
            new_cache.push(item);
            return (true, new_cache);
        }

        let mut evict_item_index = 0;
        let mut max_prediction = 0;
        for i in 0..new_cache.len() {
            let prediction = self.predictions.get(&new_cache[i]).unwrap_or(&u32::MAX);
            if *prediction > max_prediction {
                max_prediction = *prediction;
                evict_item_index = i;
            }
        }
        new_cache.remove(evict_item_index);
        new_cache.push(item);
        (false, new_cache)
    }
}

/// Implements a learning-augmented Oneway Trading algorithm.
///
/// This algorithm addresses the problem of converting an initial amount of one asset
/// into another by choosing the best time to execute the trade. The goal is to maximize
/// the amount of the target asset obtained. This version uses a price prediction to
/// decide when to trade.
#[pyclass]
pub struct OnewayTrading {
    buy_price: f64,
}

#[pymethods]
impl OnewayTrading {
    /// Creates a new `OnewayTrading` instance.
    ///
    /// # Arguments
    ///
    /// * `buy_price` - The initial price of the asset, used as a reference for the
    ///                 deterministic part of the algorithm.
    #[new]
    pub fn new(buy_price: f64) -> Self {
        OnewayTrading { buy_price }
    }

    /// Decides whether to execute the trade or to wait.
    ///
    /// The decision is based on a threshold that blends the initial price with the
    /// predicted future price, weighted by the trust parameter.
    ///
    /// # Arguments
    ///
    /// * `current_price` - The current market price of the asset.
    /// * `prediction` - The predicted future price of the asset.
    /// * `trust` - A confidence score in the prediction, typically in [0.0, 1.0].
    ///
    /// # Returns
    ///
    /// * `bool` - Returns `true` to execute the trade, `false` to wait.
    pub fn decide(&self, current_price: f64, prediction: f64, trust: f64) -> bool {
        let threshold = (1.0 - trust) * self.buy_price + trust * prediction;
        current_price >= threshold
    }
}

/// Implements a learning-augmented scheduling algorithm (makespan minimization).
///
/// This algorithm assigns a set of jobs to a fixed number of machines with the goal
/// of minimizing the makespan, which is the total time until the last job completes.
/// It uses predictions of job lengths to sort them, aiming to schedule shorter jobs
/// first (a variant of the Shortest Processing Time heuristic).
#[pyclass]
pub struct Scheduling {
    num_machines: usize,
}

#[pymethods]
impl Scheduling {
    /// Creates a new `Scheduling` instance.
    ///
    /// # Arguments
    ///
    /// * `num_machines` - The number of identical machines available for processing jobs.
    #[new]
    pub fn new(num_machines: usize) -> Self {
        Scheduling { num_machines }
    }

    /// Assigns a list of jobs to the available machines.
    ///
    /// This method sorts jobs based on their predicted lengths and then assigns each
    /// job to the machine that will become free earliest.
    ///
    /// # Arguments
    ///
    /// * `job_lengths` - A `Vec<u32>` containing the true, actual lengths of the jobs.
    /// * `predictions` - A `Vec<u32>` containing the predicted lengths of the jobs.
    ///                   The order of predictions must correspond to the order of `job_lengths`.
    ///
    /// # Returns
    ///
    /// * `Vec<usize>` - A vector where the element at index `i` is the machine ID
    ///                  (0 to `num_machines - 1`) assigned to job `i`.
    pub fn decide(&self, job_lengths: Vec<u32>, predictions: Vec<u32>) -> Vec<usize> {
        let jobs: Vec<(usize, u32)> = job_lengths.iter().map(|&x| x).enumerate().collect();
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

/// Implements a learning-augmented search algorithm.
///
/// This algorithm finds the maximum value in a list. It uses a prediction for the
/// index of the maximum value as a starting point for its search, which can improve
/// performance in certain online or resource-constrained scenarios.
#[pyclass]
pub struct Search {
    #[allow(dead_code)]
    max_value: u32,
}

#[pymethods]
impl Search {
    /// Creates a new `Search` instance.
    ///
    /// # Arguments
    ///
    /// * `max_value` - The theoretical maximum possible value in the search space.
    ///                 (Note: This is not currently used in the `decide` method but
    ///                 is part of the class structure for future extensions).
    #[new]
    pub fn new(max_value: u32) -> Self {
        Search { max_value }
    }

    /// Finds the index of the maximum value in a list.
    ///
    /// It starts its search from the predicted index and wraps around the list,
    /// which can be advantageous if the search can be terminated early.
    ///
    /// # Arguments
    ///
    /// * `values` - The `Vec<u32>` of values to search through.
    /// * `prediction` - The predicted index of the maximum value.
    ///
    /// # Returns
    ///
    /// * `usize` - The index of the first occurrence of the maximum value found.
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

/// Defines the Python module for the Learning-Augmented Algorithms core library.
///
/// This function exposes the Rust implementations of the LAA classes (`SkiRental`,
/// `Caching`, `OnewayTrading`, `Scheduling`, `Search`) to Python, allowing them
/// to be imported and used seamlessly.
#[pymodule]
fn laa_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<SkiRental>()?;
    m.add_class::<RandomizedSkiRental>()?;
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
    fn test_ski_rental_no_trust() {
        let ski_rental = SkiRental::new(100.0);
        assert_eq!(ski_rental.decide(99, 10.0, 0.0), false);
        assert_eq!(ski_rental.decide(100, 10.0, 0.0), true);
    }

    #[test]
    fn test_ski_rental_full_trust_good_prediction() {
        let ski_rental = SkiRental::new(100.0);
        assert_eq!(ski_rental.decide(24, 25.0, 1.0), false);
        assert_eq!(ski_rental.decide(25, 25.0, 1.0), true);
    }

    #[test]
    fn test_ski_rental_full_trust_bad_prediction() {
        let ski_rental = SkiRental::new(100.0);
        // Prediction is 120, but it's clamped at buy_cost (100), so threshold is 100.
        assert_eq!(ski_rental.decide(99, 120.0, 1.0), false);
        assert_eq!(ski_rental.decide(100, 120.0, 1.0), true);
    }

    #[test]
    fn test_caching_hit() {
        let caching = Caching::new(3, HashMap::new());
        let cache = vec![1, 2, 3];
        let (hit, new_cache) = caching.decide(2, cache.clone());
        assert_eq!(hit, true);
        assert_eq!(new_cache, cache);
    }

    #[test]
    fn test_caching_miss_no_eviction() {
        let caching = Caching::new(3, HashMap::new());
        let cache = vec![1, 2];
        let (hit, new_cache) = caching.decide(3, cache.clone());
        assert_eq!(hit, true);
        assert_eq!(new_cache, vec![1, 2, 3]);
    }

    #[test]
    fn test_caching_miss_with_eviction() {
        let mut predictions = HashMap::new();
        predictions.insert(1, 10);
        predictions.insert(2, 5);
        predictions.insert(3, 15);
        let caching = Caching::new(3, predictions);
        let cache = vec![1, 2, 3];
        let (hit, new_cache) = caching.decide(4, cache.clone());
        assert_eq!(hit, false);
        assert_eq!(new_cache, vec![1, 2, 4]);
    }

    #[test]
    fn test_oneway_trading_no_trust() {
        let trading = OnewayTrading::new(100.0);
        assert_eq!(trading.decide(99.0, 120.0, 0.0), false);
        assert_eq!(trading.decide(100.0, 120.0, 0.0), true);
    }

    #[test]
    fn test_oneway_trading_full_trust() {
        let trading = OnewayTrading::new(100.0);
        assert_eq!(trading.decide(119.0, 120.0, 1.0), false);
        assert_eq!(trading.decide(120.0, 120.0, 1.0), true);
    }

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

    #[test]
    fn test_randomized_ski_rental_statistical() {
        let buy_cost = 100.0;
        let num_simulations = 10000;
        let mut total_ratio = 0.0;
        let mut rng = rand::thread_rng();

        for _ in 0..num_simulations {
            let ski_days = rng.gen_range(1..150);
            // Add more realistic noise to the prediction
            let noise = rng.gen_range(0.7..1.3);
            let prediction = (ski_days as f64 * noise).max(1.0);
            let trust = 0.8;
            let rental = RandomizedSkiRental::new(buy_cost);

            let mut alg_cost = ski_days as f64; // Default cost is renting all days
            for day in 1..=ski_days {
                if rental.decide(day, prediction, trust) {
                    alg_cost = (day - 1) as f64 + buy_cost;
                    break; // Decision is final
                }
            }

            let optimal_cost = (ski_days as f64).min(buy_cost);
            total_ratio += alg_cost / optimal_cost;
        }

        let avg_ratio = total_ratio / num_simulations as f64;
        assert!(avg_ratio < 1.7, "Average ratio was {}", avg_ratio);
    }
}

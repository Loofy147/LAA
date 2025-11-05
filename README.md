# Learning-Augmented Algorithms (LAA) Core Library & Tools

This repository contains a high-performance Rust-based core library of Learning-Augmented Algorithms (LAA) with Python bindings, alongside a suite of Python tools for analyzing and deploying them.

## Project Purpose

The goal of this project is to provide a practical and robust implementation of Learning-Augmented Algorithms. These algorithms combine the theoretical worst-case guarantees of classical algorithms with the real-world performance benefits of machine learning predictions. This library allows developers to build systems that are both fast on average (when predictions are good) and resilient to failure (when predictions are bad).

## Getting Started

To get started with the LAA library and tools, you'll need to set up your environment and build the Rust core.

### Prerequisites

*   Python 3.8+
*   Rust (latest stable version, install via [rustup](https://rustup.rs/))
*   `pip` and `venv` for Python package management

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/laa-venture.git
    cd laa-venture
    ```

2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install numpy
    ```

4.  **Build the Rust core library:**
    This command compiles the Rust code into a Python module.
    ```bash
    cd laa_core
    cargo build --release
    cd ..
    ```

5.  **Copy the compiled library to the root directory:**
    This makes the `laa_core` module importable by Python scripts in the root of the project.
    ```bash
    cp laa_core/target/release/liblaa_core.so ./laa_core.so
    ```

6.  **Set the `PYTHONPATH`:**
    This allows Python to find the modules in the `laa_tools` directory.
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    ```

### Running Tests

To verify that everything is set up correctly, run the Rust tests:
```bash
cd laa_core && cargo test && cd ..
```

## Core Algorithms (`laa_core`)

The core of the project is a Rust library with Python bindings that provides several LAA implementations.

### Usage from Python

After building and copying the library, you can import and use the algorithms in your Python code:

```python
from laa_core import SkiRental, RandomizedSkiRental, Caching, OnewayTrading, Scheduling, Search

# Example: Using the deterministic SkiRental algorithm
ski_rental = SkiRental(buy_cost=100.0)
decision = ski_rental.decide(day=25, prediction=30.0, trust=0.8)
print(f"Should buy skis? {decision}")

# Example: Using the randomized SkiRental algorithm
rand_ski_rental = RandomizedSkiRental(buy_cost=100.0)
decision = rand_ski_rental.decide(day=25, prediction=30.0, trust=0.8)
print(f"Should buy skis (randomized)? {decision}")
```

### Implemented Algorithms

*   **`SkiRental`**: The classic online problem of deciding when to buy skis versus continuing to rent. This version uses a prediction of the total number of ski days.
*   **`RandomizedSkiRental`**: A probabilistic version of the Ski Rental algorithm that can achieve a better worst-case competitive ratio.
*   **`Caching`**: A learning-augmented caching algorithm that uses predictions of the next access time for each item to make smarter eviction decisions.
*   **`OnewayTrading`**: An algorithm for deciding the best time to trade one asset for another, based on a prediction of the future price.
*   **`Scheduling`**: An algorithm for scheduling jobs on multiple machines to minimize the makespan, using predictions of job lengths.
*   **`Search`**: A simple algorithm for finding the maximum value in a list, using a prediction of the index of the maximum value as a starting point.

## Python Tools (`laa_tools`)

This project also includes a set of Python tools for working with LAA.

### `BrittlenessDetector`

Analyzes how sensitive an algorithm is to noisy predictions.

```python
from laa_tools.brittleness_detector import BrittlenessDetector
# (See laa_tools/brittleness_detector.py for a complete usage example)
```

### `UQPredictionAdapter`

Wraps a scikit-learn model to provide uncertainty quantification for its predictions using conformal prediction.

```python
from laa_tools.uq_prediction_adapter import UQPredictionAdapter
# (See laa_tools/uq_prediction_adapter.py for a complete usage example)
```

## Key Documents

*   **[Technical Deep Dive & Gap Analysis](laa_technical_deepdive.md)**: A detailed analysis of the technical gaps in the LAA space.
*   **[Gaps & Improvements Report](gaps-reports.md)**: A report on the new gaps identified and filled during the latest round of improvements.
*   **[Project Overview](project_overview.md)**: The original high-level project overview.

# Learning-Augmented Algorithms Venture

This repository contains the business plan, technical roadmap, and supporting documentation for a new venture focused on Learning-Augmented Algorithms (LAA).

## Project Overview

The core of this project is a business plan to commercialize recent breakthroughs in LAA. The venture will create a platform that allows companies to integrate machine learning predictions into their algorithms while maintaining worst-case performance guarantees.

## Getting Started

To get started with the LAA platform, you'll need to set up the backend services and familiarize yourself with the available tools and SDKs.

### Prerequisites

- Python 3.8+
- Rust (latest stable version)
- An API key for the LAA Platform

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/laa-venture.git
    cd laa-venture
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r api/requirements.txt
    ```

3.  **Build the Rust core:**
    ```bash
    cd laa_core
    cargo build --release
    cd ..
    ```

4.  **Install the SDK:**
    ```bash
    cd sdk
    pip install .
    cd ..
    ```

### Running the API

To start the FastAPI server, run the following command from the root directory:
```bash
uvicorn api.main:app --reload
```

## Usage

### API

The API provides several endpoints for applying learning-augmented algorithms to common problems. You can interact with the API directly or use the Python SDK.

**Example: Ski Rental Decision**
```bash
curl -X POST "http://127.0.0.1:8000/algorithms/ski-rental/decide" \
-H "Content-Type: application/json" \
-d '{
    "buy_cost": 100,
    "current_day": 10,
    "prediction_days": 25,
    "trust": 0.8
}'
```

### Python SDK

The `laa_sdk` provides a convenient way to interact with the API from your Python applications.

**Example: Ski Rental Decision with the SDK**
```python
from laa_sdk import LAAClient

client = LAAClient(api_url="http://127.0.0.1:8000", api_key="your-api-key")

decision = client.ski_rental_decide(
    buy_cost=100,
    current_day=10,
    prediction_days=25,
    trust=0.8
)

print(decision)
```

## Key Documents

*   **[Project Overview](project_overview.md)**: A unified document that synthesizes the business strategy, 90-day launch plan, technical roadmap, and a primer on LAA.

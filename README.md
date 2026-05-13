# Container Relocation Problem (CRP) Solver

This repository provides a modular, Python-based solver for the **Container Relocation Problem (CRP)**. The project benchmarks different search algorithms—specifically a baseline Greedy approach and A* search with varying heuristics—evaluating their computational efficiency and solution quality.

## 🌟 Features

* **Modular Architecture**: The environment physics, search algorithms, heuristic functions, and visualization are highly decoupled. This makes the codebase clean and easy to extend for secondary development (e.g., integrating Reinforcement Learning).
* **Algorithm Benchmarking**: Built-in head-to-head comparisons between:
  * Baseline Greedy Algorithm
  * Classic A* Algorithm (Weak heuristic)
  * Feature-Guided A* Algorithm (Custom multidimensional heuristic)
* **Customizable Heuristics**: Fine-tune the A* search by adjusting weights for three core spatial features:
  1. *Direct Obstruction*: The number of containers blocking the current target.
  2. *Global Priority Inversion*: Severe states where containers needed later are placed on top of containers needed earlier.
  3. *Space Scarcity*: Penalties for nearly full bays that restrict future movements.
* **Automated Evaluation & Visualization**: Includes a pure-random scenario stress test that automatically plots performance metrics (relocation counts, computation time, average relocation rates) using `matplotlib`.

## 📂 Project Structure

* `src/config.py`: Core configuration for heuristic weighting parameters.
* `src/environment.py`: Physical environment rules and state management.
* `src/heuristics.py`: Classic and custom heuristic evaluation functions.
* `src/algorithms.py`: Decoupled search algorithms (Greedy, A*).
* `src/visualization.py`: Matplotlib-based evaluation charting.
* `main.py`: Main entry point for initializing parameters, running benchmarks, and displaying results.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system.

### 1. Installation

Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/whmxwl/crp_solver.git](https://github.com/whmxwl/crp_solver.git)
cd crp_solver
pip install -r requirements.txt
```

### 2. Running the Benchmark

Execute the main script to generate random port/yard scenarios and run the algorithms against each other:

```bash
python main.py
```

Upon completion, a comprehensive `matplotlib` dashboard will appear, displaying algorithm performance comparisons across multiple dimensions.

## ⚙️ Configuration

You can easily experiment with the feature-guided A* algorithm's behavior by adjusting the heuristic weights. Open `src/config.py` and modify the following parameters:

* `A_WEIGHT`: Weight for Direct Obstructions (Default: ~1.0).
* `B_WEIGHT`: Weight for Priority Inversions (Recommended to be 1.0, avoiding over-penalization).
* `C_WEIGHT`: Weight for Space Scarcity (Default: ~0.5).

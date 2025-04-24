# Risk-Aware Package Delivery Planner

This repository contains implementations for solving the **Risk-Aware Single-Agent Package Delivery (RSPD)** problem, as described in the paper ["Planning for Package Deliveries in Risky Environments Over Multiple Epochs"](https://ieeexplore.ieee.org/document/9867854) by Wilson, Hudack, and Sundaram. The solutions address both finite-horizon and infinite-horizon scenarios where a dispatcher must maximize expected reward while accounting for the risk of agent failure.

## Features

- **Finite Horizon Solution**: Optimal package delivery plan for a fixed number of epochs (`finite-horizon-problem.py`)
- **Infinite Horizon Solution**: Optimal stationary policy for indefinite operation (`infinite-horizon-problem.py`)
- **Interactive GUI**: Visual interface for parameter input and result visualization (`GUI.py`)
- **Mathematical Foundation**: Implements the reward-to-risk ratio optimization from the original paper


## Requirements:
- Python 3.x
- numpy
- matplotlib
- tkinter

## How to Run:

1. Command Line:
   For finite horizon:
   ```bash
   python finite-horizon-problem.py
   ```
   
   For infinite horizon:
   ```bash
   python infinite-horizon-problem.py
   ```

3. Graphical Interface:
   ```bash
   python GUI.py
   ```

## Key Algorithms:

Finite Horizon:
- Sorts packages by reward-to-risk ratio: γ = (r*p²)/(1-p²)
- Uses backward induction from final epoch
- O(n log n) time complexity

Infinite Horizon:
- Finds package with maximum γ > replacement cost
- Implements stationary optimal policy
- O(n) time complexity

## Example Input:
```bash
packages = [
    (10, 0.9),  # (reward, probability)
    (8, 0.8),
    (15, 0.7),
    (6, 0.6),
    (20, 0.5)
]
K = 5 epochs
replacement_cost = 3
```

## Expected Output:
```bash
Finite Horizon Plan:
Epoch 1: [20, 15, 10]
Epoch 2: [20, 15]
Epoch 3: [20]
Total Expected Reward: 42.17

Infinite Horizon:
Optimal Package: Reward=20, Prob=0.5
Expected Reward per Epoch: 3.67
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
   

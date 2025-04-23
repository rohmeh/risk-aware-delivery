#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

def calculate_reward_to_risk_ratio(package):
    r, p = package
    return (r * p**2) / (1 - p**2)

def optimal_finite_horizon_solution(packages, K, replacement_cost):
    """
    Optimal solution for the finite horizon Risk-Aware Single-Agent Package Delivery problem.

    packages: list of tuples (reward, probability_of_success)
    K: number of epochs
    replacement_cost: cost of replacing the agent

    Returns:
    optimal_plan: list of package delivery plans for each epoch
    total_expected_reward: total expected reward across all epochs
    """
    n = len(packages)

    ratios = [(i, calculate_reward_to_risk_ratio(packages[i])) for i in range(n)]

    sorted_ratios = sorted(ratios, key=lambda x: x[1], reverse=True)

    V = [0] * (K + 1)  
    C = [[] for _ in range(K)] 

    # Step 4: Work backwards from epoch K to 1
    for h in range(K-1, -1, -1):
        included_packages = []
        cumulative_probability = 1

        for idx, ratio in sorted_ratios:
            r, p = packages[idx]

            if ratio > replacement_cost + V[h+1]:
                included_packages.append(idx)

                cumulative_probability *= p**2
                
                V[h] += r * cumulative_probability

                V[h] -= replacement_cost * (1 - cumulative_probability)
            else:
                break  

        C[h] = [packages[i] for i in included_packages]

        V[h] += cumulative_probability * V[h+1]

    optimal_plan = C

    total_expected_reward = V[0]

    return optimal_plan, total_expected_reward

if __name__ == "__main__":
    packages = [
        (10, 0.9),  # (reward, probability_of_success)
        (8, 0.8),
        (15, 0.7),
        (6, 0.6),
        (20, 0.5)
    ]
    K = 5 
    replacement_cost = 3 

    optimal_plan, total_reward = optimal_finite_horizon_solution(packages, K, replacement_cost)

    print("Optimal Package Delivery Plan:")
    for epoch, plan in enumerate(optimal_plan):
        print(f"Epoch {epoch+1}: {[p[0] for p in plan]}")

    print(f"\nTotal Expected Reward: {total_reward}")


# In[ ]:





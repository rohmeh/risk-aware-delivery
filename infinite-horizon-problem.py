def calculate_reward_to_risk_ratio(package):
    """
    Calculate the reward-to-risk ratio for a package.
    package: tuple of (reward, probability_of_success)
    """
    r, p = package
    return (r * p**2) / (1 - p**2)

def optimal_infinite_horizon_solution(packages, replacement_cost):
    """
    Optimal solution for the infinite horizon Risk-Aware Single-Agent Package Delivery problem.

    packages: list of tuples (reward, probability_of_success)
    replacement_cost: cost of replacing the agent

    Returns:
    optimal_package: the package with the highest reward-to-risk ratio that satisfies the condition
    expected_reward: the expected reward per epoch
    """
    n = len(packages)

    ratios = [(i, calculate_reward_to_risk_ratio(packages[i])) for i in range(n)]

    max_ratio = -float('inf')
    optimal_package = None

    for idx, ratio in ratios:
        if ratio > replacement_cost:
            if ratio > max_ratio:
                max_ratio = ratio
                optimal_package = packages[idx]

    if optimal_package:
        r_max, p_max = optimal_package
        expected_reward = (r_max * p_max**2 - replacement_cost * (1 - p_max**2)) / (1 - p_max**2)
    else:
        expected_reward = 0

    return optimal_package, expected_reward

if __name__ == "__main__":
    packages = [
        (10, 0.9),  # (reward, probability_of_success)
        (8, 0.8),
        (15, 0.7),
        (6, 0.6),
        (20, 0.5)
    ]
    K = 5  # Number of epochs
    replacement_cost = 3
    optimal_package, expected_reward = optimal_infinite_horizon_solution(packages, replacement_cost)

    if optimal_package:
        print(f"Optimal Package to Deliver: {optimal_package[0]} (Reward: {optimal_package[0]}, Probability: {optimal_package[1]:.2f})")
    else:
        print("No package satisfies the condition for infinite horizon delivery.")

    print(f"Expected Reward per Epoch: {expected_reward:.2f}")

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_reward_to_risk_ratio(package):
    r, p = package
    return (r * p**2) / (1 - p**2)

def optimal_finite_horizon_solution(packages, K, replacement_cost):
    n = len(packages)
    ratios = [(i, calculate_reward_to_risk_ratio(packages[i])) for i in range(n)]
    sorted_ratios = sorted(ratios, key=lambda x: x[1], reverse=True)
    
    V = [0] * (K + 1) 
    C = [[] for _ in range(K)]  
    
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
    
    return C, V[0]

def optimal_infinite_horizon_solution(packages, replacement_cost):
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

# GUI Functions
def visualize_results():
    try:
        # Get inputs from the GUI
        num_packages = int(num_packages_entry.get())
        replacement_cost = float(replacement_cost_entry.get())
        K = int(epochs_entry.get())

        # Parse package data
        packages = []
        for i in range(num_packages):
            reward = float(package_rewards[i].get())
            prob_success = float(package_probs[i].get())
            packages.append((reward, prob_success))

        # Solve finite horizon problem
        finite_plan, finite_reward = optimal_finite_horizon_solution(packages, K, replacement_cost)

        # Solve infinite horizon problem
        infinite_package, infinite_reward = optimal_infinite_horizon_solution(packages, replacement_cost)

        # Display results in the text box
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Finite Horizon Plan:\n")
        for epoch, plan in enumerate(finite_plan):
            result_text.insert(tk.END, f"Epoch {epoch+1}: {[p[0] for p in plan]}\n")
        result_text.insert(tk.END, f"\nTotal Expected Reward (Finite): {finite_reward:.2f}\n")

        result_text.insert(tk.END, "\nInfinite Horizon Plan:\n")
        if infinite_package:
            result_text.insert(tk.END, f"Optimal Package: {infinite_package[0]} (Reward: {infinite_package[0]}, Probability: {infinite_package[1]:.2f})\n")
        else:
            result_text.insert(tk.END, "No package satisfies the condition for infinite horizon delivery.\n")
        result_text.insert(tk.END, f"Expected Reward per Epoch (Infinite): {infinite_reward:.2f}\n")

        # Visualize results
        visualize_rewards(finite_plan, finite_reward, infinite_package, infinite_reward)

    except Exception as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")

def visualize_rewards(finite_plan, finite_reward, infinite_package, infinite_reward):
    # Create a new figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot finite horizon rewards
    finite_rewards = [sum(p[0] for p in epoch) for epoch in finite_plan]
    ax.plot(range(1, len(finite_rewards) + 1), finite_rewards, label="Finite Horizon", marker='o')

    # Plot infinite horizon rewards
    if infinite_package:
        infinite_rewards = [infinite_reward] * len(finite_rewards)
        ax.plot(range(1, len(infinite_rewards) + 1), infinite_rewards, label="Infinite Horizon", linestyle='--', marker='x')

    # Add labels and legend
    ax.set_title("Expected Rewards Over Epochs")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Expected Reward")
    ax.legend()
    ax.grid(True)

    # Embed the plot into the GUI
    canvas = FigureCanvasTkAgg(fig, master=visualization_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def update_package_entries():
    # Clear previous widgets in the package frame
    for widget in package_frame.winfo_children():
        widget.destroy()

    # Get the number of packages
    num_packages = int(num_packages_entry.get())

    # Dynamically create entry fields for rewards and probabilities
    global package_rewards, package_probs
    package_rewards = []
    package_probs = []

    for i in range(num_packages):
        ttk.Label(package_frame, text=f"Package {i+1} Reward:").grid(row=i, column=0, sticky="w")
        reward_entry = ttk.Entry(package_frame)
        reward_entry.grid(row=i, column=1, sticky="ew")
        package_rewards.append(reward_entry)

        ttk.Label(package_frame, text=f"Package {i+1} Probability:").grid(row=i, column=2, sticky="w")
        prob_entry = ttk.Entry(package_frame)
        prob_entry.grid(row=i, column=3, sticky="ew")
        package_probs.append(prob_entry)

root = tk.Tk()
root.title("Package Delivery Planner")

input_frame = ttk.Frame(root, padding="10")
input_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(input_frame, text="Number of Packages:").grid(row=0, column=0, sticky="w")
num_packages_entry = ttk.Entry(input_frame)
num_packages_entry.grid(row=0, column=1, sticky="ew")

ttk.Label(input_frame, text="Replacement Cost:").grid(row=1, column=0, sticky="w")
replacement_cost_entry = ttk.Entry(input_frame)
replacement_cost_entry.grid(row=1, column=1, sticky="ew")

ttk.Label(input_frame, text="Number of Epochs:").grid(row=2, column=0, sticky="w")
epochs_entry = ttk.Entry(input_frame)
epochs_entry.grid(row=2, column=1, sticky="ew")

package_rewards = []
package_probs = []

package_frame = ttk.Frame(input_frame, padding="10")
package_frame.grid(row=3, column=0, columnspan=4, sticky="ew")

update_button = ttk.Button(input_frame, text="Update Package Entries", command=update_package_entries)
update_button.grid(row=4, column=0, columnspan=4, pady=10)

visualization_frame = ttk.Frame(root, padding="10")
visualization_frame.pack(fill=tk.BOTH, expand=True)

result_text = tk.Text(root, height=10, width=80)
result_text.pack(fill=tk.BOTH, expand=True)
run_button = ttk.Button(root, text="Run Simulation", command=visualize_results)
run_button.pack(pady=10)

root.mainloop()

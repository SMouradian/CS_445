# Homework - 1
# Professor - Shamik Sengupta
# Author - Samuel Mouradian
# Due Date - 02 / 18 / 2026



import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict



# ----------------------------------------
# ---------   INPUT PARAMETERS   ---------
# ----------------------------------------
p_values = [0.2, 0.4, 0.5, 0.6, 0.8]  # Packet Marking Probabilities
x = [10, 100, 1000]  # Attacker's rate of pumping packets
runs = 100  # Runs that will occur within the simulations
normal_rate = 1  # Normal user's rate of pumping packets



# ----------------------------------------
# -------------   TOPOLOGY   -------------
# ----------------------------------------
def create_topology():
    total_routers = random.randint(10, 20)
    num_branches = random.randint(3, 5)
    branches = [[] for _ in range(num_branches)]
    router_id = 1

    remaining = total_routers  # Distribute attack across all available routers within simulation

    for i in range(num_branches):
        # Checks to ensure there is (at the very least) one router per branch
        if i == num_branches - 1:
            branch_size = remaining
        else:
            max_routers_remaining  = remaining - (num_branches - i - 1)
            branch_size = random.randint(1, max_routers_remaining)

        # Initialize hop constraint
        branch_size = min(branch_size, 15)

        for _ in range(branch_size):
            branches[i].append(router_id)
            router_id += 1
        
        remaining -= branch_size
    
    return branches



# ----------------------------------------
# ----------   NODE  SAMPLING   ----------
# ----------------------------------------
def node_sampling(branches, attackers, p, x):
    # Set count for how many times each branch is marked
    observations = defaultdict(int)

    # Set packet transmission rate to x if attacker is on branch, and to normal_rate when there is no attacker
    for index, branch in enumerate(branches):
        rate = x if index in attackers else normal_rate

        # Begin packet transmission simulation
        for _ in range(rate):
            # Track attacker route by traversing each branch
            for router in reversed(branch):
                if random.random() < p:
                    observations[index] += 1
                    break
                else:
                    break
        # If no marks have been observed within the simulation, return nothing
        if not observations:
            return None
    
    # Prediction of which branch the attacker is on using the marked branches
    return max(observations, key = observations.get)



# ----------------------------------------
# ----------   EDGE  SAMPLING   ----------
# ----------------------------------------
def edge_sampling(branches, attackers, p, x):
    # Set count for how many times each branch is marked
    observations = defaultdict(int)

    # Set packet transmission rate to x if attacker is on branch, and to normal_rate when there is no attacker
    for index, branch in enumerate(branches):
        rate = x if index in attackers else normal_rate

        # Begin packet transmission simulation
        for _ in range(rate):
            start = 0
            distance = 0
            # Track attacker route by traversing each branch
            for router in reversed(branch):
                if random.random() < p:
                    start = router
                    distance = 0
                else:
                    if start is not None:
                        if distance == 0:
                            end = router
                            observations[index] += 1
                        distance += 1
        # If no marks have been observed within the simulation, return nothing
        if not observations:
            return None
        
    # Prediction of which branch the attacker is on using the marked branches
    return max(observations, key = observations.get)



# ----------------------------------------
# -------   P1: SINGLE  ATTACKER   -------
# ----------------------------------------
single_node_results = {}
single_edge_results = {}

for rate in x:
    node_accuracy = []
    edge_accuracy = []

    for p in p_values:
        node_correct = 0
        edge_correct = 0
        
        for _ in range(runs):
            branches = create_topology()
            attacker_branch = random.randint(0, len(branches) - 1)
            attackers = {attacker_branch}
            predicted_node = node_sampling(branches, attackers, p, rate)
            predicted_edge = edge_sampling(branches, attackers, p, rate)
            if predicted_node == attacker_branch:
                node_correct += 1
            if predicted_edge == attacker_branch:
                edge_correct += 1
        
        node_accuracy.append(node_correct / runs)
        edge_accuracy.append(edge_correct / runs)
    single_node_results[rate] = node_accuracy
    single_edge_results[rate] = edge_accuracy

for rate in x:
    plt.figure()
    plt.plot(p_values, single_node_results[rate], marker = 'o', label = 'Node Sampling')
    plt.plot(p_values, single_edge_results[rate], marker = 'x', label = 'Edge Sampling')
    plt.xlabel("Packet Marking Probability (p)")
    plt.ylabel("Traceback Accuracy")
    plt.title(f"Single Attacker (x = {rate})")
    plt.legend()
    plt.grid(True)
    plt.show()



# ----------------------------------------
# --------   P2: TWO  ATTACKERS   --------
# ----------------------------------------
double_node_results = {}
double_edge_results = {}

for rate in x:
    node_accuracy = []
    edge_accuracy = []

    for p in p_values:
        node_correct = 0
        edge_correct = 0
        
        for _ in range(runs):
            branches = create_topology()
            attackers = set(random.sample(range(len(branches)), 2))
            predicted_node = node_sampling(branches, attackers, p, rate)
            predicted_edge = edge_sampling(branches, attackers, p, rate)
            if predicted_node == attackers:
                node_correct += 1
            if predicted_edge == attackers:
                edge_correct += 1
        
        node_accuracy.append(node_correct / runs)
        edge_accuracy.append(edge_correct / runs)
    double_node_results[rate] = node_accuracy
    double_edge_results[rate] = edge_accuracy

for rate in x:
    plt.figure()
    plt.plot(p_values, single_node_results[rate], marker = 'o', label = 'Node Sampling')
    plt.plot(p_values, single_edge_results[rate], marker = 'x', label = 'Edge Sampling')
    plt.xlabel("Packet Marking Probability (p)")
    plt.ylabel("Traceback Accuracy")
    plt.title(f"Two Attackers (x = {rate})")
    plt.legend()
    plt.grid(True)
    plt.show()
# Homework - 1
# Professor - Shamik Sengupta
# Author - Samuel Mouradian
# Due Date - 02 / 18 / 2026



import random
import numpy as np
import matplotlib as plt
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
    branches = [[] for i in range(num_branches)]
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

        for i in range(branch_size):
            branches[i].append(router_id)
            router_id += 1
        
        remaining -= branch_size
    
    return branches



# ----------------------------------------
# ----------   NODE  SAMPLING   ----------
# ----------------------------------------
def edge_sampling(branches, attackers, p, x):
    # Set count for how many times each branch is marked
    observations = defaultdict(int)

    # Set packet transmission rate to x if attacker is on branch, and to normal_rate when there is no attacker
    for i, branch in enumerate(branches):
        rate = x if i in attackers else normal_rate

        # Begin packet transmission simulation
        for i in range(rate):
            # Track attacker route by traversing each branch
            for router in reversed(branch):
                if random.random() < p:
                    observations[i] += 1
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



# ----------------------------------------
# -------   P1: SINGLE  ATTACKER   -------
# ----------------------------------------



# ----------------------------------------
# --------   P2: TWO  ATTACKERS   --------
# ----------------------------------------
import json
import numpy as np
import math
import random

with open("live.json","r") as f:
    data = json.load(f)

subset_size = 10
all_currencies = list(data["quotes"].keys())
subset = random.sample(all_currencies, subset_size)

n = len(subset)
nodes = {subset[i]: i for i in range(n)}
nodes_rev = {i: subset[i] for i in range(n)}

# Build adjacency matrix
rates = np.empty((n,n))
for i in range(n):
    for j in range(n):
        rateA = data["quotes"][nodes_rev[i]]
        rateB = data["quotes"][nodes_rev[j]]
        rateAB = rateB / rateA
        rates[i][j] = -math.log(rateAB)

found_cycle = []
x=1
while( len(found_cycle)<=3):
    print(x," try : not found yet")
    x+=1
    found_cycle = []

    num_triangles = 3
    for _ in range(num_triangles):
        i, j, k = random.sample(range(n), 3)
        factor = random.uniform(1.05, 1.15)  # ensure arbitrage
        rates[i][j] *= factor
        rates[j][k] *= factor
        rates[k][i] *= factor

    # Bellman-Ford to find first arbitrage
    dist = [math.inf] * n
    dist[0] = 0
    parent = [-1] * n
    EPS = 1e-9

    # Relax edges n-1 times
    for _ in range(n-1):
        for u in range(n):
            for v in range(n):
                if dist[u] + rates[u][v] < dist[v]-EPS:
                    dist[v] = dist[u] + rates[u][v]
                    parent[v] = u

    # Check for negative cycle
    for u in range(n):
        for v in range(n):
            if dist[u] + rates[u][v] < dist[v]-EPS:
                # reconstruct cycle
                curr = v
                for _ in range(n):
                    curr = parent[curr]
                cycle_start = curr
                arbitrage_cycle = [curr]
                curr = parent[curr]
                while curr != cycle_start:
                    arbitrage_cycle.append(curr)
                    curr = parent[curr]
                arbitrage_cycle.append(cycle_start)
                arbitrage_cycle.reverse()

                # convert to currency codes and return immediately
                found_cycle = [nodes_rev[idx][3:] for idx in arbitrage_cycle]
                break
        if found_cycle:
            break


print("Arbitrage detected:", " -> ".join(found_cycle))


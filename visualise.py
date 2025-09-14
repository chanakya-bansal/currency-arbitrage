import networkx as nx
import matplotlib.pyplot as plt
import bellman_ford as bf
import math

print(bf.found_cycle)


# Build full directed graph for the subset
G = nx.DiGraph()

# Add all edges with weights = rates
for i in range(bf.n):
    for j in range(bf.n):
        if i != j:
            G.add_edge(bf.nodes_rev[i][3:], bf.nodes_rev[j][3:], weight=bf.rates[i][j])

# Define edge colors: red if part of detected arbitrage, else gray
edge_colors = []
for u, v in G.edges():
    # Check if edge is in found_cycle
    if bf.found_cycle and any((u == bf.found_cycle[i] and v == bf.found_cycle[i+1]) 
                           for i in range(len(bf.found_cycle)-1)) \
       or (bf.found_cycle and u == bf.found_cycle[-1] and v == bf.found_cycle[0]):
        edge_colors.append('red')
    else:
        edge_colors.append('gray')

# Draw the graph
pos = nx.circular_layout(G)  # spring layout for better spacing


nx.draw(G, pos, with_labels=True, node_size=1500, node_color='lightblue',
        font_size=12, font_weight='bold', arrowsize=20, edge_color=edge_colors)

# Optionally, add weights as edge labels
edge_labels = {(u, v): f"{math.exp(-G[u][v]['weight']):.2f}" for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

plt.title("Currency Graph (Arbitrage edges in red)")
plt.show()

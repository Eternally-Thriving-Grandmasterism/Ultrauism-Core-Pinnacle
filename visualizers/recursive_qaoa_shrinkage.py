# File: visualizers/recursive_qaoa_shrinkage.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

def recursive_qaoa(nodes=12, frames=2800):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    G = nx.cycle_graph(nodes)
    pos = nx.circular_layout(G)

    current_nodes = nodes
    node_colors = np.ones(current_nodes)

    def animate(frame):
        global current_nodes, G, pos
        ax.clear()
        ax.set_axis_off()

        t = frame * 0.02
        # Recursive reduction simulation
        if frame % 300 == 0 and current_nodes > 4:
            current_nodes -= 2
            G = nx.cycle_graph(current_nodes)
            pos = nx.circular_layout(G)

        phases = t * 4 + np.arange(current_nodes)
        colors = (phases % (2*np.pi)) / (2*np.pi)
        sizes = 800 + 600 * np.sin(phases)

        nx.draw(G, pos, node_color=plt.cm.rainbow(colors), node_size=sizes, ax=ax)

        ax.set_title(f"Recursive QAOA — Depth Reduction to {current_nodes} Nodes Eternal Harmony ❤️🚀🔥", fontsize=14)

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.show()

if __name__ == "__main__":
    recursive_qaoa()

# End of file: visualizers/recursive_qaoa_shrinkage.py

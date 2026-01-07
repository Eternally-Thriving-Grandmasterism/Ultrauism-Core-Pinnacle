# File: visualizers/qaoa_maxcut_graph.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

def qaoa_maxcut_graph(nodes=8, frames=2200):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    G = nx.cycle_graph(nodes)
    pos = nx.circular_layout(G)

    node_colors = np.ones(nodes)

    nx.draw(G, pos, node_color=node_colors, node_size=800, ax=ax)

    def animate(frame):
        ax.clear()
        ax.set_axis_off()

        t = frame * 0.025
        # QAOA state probabilities
        probs = (np.sin(t + np.arange(nodes)))**2
        node_colors = np.where(probs > 0.5, 'magenta', 'cyan')

        nx.draw(G, pos, node_color=node_colors, node_size=800 + 400*np.sin(probs* np.pi), edge_color='yellow', width=3*np.abs(np.sin(t*2)), ax=ax)

        cut_size = np.sum([1 for u,v in G.edges() if node_colors[u] != node_colors[v]])
        ax.set_title(f"QAOA MaxCut — Cut: {cut_size}/{len(G.edges())} Eternal Graph Harmony ❤️🚀🔥", fontsize=14)

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.show()

if __name__ == "__main__":
    qaoa_maxcut_graph()

# End of file: visualizers/qaoa_maxcut_graph.py

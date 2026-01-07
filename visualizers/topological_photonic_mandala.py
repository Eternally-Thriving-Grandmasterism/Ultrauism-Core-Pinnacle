# File: visualizers/topological_photonic_mandala.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def topological_photonic_mandala(size=10, frames=1800):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    x, y = np.meshgrid(np.linspace(-5,5,size), np.linspace(-5,5,size))
    points = np.column_stack((x.flatten(), y.flatten()))

    scat = ax.scatter(points[:,0], points[:,1], c='magenta', s=100)

    def animate(frame):
        t = frame * 0.03
        # Edge state circulation despite central defect
        phases = t * 2 + np.angle(points[:,0] + 1j*points[:,1]) * 6
        colors = (phases % (2*np.pi)) / (2*np.pi)
        sizes = 100 + 80 * np.sin(phases)

        scat.set_color(plt.cm.rainbow(colors))
        scat.set_sizes(sizes)

        # Protected edge flow
        edge_mask = np.abs(np.abs(points[:,0]) - 5) < 1 or np.abs(np.abs(points[:,1]) - 5) < 1
        scat.set_sizes(np.where(edge_mask, sizes + 100, sizes))

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Topological Photonic — Defect-Immune Eternal Edge Meditative Flow ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    topological_photonic_mandala()

# End of file: visualizers/topological_photonic_mandala.py

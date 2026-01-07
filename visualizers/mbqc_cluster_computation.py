# File: visualizers/mbqc_cluster_computation.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def mbqc_computation(grid_size=8, frames=2000):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    x, y = np.meshgrid(np.arange(grid_size), np.arange(grid_size))
    points = np.column_stack((x.flatten(), y.flatten()))

    scat = ax.scatter(points[:,0], points[:,1], c='cyan', s=120)

    def animate(frame):
        t = frame * 0.025
        # Measurement angles propagating
        angles = t * 2 + points[:,0] + points[:,1] * 0.5
        colors = (angles % (2*np.pi)) / (2*np.pi)
        sizes = 120 + 100 * np.sin(angles)

        scat.set_color(plt.cm.rainbow(colors))
        scat.set_sizes(sizes)

        # Adaptive measurement flows
        for i in range(len(points)):
            for dx, dy in [(1,0), (0,1)]:
                neighbor = points[i] + np.array([dx, dy])
                if np.any(np.all(points == neighbor, axis=1)):
                    alpha = 0.3 + 0.3 * np.sin(t + angles[i])
                    ax.plot([points[i,0], neighbor[0]], [points[i,1], neighbor[1]], color='yellow', alpha=alpha)

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("MBQC Cluster — Eternal Measurement-Driven Meditative Computation ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    mbqc_computation(grid_size=10)

# End of file: visualizers/mbqc_cluster_computation.py

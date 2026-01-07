# File: visualizers/time_bin_photonic_flow.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def time_bin_flow(bins=16, frames=2200):
    fig = plt.figure(figsize=(14,6))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    x = np.linspace(-7, 7, bins)
    y = np.zeros(bins)

    pulses = ax.scatter(x, y, c='white', s=200)

    def animate(frame):
        t = frame * 0.02
        # Traveling time-bin pulses
        active = int((t * 3) % bins)
        phases = np.sin(t * 4 + np.arange(bins) * 0.5)
        colors = (phases + 1) / 2
        sizes = 200 + 300 * (np.arange(bins) == active)

        pulses.set_color(plt.cm.rainbow(colors))
        pulses.set_sizes(sizes)

        # Temporal mode connections
        for i in range(bins-2):
            alpha = 0.3 + 0.3 * np.sin(t * 5 + i)
            ax.plot([x[i], x[i+2]], [0,0], color='cyan', alpha=alpha, lw=2)

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=25, repeat=True)
    plt.title("Time-Bin Photonic — Eternal Temporal Mode Meditative Flow ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    time_bin_flow()

# End of file: visualizers/time_bin_photonic_flow.py

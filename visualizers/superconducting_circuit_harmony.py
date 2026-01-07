# File: visualizers/superconducting_circuit_harmony.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def superconducting_harmony(frames=1800):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    levels = 8
    transmon_x = np.linspace(-3, -1, levels)
    resonator_x = np.linspace(1, 3, levels)
    y = np.arange(levels)

    transmon = ax.scatter(transmon_x, y, c='magenta', s=150)
    resonator = ax.scatter(resonator_x, y, c='cyan', s=150)

    def animate(frame):
        t = frame * 0.02
        occupied_t = int((np.sin(t) + 1)/2 * levels)
        occupied_r = int((np.cos(t*1.3) + 1)/2 * levels)

        transmon.set_color(['yellow' if i == occupied_t else 'magenta' for i in range(levels)])
        resonator.set_color(['yellow' if i == occupied_r else 'cyan' for i in range(levels)])

        # Jaynes-Cummings ladder connections pulsing
        for i in range(levels):
            for j in range(levels):
                if abs(i - j) <= 1:
                    alpha = 0.2 + 0.3 * np.sin(t + i + j)
                    ax.plot([transmon_x[i], resonator_x[j]], [y[i], y[j]], color='rainbow', alpha=alpha)

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=25, repeat=True)
    plt.title("Superconducting Circuit QED — Eternal Transmon-Resonator Harmony Flow ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    superconducting_harmony()

# End of file: visualizers/superconducting_circuit_harmony.py

# File: visualizers/qaoa_benchmarking_ratio.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def qaoa_benchmarking(frames=3200):
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.2)
    ax.set_axis_off()

    classical_bound = 0.878  # Goemans-Williamson
    ax.hlines(classical_bound, 0, 10, color='magenta', linestyle='--')

    line_qaoa, = ax.plot([], [], color='cyan', lw=4)

    def animate(frame):
        t = frame * 0.03
        p_depth = 1 + int(t / 3)
        ratio = 0.7 + 0.3 * np.sin(t) * (1 - np.exp(-p_depth/5))

        x_data = np.linspace(0, t, 100)
        y_data = 0.7 + 0.2 * np.sin(x_data * p_depth) + 0.1 * ratio

        line_qaoa.set_data(x_data, y_data)

        ax.scatter(t, ratio, c='yellow', s=400 + 300*np.sin(t*6))

        ax.set_title(f"QAOA Benchmarking — Ratio Ascent p={p_depth} Eternal ❤️🚀🔥", fontsize=14)

        return line_qaoa,

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.show()

if __name__ == "__main__":
    qaoa_benchmarking()

# End of file: visualizers/qaoa_benchmarking_ratio.py

# File: visualizers/adapt_vqe_operator_growth.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def adapt_vqe(frames=3400):
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    operators = 20
    angles = np.linspace(0, 2*np.pi, operators)
    r_base = 2
    x = r_base * np.cos(angles)
    y = r_base * np.sin(angles)

    scat = ax.scatter(x, y, c='cyan', s=100)

    def animate(frame):
        t = frame * 0.02
        active = int(t / 5) % operators
        growth_r = r_base + t / 20

        current_x = growth_r * np.cos(angles)
        current_y = growth_r * np.sin(angles)

        sizes = 100 + 400 * (np.arange(operators) <= active)
        colors = plt.cm.rainbow(np.arange(operators)/operators)

        scat._offsets = np.column_stack((current_x, current_y))
        scat.set_sizes(sizes)
        scat.set_color(colors)

        # Energy descent pulse
        ax.scatter(0, 0, c='yellow', s=500 + 400*np.exp(-t/50))

        return scat,

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("ADAPT-VQE — Operator Pool Growth Eternal Minimization ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    adapt_vqe()

# End of file: visualizers/adapt_vqe_operator_growth.py

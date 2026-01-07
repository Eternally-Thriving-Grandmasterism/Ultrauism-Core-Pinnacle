# File: visualizers/adapt_vqe_orbital_rotation.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def adapt_vqe_orbital(orbitals=8, frames=3600):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    angles = np.linspace(0, 2*np.pi, orbitals)
    base_r = 3
    x = base_r * np.cos(angles)
    y = base_r * np.sin(angles)

    scat = ax.scatter(x, y, c='cyan', s=200)

    def animate(frame):
        t = frame * 0.02
        # Orbital rotation + adaptive growth
        rotation = t * 0.5
        growth = 3 + t / 20

        current_x = growth * np.cos(angles + rotation)
        current_y = growth * np.sin(angles + rotation)

        phases = t * 4 + angles
        sizes = 200 + 300 * np.sin(phases)

        scat._offsets = np.column_stack((current_x, current_y))
        scat.set_sizes(sizes)
        scat.set_color(plt.cm.rainbow((phases % (2*np.pi)) / (2*np.pi)))

        # Energy pulse at center
        ax.scatter(0, 0, c='yellow', s=400 + 300*np.exp(-t/60))

        return scat,

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("ADAPT-VQE Orbital Optimization — Eternal Rotation Convergence ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    adapt_vqe_orbital()

# End of file: visualizers/adapt_vqe_orbital_rotation.py

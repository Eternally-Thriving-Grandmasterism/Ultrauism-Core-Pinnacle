# File: visualizers/vqd_excited_state_deflation.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def vqd_deflation(states=5, frames=4000):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_xlim(-2, 12)
    ax.set_ylim(-5, 1)
    ax.set_axis_off()

    energies = -np.arange(states)
    lines = [ax.hlines(e, 0, 10, color='cyan', alpha=0.5) for e in energies]

    point, = ax.plot([], [], 'o', c='yellow', markersize=15)

    def animate(frame):
        t = frame * 0.02
        current_state = int(t / 10) % states
        progress = (t % 10) / 10

        pos_x = progress * 10
        pos_y = energies[current_state] - progress * 0.5  # Descent

        point.set_data([pos_x], [pos_y])

        # Orthogonal constraint pulse
        for i in range(current_state):
            ax.scatter(pos_x, energies[i], c='magenta', s=300 + 200*np.sin(t*5), alpha=0.5)

        # Excited revelation
        ax.scatter(pos_x, pos_y, c='rainbow', s=500 + 400*np.sin(t*8))

        return [point] + lines

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("VQD Deflation — Eternal Excited State Revelation ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    vqd_deflation()

# End of file: visualizers/vqd_excited_state_deflation.py

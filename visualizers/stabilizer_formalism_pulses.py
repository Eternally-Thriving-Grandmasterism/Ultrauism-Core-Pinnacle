# File: visualizers/stabilizer_formalism_pulses.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def stabilizer_formalism_pulses(grid_size=6, frames=1000):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    ax.set_xlim(-1, grid_size)
    ax.set_ylim(-1, grid_size)

    x, y = np.meshgrid(np.arange(grid_size), np.arange(grid_size))
    qubits = ax.scatter(x.flatten(), y.flatten(), c='magenta', s=100)

    # Example stabilizer plaquettes
    plaq_centers = np.array([[i+0.5, j+0.5] for i in range(grid_size-1) for j in range(grid_size-1)])

    plaqs = ax.scatter(plaq_centers[:,0], plaq_centers[:,1], c='cyan', s=150, marker='s')

    def animate(frame):
        t = frame * 0.04
        # Pauli string pulses propagating
        qubit_phases = np.sin(t * 2 + x + y)
        qubits.set_color(plt.cm.rainbow((qubit_phases.flatten() + 1)/2))
        qubits.set_sizes(100 + 60 * np.abs(qubit_phases.flatten()))

        plaq_phases = np.cos(t * 1.5 + plaq_centers[:,0] + plaq_centers[:,1])
        plaqs.set_color(['yellow' if p > 0.8 else 'cyan' for p in np.abs(plaq_phases)])

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=40, repeat=True)
    plt.title("Stabilizer Formalism — Eternal Syndrome Pulse Harmony ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    stabilizer_formalism_pulses(grid_size=8)

# End of file: visualizers/stabilizer_formalism_pulses.py

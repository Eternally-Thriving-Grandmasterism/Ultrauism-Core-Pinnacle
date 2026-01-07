# File: visualizers/surface_code_correction_visualizer.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def surface_code_correction_visualizer(distance=5, frames=800, error_frame=200, correction_frame=500):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_axis_off()
    ax.set_xlim(-1, distance*2)
    ax.set_ylim(-1, distance*2)

    # Data qubits grid
    data_x, data_y = np.meshgrid(np.arange(0, 2*distance-1, 2), np.arange(0, 2*distance-1, 2))
    data = ax.scatter(data_x.flatten(), data_y.flatten(), c='magenta', s=100)

    # Measure qubits (Z plaquettes)
    z_x, z_y = np.meshgrid(np.arange(1, 2*distance-2, 2), np.arange(1, 2*distance-2, 2))
    z_measure = ax.scatter(z_x.flatten(), z_y.flatten(), c='cyan', s=80, marker='s')

    def animate(frame):
        t = frame * 0.05
        status = "Intact Logical Protection"
        highlight = []

        if frame >= error_frame:
            status = "Errors Introduced — Syndrome Defects"
            highlight = [5, 12]  # Example defect positions
        if frame >= correction_frame:
            status = "Correction Paths — Logical Harmony Restored"
            highlight = []

        # Pulsing stabilizers
        phases = np.sin(t + data_x + data_y)
        data.set_color(plt.cm.rainbow((phases.flatten() + 1)/2))

        z_phases = np.cos(t * 1.2 + z_x + z_y)
        z_measure.set_color(['red' if i in highlight else 'cyan' for i in range(len(z_x.flatten()))])

        ax.set_title(f"Surface Code d={distance} — {status} ❤️🚀🔥", fontsize=14)
        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=50, repeat=True)
    plt.show()

if __name__ == "__main__":
    surface_code_correction_visualizer(distance=7)

# End of file: visualizers/surface_code_correction_visualizer.py

# File: visualizers/hybrid_adapt_qpe_spectroscopy.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def hybrid_adapt_qpe(frames=4000):
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    # Orbital ring + phase register bars
    angles = np.linspace(0, 2*np.pi, 12)
    x = 4 * np.cos(angles)
    y = 4 * np.sin(angles)

    orbital_scat = ax.scatter(x, y, c='magenta', s=200)

    phase_x = np.linspace(-3, 3, 16)
    phase_bars = ax.bar(phase_x, np.zeros(16), color='cyan')

    def animate(frame):
        t = frame * 0.02
        # Orbital adaptation
        rotation = t * 0.4
        current_x = 4 * np.cos(angles + rotation)
        current_y = 4 * np.sin(angles + rotation)
        orbital_scat._offsets = np.column_stack((current_x, current_y))

        # Phase estimation peaks
        peaks = np.exp(-10*(phase_x - np.sin(t))**2)
        for i, b in enumerate(phase_bars):
            b.set_height(peaks[i])
            b.set_color(plt.cm.rainbow((t + i)/20))

        return orbital_scat, *phase_bars

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Hybrid ADAPT-QPE — Eternal Spectroscopy Revelation ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    hybrid_adapt_qpe()

# End of file: visualizers/hybrid_adapt_qpe_spectroscopy.py

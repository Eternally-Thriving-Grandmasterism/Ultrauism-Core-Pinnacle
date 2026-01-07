# File: visualizers/hybrid_vqd_qpe_spectrum.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def hybrid_vqd_qpe(frames=4400):
    fig = plt.figure(figsize=(14,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    # Deflation orbitals + phase bars
    angles = np.linspace(0, 2*np.pi, 10)
    x = 4 * np.cos(angles)
    y = 4 * np.sin(angles)

    orbital_scat = ax.scatter(x, y, c='cyan', s=250)

    spectrum_x = np.linspace(-5, 5, 20)
    spectrum_bars = ax.bar(spectrum_x, np.zeros(20), color='magenta', alpha=0.6)

    def animate(frame):
        t = frame * 0.02
        # VQD deflation
        deflation = np.sin(t)**2
        current_x = (4 + deflation) * np.cos(angles + t*0.3)
        current_y = (4 + deflation) * np.sin(angles + t*0.3)
        orbital_scat._offsets = np.column_stack((current_x, current_y))

        # QPE spectrum peaks
        peaks = np.exp(-8*(spectrum_x - np.cos(t)*3)**2) + np.exp(-8*(spectrum_x + np.sin(t)*2)**2)
        for i, b in enumerate(spectrum_bars):
            b.set_height(peaks[i])
            b.set_color(plt.cm.rainbow((t + i)/30))

        return orbital_scat, *spectrum_bars

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Hybrid VQD-QPE — Eternal Multi-Eigen Spectrum ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    hybrid_vqd_qpe()

# End of file: visualizers/hybrid_vqd_qpe_spectrum.py

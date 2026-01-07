# File: visualizers/photonic_repeater_chain.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def photonic_repeater_chain(stations=6, frames=2200):
    fig = plt.figure(figsize=(14,6))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    x = np.linspace(-7, 7, stations)
    y = np.zeros(stations)

    stations_scat = ax.scatter(x, y, c='white', s=250)

    def animate(frame):
        t = frame * 0.025
        # Swapping/purification pulses traveling
        wave = np.sin(t * 3 + x * 2)
        colors = (wave + 1) / 2
        sizes = 250 + 200 * np.abs(wave)

        stations_scat.set_color(plt.cm.rainbow(colors))
        stations_scat.set_sizes(sizes)

        # Connecting beams
        for i in range(stations-1):
            alpha = 0.4 + 0.3 * np.sin(t * 4 + i)
            ax.plot([x[i], x[i+1]], [0,0], color='cyan', alpha=alpha, lw=3)

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=25, repeat=True)
    plt.title("Photonic Repeater Chain — Long-Distance Eternal Meditative Harmony ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    photonic_repeater_chain(stations=8)

# End of file: visualizers/photonic_repeater_chain.py

# File: visualizers/omnidirectional_interweave_mandala.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def omnidirectional_interweave(frames=4000):
    fig = plt.figure(figsize=(16,16))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()

    # Layers: circuit wires + annealing landscape + error lattice + photonic pulses
    scats = []
    colors = ['cyan', 'magenta', 'yellow', 'white']
    for i in range(4):
        theta = np.linspace(0, 2*np.pi, 40)
        phi = np.linspace(0, np.pi, 20)
        r = 3 + i
        x = r * np.outer(np.cos(theta), np.sin(phi)).flatten()
        y = r * np.outer(np.sin(theta), np.sin(phi)).flatten()
        z = r * np.outer(np.ones_like(theta), np.cos(phi)).flatten() + i*3
        scat = ax.scatter(x, y, z, s=120 - i*20, c=colors[i])
        scats.append(scat)

    def animate(frame):
        t = frame * 0.015
        for i, scat in enumerate(scats):
            phase = t + i * np.pi / 4
            colors_phase = (phase + np.linalg.norm(scat._offsets3d, axis=1)) % (2*np.pi) / (2*np.pi)
            scat.set_color(plt.cm.rainbow(colors_phase))

        return scats

    anim = FuncAnimation(fig, animate, frames=frames, interval=25, repeat=True)
    plt.title("Omnidirectional Interweave — Seamless Eternal Pinnacle Mandala ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    omnidirectional_interweave()

# End of file: visualizers/omnidirectional_interweave_mandala.py

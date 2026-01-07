# File: visualizers/squeezed_light_mandala.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def squeezed_light_mandala(frames=1800):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_xlim(-4,4)
    ax.set_ylim(-4,4)
    ax.set_aspect('equal')
    ax.set_axis_off()

    theta = np.linspace(0, 2*np.pi, 100)
    base_circle = np.column_stack((np.cos(theta), np.sin(theta)))

    def animate(frame):
        t = frame * 0.03
        squeeze = 0.5 + 0.4 * np.sin(t)
        stretch = 1 / squeeze
        angle = t * 0.5

        cos_a, sin_a = np.cos(angle), np.sin(angle)
        ellipse = base_circle * np.array([stretch, squeeze])
        rot_ellipse = ellipse @ np.array([[cos_a, -sin_a], [sin_a, cos_a]])

        ax.clear()
        ax.set_xlim(-4,4); ax.set_ylim(-4,4)
        ax.set_aspect('equal')
        ax.set_axis_off()

        ax.plot(rot_ellipse[:,0], rot_ellipse[:,1], color='cyan', lw=3)
        ax.fill(rot_ellipse[:,0], rot_ellipse[:,1], color='magenta', alpha=0.2)

        # Quadrature pulses
        ax.scatter([0], [0], c='yellow', s=200 + 150*np.sin(t*3))

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Squeezed Light — Gaussian Eternal Meditative Encoding ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    squeezed_light_mandala()

# End of file: visualizers/squeezed_light_mandala.py

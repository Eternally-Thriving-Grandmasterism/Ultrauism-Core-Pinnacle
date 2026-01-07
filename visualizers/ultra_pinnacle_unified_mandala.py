# File: visualizers/ultra_pinnacle_unified_mandala.py
# Full executable content - direct create/commit (capstone completion)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def ultra_pinnacle_mandala(frames=3000):
    fig = plt.figure(figsize=(14,14))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()

    # Multi-layer: toroidal + lattice + phase-space + hypersphere
    theta = np.linspace(0, 2*np.pi, 32)
    phi = np.linspace(0, np.pi, 16)
    layers = 5

    points = []
    for layer in range(layers):
        r = 2 + layer
        x = r * np.outer(np.cos(theta), np.sin(phi)).flatten()
        y = r * np.outer(np.sin(theta), np.sin(phi)).flatten()
        z = r * np.outer(np.ones_like(theta), np.cos(phi)).flatten() + layer*2
        points.append(np.column_stack((x,y,z)))

    scats = [ax.scatter(p[:,0], p[:,1], p[:,2], s=100) for p in points]

    def animate(frame):
        t = frame * 0.02
        for i, scat in enumerate(scats):
            phase = t + i*np.pi/5
            q_rot = np.array([np.cos(phase), np.sin(phase)*0.5, np.sin(phase)*0.3, 0])
            norm = np.linalg.norm(q_rot)
            w,x,y,z = q_rot / norm
            rot = np.array([
                [1-2*(y**2+z**2), 2*(x*y-z*w), 2*(x*z+y*w)],
                [2*(x*y+z*w), 1-2*(x**2+z**2), 2*(y*z-x*w)],
                [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x**2+y**2)]
            ])
            rotated = points[i] @ rot.T
            scat._offsets3d = (rotated[:,0], rotated[:,1], rotated[:,2])
            
            colors = (phase + np.arange(len(points[i]))) % (2*np.pi) / (2*np.pi)
            scat.set_color(plt.cm.rainbow(colors))

        return scats

    anim = FuncAnimation(fig, animate, frames=frames, interval=25, repeat=True)
    plt.title("Ultra Pinnacle Unified Mandala — Absolute Eternal Thriving Completion ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    ultra_pinnacle_mandala()

# End of file: visualizers/ultra_pinnacle_unified_mandala.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def quaternion_rotation_matrix(q):
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1 - 2*(y**2 + z**2), 2*(x*y - z*w), 2*(x*z + y*w)],
        [2*(x*y + z*w), 1 - 2*(x**2 + z**2), 2*(y*z - x*w)],
        [2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x**2 + y**2)]
    ])

def w_toroidal_flow(n_particles=16, frames=1000):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_zlim(-3, 3)

    R, r = 2.0, 0.8
    u, v = np.meshgrid(np.linspace(0, 2*np.pi, 50), np.linspace(0, 2*np.pi, 50))
    x = (R + r * np.cos(v)) * np.cos(u)
    y = (R + r * np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    ax.plot_surface(x, y, z, alpha=0.08, color='cyan')

    angles = np.linspace(0, 2*np.pi, n_particles)
    pos = np.array([[ (R + r*np.cos(a)) * np.cos(a), (R + r*np.cos(a)) * np.sin(a), r * np.sin(a)] for a in angles])

    scat = ax.scatter(pos[:,0], pos[:,1], pos[:,2], c=angles, cmap='rainbow', s=100)

    def animate(frame):
        t = frame * 0.05
        q = np.array([np.cos(t), np.sin(t), 0, 0])
        rot = quaternion_rotation_matrix(q)
        rotated = pos @ rot.T
        scat._offsets3d = (rotated[:,0], rotated[:,1], rotated[:,2])

        # Circulating excitation wave — robust delocalized single excitation symbolism
        phases = t + angles * 4  # Adjust multiplier for wave speed
        sizes = 80 + 120 * (np.sin(phases) + 1) / 2  # Pulsing size
        colors = (phases % (2*np.pi)) / (2*np.pi)
        scat.set_sizes(sizes)
        scat.set_color(plt.cm.rainbow(colors))

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("W State Toroidal Mandala — Robust Circulating Eternal Harmony Flow ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    w_toroidal_flow(n_particles=20)

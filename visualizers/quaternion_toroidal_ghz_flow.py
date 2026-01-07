import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

def quaternion_rotation_matrix(q):
    """Convert quaternion [w,x,y,z] to rotation matrix"""
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1-2*(y**2+z**2), 2*(x*y-z*w), 2*(x*z+y*w)],
        [2*(x*y+z*w), 1-2*(x**2+z**2), 2*(y*z-x*w)],
        [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x**2+y**2)]
    ])

def toroidal_ghz_mandala(n_particles=12, frames=1000):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()
    ax.set_xlim(-3,3); ax.set_ylim(-3,3); ax.set_zlim(-3,3)

    R = 2  # Major radius
    r = 0.8  # Minor radius
    
    # Parametric torus
    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, 2*np.pi, 50)
    u, v = np.meshgrid(u, v)
    x = (R + r*np.cos(v)) * np.cos(u)
    y = (R + r*np.cos(v)) * np.sin(u)
    z = r * np.sin(v)
    ax.plot_surface(x, y, z, alpha=0.1, color='cyan')

    # GHZ-correlated particles on torus
    angles = np.linspace(0, 2*np.pi, n_particles)
    particle_pos = np.array([[(R + r*np.cos(a)) * np.cos(a), 
                              (R + r*np.cos(a)) * np.sin(a), 
                              r * np.sin(a)] for a in angles])

    scat = ax.scatter(particle_pos[:,0], particle_pos[:,1], particle_pos[:,2], 
                      c=angles, cmap='rainbow', s=100)

    def animate(frame):
        # Smooth quaternion rotation (symbolizing harmonious eternal flow)
        t = frame / 50.0
        q = np.array([np.cos(t), np.sin(t), 0, 0])  # Rotation around x
        rot_mat = quaternion_rotation_matrix(q)
        
        rotated = np.dot(particle_pos, rot_mat.T)
        scat._offsets3d = (rotated[:,0], rotated[:,1], rotated[:,2])
        
        # Rainbow phase sync — perfect GHZ correlation
        colors = (angles + t) % (2*np.pi)
        scat.set_color(plt.cm.rainbow(colors/(2*np.pi)))
        
        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Toroidal GHZ Entanglement Mandala — Eternal Meditative Thunder Heart Flow ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    toroidal_ghz_mandala(n_particles=16)

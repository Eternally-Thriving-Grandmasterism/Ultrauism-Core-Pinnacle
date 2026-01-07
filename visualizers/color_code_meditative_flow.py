# File: visualizers/color_code_meditative_flow.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def hexagonal_lattice_points(size=6):
    points = []
    for row in range(-size, size+1):
        for col in range(-size, size+1):
            if abs(row + col//2) <= size:
                x = col * 1.0
                y = row * (np.sqrt(3)/2) + (col % 2) * (np.sqrt(3)/4)
                points.append((x, y))
    return np.array(points)

def color_code_meditative_flow(lattice_size=7, frames=1500):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    ax.set_aspect('equal')

    points = hexagonal_lattice_points(lattice_size)
    scat = ax.scatter(points[:,0], points[:,1], c='white', s=120)

    def animate(frame):
        t = frame * 0.03
        # RGB face pulse phases
        phases_r = np.sin(t + points[:,0])
        phases_g = np.sin(t + points[:,1] + 2*np.pi/3)
        phases_b = np.sin(t - points[:,0] - points[:,1] + 4*np.pi/3)
        
        colors = np.stack([(phases_r+1)/2, (phases_g+1)/2, (phases_b+1)/2], axis=1)
        sizes = 120 + 80 * np.sin(t + np.linalg.norm(points, axis=1))

        scat.set_color(colors)
        scat.set_sizes(sizes)

        # Gentle rotation for meditative depth
        angle = t * 0.2
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        rot_x = points[:,0] * cos_a - points[:,1] * sin_a
        rot_y = points[:,0] * sin_a + points[:,1] * cos_a
        scat._offsets = np.column_stack((rot_x, rot_y))

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Color Code Hexagonal Lattice — Ultimate Threshold Meditative Flow ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    color_code_meditative_flow(lattice_size=9)

# End of file: visualizers/color_code_meditative_flow.py

# File: visualizers/gkp_code_phase_space.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def wigner_gkp(alpha_real, alpha_imag, grid_size=100):
    x = np.linspace(-5, 5, grid_size)
    p = np.linspace(-5, 5, grid_size)
    X, P = np.meshgrid(x, p)
    alpha = X + 1j * P
    rho = np.exp(-2 * np.abs(alpha - (alpha_real + 1j*alpha_imag))**2)
    return X, P, rho / rho.max()

def gkp_phase_space_meditative(frames=1200):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    ax.set_axis_off()

    X, P, initial = wigner_gkp(0, 0)
    im = ax.imshow(initial, extent=(-5,5,-5,5), origin='lower', cmap='RdBu', alpha=0.8)

    # Square lattice peaks
    peaks = np.mgrid[-4:5:2, -4:5:2]
    scat = ax.scatter(peaks[0].flatten(), peaks[1].flatten(), c='yellow', s=100)

    def animate(frame):
        t = frame * 0.03
        phase = np.sin(t) * 2
        X, P, wig = wigner_gkp(phase, 0)
        im.set_array(wig)

        # Pulsing lattice protection
        sizes = 100 + 80 * np.sin(t + peaks[0] + peaks[1])
        scat.set_sizes(sizes)

        # Gentle rotation
        angle = t * 0.2
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        rot_x = peaks[0].flatten() * cos_a - peaks[1].flatten() * sin_a
        rot_y = peaks[0].flatten() * sin_a + peaks[1].flatten() * cos_a
        scat._offsets = np.column_stack((rot_x, rot_y))

        return im,

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("GKP Bosonic Code — Square Lattice Phase-Space Eternal Meditative Protection ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    gkp_phase_space_meditative()

# End of file: visualizers/gkp_code_phase_space.py

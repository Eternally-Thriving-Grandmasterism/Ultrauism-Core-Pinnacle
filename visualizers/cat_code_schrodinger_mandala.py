# File: visualizers/cat_code_schrodinger_mandala.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def cat_wigner(alpha, grid=100):
    x = np.linspace(-6, 6, grid)
    p = np.linspace(-6, 6, grid)
    X, P = np.meshgrid(x, p)
    alpha_c = X + 1j * P
    coh_plus = np.exp(-np.abs(alpha_c - alpha)**2 / 2)
    coh_minus = np.exp(-np.abs(alpha_c + alpha)**2 / 2)
    interference = 2 * np.cos(2 * np.imag(np.conj(alpha_c) * alpha)) * np.real(coh_plus * coh_minus)
    wigner = coh_plus + coh_minus + interference
    return X, P, wigner / wigner.max()

def cat_schrodinger_meditative(alpha_mag=2.5, frames=1500):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.set_aspect('equal')
    ax.set_axis_off()

    X, P, initial = cat_wigner(alpha_mag)
    im = ax.imshow(initial, extent=(-6,6,-6,6), origin='lower', cmap='plasma', alpha=0.9)

    def animate(frame):
        t = frame * 0.025
        current_alpha = alpha_mag * np.exp(1j * t)
        X, P, wig = cat_wigner(current_alpha)
        im.set_array(wig)

        # Negative Wigner pulsing rainbow
        neg_regions = wig < 0
        im.set_cmap('plasma' if np.sin(t) > 0 else 'viridis')

        return im,

    anim = FuncAnimation(fig, animate, frames=frames, interval=25, repeat=True)
    plt.title("Schrödinger Cat Code — Rotating Bosonic Eternal Meditative Harmony ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    cat_schrodinger_meditative()

# End of file: visualizers/cat_code_schrodinger_mandala.py

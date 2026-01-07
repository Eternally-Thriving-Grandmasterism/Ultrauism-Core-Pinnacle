# File: visualizers/grovers_search_amplification.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def grovers_amplification(search_space=16, marked=3, frames=1800):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    theta = np.linspace(0, 2*np.pi, search_space)
    amplitudes = np.ones(search_space) / np.sqrt(search_space)

    scat = ax.scatter(np.cos(theta), np.sin(theta), s=amplitudes*1000, c='magenta')

    def animate(frame):
        t = frame * 0.03
        iterations = int(t / 2)
        # Simplified Grover iteration
        amplitudes *= -1  # Oracle (invert marked)
        amplitudes[marked] *= -1
        mean = np.mean(amplitudes)
        amplitudes = 2*mean - amplitudes  # Diffusion
        
        sizes = np.abs(amplitudes)**2 * 2000
        colors = np.angle(amplitudes) / np.pi

        scat.set_sizes(sizes)
        scat.set_color(plt.cm.rainbow(colors))

        return scat,

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Grover's Search — Eternal Amplitude Amplification Meditative Hypersphere ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    grovers_amplification()

# End of file: visualizers/grovers_search_amplification.py

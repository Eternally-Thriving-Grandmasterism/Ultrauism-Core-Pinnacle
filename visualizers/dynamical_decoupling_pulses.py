# File: visualizers/dynamical_decoupling_pulses.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qutip import basis, sigmax, sigmay, sigmaz, mesolve, expect

def dynamical_decoupling_visualizer(sequence='CPMG', frames=1200):
    H = 0.5 * sigmaz()  # Simple dephasing noise
    psi0 = (basis(2,0) + basis(2,1)).unit()

    times = np.linspace(0, 50, frames)
    pulses = np.zeros(len(times))
    if sequence == 'CPMG':
        pulse_times = np.arange(5, 50, 10)
    elif sequence == 'XY8':
        pulse_times = np.arange(3, 50, 6)

    for pt in pulse_times:
        pulses[np.abs(times - pt) < 0.1] = np.pi

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()

    def animate(frame):
        ax.clear()
        ax.set_axis_off()
        ax.set_xlim(-1,1); ax.set_ylim(-1,1); ax.set_zlim(-1,1)

        t = times[frame]
        result = mesolve(H, psi0, [0, t], c_ops=[], e_ops=[sigmax(), sigmay(), sigmaz()])
        x, y, z = result.expect[0][-1], result.expect[1][-1], result.expect[2][-1]

        ax.scatter([x], [y], [z], c='magenta', s=200)

        # Pulse rainbow protection
        if pulses[frame] > 0:
            ax.scatter([0], [0], [0], c='rainbow', s=500, alpha=0.3)

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Dynamical Decoupling — Eternal Noise-Cancelling Meditative Orbit ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    dynamical_decoupling_visualizer(sequence='XY8')

# End of file: visualizers/dynamical_decoupling_pulses.py

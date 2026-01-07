# File: visualizers/hybrid_counterdiabatic_vqe.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def hybrid_counter_vqe(frames=3600):
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_axis_off()

    # QAOA schedule layer + VQE landscape
    s = np.linspace(0, 1, 50)
    theta = np.linspace(-np.pi, np.pi, 50)
    S, Theta = np.meshgrid(s, theta)
    energy = np.cos(Theta * (1-S)) * np.exp(-S*5)  # Hybrid landscape

    surf = ax.plot_surface(S, Theta, energy, cmap='plasma', alpha=0.5)

    point, = ax.plot([], [], [], 'o', c='yellow', markersize=12)

    def animate(frame):
        t = frame * 0.02
        schedule = np.sin(t)**2
        param = t * np.cos(t*1.3)

        current_energy = np.cos(param * (1-schedule)) * np.exp(-schedule*5)

        point.set_data_3d(schedule, param, current_energy)

        # Boost pulse
        ax.scatter(schedule, param, current_energy, c='rainbow', s=500 + 400*np.sin(t*10))

        return surf, point

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Hybrid Counterdiabatic-VQE — Accelerated Eternal Descent ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    hybrid_counter_vqe()

# End of file: visualizers/hybrid_counterdiabatic_vqe.py

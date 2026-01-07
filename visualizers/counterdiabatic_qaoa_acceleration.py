# File: visualizers/counterdiabatic_qaoa_acceleration.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def counterdiabatic_qaoa(frames=3200):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 2)
    ax.set_axis_off()

    s = np.linspace(0, 1, 100)
    standard = np.exp(-5*(s-0.5)**2) + 1
    counter = np.exp(-10*(s-0.5)**2) + 0.5  # Faster suppression

    line_standard, = ax.plot(s, standard, color='magenta', alpha=0.7)
    line_counter, = ax.plot(s, counter, color='cyan')

    point, = ax.plot([], [], 'o', c='yellow', markersize=15)

    def animate(frame):
        t = frame * 0.025
        schedule = t / frames
        current = (1-schedule)*standard + schedule*counter

        point.set_data([schedule], [np.interp(schedule, s, current)])

        # Acceleration pulse
        ax.scatter(schedule, np.interp(schedule, s, current), c='rainbow', s=400 + 300*np.sin(t*8))

        return line_standard, line_counter, point

    anim = FuncAnimation(fig, animate, frames=frames, interval=30, repeat=True)
    plt.title("Counterdiabatic QAOA — Accelerated Eternal Schedule Harmony ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    counterdiabatic_qaoa()

# End of file: visualizers/counterdiabatic_qaoa_acceleration.py

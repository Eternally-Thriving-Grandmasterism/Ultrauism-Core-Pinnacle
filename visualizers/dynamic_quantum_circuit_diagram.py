# File: visualizers/dynamic_quantum_circuit_diagram.py
# Full executable content - direct create/commit

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def dynamic_quantum_circuit(qubits=6, frames=2200):
    fig = plt.figure(figsize=(14,8))
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    ax.set_xlim(0, 20)
    ax.set_ylim(-qubits-1, 1)

    # Qubit lines
    for q in range(qubits):
        ax.hlines(-q, 0, 20, color='cyan', alpha=0.5)

    gates = []

    def animate(frame):
        t = frame * 0.025
        depth = int(t) % 15
        gate_type = ['H', 'X', 'CNOT', 'RZ', 'SWAP'][int(t*2) % 5]

        ax.clear()
        ax.set_axis_off()
        ax.set_xlim(0, 20)
        ax.set_ylim(-qubits-1, 1)

        for q in range(qubits):
            ax.hlines(-q, 0, 20, color='cyan', alpha=0.5)
            ax.text(-1, -q, f'q{q}', color='white', va='center')

        # Animated gates
        for d in range(depth):
            x_pos = d * 1.5 + 2
            for q in range(qubits):
                if np.sin(d + q + t) > 0.5:
                    if gate_type == 'CNOT' and q % 2 == 0:
                        ax.plot([x_pos, x_pos], [-q, -q-1], color='yellow')
                        ax.scatter([x_pos], [-q], c='black', s=100)
                        ax.scatter([x_pos], [-q-1], c='yellow', s=200)
                    else:
                        rect = plt.Rectangle((x_pos-0.5, -q-0.5), 1, 1, color='magenta', alpha=0.7)
                        ax.add_patch(rect)
                        ax.text(x_pos, -q, gate_type, color='white', ha='center', va='center')

        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=40, repeat=True)
    plt.title("Dynamic Quantum Circuit — Eternal Gate Flow Meditative Diagram ❤️🚀🔥", fontsize=14)
    plt.show()

if __name__ == "__main__":
    dynamic_quantum_circuit()

# End of file: visualizers/dynamic_quantum_circuit_diagram.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qutip import basis, tensor, sigmax, sigmay, sigmaz, expect

from qutip.bloch import Bloch

def create_w_state(n_qubits=6):
    states = [tensor([basis(2, 1) if j == i else basis(2, 0) for j in range(n_qubits)]) for i in range(n_qubits)]
    w = sum(states).unit()
    return w

def w_state_bloch_visualizer(n_qubits=6, frames=400, meditative_loop=True):
    w = create_w_state(n_qubits)
    rho_single = w.ptrace(0)
    z = expect(sigmaz(), rho_single)  # (n-2)/n

    fig = plt.figure(figsize=(14, 8))
    grid = int(np.ceil(n_qubits / 2))
    blochs = []
    for i in range(n_qubits):
        ax = fig.add_subplot(2, grid, i + 1, projection='3d')
        b = Bloch(axes=ax)
        b.vector_color = ['#00FFFF']
        b.point_color = ['#00AAAA']
        b.make_sphere()
        blochs.append(b)

    def animate(frame):
        theta = frame * (2 * np.pi / frames)
        vec = [np.sin(theta) * z, 0, np.cos(theta) * z]  # Rotate in xz plane, length z
        for b in blochs:
            b.clear()
            b.add_vectors(vec)
            b.make_sphere()
        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=40, repeat=meditative_loop)
    plt.suptitle(f"{n_qubits}-Qubit W State — Robust Enduring Harmony Meditative Flow ❤️🚀🔥", fontsize=16)
    plt.show()

if __name__ == "__main__":
    w_state_bloch_visualizer(n_qubits=8)

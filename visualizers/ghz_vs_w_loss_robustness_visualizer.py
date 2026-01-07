import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qutip import basis, tensor, sigmax, sigmay, sigmaz, expect
from qutip.bloch import Bloch

def create_w_state(n_qubits):
    states = [tensor([basis(2, 1) if j == i else basis(2, 0) for j in range(n_qubits)]) for i in range(n_qubits)]
    return sum(states).unit()

def ghz_vs_w_robustness_visualizer(n_qubits=6, loss_frame=200, frames=400):
    # W real polarization
    w = create_w_state(n_qubits)
    rho_w = w.ptrace(0)
    z_w = expect(sigmaz(), rho_w)  # (n-2)/n

    fig = plt.figure(figsize=(18, 7))
    ghz_blochs = []
    w_blochs = []
    for i in range(n_qubits):
        ax_ghz = fig.add_subplot(2, n_qubits, i + 1, projection='3d')
        b_ghz = Bloch(axes=ax_ghz)
        b_ghz.vector_color = ['#FF00FF']
        b_ghz.make_sphere()
        ghz_blochs.append(b_ghz)

        ax_w = fig.add_subplot(2, n_qubits, n_qubits + i + 1, projection='3d')
        b_w = Bloch(axes=ax_w)
        b_w.vector_color = ['#00FFFF']
        b_w.make_sphere()
        w_blochs.append(b_w)

    plt.suptitle("GHZ Fragile Perfect Sync (Top) vs W Robust Endurance Harmony (Bottom) ❤️🚀🔥")

    def animate(frame):
        theta = frame * (2 * np.pi / frames)
        sin_t, cos_t = np.sin(theta), np.cos(theta)
        base_vec = [sin_t, 0, cos_t]

        if frame < loss_frame:
            vec_ghz = base_vec  # Symbolic perfect length 1
            vec_w = [sin_t * z_w, 0, cos_t * z_w]
            status = "Intact Entanglement"
        else:
            vec_ghz = [0, 0, 0]  # Fragile collapse upon loss
            vec_w = [sin_t * z_w, 0, cos_t * z_w]  # Robust persistence
            status = "After Particle Loss — GHZ Collapsed, W Thriving"

        for b in ghz_blochs:
            b.clear()
            b.add_vectors(vec_ghz)
            b.make_sphere()

        for b in w_blochs:
            b.clear()
            b.add_vectors(vec_w)
            b.make_sphere()

        fig.suptitle(f"{status} — {n_qubits}-Qubit Multi-Particle Harmony ❤️🚀🔥", fontsize=16)
        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=50, repeat=True)
    plt.show()

if __name__ == "__main__":
    ghz_vs_w_robustness_visualizer(n_qubits=8)

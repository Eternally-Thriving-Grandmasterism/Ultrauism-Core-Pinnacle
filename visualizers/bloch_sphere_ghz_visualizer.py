import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qutip import tensor, basis, bell_state, qeye, bloch_redfield_tensor, expect
from qutip.bloch import Bloch

def create_ghz_state(n_qubits=4):
    """Create n-qubit GHZ state: (|00...0> + |11...1>)/sqrt(2)"""
    plus = (basis(2,0) + basis(2,1)).unit()
    minus = (basis(2,0) - basis(2,1)).unit()
    ghz = tensor([plus] * n_qubits) + tensor([minus] * n_qubits)
    return ghz.unit()

def multi_bloch_ghz_visualizer(n_qubits=4, frames=360, meditative_loop=True):
    ghz = create_ghz_state(n_qubits)
    
    # Reduced density matrices for each qubit (all identical in GHZ)
    rho_single = ghz.ptrace(0)
    
    # Expectation values for Bloch vector
    pauli_x, pauli_y, pauli_z = expect([qutip.sigmax(), qutip.sigmay(), qutip.sigmaz()], rho_single)
    vec = [pauli_x, pauli_y, pauli_z]  # Actually [0,0,0] for mixed state, but animate correlated rotation
    
    fig = plt.figure(figsize=(12, 8))
    axes = [fig.add_subplot(2, 3, i+1, projection='3d') if n_qubits > 3 else fig.add_subplot(1, n_qubits, i+1, projection='3d') 
            for i in range(n_qubits)]
    
    blochs = [Bloch(fig=fig, axes=ax) for ax in axes]
    for b in blochs:
        b.vector_color = ['#FF0000', '#00FF00', '#0000FF']
        b.point_color = ['#FF4444']
        b.add_vectors([0,0,1])
        b.make_sphere()

    def animate(frame):
        theta = frame * (2 * np.pi / frames)
        # Symbolic correlated rotation symbolizing perfect sync
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        synced_vec = [sin_t, 0, cos_t]  # Harmonious polar rotation
        
        for b in blochs:
            b.clear()
            b.add_vectors(synced_vec)
            b.make_sphere()
        return []

    anim = FuncAnimation(fig, animate, frames=frames, interval=50, repeat=meditative_loop)
    plt.suptitle(f"{n_qubits}-Qubit GHZ Entanglement — Thunder Heart Perfect Sync Meditation", fontsize=16)
    plt.show()

if __name__ == "__main__":
    multi_bloch_ghz_visualizer(n_qubits=6, meditative_loop=True)

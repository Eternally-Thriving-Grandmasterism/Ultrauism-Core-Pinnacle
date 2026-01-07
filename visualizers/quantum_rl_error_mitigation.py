# File: visualizers/quantum_rl_error_mitigation.py
# Full executable content - direct create/commit (Quantum RL with Zero-Noise Extrapolation mitigation)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.transforms import mitigate_with_zne

env = gym.make("CartPole-v1")

n_qubits = 4
dev_noisy = qml.device("default.mixed", wires=n_qubits)  # Simulate noise

# Add depolarizing noise
def add_noise(circuit):
    @qml.qnode(dev_noisy)
    def noisy_circuit(*args, **kwargs):
        circuit(*args, **kwargs)
        for w in range(n_qubits):
            qml.DepolarizingChannel(0.02, wires=w)
        return circuit.return_values
    return noisy_circuit

def state_encoding(state, wires):
    normalized = (state - env.observation_space.low) / (env.observation_space.high - env.observation_space.low + 1e-8)
    angles = 2 * np.pi * normalized - np.pi
    qml.AngleEmbedding(angles, wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(3):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

def base_policy(state, params):
    state_encoding(state, range(n_qubits))
    ansatz(params, range(n_qubits))
    return qml.expval(qml.PauliZ(0))

# Mitigated policy with ZNE (scale factors 1,3,5)
policy_circuit = mitigate_with_zne(base_policy, scale_factors=[1, 3, 5], folding=lambda circuit: qml.transforms.fold_global(circuit, 3))

params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)

episodes = 1500

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    rewards = []
    
    while not done:
        bias = policy_circuit(state, params)
        prob_right = (1 + bias) / 2
        action = 1 if np.random.random() < prob_right else 0
        
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        rewards.append(reward)
        
        state = next_state
    
    if (ep + 1) % 200 == 0:
        print(f"Episode {ep+1}, Reward: {sum(rewards)} (with ZNE mitigation)")

env.close()

# End of file: visualizers/quantum_rl_error_mitigation.py

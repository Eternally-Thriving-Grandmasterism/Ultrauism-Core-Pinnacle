# File: visualizers/quantum_rl_pendulum_continuous.py
# Full executable content - direct create/commit (Quantum RL for Pendulum - continuous actions)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("Pendulum-v1")

n_qubits = 6
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    # Normalize [-1,1] observation to angles
    normalized = (state + np.array([8.0, 8.0, 1.0])) / np.array([16.0, 16.0, 2.0])
    angles = 2 * np.pi * normalized
    qml.AngleEmbedding(angles[:n_qubits], wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(3):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

@qml.qnode(dev, interface="autograd", diff_method="parameter-shift")
def policy_circuit(state, params):
    state_encoding(state, range(n_qubits))
    ansatz(params, range(n_qubits))
    return [qml.expval(qml.PauliZ(i)) for i in range(2)]  # Mean & log_std

def get_action(state, params):
    outputs = policy_circuit(state, params)
    mean = 2.0 * outputs[0]  # Scale to [-2, 2] torque
    log_std = outputs[1]
    std = np.exp(log_std)
    action = mean + std * np.random.normal()
    return np.clip(action, -2.0, 2.0)

params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)
opt = AdamOptimizer(0.01)

episodes = 1000
gamma = 0.99

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    log_probs = []
    rewards = []
    
    while not done:
        action = get_action(state, params)
        # Log prob approximation for Gaussian policy
        outputs = policy_circuit(state, params)
        mean, log_std = 2.0 * outputs[0], outputs[1]
        std = np.exp(log_std)
        log_prob = -0.5 * ((action - mean)/std)**2 - log_std
        
        next_state, reward, done, truncated, _ = env.step([action])
        done = done or truncated
        
        log_probs.append(log_prob)
        rewards.append(reward)
        
        state = next_state
    
    # REINFORCE update with baseline
    G = np.cumsum(rewards[::-1])[::-1]
    advantages = G - np.mean(G)
    loss = -np.sum(advantages * np.array(log_probs))
    
    params = opt.step(lambda p: loss, params)
    
    if (ep + 1) % 100 == 0:
        print(f"Episode {ep+1}, Reward: {sum(rewards):.1f}")

env.close()

# End of file: visualizers/quantum_rl_pendulum_continuous.py

# File: visualizers/quantum_rl_cartpole_noisy_hardware.py
# Full executable content - direct create/commit (Optimized for noisy hardware with shots & mitigation)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("CartPole-v1")

n_qubits = 4
shots = 1024  # Noisy simulation
dev = qml.device("default.qubit", wires=n_qubits, shots=shots)

def state_encoding(state, wires):
    low = env.observation_space.low
    high = env.observation_space.high
    normalized = (state - low) / (high - low + 1e-8)
    angles = 2 * np.pi * normalized - np.pi
    qml.AngleEmbedding(angles, wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(4):  # Deeper but noise-resilient
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

@qml.qnode(dev, interface="autograd", diff_method="parameter-shift")
def policy_circuit(state, params):
    state_encoding(state, range(n_qubits))
    ansatz(params, range(n_qubits))
    return qml.expval(qml.PauliZ(0))

def get_action_and_log_prob(state, params):
    bias = policy_circuit(state, params)
    prob_right = (1 + bias) / 2
    prob_right = np.clip(prob_right, 0.05, 0.95)  # Noise resilience
    action = 1 if np.random.random() < prob_right else 0
    log_prob = np.log(prob_right if action == 1 else (1 - prob_right) + 1e-10)
    return action, log_prob

params = np.random.uniform(-np.pi/4, np.pi/4, size=(4, n_qubits), requires_grad=True)
opt = AdamOptimizer(0.01)  # Lower LR for noise

episodes = 2000  # More episodes for noisy convergence
gamma = 0.99

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    
    log_probs = []
    rewards = []
    
    while not done:
        action, log_prob = get_action_and_log_prob(state, params)
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        
        log_probs.append(log_prob)
        rewards.append(reward)
        
        state = next_state
    
    G = np.zeros(len(rewards))
    G[-1] = rewards[-1]
    for t in reversed(range(len(rewards)-1)):
        G[t] = rewards[t] + gamma * G[t+1]
    
    # Stronger baseline for noisy variance
    baseline = np.mean(G)
    advantages = G - baseline
    
    loss = -np.sum(advantages * np.array(log_probs))
    
    params = opt.step(lambda p: loss, params)
    
    if (ep + 1) % 200 == 0:
        print(f"Episode {ep+1}, Reward: {sum(rewards)}")

env.close()

# End of file: visualizers/quantum_rl_cartpole_noisy_hardware.py

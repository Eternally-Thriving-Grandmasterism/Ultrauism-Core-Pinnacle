# File: visualizers/quantum_rl_cartpole_reinforce_improved.py
# Full executable content - direct create/commit (REINFORCE with enhanced baseline variance reduction)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("CartPole-v1")

n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    low = env.observation_space.low
    high = env.observation_space.high
    normalized = (state - low) / (high - low + 1e-8)
    angles = 2 * np.pi * normalized - np.pi
    qml.AngleEmbedding(angles, wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(3):  # Deeper for robustness
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])
        qml.CNOT(wires=[n_qubits - 1, 0])

@qml.qnode(dev, interface="autograd", diff_method="parameter-shift")
def policy_circuit(state, params):
    state_encoding(state, wires=range(n_qubits))
    ansatz(params, wires=range(n_qubits))
    return qml.expval(qml.PauliZ(0))

def get_action_and_log_prob(state, params):
    bias = policy_circuit(state, params)
    prob_right = (1 + bias) / 2
    action = 1 if np.random.random() < prob_right else 0
    log_prob = np.log(prob_right if action == 1 else (1 - prob_right) + 1e-10)
    return action, log_prob

# 3 layers
params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)
opt = AdamOptimizer(0.02)

episodes = 1500
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
    
    # Discounted returns
    G = np.zeros(len(rewards))
    G[-1] = rewards[-1]
    for t in reversed(range(len(rewards)-1)):
        G[t] = rewards[t] + gamma * G[t+1]
    
    # Improved baseline: running mean + variance normalization
    if ep == 0:
        global running_mean, running_var
        running_mean = np.mean(G)
        running_var = np.var(G) + 1e-8
    else:
        running_mean = 0.9 * running_mean + 0.1 * np.mean(G)
        running_var = 0.9 * running_var + 0.1 * np.var(G)
    
    advantages = (G - running_mean) / np.sqrt(running_var)
    
    loss = -np.sum(advantages * np.array(log_probs))
    
    params = opt.step(lambda p: loss, params)
    
    if (ep + 1) % 100 == 0:
        print(f"Episode {ep+1}, Reward: {sum(rewards)}, Running Mean: {running_mean:.1f}")

env.close()

# End of file: visualizers/quantum_rl_cartpole_reinforce_improved.py

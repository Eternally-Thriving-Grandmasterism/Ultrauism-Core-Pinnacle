# File: visualizers/quantum_rl_mountaincar_reinforce.py
# Full executable content - direct create/commit (Quantum RL REINFORCE for MountainCar-v0)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("MountainCar-v0")

n_qubits = 6  # More qubits for 2D state + actions
n_actions = env.action_space.n  # 3 actions
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    # Normalize position [-1.2, 0.6] and velocity [-0.07, 0.07]
    pos_norm = (state[0] + 1.2) / 1.8
    vel_norm = (state[1] + 0.07) / 0.14
    angles = 2 * np.pi * np.array([pos_norm, vel_norm])
    qml.AngleEmbedding(np.tile(angles, n_qubits // 2), wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(3):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])
        qml.CNOT(wires=[n_qubits - 1, 0])

@qml.qnode(dev, interface="autograd", diff_method="parameter-shift")
def policy_circuit(state, params):
    state_encoding(state, range(n_qubits))
    ansatz(params, range(n_qubits))
    # Measure expectations on first log2(3)≈2 qubits for softmax probs
    return [qml.expval(qml.PauliZ(i)) for i in range(3)]

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()

def get_action_and_log_prob(state, params):
    expectations = policy_circuit(state, params)
    probs = softmax(expectations)
    action = np.random.choice(n_actions, p=probs)
    log_prob = np.log(probs[action] + 1e-10)
    return action, log_prob

params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)
opt = AdamOptimizer(0.02)

episodes = 2000  # MountainCar needs more episodes
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
    
    # Discounted returns + baseline
    G = np.zeros(len(rewards))
    G[-1] = rewards[-1]
    for t in reversed(range(len(rewards)-1)):
        G[t] = rewards[t] + gamma * G[t+1]
    
    baseline = np.mean(G)
    advantages = G - baseline
    
    loss = -np.sum(advantages * np.array(log_probs))
    
    params = opt.step(lambda p: loss, params)
    
    if (ep + 1) % 200 == 0:
        print(f"Episode {ep+1}, Total Reward: {sum(rewards):.1f} (goal ~ -110)")

env.close()

# End of file: visualizers/quantum_rl_mountaincar_reinforce.py

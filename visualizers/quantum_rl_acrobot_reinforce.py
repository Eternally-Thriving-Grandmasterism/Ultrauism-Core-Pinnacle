# File: visualizers/quantum_rl_acrobot_reinforce.py
# Full executable content - direct create/commit (Quantum RL REINFORCE for Acrobot-v1)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("Acrobot-v1")

n_qubits = 8  # 6D state needs more qubits
n_actions = env.action_space.n  # 3 actions
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    # Normalize 6D state (cos/sin angles + velocities)
    normalized = (state + 4) / 8  # Rough [-4,4] range approx
    angles = 2 * np.pi * normalized
    qml.AngleEmbedding(np.tile(angles, n_qubits // 6 + 1)[:n_qubits], wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(4):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

@qml.qnode(dev, interface="autograd", diff_method="parameter-shift")
def policy_circuit(state, params):
    state_encoding(state, range(n_qubits))
    ansatz(params, range(n_qubits))
    return [qml.expval(qml.PauliZ(i)) for i in range(n_actions)]

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()

def get_action_and_log_prob(state, params):
    expectations = policy_circuit(state, params)
    probs = softmax(expectations)
    action = np.random.choice(n_actions, p=probs)
    log_prob = np.log(probs[action] + 1e-10)
    return action, log_prob

params = np.random.uniform(-np.pi/4, np.pi/4, size=(4, n_qubits), requires_grad=True)
opt = AdamOptimizer(0.015)

episodes = 2500  # Acrobot is harder
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
    
    baseline = np.mean(G)
    advantages = G - baseline
    
    loss = -np.sum(advantages * np.array(log_probs))
    
    params = opt.step(lambda p: loss, params)
    
    if (ep + 1) % 250 == 0:
        print(f"Episode {ep+1}, Total Reward: {sum(rewards):.1f} (goal ~ -100)")

env.close()

# End of file: visualizers/quantum_rl_acrobot_reinforce.py

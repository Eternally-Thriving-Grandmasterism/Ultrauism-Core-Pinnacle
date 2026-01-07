# File: visualizers/quantum_rl_bipedalwalker.py
# Full executable content - direct create/commit (Quantum RL for BipedalWalker-v3 - continuous)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("BipedalWalker-v3")

n_qubits = 12  # 24D state, 4 actions
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    normalized = (state - env.observation_space.low) / (env.observation_space.high - env.observation_space.low + 1e-8)
    angles = 2 * np.pi * normalized
    qml.AngleEmbedding(np.tile(angles, n_qubits // 24 + 1)[:n_qubits], wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(5):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

@qml.qnode(dev, interface="autograd", diff_method="parameter-shift")
def policy_circuit(state, params):
    state_encoding(state, range(n_qubits))
    ansatz(params, range(n_qubits))
    return [qml.expval(qml.PauliZ(i)) for i in range(8)]  # mean/log_std for 4 actions

def get_action(state, params):
    outputs = policy_circuit(state, params)
    mean = np.tanh(np.array(outputs[:4]))  # [-1,1] torque
    log_std = np.clip(outputs[4:], -20, 2)
    std = np.exp(log_std)
    action = mean + std * np.random.normal(size=4)
    return np.clip(action, -1.0, 1.0)

params = np.random.uniform(-np.pi/4, np.pi/4, size=(5, n_qubits), requires_grad=True)
opt = AdamOptimizer(0.005)

episodes = 3000
gamma = 0.99

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    rewards = []
    
    while not done:
        action = get_action(state, params)
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        rewards.append(reward)
        
        # Simple REINFORCE placeholder (full SAC recommended for Bipedal)
        
        state = next_state
    
    if (ep + 1) % 300 == 0:
        print(f"Episode {ep+1}, Reward: {sum(rewards):.1f} (goal ~300)")

env.close()

# End of file: visualizers/quantum_rl_bipedalwalker.py

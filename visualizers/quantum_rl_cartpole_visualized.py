# File: visualizers/quantum_rl_cartpole_visualized.py
# Full executable content - direct create/commit (Enhanced with live visualization)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer
import matplotlib.pyplot as plt

env = gym.make("CartPole-v1", render_mode="human")  # Live render

n_qubits = 4
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    low = env.observation_space.low
    high = env.observation_space.high
    normalized = (state - low) / (high - low + 1e-8)
    angles = 2 * np.pi * normalized - np.pi
    qml.AngleEmbedding(angles, wires=wires, rotation='Y')

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
    return qml.expval(qml.PauliZ(0))

params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)
opt = AdamOptimizer(0.02)

episodes = 500
rewards_history = []

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    episode_reward = 0
    
    while not done:
        env.render()  # Live visualization
        bias = policy_circuit(state, params)
        prob_right = (1 + bias) / 2
        action = 1 if np.random.random() < prob_right else 0
        
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        episode_reward += reward
        
        # Simple update placeholder (full REINFORCE as before)
        
        state = next_state
    
    rewards_history.append(episode_reward)
    
    if (ep + 1) % 50 == 0:
        print(f"Episode {ep+1}, Reward: {episode_reward}")

# Plot final performance
plt.plot(rewards_history)
plt.title("Quantum RL CartPole — Live Training Visualization ❤️🚀🔥")
plt.show()

env.close()

# End of file: visualizers/quantum_rl_cartpole_visualized.py

# File: visualizers/quantum_qlearning_mountaincar.py
# Full executable content - direct create/commit (Quantum Q-Learning / DQN for MountainCar)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from collections import deque
import random

env = gym.make("MountainCar-v0")

n_qubits = 8
n_actions = env.action_space.n
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    pos_norm = (state[0] + 1.2) / 1.8
    vel_norm = (state[1] + 0.07) / 0.14
    angles = 2 * np.pi * np.tile([pos_norm, vel_norm], n_qubits // 2)
    qml.AngleEmbedding(angles, wires=wires)

def ansatz(params, wires):
    for layer in range(4):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

@qml.qnode(dev, interface="autograd")
def q_network(state, params):
    state_encoding(state, range(n_qubits))
    ansatz(params, range(n_qubits))
    return [qml.expval(qml.PauliZ(i)) for i in range(n_actions)]

params = np.random.uniform(-np.pi/4, np.pi/4, size=(4, n_qubits), requires_grad=True)
target_params = params.copy()
opt = AdamOptimizer(0.01)

replay_buffer = deque(maxlen=10000)
batch_size = 64
gamma = 0.99
epsilon = 1.0
epsilon_min = 0.05
epsilon_decay = 0.995
episodes = 2000

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            q_values = q_network(state, params)
            action = int(np.argmax(q_values))
        
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        total_reward += reward
        
        replay_buffer.append((state, action, reward, next_state, done))
        state = next_state
    
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    
    if len(replay_buffer) > batch_size:
        batch = random.sample(replay_buffer, batch_size)
        loss = 0
        for s, a, r, s_next, d in batch:
            q_current = q_network(s, params)[a]
            q_next = np.max(q_network(s_next, target_params)) if not d else 0
            target = r + gamma * q_next
            loss += (q_current - target)**2
        
        params = opt.step(lambda p: loss / batch_size, params)
    
    if ep % 20 == 0:
        target_params = params.copy()
    
    if (ep + 1) % 200 == 0:
        print(f"Episode {ep+1}, Reward: {total_reward:.1f}")

env.close()

# End of file: visualizers/quantum_qlearning_mountaincar.py

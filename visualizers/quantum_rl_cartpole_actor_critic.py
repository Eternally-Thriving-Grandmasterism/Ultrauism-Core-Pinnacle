# File: visualizers/quantum_rl_cartpole_actor_critic.py
# Full executable content - direct create/commit (Quantum Actor-Critic variant)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("CartPole-v1")

n_qubits = 4
dev_actor = qml.device("default.qubit", wires=n_qubits, shots=None)
dev_critic = qml.device("default.qubit", wires=n_qubits, shots=None)

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

@qml.qnode(dev_actor, interface="autograd", diff_method="parameter-shift")
def actor_circuit(state, actor_params):
    state_encoding(state, range(n_qubits))
    ansatz(actor_params, range(n_qubits))
    return qml.expval(qml.PauliZ(0))

@qml.qnode(dev_critic, interface="autograd", diff_method="parameter-shift")
def critic_circuit(state, critic_params):
    state_encoding(state, range(n_qubits))
    ansatz(critic_params, range(n_qubits))
    return qml.expval(qml.PauliZ(0))  # Value estimate

actor_params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)
critic_params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)

actor_opt = AdamOptimizer(0.01)
critic_opt = AdamOptimizer(0.03)

episodes = 1000
gamma = 0.99

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    
    while not done:
        bias = actor_circuit(state, actor_params)
        prob_right = (1 + bias) / 2
        action = 1 if np.random.random() < prob_right else 0
        log_prob = np.log(prob_right if action == 1 else (1 - prob_right) + 1e-10)
        
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        
        value = critic_circuit(state, critic_params)
        next_value = critic_circuit(next_state, critic_params) if not done else 0.0
        
        td_error = reward + gamma * next_value - value
        
        # Critic update
        critic_loss = td_error ** 2
        critic_params = critic_opt.step(lambda p: critic_loss, critic_params)
        
        # Actor update
        actor_loss = -log_prob * td_error
        actor_params = actor_opt.step(lambda p: actor_loss, actor_params)
        
        state = next_state
    
    if (ep + 1) % 100 == 0:
        print(f"Episode {ep+1} complete")

env.close()

# End of file: visualizers/quantum_rl_cartpole_actor_critic.py

# File: visualizers/quantum_rl_lunarlander_actor_critic.py
# Full executable content - direct create/commit (Quantum Actor-Critic for LunarLander-v2)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("LunarLander-v2")

n_qubits = 10  # 8D state needs more capacity
n_actions = env.action_space.n  # 4 discrete actions
dev_actor = qml.device("default.qubit", wires=n_qubits, shots=None)
dev_critic = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    # Normalize 8D state
    normalized = (state - env.observation_space.low) / (env.observation_space.high - env.observation_space.low + 1e-8)
    angles = 2 * np.pi * normalized
    qml.AngleEmbedding(np.tile(angles, n_qubits // 8 + 1)[:n_qubits], wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(4):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

@qml.qnode(dev_actor, interface="autograd", diff_method="parameter-shift")
def actor_circuit(state, actor_params):
    state_encoding(state, range(n_qubits))
    ansatz(actor_params, range(n_qubits))
    return [qml.expval(qml.PauliZ(i)) for i in range(n_actions)]

@qml.qnode(dev_critic, interface="autograd", diff_method="parameter-shift")
def critic_circuit(state, critic_params):
    state_encoding(state, range(n_qubits))
    ansatz(critic_params, range(n_qubits))
    return qml.expval(qml.PauliZ(0))

def softmax(x):
    e = np.exp(x - np.max(x))
    return e / e.sum()

actor_params = np.random.uniform(-np.pi/4, np.pi/4, size=(4, n_qubits), requires_grad=True)
critic_params = np.random.uniform(-np.pi/4, np.pi/4, size=(4, n_qubits), requires_grad=True)

actor_opt = AdamOptimizer(0.005)
critic_opt = AdamOptimizer(0.01)

episodes = 2000
gamma = 0.99

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    
    while not done:
        probs_raw = actor_circuit(state, actor_params)
        probs = softmax(probs_raw)
        action = np.random.choice(n_actions, p=probs)
        log_prob = np.log(probs[action] + 1e-10)
        
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
    
    if (ep + 1) % 200 == 0:
        print(f"Episode {ep+1} complete (LunarLander goal ~200)")

env.close()

# End of file: visualizers/quantum_rl_lunarlander_actor_critic.py

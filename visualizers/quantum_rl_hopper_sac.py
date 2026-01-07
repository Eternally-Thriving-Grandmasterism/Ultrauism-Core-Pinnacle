# File: visualizers/quantum_rl_hopper_sac.py
# Full executable content - direct create/commit (Quantum SAC for Hopper-v3 - continuous control)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("Hopper-v3")

n_qubits = 14  # 11D state + 3 actions needs capacity
dev_actor = qml.device("default.qubit", wires=n_qubits, shots=None)
dev_critic = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    # Normalize 11D state
    low = env.observation_space.low
    high = env.observation_space.high
    normalized = (state - low) / (high - low + 1e-8)
    angles = 2 * np.pi * normalized
    qml.AngleEmbedding(np.tile(angles, n_qubits // 11 + 1)[:n_qubits], wires=wires, rotation='Y')

def ansatz(params, wires):
    for layer in range(5):
        for i in range(n_qubits):
            qml.RY(params[layer, i], wires=i)
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])

@qml.qnode(dev_actor, interface="autograd", diff_method="parameter-shift")
def actor_circuit(state, actor_params):
    state_encoding(state, range(n_qubits))
    ansatz(actor_params, range(n_qubits))
    return [qml.expval(qml.PauliZ(i)) for i in range(6)]  # mean/log_std for 3 actions

@qml.qnode(dev_critic, interface="autograd", diff_method="parameter-shift")
def critic_circuit(state_action, critic_params):
    state = state_action[:-3]
    action = state_action[-3:]
    state_encoding(state, range(n_qubits))
    # Action encoding on last wires
    qml.RY(action[0], wires=n_qubits-3)
    qml.RY(action[1], wires=n_qubits-2)
    qml.RY(action[2], wires=n_qubits-1)
    ansatz(critic_params, range(n_qubits))
    return qml.expval(qml.PauliZ(0))

actor_params = np.random.uniform(-np.pi/4, np.pi/4, size=(5, n_qubits), requires_grad=True)
critic1_params = np.random.uniform(-np.pi/4, np.pi/4, size=(5, n_qubits), requires_grad=True)
critic2_params = critic1_params.copy()
target_critic1 = critic1_params.copy()
target_critic2 = critic2_params.copy()

actor_opt = AdamOptimizer(0.001)
critic_opt = AdamOptimizer(0.003)

alpha = np.array([0.2], requires_grad=True)
alpha_opt = AdamOptimizer(0.01)

episodes = 4000
gamma = 0.99
tau = 0.005
target_entropy = -3.0  # For 3D action

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    
    while not done:
        outputs = actor_circuit(state, actor_params)
        mean = np.tanh(np.array(outputs[:3]))  # [-1,1] range approx
        log_std = np.clip(outputs[3:], -20, 2)
        std = np.exp(log_std)
        
        dist = np.random.normal(mean, std)
        action = np.tanh(dist)
        log_prob = -0.5 * np.sum(((dist - mean)/std)**2) - np.sum(log_std)
        
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        
        q1 = critic_circuit(np.concatenate([state, action]), critic1_params)
        q2 = critic_circuit(np.concatenate([state, action]), critic2_params)
        q = np.minimum(q1, q2)
        
        next_outputs = actor_circuit(next_state, actor_params)
        next_mean = np.tanh(np.array(next_outputs[:3]))
        next_log_std = np.clip(next_outputs[3:], -20, 2)
        next_std = np.exp(next_log_std)
        next_dist = np.random.normal(next_mean, next_std)
        next_action = np.tanh(next_dist)
        next_log_prob = -0.5 * np.sum(((next_dist - next_mean)/next_std)**2) - np.sum(next_log_std)
        
        target_q1 = critic_circuit(np.concatenate([next_state, next_action]), target_critic1)
        target_q2 = critic_circuit(np.concatenate([next_state, next_action]), target_critic2)
        target_q = np.minimum(target_q1, target_q2) - alpha * next_log_prob
        y = reward + gamma * target_q * (1 - done)
        
        critic_loss = (q - y)**2
        
        critic1_params = critic_opt.step(lambda p: critic_loss, critic1_params)
        critic2_params = critic_opt.step(lambda p: critic_loss, critic2_params)
        
        actor_loss = (alpha * log_prob - q)
        actor_params = actor_opt.step(lambda p: actor_loss, actor_params)
        
        alpha_loss = -alpha * (log_prob + target_entropy)
        alpha = alpha_opt.step(lambda a: alpha_loss, alpha)
        
        target_critic1 = tau * critic1_params + (1 - tau) * target_critic1
        target_critic2 = tau * critic2_params + (1 - tau) * target_critic2
        
        state = next_state
    
    if (ep + 1) % 400 == 0:
        print(f"Episode {ep+1} complete (Hopper goal ~3000+)")

env.close()

# End of file: visualizers/quantum_rl_hopper_sac.py

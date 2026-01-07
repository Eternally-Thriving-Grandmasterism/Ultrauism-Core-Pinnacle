# File: visualizers/quantum_sac_lunarlander.py
# Full executable content - direct create/commit (Quantum Soft Actor-Critic for LunarLanderContinuous-v2)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("LunarLanderContinuous-v2")

n_qubits = 10
dev_actor = qml.device("default.qubit", wires=n_qubits, shots=None)
dev_critic = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
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
    return [qml.expval(qml.PauliZ(i)) for i in range(4)]  # mean/log_std for 2 actions

@qml.qnode(dev_critic, interface="autograd", diff_method="parameter-shift")
def critic_circuit(state_action, critic_params):
    state_encoding(state_action[:-2], range(n_qubits))  # state + action concat
    # Simple action encoding
    qml.RY(state_action[-2], wires=0)
    qml.RY(state_action[-1], wires=1)
    ansatz(critic_params, range(n_qubits))
    return qml.expval(qml.PauliZ(0))

actor_params = np.random.uniform(-np.pi/4, np.pi/4, size=(4, n_qubits), requires_grad=True)
critic1_params = np.random.uniform(-np.pi/4, np.pi/4, size=(4, n_qubits), requires_grad=True)
critic2_params = critic1_params.copy()
target_critic1 = critic1_params.copy()
target_critic2 = critic2_params.copy()

actor_opt = AdamOptimizer(0.001)
critic_opt = AdamOptimizer(0.003)

alpha = np.array([0.2], requires_grad=True)  # Entropy temp
alpha_opt = AdamOptimizer(0.01)

episodes = 3000
gamma = 0.99
tau = 0.005
target_entropy = -2.0  # For 2D action

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    
    while not done:
        outputs = actor_circuit(state, actor_params)
        mean = np.tanh(np.array(outputs[:2])) * 2  # Scale to [-2,2]
        log_std = np.clip(outputs[2:], -20, 2)
        std = np.exp(log_std)
        
        dist = np.random.normal(mean, std)
        action = np.tanh(dist) * 2  # Reparameterization
        log_prob = -0.5 * np.sum(((dist - mean)/std)**2) - np.sum(log_std)
        
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        
        # Double Q
        q1 = critic_circuit(np.concatenate([state, action]), critic1_params)
        q2 = critic_circuit(np.concatenate([state, action]), critic2_params)
        q = np.minimum(q1, q2)
        
        # Target
        next_outputs = actor_circuit(next_state, actor_params)
        next_mean = np.tanh(np.array(next_outputs[:2])) * 2
        next_log_std = np.clip(next_outputs[2:], -20, 2)
        next_std = np.exp(next_log_std)
        next_dist = np.random.normal(next_mean, next_std)
        next_action = np.tanh(next_dist) * 2
        next_log_prob = -0.5 * np.sum(((next_dist - next_mean)/next_std)**2) - np.sum(next_log_std)
        
        target_q1 = critic_circuit(np.concatenate([next_state, next_action]), target_critic1)
        target_q2 = critic_circuit(np.concatenate([next_state, next_action]), target_critic2)
        target_q = np.minimum(target_q1, target_q2) - alpha * next_log_prob
        y = reward + gamma * target_q * (1 - done)
        
        # Critic loss
        critic_loss = (q - y)**2
        
        critic1_params = critic_opt.step(lambda p: critic_loss, critic1_params)
        critic2_params = critic_opt.step(lambda p: critic_loss, critic2_params)
        
        # Actor & alpha
        actor_loss = (alpha * log_prob - q)
        actor_params = actor_opt.step(lambda p: actor_loss, actor_params)
        
        alpha_loss = -alpha * (log_prob + target_entropy)
        alpha = alpha_opt.step(lambda a: alpha_loss, alpha)
        
        # Soft target update
        target_critic1 = tau * critic1_params + (1 - tau) * target_critic1
        target_critic2 = tau * critic2_params + (1 - tau) * target_critic2
        
        state = next_state
    
    if (ep + 1) % 300 == 0:
        print(f"Episode {ep+1} complete (SAC LunarLander goal ~200+)")

env.close()

# End of file: visualizers/quantum_sac_lunarlander.py

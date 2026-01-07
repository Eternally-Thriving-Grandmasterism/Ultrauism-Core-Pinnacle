# File: visualizers/quantum_ppo_cartpole.py
# Full executable content - direct create/commit (Simplified Quantum PPO for CartPole)

import gymnasium as gym
import pennylane as qml
from pennylane import numpy as np
from pennylane.optimize import AdamOptimizer

env = gym.make("CartPole-v1")

n_qubits = 6
dev = qml.device("default.qubit", wires=n_qubits, shots=None)

def state_encoding(state, wires):
    normalized = (state - env.observation_space.low) / (env.observation_space.high - env.observation_space.low + 1e-8)
    angles = 2 * np.pi * normalized
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

old_params = np.random.uniform(-np.pi/4, np.pi/4, size=(3, n_qubits), requires_grad=True)
params = old_params.copy()
opt = AdamOptimizer(0.01)

clip_eps = 0.2
episodes = 1500
gamma = 0.99
gae_lambda = 0.95

for ep in range(episodes):
    state, _ = env.reset()
    done = False
    
    states = []
    actions = []
    old_probs = []
    rewards = []
    
    while not done:
        bias = policy_circuit(state, old_params)
        prob_right = (1 + bias) / 2
        action = 1 if np.random.random() < prob_right else 0
        old_log_prob = np.log(prob_right if action == 1 else (1 - prob_right) + 1e-10)
        
        next_state, reward, done, truncated, _ = env.step(action)
        done = done or truncated
        
        states.append(state)
        actions.append(action)
        old_probs.append(old_log_prob)
        rewards.append(reward)
        
        state = next_state
    
    # GAE advantages
    values = [policy_circuit(s, params) for s in states]  # Approx value from policy bias
    advantages = np.zeros(len(rewards))
    gae = 0
    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * (values[t+1] if t+1 < len(values) else 0) - values[t]
        gae = delta + gamma * gae_lambda * gae
        advantages[t] = gae
    
    # PPO clipped loss
    def ppo_loss(params):
        loss = 0
        for s, a, old_p, adv in zip(states, actions, old_probs, advantages):
            bias = policy_circuit(s, params)
            prob_right = (1 + bias) / 2
            new_log_prob = np.log(prob_right if a == 1 else (1 - prob_right) + 1e-10)
            ratio = np.exp(new_log_prob - old_p)
            clipped = np.clip(ratio, 1-clip_eps, 1+clip_eps) * adv
            loss -= np.minimum(ratio * adv, clipped)
        return loss / len(states)
    
    params = opt.step(ppo_loss, params)
    
    # Update old params periodically
    if ep % 10 == 0:
        old_params = params.copy()
    
    if (ep + 1) % 200 == 0:
        print(f"Episode {ep+1}, Reward: {sum(rewards)}")

env.close()

# End of file: visualizers/quantum_ppo_cartpole.py

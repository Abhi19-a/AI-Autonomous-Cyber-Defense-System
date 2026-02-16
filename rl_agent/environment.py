import gymnasium as gym
from gymnasium import spaces
import numpy as np
import networkx as nx 
import random

from simulation.network_model import NetworkModel
from simulation.attack_simulator import AttackSimulator

class NetworkDefenseEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, num_nodes=10):
        super(NetworkDefenseEnv, self).__init__()
        self.num_nodes = num_nodes
        
        # Actions: 
        # 0: No Op
        # 1..N: Isolate Node i-1
        # N+1..2N: Restore/Patch Node i-(N+1)
        self.action_space = spaces.Discrete(1 + 2 * self.num_nodes)
        
        # Observation: 
        # Status of each node: 0=Normal, 1=Compromised, 2=Isolated
        # This is a MultiDiscrete space where each element can be 0, 1, or 2
        self.observation_space = spaces.MultiDiscrete([3] * self.num_nodes)

        self.network = None
        self.attack_sim = None
        self.max_steps = 100
        self.current_step = 0
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.network = NetworkModel(num_nodes=self.num_nodes)
        self.attack_sim = AttackSimulator(self.network)
        self.current_step = 0
        
        obs = self.get_observation()
        info = {}
        return obs, info

    def get_observation(self):
        # Convert string statuses to integers
        raw_states = self.network.get_state_vector()
        return np.array(raw_states, dtype=np.int32)

    def step(self, action):
        # 1. Execute Defense Action
        terminated = False
        truncated = False
        reward = 0
        
        if action == 0:
            pass # No Op
        elif 1 <= action <= self.num_nodes:
            # Isolate
            node_idx = action - 1
            node = self.network.graph.nodes[node_idx]
            if node['status'] != 'isolated':
                self.network.isolate_node(node_idx)
                # Small penalty for isolation (service disruption)
                reward -= 1 
        elif self.num_nodes < action <= 2 * self.num_nodes:
            # Restore/Patch
            node_idx = action - (self.num_nodes + 1)
            node = self.network.graph.nodes[node_idx]
            # Restoration takes time/effort
            self.network.restore_node(node_idx)
            reward -= 0.5 # Cost of patching

        # 2. Run Attack Step
        self.attack_sim.run_random_attack_step()

        # 3. Calculate Reward
        obs = self.get_observation()
        
        # Count states
        normal_count = np.sum(obs == 0)
        compromised_count = np.sum(obs == 1)
        isolated_count = np.sum(obs == 2)
        
        # Reward logic: Try to maximize normal nodes, heavily penalize compromised
        reward += (normal_count * 1.0)
        reward -= (compromised_count * 5.0)
        reward -= (isolated_count * 0.5) # Disruption penalty

        # Check termination
        self.current_step += 1
        if self.current_step >= self.max_steps:
            truncated = True
        
        # If all nodes compromised, terminate with huge penalty
        if compromised_count == self.num_nodes:
            terminated = True
            reward -= 100

        info = {
            "compromised": compromised_count,
            "isolated": isolated_count
        }
        
        return obs, reward, terminated, truncated, info

    def render(self):
        print(f"Step: {self.current_step}")
        print(f"Nodes: {self.get_observation()}")

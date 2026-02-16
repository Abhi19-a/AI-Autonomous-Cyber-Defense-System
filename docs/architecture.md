# AI Autonomous Cyber Defense System Architecture

## Overview
This system simulates a virtual network under various cyber attacks and employs both rule-based and Reinforcement Learning (RL) agents to defend it autonomously. The architecture is modular, separating the simulation environment, the AI decision-making, and the execution of defense strategies.

## Modules

### 1. Simulation (`simulation/`)
- **NetworkModel (`network_model.py`)**: Represents the network as a directed graph using `NetworkX`. Nodes have properties like OS, role, vulnerabilities, and status. Edges represent connections with protocols and firewall rules.
- **AttackSimulator (`attack_simulator.py`)**: Simulates red-team activities:
  - **DDoS**: Overloads nodes traffic capacity.
  - **SQL Injection**: Exploits vulnerabilities in database/server nodes.
  - **Lateral Movement**: Spreads infection to adjacent nodes.

### 2. Reinforcement Learning Agent (`rl_agent/`)
- **NetworkDefenseEnv (`environment.py`)**: An OpenAI Gym (Gymnasium) environment that wraps the `NetworkModel`.
  - **Observation**: Status vector of all nodes (Normal, Compromised, Isolated).
  - **Action**: Discrete actions to Isolate or Restore specific nodes.
  - **Reward**: Calculated based on network health (service availability vs. compromise).
- **RLAgent (`agent_model.py`)**: Uses **Stable-Baselines3** (PPO/DQN) to train a policy that maximizes the reward.

### 3. Defense Engine (`defense_engine/`)
- **SelfHealingSystem (`self_healing.py`)**: A rule-based autonomous system that:
  - Continuously monitors node health.
  - Isolates compromised nodes immediately to prevent spread.
  - Attempts to restore services after patching.
- **RiskEngine (`risk_engine.py`)**: Calculates dynamic risk scores based on node criticality, vulnerability count, and neighbor compromise status.

### 4. Visualization & API (`visualization/`, `api/`)
- **GraphVisualizer (`graph_visualizer.py`)**: Uses `matplotlib` to render the network graph, coloring nodes by status (Green=Safe, Red=Compromised, Gray=Isolated).
- **API (`main.py`)**: A Flask REST API to control the simulation, trigger attacks, view state, and integrate with a frontend dashboard.

## Data Flow
1.  **Simulation Loop**: The environment steps forward.
2.  **Attack**: `AttackSimulator` attempts to compromise nodes based on probabilities.
3.  **Observation**: The system observes the new state (e.g., Node 5 is compromised).
4.  **Decision**:
    - **RL Agent**: Predicts the best action (e.g., Isolate Node 5) to maximize long-term reward.
    - **Self-Healing**: Checks if risk > threshold and applies immediate fixes.
5.  **Execution**: The `NetworkModel` updates node statuses and edge availability.
6.  **Feedback**: Risk score is updated, and the cycle continues.

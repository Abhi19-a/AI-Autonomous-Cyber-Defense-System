# Research Summary: Reinforcement Learning for Autonomous Cyber Defense

## Overview
Reinforcement Learning (RL) is transforming cyber defense by enabling autonomous agents to learn optimal strategies through interaction with simulated network environments. Unlike static rule-based systems, RL agents can adapt to novel and evolving attack patterns.

## Key Findings

### 1. Algorithms
- **Deep Q-Networks (DQN)**: Effective for discrete action spaces, such as choosing specific defense mechanisms (e.g., blocking a port, isolating a node).
- **Proximal Policy Optimization (PPO)**: Suitable for continuous or large action spaces, offering stable training for complex network configurations.
- **Multi-Agent RL (MARL)**: essential for large-scale networks where multiple defenders must coordinate to protect different segments.

### 2. Simulation Environments
Realistic simulations are critical for training:
- **CybORG (Cyber Operations Research Gym)**: Simulates enterprise networks with red (attacker) and blue (defender) agents.
- **CyberBattleSim**: Microsoft's toolkit for modeling lateral movement and defense using RL.
- **Yawning Titan**: Focuses on abstract graph-based network defense scenarios.

### 3. Challenges
- **State Space Explosion**: Representing the full state of a large network is computationally expensive.
- **Sim-to-Real Gap**: Transferring policies trained in simulation to real hardware remains difficult due to noise and unmodeled dynamics.
- **Adversarial Attacks on RL**: Attackers may exploit the RL agent's learning process itself.

## Application in Project
This project utilizes **Stable-Baselines3 (PPO/DQN)** within an **OpenAI Gym-style** custom environment to train a defensive agent. The environment models the network as a graph (NetworkX), allowing the agent to observe node states (compromised, healthy) and take actions (isolate, patch).

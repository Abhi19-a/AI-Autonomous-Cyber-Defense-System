# AI Autonomous Cyber Defense System

A comprehensive simulation and defense platform that uses Reinforcement Learning (RL) and self-healing mechanisms to protect virtual networks from cyber attacks.

## Features
- **Virtual Network Simulation**: Graph-based modeling of nodes (servers, clients, DBs) and connections using `NetworkX`.
- **Attack Simulation**: Realistic simulation of DDoS, SQL Injection, and Lateral Movement.
- **Autonomous Defense**:
  - **RL Agent**: Trained using PPO (Proximal Policy Optimization) to make optimal defense decisions.
  - **Self-Healing**: Automatic isolation of infected nodes and service restoration.
- **Risk Assessment**: Real-time risk scoring engine.
- **Visualization**: Dynamic graph visualization of network state.
- **API**: Flask-based REST API for integration.

## Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 1. Training the RL Agent
Train the autonomous defense agent:
```bash
python -m rl_agent.train
```
This will save the model to `rl_agent/models/`.

### 2. Running the API Simulation
Start the simulation server:
```bash
python -m api.main
```
The API will be available at `http://localhost:5000`.

### 3. API Endpoints
- `GET /api/state`: Get current network status.
- `POST /api/step`: Advance simulation by one step.
- `POST /api/attack`: Trigger an attack on a specific node.
- `GET /api/visualize`: Get a visualization of the network graph.

## Research
The `research_papers/` folder contains summaries of key papers on:
- Reinforcement Learning in Cyber Defense
- Self-Healing Networks

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed design.

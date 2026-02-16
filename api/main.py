from flask import Flask, jsonify, request, send_from_directory
import sys
import os

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.network_model import NetworkModel
from simulation.attack_simulator import AttackSimulator
from defense_engine.self_healing import SelfHealingSystem
from defense_engine.risk_engine import RiskEngine
from visualization.graph_visualizer import GraphVisualizer
from rl_agent.agent_model import RLAgent
from rl_agent.environment import NetworkDefenseEnv
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
network = NetworkModel(num_nodes=15)
attack_sim = AttackSimulator(network)
defense_sys = SelfHealingSystem(network)
risk_engine = RiskEngine(network)
visualizer = GraphVisualizer(network)

# Try to load RL Agent
# Note: In a real scenario, you'd load a trained model. 
# Here we'll just instantiate the class, but prediction might fail if model not loaded.
# We'll use a dummy wrapper or try/except.
rl_agent = None
try:
    # Use dummy env for agent loading, sharing same config
    dummy_env = NetworkDefenseEnv(num_nodes=15)
    rl_agent = RLAgent(dummy_env, algo='PPO', model_path="rl_agent/models/ppo_agent_v1")
    if os.path.exists("rl_agent/models/ppo_agent_v1.zip"):
        rl_agent.load()
    else:
        print("RL Model not found, running in manual mode.")
        rl_agent = None
except Exception as e:
    print(f"Failed to load RL Agent: {e}")

@app.route('/')
def index():
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend')), 'index.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    nodes = network.get_all_nodes()
    return jsonify({
        "nodes": [n for n in nodes],
        "risk_score": risk_engine.calculate_network_risk()
    })

@app.route('/api/step', methods=['POST'])
def step():
    """Advances the simulation by one step."""
    # 1. Random Attack
    attack_sim.run_random_attack_step()
    
    # 2. Risk Assessment
    current_risk = risk_engine.calculate_network_risk()
    
    # 3. RL / Defense Action
    action_taken = "None"
    if rl_agent:
        try:
             # Get observation
             obs = np.array(network.get_state_vector(), dtype=np.int32)
             action = rl_agent.predict(obs)
             # Apply action (simplified mapping)
             # map logic from monitor_and_heal
             action_taken = f"RL Action: {action}"
             # In a real integration, we'd map RL action back to network calls
             # For now, let's use the Self-Healing module as the rigorous defense
        except Exception as e:
             print(f"RL Error: {e}")

    # 4. Self-Healing (Always active as fallback/complement)
    healing_actions = defense_sys.monitor_and_heal()
    
    return jsonify({
        "message": "Step executed",
        "risk": current_risk,
        "healing_actions": healing_actions,
        "rl_action": action_taken
    })

@app.route('/api/attack', methods=['POST'])
def trigger_attack():
    data = request.json
    target = data.get('target_id')
    type = data.get('type', 'ddos')
    
    if type == 'ddos':
        attack_sim.simulate_ddos(target, 100)
    elif type == 'sqli':
        attack_sim.simulate_sql_injection(target)
        
    return jsonify({"message": f"Attacked Node {target} with {type}"})

@app.route('/api/visualize', methods=['GET'])
def visualize():
    # Return base64 image
    img_data = visualizer.plot_network()
    return jsonify({"image": img_data})

@app.route('/api/reset', methods=['POST'])
def reset():
    global network, attack_sim, defense_sys, risk_engine, visualizer
    network = NetworkModel(num_nodes=15)
    attack_sim = AttackSimulator(network)
    defense_sys = SelfHealingSystem(network)
    risk_engine = RiskEngine(network)
    visualizer = GraphVisualizer(network)
    return jsonify({"message": "Simulation reset"})

if __name__ == '__main__':
    print("STARTING SERVER ON PORT 5001... PLEASE OPEN http://localhost:5001")
    app.run(debug=True, port=5001)

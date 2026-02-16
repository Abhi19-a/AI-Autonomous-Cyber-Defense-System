import random
from typing import List

class AttackSimulator:
    def __init__(self, network):
        self.network = network

    def simulate_ddos(self, target_node_id: int, intensity: float):
        """Simulates a DDoS attack on a specific node."""
        node = self.network.graph.nodes[target_node_id]
        if node['status'] == 'isolated': return

        current_load = node.get('traffic_load', 0)
        new_load = current_load + intensity
        
        # Threshold for crashing
        max_load = 100 
        node['traffic_load'] = new_load
        
        if new_load > max_load:
            # Overloaded
            print(f"Node {target_node_id} crashed due to DDoS!")
            # In a real simulation, this might be a different state like 'down'
            # Here, we treat 'compromised' broadly as 'unavialable/hacked' for simplicity
            # Or maybe just add a 'down' state? For RL simplicity, let's say compromised.
            self.network.update_node_status(target_node_id, 'compromised') 

    def simulate_sql_injection(self, target_node_id: int):
        """Simulates SQLi attempt on database/server nodes."""
        node = self.network.graph.nodes[target_node_id]
        if node['status'] == 'isolated': return
        
        if node['role'] in ['database', 'server']:
            # Success probability based on vulnerabilities
            success_prob = min(0.1 + (node['vulnerabilities'] * 0.15), 0.9)
            if random.random() < success_prob:
                print(f"SQL Injection successful on Node {target_node_id}")
                self.network.update_node_status(target_node_id, 'compromised')

    def simulate_lateral_movement(self):
        """Attempts to spread compromise from infected nodes to neighbors."""
        compromised_nodes = [n for n, data in self.network.graph.nodes(data=True) if data['status'] == 'compromised']
        
        for source in compromised_nodes:
            # Check outgoing edges using updated API for getting active edges? Or direct since we have access
            # Use out_edges for directed graph
            neighbors = self.network.graph.successors(source)
            for target in neighbors:
                target_node = self.network.graph.nodes[target]
                if target_node['status'] == 'normal':
                    # Check if edge is active
                    edge_data = self.network.graph.get_edge_data(source, target)
                    if edge_data.get('active', True):
                         # Probability based on target vulnerabilities
                         # Simulating lateral movement across active path
                         success_prob = 0.2 + (target_node['vulnerabilities'] * 0.1)
                         if random.random() < success_prob:
                             print(f"Lateral Movement: Node {source} -> Node {target}")
                             self.network.update_node_status(target, 'compromised')

    def run_random_attack_step(self):
        """Executes a random attack action for the environment step."""
        attack_type = random.choice(['ddos', 'sqli', 'lateral'])
        nodes = list(self.network.graph.nodes)
        target = random.choice(nodes)

        if attack_type == 'ddos':
            self.simulate_ddos(target, intensity=random.randint(20, 120))
        elif attack_type == 'sqli':
            self.simulate_sql_injection(target)
        elif attack_type == 'lateral':
            self.simulate_lateral_movement()

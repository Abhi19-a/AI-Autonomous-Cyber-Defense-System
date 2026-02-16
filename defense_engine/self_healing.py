from typing import Dict
from simulation.network_model import NetworkModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelfHealingSystem:
    def __init__(self, network: NetworkModel):
        self.network = network
        self.risk_threshold = 0.7 # If risk > 0.7, isolate
        
    def monitor_and_heal(self):
        """Scans all nodes and applies healing actions based on risk."""
        nodes = self.network.get_all_nodes()
        actions_taken = []
        
        for node in nodes:
            node_id = node['id']
            status = node['status']
            
            if status == 'isolated':
                # Attempt restoration periodically or based on condition?
                # Simple logic: If isolated, try to patch and restore
                if self._can_restore(node):
                    self.network.restore_node(node_id)
                    actions_taken.append(f"Restored Node {node_id}")
            
            elif status == 'compromised':
                # Isolate immediately
                self.network.isolate_node(node_id)
                actions_taken.append(f"Isolated Compromised Node {node_id}")
                
            elif status == 'normal':
                # Check neighbors risk? 
                risk = self._calculate_risk(node)
                if risk > self.risk_threshold:
                    self.network.isolate_node(node_id)
                    actions_taken.append(f"Preemptively Isolated Node {node_id} (High Risk: {risk})")

        return actions_taken

    def _calculate_risk(self, node: Dict) -> float:
        """Simple risk calculation based on vulnerabilities and neighbor status."""
        base_risk = node['vulnerabilities'] * 0.1
        
        # Check neighbors
        neighbors = []
        try:
            # Check incoming edges 
            preds = list(self.network.graph.predecessors(node['id']))
            neighbors.extend(preds)
        except Exception:
            pass

        neighbor_risk = 0
        for n_id in neighbors:
            neighbor = self.network.graph.nodes[n_id]
            if neighbor['status'] == 'compromised':
                neighbor_risk += 0.3 # High risk from compromised neighbor
        
        total_risk = min(base_risk + neighbor_risk, 1.0)
        return total_risk

    def _can_restore(self, node: Dict) -> bool:
        """Determines if a node is safe to restore."""
        # Check if all neighbors are safe?
        # Or just probability for simulation
        neighbors = list(self.network.graph.predecessors(node['id']))
        safe = True
        for n_id in neighbors:
            if self.network.graph.nodes[n_id]['status'] == 'compromised':
                safe = False
                break
        return safe

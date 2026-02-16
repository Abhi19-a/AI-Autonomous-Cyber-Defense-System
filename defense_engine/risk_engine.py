from typing import Dict, List
import networkx as nx

class RiskEngine:
    def __init__(self, network_model):
        self.network_model = network_model
        
    def calculate_node_risk(self, node_id: int) -> float:
        """
        Calculates a sophisticated risk score (0.0 to 1.0) for a single node.
        Factors:
        - Criticality (0-1)
        - Vulnerability Count (normalized)
        - Exposure (Compromised Neighbors)
        - Traffic Load (if under DDoS)
        """
        node = self.network_model.get_node_state(node_id)
        
        # Base Risk: Vulnerabilities and Criticality
        base_risk = (node['criticality'] * 0.4) + (min(node['vulnerabilities'], 5) * 0.1)
        
        # Neighbor Risk
        exposure = 0.0
        in_edges = self.network_model.graph.in_edges(node_id, data=True)
        active_in_edges = [u for u, v, data in in_edges if data.get('active', True)]
        
        for neighbor_id in active_in_edges:
            neighbor = self.network_model.get_node_state(neighbor_id)
            if neighbor['status'] == 'compromised':
                exposure += 0.25
        
        # Constraint exposure to max 0.5 impact
        exposure = min(exposure, 0.5)
        
        total_risk = base_risk + exposure
        return min(total_risk, 1.0)

    def calculate_network_risk(self) -> float:
        """Returns the average risk of the entire network."""
        total_risk = 0.0
        nodes = self.network_model.graph.nodes
        for n in nodes:
            total_risk += self.calculate_node_risk(n)
        return total_risk / len(nodes) if nodes else 0.0

    def recommend_critical_fixes(self, top_n: int = 3) -> List[int]:
        """Returns IDs of top N nodes that need immediate attention."""
        risks = []
        for n in self.network_model.graph.nodes:
            risk = self.calculate_node_risk(n)
            risks.append((n, risk))
        
        risks.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in risks[:top_n]]

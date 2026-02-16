import networkx as nx
import random
from typing import List, Dict, Tuple

class NetworkModel:
    def __init__(self, num_nodes: int = 10):
        self.graph = nx.DiGraph()
        self.num_nodes = num_nodes
        self._initialize_network()

    def _initialize_network(self):
        """Initializes the network with random nodes and connections."""
        roles = ['client', 'server', 'database', 'firewall']
        os_types = ['windows', 'linux', 'macos']
        
        for i in range(self.num_nodes):
            role = random.choice(roles)
            criticality = 0.8 if role == 'database' else 0.5 if role == 'server' else 0.2
            
            self.graph.add_node(i, 
                                id=i,
                                role=role,
                                os=random.choice(os_types),
                                status='normal', # normal, compromised, isolated
                                vulnerabilities=random.randint(0, 5), # Count of vulns
                                criticality=criticality,
                                traffic_load=0)

        # Create random connections
        # Ensure graph is somewhat connected
        for i in range(self.num_nodes):
            targets = random.sample(range(self.num_nodes), k=random.randint(1, 3))
            for target in targets:
                if i != target:
                    self.graph.add_edge(i, target, protocol='tcp', active=True)

    def get_node_state(self, node_id: int) -> Dict:
        return self.graph.nodes[node_id]

    def update_node_status(self, node_id: int, status: str):
        if status not in ['normal', 'compromised', 'isolated']:
            raise ValueError("Invalid status")
        self.graph.nodes[node_id]['status'] = status

    def isolate_node(self, node_id: int):
        """Temporarily disables all edges connected to the node."""
        self.graph.nodes[node_id]['status'] = 'isolated'
        # Logically 'shutdown' edges by marking them inactive
        for u, v, data in self.graph.edges(node_id, data=True):
             data['active'] = False
        for u, v, data in self.graph.in_edges(node_id, data=True):
             data['active'] = False

    def restore_node(self, node_id: int):
        """Restores a node to normal operation and re-enables edges."""
        self.graph.nodes[node_id]['status'] = 'normal'
        self.graph.nodes[node_id]['vulnerabilities'] = 0 # Patched
        self.graph.nodes[node_id]['traffic_load'] = 0
        
        for u, v, data in self.graph.edges(node_id, data=True):
             data['active'] = True
        for u, v, data in self.graph.in_edges(node_id, data=True):
             data['active'] = True

    def get_all_nodes(self) -> List[Dict]:
        return [self.graph.nodes[n] for n in self.graph.nodes]

    def get_active_edges(self) -> List[Tuple]:
        return [(u, v) for u, v, data in self.graph.edges(data=True) if data.get('active', True)]

    def get_state_vector(self) -> List[int]:
        """Returns a simple vector representation of node statuses for RL agent."""
        # 0: normal, 1: compromised, 2: isolated
        state = []
        mapping = {'normal': 0, 'compromised': 1, 'isolated': 2}
        for i in range(self.num_nodes):
            status = self.graph.nodes[i]['status']
            state.append(mapping.get(status, 0))
        return state

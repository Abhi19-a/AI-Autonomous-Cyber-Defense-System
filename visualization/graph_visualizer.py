import matplotlib.pyplot as plt
import networkx as nx
import io
import base64

class GraphVisualizer:
    def __init__(self, network_model):
        self.network = network_model.graph
        self.pos = nx.spring_layout(self.network, seed=42) # Fixed layout for consistency

    def plot_network(self, save_path=None):
        plt.style.use('dark_background')
        plt.figure(figsize=(10, 8), facecolor='#050505')
        
        # Color nodes by status
        colors = []
        node_border_colors = []
        
        for node in self.network.nodes(data=True):
            status = node[1].get('status', 'normal')
            if status == 'compromised':
                colors.append('#ff0055') # Neon Red
                node_border_colors.append('#ff0055')
            elif status == 'isolated':
                colors.append('#2d2d2d') # Dark Grey
                node_border_colors.append('#666666')
            else:
                colors.append('#00ff41') # Matrix Green
                node_border_colors.append('#00ff41')
        
        ax = plt.gca()
        ax.set_facecolor('#050505')
        
        nx.draw(self.network, self.pos, 
                with_labels=True, 
                node_color=colors, 
                node_size=1200, 
                font_color='black',
                font_weight='bold',
                font_family='monospace',
                edge_color='#00f3ff', # Cyan edges
                edgecolors=node_border_colors, # Node borders
                linewidths=2,
                width=1.5,
                arrows=True,
                arrowstyle='-|>',
                arrowsize=15)
        
        plt.title("ACTIVE THREAT MAP", color='#00f3ff', fontsize=20, fontfamily='monospace', pad=20)
        
        if save_path:
            plt.savefig(save_path, facecolor='#050505')
            plt.close()
        else:
            # Return as base64 string for API
            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor='#050505')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            return img_str

    def get_cytoscape_json(self):
        """Returns JSON compatible with Cytoscape.js for frontend."""
        elements = []
        
        # Nodes
        for node_id, data in self.network.nodes(data=True):
            elements.append({
                "data": {
                    "id": str(node_id),
                    "label": f"Node {node_id} ({data['role']})",
                    "status": data['status'],
                    "criticality": data['criticality']
                }
            })
            
        # Edges
        for u, v, data in self.network.edges(data=True):
            elements.append({
                "data": {
                    "source": str(u),
                    "target": str(v),
                    "active": data.get('active', True)
                }
            })
            
        return elements

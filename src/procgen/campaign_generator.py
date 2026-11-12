"""
Campaign map generation for roguelike world navigation.
"""

import random
from typing import List, Dict, Any, Tuple


class CampaignNode:
    """Represents a node on the campaign map."""

    def __init__(
        self,
        node_id: int,
        position: Tuple[int, int],
        node_type: str,
        difficulty: int = 1,
    ):
        """
        Initialize campaign node.

        Args:
            node_id: Unique node ID
            position: (x, y) position on map
            node_type: Type of node (battle, merchant, event, rest, boss)
            difficulty: Difficulty level
        """
        self.id = node_id
        self.position = position
        self.node_type = node_type
        self.difficulty = difficulty
        self.cleared = False
        self.connections: List[int] = []  # IDs of connected nodes


class CampaignGenerator:
    """
    Generates procedural campaign maps for roguelike progression.
    """

    def __init__(self, seed: int = None):
        """
        Initialize campaign generator.

        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)

        self.nodes: Dict[int, CampaignNode] = {}
        self.next_id = 0

    def generate_campaign(
        self, num_layers: int = 10, nodes_per_layer: Tuple[int, int] = (2, 4)
    ) -> Dict[int, CampaignNode]:
        """
        Generate a layered campaign map.

        Args:
            num_layers: Number of layers (depth)
            nodes_per_layer: (min, max) nodes per layer

        Returns:
            Dict mapping node IDs to CampaignNode objects
        """
        self.nodes.clear()
        self.next_id = 0

        layers: List[List[int]] = []

        # Generate layers
        for layer_idx in range(num_layers):
            layer_size = random.randint(*nodes_per_layer)
            layer_nodes = []

            for node_idx in range(layer_size):
                # Determine node type
                node_type = self._determine_node_type(layer_idx, num_layers)

                # Calculate position
                x = 100 + layer_idx * 150
                y_spacing = 600 // (layer_size + 1)
                y = y_spacing * (node_idx + 1)

                # Create node
                node = CampaignNode(
                    node_id=self.next_id,
                    position=(x, y),
                    node_type=node_type,
                    difficulty=layer_idx + 1,
                )

                self.nodes[self.next_id] = node
                layer_nodes.append(self.next_id)
                self.next_id += 1

            layers.append(layer_nodes)

        # Connect nodes between layers
        for layer_idx in range(len(layers) - 1):
            current_layer = layers[layer_idx]
            next_layer = layers[layer_idx + 1]

            for node_id in current_layer:
                # Connect to 1-3 nodes in next layer
                num_connections = random.randint(1, min(3, len(next_layer)))
                connections = random.sample(next_layer, num_connections)

                for conn_id in connections:
                    self.nodes[node_id].connections.append(conn_id)

        return self.nodes

    def _determine_node_type(self, layer_idx: int, total_layers: int) -> str:
        """
        Determine node type based on layer position.

        Args:
            layer_idx: Current layer index
            total_layers: Total number of layers

        Returns:
            Node type string
        """
        # First layer is always battle
        if layer_idx == 0:
            return "battle"

        # Last layer is always boss
        if layer_idx == total_layers - 1:
            return "boss"

        # Every 3rd layer has a rest area
        if layer_idx % 3 == 2:
            if random.random() < 0.6:
                return "rest"

        # Random distribution for other nodes
        roll = random.random()
        if roll < 0.5:
            return "battle"
        elif roll < 0.7:
            return "merchant"
        elif roll < 0.85:
            return "event"
        else:
            return "elite"

    def get_node(self, node_id: int) -> CampaignNode:
        """Get node by ID."""
        return self.nodes.get(node_id)

    def get_connected_nodes(self, node_id: int) -> List[CampaignNode]:
        """Get all nodes connected to a given node."""
        node = self.get_node(node_id)
        if not node:
            return []

        return [self.nodes[conn_id] for conn_id in node.connections if conn_id in self.nodes]

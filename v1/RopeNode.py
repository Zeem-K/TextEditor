class RopeNode:
    def __init__(self, data=None):
        self.data = data  # String data for leaf nodes; None for internal nodes
        self.weight = len(data) if data else 0  # Length of the string in the left subtree
        self.left = None  # Left child
        self.right = None  # Right child

from RopeNode import RopeNode
import math
class Rope:
    def __init__(self, string=""):
        self.root = RopeNode(string) if string else None
    
    def concatenate(self, rope1, rope2):
        """Concatenate two ropes."""

        new_root = RopeNode()
        new_root.left = rope1.root
        new_root.right = rope2.root
        new_root.weight = self._get_weight(rope1.root)
        self.root = new_root
    
    def get_character_at_index(self, index):
        """Return the character at the specified index."""
        # self._validate_index(index)
        return self._get_character_at_index(self.root, index)

    def _get_character_at_index(self, node, index):
        """Recursively find the character at the specified index."""
        if not node:
            return None

        if node.data:  # Leaf node
            if 0 <= index < len(node.data):
                return node.data[index]
            else:
                return None
        if index < node.weight:
            return self._get_character_at_index(node.left, index)
        else:
            return self._get_character_at_index(node.right, index - node.weight)

    def _get_weight(self, node):
        """Utility function to calculate weight of a subtree."""
        if not node:
            return 0
        if node.data:  # Leaf node with data
            return len(node.data)
        #internal node
        else:
            return self._get_weight(node.left) + self._get_weight(node.right)

    def _validate_index(self, index, allow_end=False):
        """Check if the index is within the bounds of the rope."""
        max_index = len(self.report()) + (1 if allow_end else 0)
        if index < 0 or index > max_index:
            raise IndexError("Index out of bounds")


    def _concatenate_nodes(self, left_node, right_node):
        if not left_node:
            return right_node
        if not right_node:
            return left_node
        
        # Create a new internal node with left and right children
        new_root = RopeNode()
        new_root.left = left_node
        new_root.right = right_node
        
        # Calculate and assign the weight of the new internal node
        # The weight is the total length of strings in the left subtree
        new_root.weight = self._get_weight(left_node)
    
        return new_root

    def insert(self, index, string):
        """Insert a string at the specified position."""
        #Check if index is valid
        self._validate_index(index,True)
         # Split the original rope at the index to get the left and right parts
        left_rope, right_rope = self._split(self.root, index)
        # Create a new rope for the string to be inserted
        new_rope_node = RopeNode(string)
        # First, concatenate the left part with the new string
        temp_root = self._concatenate_nodes(left_rope, new_rope_node)
        # Then, concatenate the result with the right part
        self.root = self._concatenate_nodes(temp_root, right_rope)
        self.rebalance()

    def _split(self, node, index):
        """Split the rope at the specified index."""
        if node is None:
            return (None, None)
        if node.data:  # Leaf node
            # Directly split the string data at the index
            left_data = node.data[:index]
            right_data = node.data[index:]
            return (RopeNode(left_data) if left_data else None, RopeNode(right_data) if right_data else None)

        # Internal node
        if index < node.weight:
            # The split index is within the left subtree
            left, temp_right = self._split(node.left, index)
            right = self._concatenate_nodes(temp_right, node.right)
        else:
            # The split index is within the right subtree or exactly at the weight
            temp_left, right = self._split(node.right, index - node.weight)
            left = self._concatenate_nodes(node.left, temp_left)

        return (left, right)

    def delete(self, start_index, length):
        self._validate_index(start_index)
        if length <= 0:
            return  # No operation if length is non-positive
        
        # Adjust the end index if it exceeds the rope's bounds
        total_length = len(self.report())
        end_index = min(start_index + length, total_length)

        left_rope, temp_rope = self._split(self.root, start_index)
        _, right_rope = self._split(temp_rope, end_index - start_index)
        
        self.root = self._concatenate_nodes(left_rope, right_rope)

    def report(self):
        # almost the same thing as collect leaves
        def collect_strings(node, start, end, path, index=0):
            if not node or index >= end:
                return index
            if node.data:  # Leaf node
                # Adjust start and end based on the current index
                start_idx = max(0, start - index)
                end_idx = min(len(node.data), end - index)
                if start_idx < end_idx:  # Ensure index is part of the index to add 
                    path.append(node.data[start_idx:end_idx])
                return index + len(node.data)
            else:
                # Internal node, traverse left then right
                index = collect_strings(node.left, start, end, path, index)
                index = collect_strings(node.right, start, end, path, index)
                return index
        path = []
        collect_strings(self.root,0,math.inf, path)
        return ''.join(path)
    
    def print_tree(self, node=None, prefix="", is_last=True):
        """Print the tree structure with branches."""
        if node is None:
            node = self.root
        
        # Determine the symbols for branches based on the node's position
        branch = "└──" if is_last else "├──"
        # Print the current node: weight for internal nodes, data for leaves
        if node.data is not None:  # Leaf node with data
            node_repr = f"'{node.data}' (Weight: {node.weight})"
        else:  # Internal node
            node_repr = f"(Weight: {node.weight})"
        
        print(prefix + branch + node_repr)

        # Prepare the prefix for child nodes
        child_prefix = prefix + ("    " if is_last else "│   ")
        children = [(node.left, False), (node.right, True)]
        for child, is_last in children:
            if child:
                self.print_tree(node=child, prefix=child_prefix, is_last=is_last)
        
    def collect_leaves(self, node=None, leaves=None):
        if leaves is None:
            leaves = []
        if node is None:
            node = self.root

        if node.data:
            leaves.append(node.data)
        else:
            if node.left:
                self.collect_leaves(node.left, leaves)
            if node.right:
                self.collect_leaves(node.right, leaves)
        return leaves
    
    def generate_fibonacci(self,n):
        fib = [0, 1]
        for i in range(2, n + 1):
            fib.append(fib[-1] + fib[-2])
        return fib

    def depth(self, node=None):
        if not node:
            return 0
        return 1 + max(self.depth(node.left), self.depth(node.right))

    def is_balanced(self, node=None):
        # If no node is explicitly provided, start with the root of the rope.
        if node is None:
            node = self.root

        # Calculate the depth of the current node (or the root, if no node is provided).
        node_depth = self.depth(node)
        # 2048 is a arbitrary number
        fibonacci_sequence = self.generate_fibonacci(2048)
        # Check if the depth of the node exceeds the bounds set by our Fibonacci sequence.
        # If it does, the rope is considered unbalanced due to excessive depth.
        if node_depth >= len(fibonacci_sequence) - 2:
            return False

        # Determines if the weight of the subtree rooted at the current node meets or exceeds
        # the value in the Fibonacci sequence at the position of "node depth + 2". This check
        # ensures that the tree's structure is not too deep relative to its weight, a condition
        # indicative of a balanced binary tree. If the weight is less than the Fibonacci value,
        # the tree is considered unbalanced otherwise, it is balanced.
        return fibonacci_sequence[node_depth + 2] <= self._get_weight(node)
    
    def merge(self, leaves, start=0, end=None):
        # If 'end' is not specified, use the length of the 'leaves' list.
        if end is None:
            end = len(leaves)
        # Calculate the range of indices to be merged.
        range = end - start
        # If the range is 1, create a RopeNode from the single element and return it.
        if range == 1:
            return RopeNode(leaves[start])
        # If the range is 2, create and return a new node by concatenating the two leaves.
        if range == 2:
            return self._concatenate_nodes(RopeNode(leaves[start]), RopeNode(leaves[start + 1]))
        # For a range greater than 2, split the list in half and merge each half recursively.
        mid = start + (range // 2)
        left_subtree = self.merge(leaves, start, mid)  # Merge the left half
        right_subtree = self.merge(leaves, mid, end)   # Merge the right half
        # Concatenate and return the two merged halves.
        return self._concatenate_nodes(left_subtree, right_subtree)
    
    def rebalance(self):
        if not self.is_balanced():
            leaves = self.collect_leaves()
            self.root = self.merge(leaves)

if __name__ == "__main__":
    rope = Rope("Bonjour")
    rope.insert(2,"a")
    rope.insert(3,"b")
    rope.insert(4,"c")
    rope.insert(9,"Je suis ta mere")
    rope.insert(24,'YYY4FF')
    rope.insert(17,'test')
    rope.print_tree()
    print(rope.is_balanced())








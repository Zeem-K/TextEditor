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
        # Internal node; weight is already calculated and stored
        return node.weight

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

    def _split(self, node, index, depth=0):
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


if __name__ == "__main__":
    rope = Rope("Hello_my_name_is_Simon")
    print(rope.report())
    # print(len(rope.report()))
    # rope.insert(22,"_Ta mere la pute")
    # print(len(rope.report()))
    # print(rope.report())
    # rope.delete(39,2)
    print(len(rope.report()))
    # print(rope.root.weight)
    rope.delete(10,5)
    print(rope.report())
    res = "DE"
    print(res[:0])
    print(res[0:])








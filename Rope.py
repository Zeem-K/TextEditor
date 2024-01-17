from collections import deque

LEAF_LEN = 6
class RopeNode:
    def __init__(self,string):
        self.string = string
        self.left = None
        self.right = None
        self.length = len(string) if string else 0

class Rope:
    def __init__(self,string):
        self.root = self.buildRopeNode(string)
            
    def buildRopeNode(self,string):
        if not string:
            return None
        if len(string) > LEAF_LEN:
            mid = len(string) // 2
            node = RopeNode(None)
            node.left = self.buildRopeNode(string[:mid])
            node.right = self.buildRopeNode(string[mid:])
            node.length  = self.calculate_length(node.left)
            return node
        return RopeNode(string)



    def calculate_length(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return node.length
        
        left_subtree_sum = self.calculate_length(node.left)
        right_subtree_sum = self.calculate_length(node.right)

        return left_subtree_sum + right_subtree_sum
        
    def print_rope(self, node=None, indent=""):
        if not node:
            node = self.root
        if node:
            print(f"{indent}[Length {node.length} , {node.string}]")
            if node.left or node.right:
                self.print_rope(node.left, indent + "  ")
                self.print_rope(node.right, indent + "  ")



def main():
   rope_string = "hello_i_am_a_rope_data_structure"
   print(len("hello_i_am_a_rope_data_structure"))
   rope = Rope(rope_string)
   rope.print_rope()

if __name__ == "__main__":
    main()
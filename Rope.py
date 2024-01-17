from collections import deque

LEAF_LEN = 6
class RopeNode:
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None
        self.length = len(data) if data else 0
    
    def height(self,node):
        if node is None:
            return 0
        if node.left or node.right:
            return max(self.height(node.left),self.height(node.right))

class Rope:
    def __init__(self,data):
        self.root = self.buildRopeNode(data)
            
    def buildRopeNode(self,data):
        if not data:
            return None
        if len(data) > LEAF_LEN:
            mid = len(data) // 2
            node = RopeNode(None)
            node.left = self.buildRopeNode(data[:mid])
            node.right = self.buildRopeNode(data[mid:])
            #Poids de chaque noeud vaut la somme des feuilles de son sous arbre gauche (D'après wikipédia)
            # node.length  = self.calculate_length(node.left)
            node.length = self.calculate_length(node.left)
            node.length += self.calculate_length(node.right)
            return node
        return RopeNode(data)

    def calculate_length(self,node):
        return node.length if node else 0
    

    # Calacul du poids des neouds parent d'après wikipédia
    # def calculate_length(self, node):
    #     if node is None:
    #         return 0
    #     if node.left is None and node.right is None:
    #         return node.length
        
    #     left_subtree_sum = self.calculate_length(node.left)
    #     right_subtree_sum = self.calculate_length(node.right)

    #     return left_subtree_sum + right_subtree_sum
        
            
    def print_rope(self, node=None, indent=""):
        if not node:
            node = self.root
        if node:
            print(f"{indent}[Length {node.length} , {node.data}]")
            if node.left or node.right:
                self.print_rope(node.left, indent + "  ")
                self.print_rope(node.right, indent + "  ")


def main():
   rope_data = "happy_birthday!"
   rope = Rope(rope_data)
   rope.print_rope()
   

if __name__ == "__main__":
    main()
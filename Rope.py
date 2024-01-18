from collections import deque

#Déterminer la taile de chaque 
LEAF_LEN = 8
class RopeNode:
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None
        self.length = len(data) if data else 0
    

class Rope:
    def __init__(self,data):
        self.root = self.buildRopeNode(data)
            
    def buildRopeNode(self,data):
        if not data:
            return None
        if len(data) > LEAF_LEN:
            mid = self.findLeafLen(data)
            node = RopeNode(None)
            node.left = self.buildRopeNode(data[:mid])
            node.right = self.buildRopeNode(data[mid:])
            #Poids de chaque noeud vaut la somme des feuilles de son sous arbre gauche (D'après wikipédia)
            # node.length  = self.calculate_length(node.left)
            node.length = self.calculate_length(node.left)
            node.length += self.calculate_length(node.right)
            return node
        return RopeNode(data)

    def findLeafLen(self,data):
        if(len(data)%2 != 0):
            return len(data) // 2
        res = 1
        for i in range(1,LEAF_LEN+1):
            if len(data) % i == 0 and i > res:
                res = i
        return res
        

    #Utiliser cette fonction pour le calcul d'équilibre est inefficient car le calcul d'équilbre calul déjà la taille
    def height_node(self,node):
        if node is None:
            return 0
        else:
            left_height = self.height_node(node.left)
            right_height = self.height_node(node.right)
        return max(left_height,right_height)+1
    
    def depth_node(self,node):
        return self.height_node(node.left) - self.height_node(node.right)

    def calculate_length(self,node):
        return node.length if node else 0
    
    #Si la valeur renvoyée est différent de -1 alors l'arbre est équilbrée
    def checkBalanced(self,node):
        if not node:
            return 0
        rigthSubTreeHeight = self.checkBalanced(node.right)
        leftSubTreeHeight = self.checkBalanced(node.left)
        if (rigthSubTreeHeight == -1):
            return -1
        if (leftSubTreeHeight == -1):
            return -1
        if(abs(leftSubTreeHeight-rigthSubTreeHeight) > 1):
            return -1
        return max(leftSubTreeHeight,rigthSubTreeHeight)+1
        
        

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
   rope_data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
   rope = Rope(rope_data)
   rope.print_rope()
   print(rope.checkBalanced(rope.root))

if __name__ == "__main__":
    main()
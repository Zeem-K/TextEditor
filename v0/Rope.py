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
        self.root = RopeNode(None)
        self.root.length = len(data)
        self.root.left = self.buildRopeNode(data)
    
    #Olog N)
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
            # node.length += self.calculate_length(node.right)
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
    
    #Complexité en temps = O(N) N étant le nombre de feuille
    #On essaye d'améliorer ça
    def collectleaves(self):
        leaf_data = []
        def dfs(node):
            if not node.left and not node.right:  # Check if the node is a leaf
                leaf_data.append(node.data)
            if node.left:
                dfs(node.left)
            if node.right:
                dfs(node.right)
        dfs(self.root)
        
        return ''.join(leaf_data)

    
    def findleaves(self):
        pass
    
    def insert(self,idx,data):
        leaves = self.collectleaves()
        new_data = leaves[:idx-1] + data + leaves[idx-1:]
        self.root = self.buildRopeNode(new_data)

    def delete(self,start,length):
        leaves = self.collectleaves()
        new_data = leaves[:start] + leaves[length+1:]
        self.root = self.buildRopeNode(new_data)

    def index(self,index):
        leaves = self.collectleaves()
        return leaves[index]
    
    def concatRope(self,rope):
        if rope.root:
            temphead = RopeNode(None)
            left_node = self.root
            self.root = temphead
            temphead.length = left_node.length + rope.root.length
            temphead.left = left_node
            temphead.right = rope.root
            new_rope = self.buildRopeNode(self.collectleaves())
            self.root = new_rope
            
    def print_rope(self, node=None, indent=""):
        if not node:
            node = self.root
        if node:
            print(f"{indent}[Length {node.length} , {node.data}]")
            if node.left or node.right:
                self.print_rope(node.left, indent + "  ")
                self.print_rope(node.right, indent + "  ")

def main():
   rope_data = "Hello_my_name_is_Simon"
   rope = Rope(rope_data)
   print(rope.root.length)
   rope.print_rope()
   rope.collectleaves()

if __name__ == "__main__":
    main()
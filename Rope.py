LEAF_LEN = 8
class RopeNode:
    def __init__(self,string) -> None:
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
        if len(string) == 1:
            return RopeNode(string)

        mid = len(string) // 2
        node = RopeNode(None)
        node.left = self.buildRopeNode(string[:mid])
        node.right = self.buildRopeNode(string[mid:])
        node.length = self.calculate_length(node.left) if node.left else 0
        node.length += self.calculate_length(node.right) if node.right else 0
        return node
    

    def calculate_length(self, node):
        return node.length if node else 0
        

    def print_rope(self, node=None, indent=""):
        if not node:
            node = self.root
        if node:
            print(indent + str(node.string))
            if node.left or node.right:
                self.print_rope(node.left, indent + "  ")
                self.print_rope(node.right, indent + "  ")


def main():
   rope_string = "Je suis un hommme"
   rope = Rope(rope_string)
   rope.print_rope()

if __name__ == "__main__":
    main()
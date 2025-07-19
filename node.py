from .tree import Tree


class Node(Tree):
    def __init__(
        self, data=None, name=None, print_function=None, print_args=None, nodes=None
    ):
        """
        name is name of node.
        data is the data stored in the node
        print_function stores the function that will be called whenever the node is printed
        print_args are the arguments supplied to print_function
        nodes is the child nodes of this node.
        """
        super().__init__(name=name)
        self.name = name
        self.data = data
        self.print_function = print_function
        self.print_args = print_args
        if not isinstance(nodes, list):
            nodes = [nodes]
        self.nodes = nodes

    def __str__(self):
        """
        Calls and returns the results of self.print_function if it exists, otherwise returns the name
        """
        if self.print_function:
            if self.print_args:
                return self.print_function(self.print_args)
            else:
                return self.print_function()
        if self.data is not None:
            return str(self.data)
        if self.name is not None:
            return str(self.name)
        return ""

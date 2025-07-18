class Node:
    def __init__(self,name=None,data=None,print_function=None,print_args=None):
        """
        name is name of node.
        data is the data stored in the node
        print_function stores the function that will be called whenever the node is printed
        print_args are the arguments supplied to print_function
        """
        self.name = name
        self.data = data
        self.print_function = print_function
        self.print_args = print_args

    def __str__(self):
        """
        Calls and returns the results of self.print_function if it exists, otherwise returns the name
        """
        if self.print_function:
            if self.print_args:
                return self.print_function(self.print_args)
            else:
                return self.print_function()
        if self.name is not None:
            return self.name
        return ""


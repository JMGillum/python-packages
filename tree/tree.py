"""
   Author: Josh Gillum              .
   Date: 16 July 2025              ":"         __ __ 
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This is a general use tree class. It can handle arbitrary depths,
    and can hold nodes of either strings or additional tree objects.
    The tree works by building the tree from the deepest point up,
    allowing it to figure out the size needed for shallower elements.

    Also supports setting the display characters to either fancy or basic.
    Basic display uses characters only found within 7 bit ASCII, while
    fance uses other characters. If the tree's branches aren't displaying
    correctly or are weird characters, try setting the fancy value to False.

    Updates to the tree object will only affect this level. To update deeper
    levels as well, the cascading_update line of functions must be used.
    These will recursively update the deeper nodes, then the current nodes.


^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

__version_info__ = ("1","0","0")
__version__ = ".".join(__version_info__)


from formatString import tabulate


class Tree:
    def __init__(
        self,
        name: str = None,
        nodes: list | None = None,
        fancy=False,
        wrap=None,
        width=None,
    ):
        self.set_name(name)
        self.set_nodes(nodes)
        self.set_fancy(fancy)
        self.dirty = True
        if width is None:
            width = -1
        if wrap is None:
            wrap = -1
        self.set_term_size(width)
        self.set_line_wrap(wrap)

    def set_name(self, name: str):
        self.name = name
        self.dirty = True

    def set_nodes(self, nodes: list | None):
        self.nodes = nodes
        self.dirty = True

    def cascading_update(self, set_fancy=None, line_width=None, term_width=None):
        if set_fancy is not None:
            self.cascading_set_fancy(set_fancy)
        if line_width is not None:
            self.cascading_set_line_wrap(line_width)
        if term_width is not None:
            self.cascading_set_term_size(term_width)

    def cascading_set_fancy(self, set_fancy: bool):
        if self.nodes is not None:
            for item in self.nodes:
                if isinstance(item, Tree):
                    item.cascading_set_fancy(set_fancy)
        self.set_fancy(set_fancy)

    def cascading_set_term_size(self, width: int):
        if self.nodes is not None:
            for item in self.nodes:
                if isinstance(item, Tree):
                    item.cascading_set_term_size(width)
        self.set_term_size(width)

    def cascading_set_line_wrap(self, line_width: int):
        if self.nodes is not None:
            for item in self.nodes:
                if isinstance(item, Tree):
                    item.cascading_set_line_wrap(line_width)
        self.set_line_wrap(line_width)

    def set_fancy(self, set_fancy: bool):
        self.fancy = set_fancy
        self.set_characters()

    def set_characters(self):
        if self.fancy:
            self.pipe = "│"
            self.branch = "├─"
            self.end = "└─"
            self.space = " "
        else:
            self.pipe = "|"
            self.branch = "|->"
            self.end = "|->"
            self.space = "  "
        self.split_line = "~"

    def set_term_size(self, width=80):
        if width is not None:
            self.width = width

    def set_line_wrap(self, line_width: int):
        if line_width is not None:
            self.line_wrap = line_width

    def print(self, as_a_string=False):
        # if self.dirty: # Doesn't regenerate tree if no changes have been made.
        # Sets entire tree as the single child node of tree. Necessary for proper spacing
        # Saves values so they can be restored after building tree
        name = self.name
        nodes = self.nodes
        child = Tree(
            name, nodes, fancy=self.fancy, wrap=self.line_wrap, width=self.width
        )
        self.name = None
        self.nodes = [child]
        # Gets the tree, as a list of lines
        self.list = self.recursive_generation(True)
        # Converts the list to a single string
        self.string = ""
        for line in self.list:
            self.string += f"{line}\n"
        # Restores the original values of the name and nodes.
        self.name = name
        self.nodes = nodes
        self.dirty = False
        return self.string if as_a_string else self.list

    def recursive_generation(self, last=False, prior_prefix=0):
        """Generates a tree, recursively

        Args:
            last (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        string = []
        if self.name:
            prefix = self.end if last else self.branch # Determine if this is the last child of its parent, and sets branch character accordingly
            try:
                if self.line_wrap > 0: # If their is a max text width set, split into multiple lines
                    # Splits the text into a number of lines with max lengths of self.line_wrap
                    temp = tabulate(self.name, self.line_wrap, 0)
                    temp = temp.split("\n") # Converts string of lines into a list of lines
                    for j in range(len(temp)): # Loops through each line in the text
                        if temp[j].strip() != "": # Ensures that this is not a blank line
                            if j == 0:
                                string.append(f"{prefix}{temp[j]}") # Adds branch character
                            else: # Or character indicating that this is continuing from the previous line.
                                string.append(f"{self.split_line}{temp[j]}") 
                else: # No line-wrapping, so just add branch character and text
                    string.append(f"{prefix}{self.name}")
            except AttributeError:
                string.append(f"{prefix}{self.name}")
        if self.nodes is not None: # This object has some children nodes
            for i in range(len(self.nodes)): # Loops through each node
                item = self.nodes[i]
                if isinstance(item, str):
                    # If the node is just text, decide if this is the last child of its parent's tree
                    # Change the branch character if it is, otherwise use standard branch character.
                    prefix = self.end if (i == len(self.nodes) - 1) else self.branch
                    # Does the same process as with the name, determining if the text needs to be
                    # split across several lines, and doing so if needed.
                    try:
                        wrap = None
                        if self.line_wrap is not None and self.line_wrap > 0:
                            wrap = self.line_wrap
                        if self.width is not None and self.width > 0:
                            # Determines the max width that the text can be. It is equal to the max width minus
                            # the length of the current prefix and the length of all of the prior prefixes
                            wrap = self.width - len(prefix) - prior_prefix
                        if wrap is not None:
                            temp = tabulate(item, wrap, 0)
                            temp = temp.split("\n")
                            for j in range(len(temp)):
                                if temp[j].strip() != "":
                                    if j == 0:
                                        string.append(f"{prefix}{temp[j]}")
                                    else:
                                        # Determines which character to use for indicating that this is wrapping.
                                        # Typically will use a pipe to extend the node if needed, but if
                                        # it is the last node, will only use a space. Regardless, it also uses the
                                        # typical split line character.
                                        # Ex normal node:         Ex last node:
                                        # -> This is a test       -> This is a test
                                        # |~ of the line           ~ of the line
                                        # |~ wrapping function.    ~ wrapping function.
                                        if i == len(self.nodes) - 1:
                                            wrap_prefix = self.space
                                        else:
                                            wrap_prefix = self.pipe
                                        string.append(
                                            f"{wrap_prefix}{self.split_line}{temp[j]}"
                                        )
                        else:
                            string.append(f"{prefix}{item}")
                    except AttributeError:
                        string.append(f"{prefix}{item}")
                elif isinstance(item, Tree): # If the child node is another Tree object, generate that object.
                    child_last = (i == len(self.nodes) - 1) # Boolean as to whether this is the last child of this node
                    prefix = self.end if last else self.branch # Determines if this is the last child node of its parent, and sets branch character accordingly
                    # Generate the child node, indicating whether it is the last node.
                    child = item.recursive_generation(
                        child_last, len(prefix) + prior_prefix
                    )
                    for j in range(1, len(child)): # Loops through all lines returned from child node
                        line = child[j]
                        # Set prefix according to whether this is the last child node or not
                        if i != len(self.nodes) - 1: 
                            child[j] = self.pipe
                        else:
                            child[j] = self.space
                        if len(line) > 0 and line[0] != self.split_line:
                            child[j] += self.space
                        child[j] += line # Add the lines from the inner tree back to the prefixes.
                    string += child # Add the lines of the child to the lines of this tree
        return string # Return the lines of this tree level back to the parent

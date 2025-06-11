# for now i will try generating a tree of node correctly and ignore the info / stratagy 
# This will represent a node in the tree, and contain all the data that each node will have
class Node:
    def __init__(self, gamestate, position, node_type, raise_level=0):
        self.gamestate = gamestate  # this will be the game state at this node

        #contain freqs of actions - we can store tham as a map like {'fold': 0.5, 'bet': 0.3, 'check': 0.2}
        self.freqs = {'fold': 0.3, 'bet': 0.3, 'check': 0.3}
        self.children = []
        self.position = position  # 'IP' or 'OOP'
        self.type = node_type # for node type, we can have action (bet, check, fold) raction (raise, call, fold) or terminal node
        self.raise_level = raise_level 

    def generate_children(self, k):
        #base case for recursion
        if self.type == 'terminal' or self.raise_level == k:
            return
        
        # based on the type of node, we'll generate the children

        
        #check what the children nodes potion should be
        if self.position == 'OOP':
            child_position = 'IP'
        else:
            child_position = 'OOP'

        # add options for action nodes
        if self.type == 'action':
                # this node is just for the calcuation
                fold_node = Node(self.gamestate, self.position, 'terminal')
                self.children.append(fold_node)

                #check if we can raise
                if self.raise_level < k:
                    #this respresents a raise
                    reaction_node = Node(self.gamestate, child_position, 'reaction', raise_level=self.raise_level + 1)
                    self.children.append(reaction_node)

                # this respresnts a check - for IP this will start a new sequence
                if self.position == 'OOP':
                    action_node = Node(self.gamestate, child_position, 'action')
                    self.children.append(action_node)
                else:
                    if len(self.gamestate.community_cards) == 5:
                        # if we are at the river it doesnt make a new sequence
                        # so we just add a terminal node
                        action_node = Node(self.gamestate, self.position, 'terminal')
                        self.children.append(action_node)
                    else:
                        new_state = self.gamestate.__copy__()
                        new_state.add_card()
                        IP_check_node = Node(new_state, child_position, 'action')
                        self.children.append(IP_check_node)

        # add options for reaction nodes
        elif self.type == 'reaction':
                # this node is just for the calcuation
                fold_node = Node(self.gamestate, self.position, 'terminal')
                self.children.append(fold_node)

                # check if we can raise
                if self.raise_level < k:
                    #this respresents a raise
                    reaction_node = Node(self.gamestate, child_position, 'reaction', raise_level=self.raise_level + 1)
                    self.children.append(reaction_node)

                if len(self.gamestate.community_cards) == 5:
                    # if we are at the river it doesnt make a new sequence
                    # so we just add a terminal node
                    check_node = Node(self.gamestate, self.position, 'terminal')
                    self.children.append(check_node)
                else:
                    # this respresnts a call - this will be terminal
                    new_state = self.gamestate.__copy__()
                    new_state.add_card()
                    call_node = Node(new_state, child_position, 'action')
                    self.children.append(call_node)

        for node in self.children:
            # recursively generate children for each child node
            node.generate_children(k)

        
    def to_string_tree(self, level=0):
        indent = "  " * level
        result = f"({indent}{self.position}, {self.type}, {len(self.gamestate.community_cards)})\n"
        if self.children:
            # Print all children on one line, comma-separated
            child_line = indent + "  " + ", ".join(
                f"{child.position}, {child.type}" for child in self.children
            )
            result += child_line + "\n"
            # Recursively print each child's subtree
            for child in self.children:
                if child.children:
                    result += child.to_string_tree(level + 1)
        return result
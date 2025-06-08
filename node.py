
# for now i will try generating a tree of node correctly and ignore the info / stratagy 
# This will represent a node in the tree, and contain all the data that each node will have
class Node:
    def __init__(self, gamestate, position, node_type):
        #contain frequences of actions - we can store tham as a map like {'fold': 0.5, 'bet': 0.3, 'check': 0.2}
        self.frequences = {'fold': 0.3, 'bet': 0.3, 'check': 0.3}
        self.children = []
        self.position = position  # 'IP' or 'OOP'
        self.type = node_type # for node type, we can have action (bet, check, fold) raction (raise, call, fold) or terminal node
    
    def generate_children(self):
        # based on the type of node, well generate the children

        #check what the children nodes potion should be
        if self.position == 'OOP':
            child_position = 'IP'
        else:
            child_position = 'OOP'

        # add options for action nodes
        if self.type == 'action':
            for action in self.frequences:
                # this node is just for the calcuation
                fold_node = Node(self.gamestate, self.position, 'terminal')

                #this respresents a raise
                reaction_node = Node(self.gamestate, child_position, 'reaction')

                # this respresnts a check - this will be terminal if position is 'IP' or will give the action node if position is 'OOP'
                if self.position == 'OOP':
                    action_node = Node(self.gamestate, self.position, 'action')
                else:
                    terminal_check_node = Node(self.gamestate, self.position, 'terminal')

        # add options for reaction nodes
        elif self.type == 'reaction':
            for action in self.frequences:
                # this node is just for the calcuation
                fold_node = Node(self.gamestate, self.position, 'terminal')

                #this respresents a raise
                reaction_node = Node(self.gamestate, child_position, 'reaction')

                # this respresnts a call - this will be terminal if position is 'IP' or will give the action node if position is 'OOP'
                if self.position == 'OOP':
                    action_node = Node(self.gamestate, self.position, 'action')
                else:
                    terminal_call_node = Node(self.gamestate, self.position, 'terminal')
        

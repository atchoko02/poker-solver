# for now i will try generating a tree of node correctly and ignore the info / stratagy 
# This will represent a node in the tree, and contain all the data that each node will have
class Node:
    def __init__(self, gamestate, position, node_type, raise_level=0, values = {'IP': None, 'OOP': None}):
        self.gamestate = gamestate  # this will be the game state at this node
        self.children = []
        self.position = position  # 'IP' or 'OOP'
        self.type = node_type # for node type, we can have action (bet, check, fold) raction (raise, call, fold) or terminal node
        self.raise_level = raise_level
        self.values = values # None if values aren't calculated yer, or a dict like {'IP': 1, 'OOP': -1} if they are 
        self.isFold = False

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
                fold_node.isFold = True
                self.children.append(fold_node)

                #check if we can raise
                if self.raise_level < k:
                    #this respresents a raise
                    new_state = self.gamestate.__copy__()
                    raise_percent = self.gamestate.betting_percents[self.position]
                    new_state.pot += new_state.pot * raise_percent
                    new_state.contribution[self.position] += new_state.pot * raise_percent
                    reaction_node = Node(new_state, child_position, 'reaction', raise_level=self.raise_level + 1)
                    self.children.append(reaction_node)
                # if we cant raise we replicate a check
                else:
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
                fold_node.isFold = True
                self.children.append(fold_node)

                # check if we can raise
                if self.raise_level < k:
                    #this respresents a raise
                    new_state = self.gamestate.__copy__()
                    raise_percent = self.gamestate.betting_percents[self.position]
                    new_state.pot += new_state.pot * raise_percent
                    new_state.contripution[self.position] += new_state.pot * raise_percent
                    reaction_node = Node(new_state, child_position, 'reaction', raise_level=self.raise_level + 1)
                    self.children.append(reaction_node)
                # if we cant raise we replicate a call
                else:
                    if len(self.gamestate.community_cards) == 5:
                        # if we are at the river it doesnt make a new sequence
                        # so we just add a terminal node
                        new_state = self.gamestate.__copy__()
                        call_amount = self.gamestate.intial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                        new_state.contribution[self.position] += call_amount
                        new_state.pot += call_amount
                        call_node = Node(new_state, self.position, 'terminal')
                        self.children.append(call_node)
                    else:
                        new_state = self.gamestate.__copy__()
                        new_state.add_card()
                        call_amount = self.gamestate.intial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                        new_state.contribution[self.position] += call_amount
                        new_state.pot += call_amount
                        call_node = Node(new_state, child_position, 'action')
                        self.children.append(call_node)
                

                # call
                if len(self.gamestate.community_cards) == 5:
                    # if we are at the river it doesnt make a new sequence
                    # so we just add a terminal node
                    new_state = self.gamestate.__copy__()
                    call_amount = self.gamestate.intial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                    new_state.contribution[self.position] += call_amount
                    new_state.pot += call_amount
                    call_node = Node(new_state, self.position, 'terminal')
                    self.children.append(call_node)
                else:
                    new_state = self.gamestate.__copy__()
                    new_state.add_card()
                    call_amount = self.gamestate.intial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                    new_state.contribution[self.position] += call_amount
                    new_state.pot += call_amount
                    call_node = Node(new_state, child_position, 'action')
                    self.children.append(call_node)

        for node in self.children:
            # recursively generate children for each child node
            node.generate_children(k)

    def calc_values(self):
        if self.type == 'terminal':
            # if a player has folded
            if self.isFold:
                other_position = 'IP' if self.position == 'OOP' else 'OOP'
                self.values[self.position] = -self.gamestate.contribution[self.position]
                self.values[other_position] = self.gamestate.pot
            # showodown node
            else:
            # Calculate the value of the terminal node based on the game state
                IPRange = self.gamestate.IPRange
                OOPRange = self.gamestate.OOPRange
                IP_win = 0
                OOP_win = 0
                split = 0
                for IPhand in IPRange.hands:
                    for card in IPhand.cards:
                        if card in self.gamestate.community_cards:
                            continue
                    for hand2 in OOPRange.hands:
                        for card2 in hand2.cards:
                            if card2 in self.gamestate.community_cards or card2 in IPhand.cards:
                                continue
                        if self.gamestate.evaluator.evaluate(IPhand.cards, self.gamestate.community_cards) > self.gamestate.evaluator.evaluate(hand2.cards, self.gamestate.community_cards):
                            IP_win += 1
                        elif self.gamestate.evaluator.evaluate(IPhand.cards, self.gamestate.community_cards) < self.gamestate.evaluator.evaluate(hand2.cards, self.gamestate.community_cards):
                            OOP_win += 1
                        else:
                            split += 1
                total = IP_win + OOP_win + split
                if total == 0:
                    self.values['IP'] = 0
                    self.values['OOP'] = 0
                else:
                    IP_win_percent = IP_win / total
                    OOP_win_percent = OOP_win / total
                    split_percent = split / total
                    self.values['IP'] = IP_win_percent * self.gamestate.pot - OOP_win_percent * self.gamestate.contribution['IP'] + split_percent * (self.gamestate.pot / 2)
                    self.values['OOP'] = OOP_win_percent * self.gamestate.pot - IP_win_percent * self.gamestate.contribution['OOP'] + split_percent * (self.gamestate.pot / 2)
            print(f"Terminal Node Values: {self.values}")
            return
        else:
            print(f"Calculating values for node: {self}")
            print(self.children)
            player_range = self.gamestate.IPRange if self.position == 'IP' else self.gamestate.OOPRange
            player_freqs = self.gamestate.IPfreqs if self.position == 'IP' else self.gamestate.OOPfreqs

            for hand in player_range.hands:
                evs = [0, 0, 0] # fold, raise, call/check
                for i in range(3):
                    print('Calculating value for child:', self.children[i])
                    self.children[i].calc_values()
                    evs[i] = self.children[i].values[self.position] * player_freqs[hand][i]
                
                strategy_value = sum(evs)
                for i in range(3):
                    if self.position == 'IP':
                        self.gamestate.IPRegret[hand][i] = max(0, evs[i] - strategy_value)
                    else:
                        self.gamestate.OOPRegret[hand][i] = max(0, evs[i] - strategy_value)
                
                # start forming new strategy values
                if self.position == 'IP':
                    for hand in self.gamestate.IPfreqs:
                        self.gamestate.IPfreqs[hand] = [
                            self.gamestate.IPRegret[hand][0] / sum(self.gamestate.IPRegret[hand]),
                            self.gamestate.IPRegret[hand][1] / sum(self.gamestate.IPRegret[hand]),
                            self.gamestate.IPRegret[hand][2] / sum(self.gamestate.IPRegret[hand])
                        ]
                else:
                    for hand in self.gamestate.OOPfreqs:
                        self.gamestate.OOPfreqs[hand] = [
                            self.gamestate.OOPRegret[hand][0] / sum(self.gamestate.OOPRegret[hand]),
                            self.gamestate.OOPRegret[hand][1] / sum(self.gamestate.OOPRegret[hand]),
                            self.gamestate.OOPRegret[hand][2] / sum(self.gamestate.OOPRegret[hand])
                        ]


    def to_string_tree(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.position}, {self.type}, {len(self.gamestate.community_cards)}\n"
        for child in self.children:
            result += child.to_string_tree(level + 1)
        return result
    
    def __repr__(self):
        return f"Node(position={self.position}, type={self.type}, card_count={len(self.gamestate.community_cards)})"
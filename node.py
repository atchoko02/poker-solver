# for now i will try generating a tree of node correctly and ignore the info / stratagy 
# This will represent a node in the tree, and contain all the data that each node will have
class Node:
    def __init__(self, gamestate, position, node_type, raise_level=0):
        self.gamestate = gamestate  # this will be the game state at this node
        self.children = []
        self.position = position  # 'IP' or 'OOP'
        self.type = node_type # for node type, we can have action (bet, check, fold) raction (raise, call, fold) or terminal node
        self.raise_level = raise_level
        self.isFold = False

    def generate_children(self, k):
        #base case for recursion
        if self.type == 'terminal':
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
                new_state = self.gamestate.__copy__()
                fold_node = Node(new_state, self.position, 'terminal')
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
                        new_state = self.gamestate.__copy__()
                        action_node = Node(new_state, child_position, 'action')
                        self.children.append(action_node)
                    else:
                        if len(self.gamestate.community_cards) == 5:
                            # if we are at the river it doesnt make a new sequence
                            # so we just add a terminal node
                            new_state = self.gamestate.__copy__()
                            action_node = Node(new_state, self.position, 'terminal')
                            self.children.append(action_node)
                        else:
                            new_state = self.gamestate.__copy__()
                            new_state.add_card()
                            IP_check_node = Node(new_state, child_position, 'action')
                            self.children.append(IP_check_node)


                # this respresnts a check - for IP this will start a new sequence
                if self.position == 'OOP':
                    action_node = Node(self.gamestate.__copy__(), child_position, 'action')
                    self.children.append(action_node)
                else:
                    if len(self.gamestate.community_cards) == 5:
                        # if we are at the river it doesnt make a new sequence
                        # so we just add a terminal node
                        action_node = Node(self.gamestate.__copy__(), self.position, 'terminal')
                        self.children.append(action_node)
                    else:
                        new_state = self.gamestate.__copy__()
                        new_state.add_card()
                        IP_check_node = Node(new_state, child_position, 'action')
                        self.children.append(IP_check_node)

        # add options for reaction nodes
        elif self.type == 'reaction':
                # this node is just for the calcuation
                new_state = self.gamestate.__copy__()
                fold_node = Node(new_state, self.position, 'terminal')
                fold_node.isFold = True
                self.children.append(fold_node)

                # check if we can raise
                if self.raise_level < k:
                    #this respresents a raise
                    new_state = self.gamestate.__copy__()
                    raise_percent = self.gamestate.betting_percents[self.position]
                    new_state.pot += new_state.pot * raise_percent
                    new_state.contribution[self.position] += new_state.pot * raise_percent
                    reaction_node = Node(new_state, child_position, 'reaction', raise_level=self.raise_level + 1)
                    self.children.append(reaction_node)
                # if we cant raise we replicate a call
                else:
                    if len(self.gamestate.community_cards) == 5:
                        # if we are at the river it doesnt make a new sequence
                        # so we just add a terminal node
                        new_state = self.gamestate.__copy__()
                        call_amount = self.gamestate.initial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                        new_state.contribution[self.position] += call_amount
                        new_state.pot += call_amount
                        call_node = Node(new_state, self.position, 'terminal')
                        self.children.append(call_node)
                    else:
                        new_state = self.gamestate.__copy__()
                        new_state.add_card()
                        call_amount = self.gamestate.initial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                        new_state.contribution[self.position] += call_amount
                        new_state.pot += call_amount
                        call_node = Node(new_state, child_position, 'action')
                        self.children.append(call_node)
                

                # call
                if len(self.gamestate.community_cards) == 5:
                    # if we are at the river it doesnt make a new sequence
                    # so we just add a terminal node
                    new_state = self.gamestate.__copy__()
                    call_amount = self.gamestate.initial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                    new_state.contribution[self.position] += call_amount
                    new_state.pot += call_amount
                    call_node = Node(new_state, self.position, 'terminal')
                    self.children.append(call_node)
                else:
                    new_state = self.gamestate.__copy__()
                    new_state.add_card()
                    call_amount = self.gamestate.initial_pot + self.gamestate.contribution[self.position] - self.gamestate.pot
                    new_state.contribution[self.position] += call_amount
                    new_state.pot += call_amount
                    call_node = Node(new_state, child_position, 'action')
                    self.children.append(call_node)

        for node in self.children:
            # recursively generate children for each child node
            node.generate_children(k)

    def calc_values(self):
        if self.type == 'terminal':
            print(f"calculating terminal node: {self}")
            # if a player has folded
            if self.isFold:
                other_position = 'IP' if self.position == 'OOP' else 'OOP'
                IPRange = self.gamestate.IPRange
                OOPRange = self.gamestate.OOPRange
                for IPhand in IPRange.hands:
                    for card in IPhand.cards:
                        if card in self.gamestate.community_cards:
                            self.gamestate.IPvalues[IPhand] = 0
                            continue
                    for OOPhand in OOPRange.hands:
                        for card2 in OOPhand.cards:
                            if card2 in self.gamestate.community_cards or card2 in IPhand.cards:
                                self.gamestate.OOPvalues[OOPhand] = 0
                                continue
                        if self.position == 'IP':
                            self.gamestate.OOPvalues[OOPhand] = self.gamestate.pot
                            self.gamestate.IPvalues[IPhand] = -self.gamestate.contribution['IP']
                        else:
                            self.gamestate.IPvalues[IPhand] = self.gamestate.pot
                            self.gamestate.OOPvalues[OOPhand] = -self.gamestate.contribution['OOP']
                
        
            # showodown node
            else:
            # Calculate the value of the terminal node based on the game state
                IPRange = self.gamestate.IPRange
                OOPRange = self.gamestate.OOPRange

                # useed for calculating the win percentages
                IP_win_map = {}
                IP_total_map = {}
                IPsplit_map = {}
                for hand in IPRange.hands:
                    IP_win_map[hand] = 0
                    IP_total_map[hand] = 0
                    IPsplit_map[hand] = 0

                OOP_win_map = {}
                OOP_total_map = {}
                OOPsplit_map = {}
                for hand in OOPRange.hands:
                    OOP_win_map[hand] = 0
                    OOP_total_map[hand] = 0
                    OOPsplit_map[hand] = 0
                
                
                # get the number of wins for each hand in both ranges 
                for IPhand in IPRange.hands:
                    for card in IPhand.cards:
                        if card in self.gamestate.community_cards:
                            continue
                    for OOPhand in OOPRange.hands:
                        for card2 in OOPhand.cards:
                            if card2 in self.gamestate.community_cards or card2 in IPhand.cards:
                                continue
                        if self.gamestate.evaluator.evaluate(list(IPhand.cards), self.gamestate.community_cards) > self.gamestate.evaluator.evaluate(list(OOPhand.cards), self.gamestate.community_cards):
                            IP_win_map[IPhand] += 1
                        elif self.gamestate.evaluator.evaluate(list(IPhand.cards), self.gamestate.community_cards) < self.gamestate.evaluator.evaluate(list(OOPhand.cards), self.gamestate.community_cards):
                            OOP_win_map[OOPhand] += 1
                        else:
                            IPsplit_map[IPhand] += 1
                            OOPsplit_map[OOPhand] += 1
                        IP_total_map[IPhand] += 1
                        OOP_total_map[OOPhand] += 1
                
                # calculate values for IP hands
                for hand in IP_win_map:
                    if IP_total_map[hand] == 0:
                        self.gamestate.IPvalues[hand] = 0
                    else:
                        IP_win_percent = IP_win_map[hand] / IP_total_map[hand]
                        split_percent = IPsplit_map[hand] / IP_total_map[hand]
                        self.gamestate.IPvalues[hand] = IP_win_percent * self.gamestate.pot - (IP_total_map[hand] - IP_win_map[hand]) * self.gamestate.contribution['IP'] + split_percent * (self.gamestate.pot / 2)

                # calculate values for OOP hands
                for hand in OOP_win_map:
                    if OOP_total_map[hand] == 0:
                        self.gamestate.OOPvalues[hand] = 0
                    else:
                        OOP_win_percent = OOP_win_map[hand] / OOP_total_map[hand]
                        split_percent = OOPsplit_map[hand] / OOP_total_map[hand]
                        self.gamestate.OOPvalues[hand] = OOP_win_percent * self.gamestate.pot - (OOP_total_map[hand] - OOP_win_map[hand]) * self.gamestate.contribution['OOP'] + split_percent * (self.gamestate.pot / 2)

                for hand in self.gamestate.IPRange.hands:
                    if hand not in self.gamestate.IPvalues or self.gamestate.IPvalues[hand] is None:
                        self.gamestate.IPvalues[hand] = 0

                for hand in self.gamestate.OOPRange.hands:
                    if hand not in self.gamestate.OOPvalues or self.gamestate.OOPvalues[hand] is None:
                        self.gamestate.OOPvalues[hand] = 0
        else:
            print(f"calculating: {self}, current values: IP{self.gamestate.IPvalues} OOP{self.gamestate.OOPvalues}")
            player_range = self.gamestate.IPRange if self.position == 'IP' else self.gamestate.OOPRange
            player_freqs = self.gamestate.IPfreqs if self.position == 'IP' else self.gamestate.OOPfreqs

            for hand in player_range.hands:
                evs = [0, 0, 0] # fold, raise, call/check
                for i in range(3):
                    if self.position == 'IP':
                        if self.children[i].gamestate.IPvalues[hand] is None:
                            self.children[i].calc_values()
                        ip_val = self.children[i].gamestate.IPvalues.get(hand)
                        freq = player_freqs[hand][i]
                        if ip_val != None:
                            evs[i] = ip_val * freq
                        else:
                            evs[i] = 0
                    else:
                        if self.children[i].gamestate.OOPvalues[hand] is None:
                            self.children[i].calc_values()
                        oop_val = self.children[i].gamestate.OOPvalues.get(hand)
                        freq = player_freqs[hand][i]
                        if oop_val != None:
                            evs[i] = oop_val * freq
                        else:
                            evs[i] = 0
                
                strategy_value = sum(evs[i] * player_freqs[hand][i] for i in range(3) if evs[i] is not None and player_freqs[hand][i] is not None)
                for i in range(3):
                    regret = evs[i] - strategy_value
                    if self.position == 'IP':
                        self.gamestate.IPRegret[hand][i] = max(0, regret)
                    else:
                        self.gamestate.OOPRegret[hand][i] = max(0, regret)
                
                # start forming new strategy values
                # if self.position == 'IP':
                #     print(f"IP Regret for {hand}: {self.gamestate.IPRegret[hand]}")
                #     print(f"sum: {sum(self.gamestate.IPRegret[hand])}")
                #     regret_sum = sum(self.gamestate.IPRegret[hand])
                #     for hand in self.gamestate.IPfreqs:
                #         self.gamestate.IPfreqs[hand] = [
                #             self.gamestate.IPRegret[hand][0] / regret_sum,
                #             self.gamestate.IPRegret[hand][1] / regret_sum,
                #             self.gamestate.IPRegret[hand][2] / regret_sum
                #         ]
                # else:
                #     for hand in self.gamestate.OOPfreqs:
                #         regret_sum = sum(self.gamestate.OOPRegret[hand])
                #         self.gamestate.OOPfreqs[hand] = [
                #             self.gamestate.OOPRegret[hand][0] / regret_sum,
                #             self.gamestate.OOPRegret[hand][1] / regret_sum,
                #             self.gamestate.OOPRegret[hand][2] / regret_sum
                #         ]


    def to_string_tree(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.position}, {self.type}, {len(self.gamestate.community_cards)}"
        for child in self.children:
            result += child.to_string_tree(level + 1)
        return result
    
    def __repr__(self):
        return f"Node(position={self.position}, type={self.type}, card_count={len(self.gamestate.community_cards)})"
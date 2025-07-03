
from treys import Card
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
                    raise_amount = new_state.pot * raise_percent
                    new_state.pot += raise_amount
                    new_state.contribution[self.position] += raise_amount
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
                            new_state.add_card(len(self.gamestate.community_cards))
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
                        new_state.add_card(len(self.gamestate.community_cards))
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
                    raise_amount = new_state.pot * raise_percent
                    new_state.pot += raise_amount
                    new_state.contribution[self.position] += raise_amount
                    reaction_node = Node(new_state, child_position, 'reaction', raise_level=self.raise_level + 1)
                    self.children.append(reaction_node)
                # if we cant raise we replicate a call
                else:
                    if len(self.gamestate.community_cards) == 5:
                        # if we are at the river it doesnt make a new sequence
                        # so we just add a terminal node
                        new_state = self.gamestate.__copy__()
                        call_amount = 0
                        if self.position == 'OOP':
                            call_amount = self.gamestate.contribution['IP'] - self.gamestate.contribution['OOP']
                        else:
                            call_amount = self.gamestate.contribution['OOP'] - self.gamestate.contribution['IP']
                        new_state.contribution[self.position] += call_amount
                        new_state.pot += call_amount
                        call_node = Node(new_state, self.position, 'terminal')
                        self.children.append(call_node)
                    else:
                        new_state = self.gamestate.__copy__()
                        new_state.add_card(len(self.gamestate.community_cards))
                        call_amount = 0
                        if self.position == 'OOP':
                            call_amount = self.gamestate.contribution['IP'] - self.gamestate.contribution['OOP']
                        else:
                            call_amount = self.gamestate.contribution['OOP'] - self.gamestate.contribution['IP']
                        new_state.contribution[self.position] += call_amount
                        new_state.pot += call_amount
                        call_node = Node(new_state, child_position, 'action')
                        self.children.append(call_node)
                

                # call
                if len(self.gamestate.community_cards) == 5:
                    # if we are at the river it doesnt make a new sequence
                    # so we just add a terminal node
                    new_state = self.gamestate.__copy__()
                    call_amount = 0
                    if self.position == 'OOP':
                        call_amount = self.gamestate.contribution['IP'] - self.gamestate.contribution['OOP']
                    else:
                        call_amount = self.gamestate.contribution['OOP'] - self.gamestate.contribution['IP']
                    new_state.contribution[self.position] += call_amount
                    new_state.pot += call_amount
                    call_node = Node(new_state, self.position, 'terminal')
                    self.children.append(call_node)
                else:
                    new_state = self.gamestate.__copy__()
                    new_state.add_card(len(self.gamestate.community_cards))
                    call_amount = 0
                    if self.position == 'OOP':
                        call_amount = self.gamestate.contribution['IP'] - self.gamestate.contribution['OOP']
                    else:
                        call_amount = self.gamestate.contribution['OOP'] - self.gamestate.contribution['IP']
                    new_state.contribution[self.position] += call_amount
                    new_state.pot += call_amount
                    #if it is OOP calling - then the next action will still be on OOP
                    if self.position == 'OOP':
                        call_node = Node(new_state, self.position, 'action')
                    else:
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
                IPRange = self.gamestate.IPRange
                OOPRange = self.gamestate.OOPRange

                # for IPhand in IPRange.hands:
                #     self.gamestate.IPvalues[IPhand] = 0
                # for OOPhand in OOPRange.hands:
                #     self.gamestate.OOPvalues[OOPhand] = 0
                
                for IPhand in IPRange.hands:
                    for card in IPhand.cards:
                        if card in self.gamestate.community_cards:
                            # self.gamestate.IPvalues[IPhand] = 0
                            continue
                    for OOPhand in OOPRange.hands:
                        for card2 in OOPhand.cards:
                            if card2 in self.gamestate.community_cards or card2 in IPhand.cards:
                                # self.gamestate.OOPvalues[OOPhand] = 0
                                continue
                        if self.position == 'IP':
                            self.gamestate.OOPvalues[OOPhand] = self.gamestate.contribution['IP']
                            self.gamestate.IPvalues[IPhand] = -self.gamestate.contribution['IP']
                        else:
                            self.gamestate.IPvalues[IPhand] = self.gamestate.contribution['OOP']
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
                        if self.gamestate.evaluator.evaluate(list(IPhand.cards), self.gamestate.community_cards) < self.gamestate.evaluator.evaluate(list(OOPhand.cards), self.gamestate.community_cards):
                            IP_win_map[IPhand] += 1
                        elif self.gamestate.evaluator.evaluate(list(IPhand.cards), self.gamestate.community_cards) > self.gamestate.evaluator.evaluate(list(OOPhand.cards), self.gamestate.community_cards):
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
                        self.gamestate.IPvalues[hand] = IP_win_percent * self.gamestate.pot - ((IP_total_map[hand] - IP_win_map[hand]) / IP_total_map[hand]) * self.gamestate.contribution['IP'] + split_percent * (self.gamestate.pot / 2)

                # calculate values for OOP hands
                for hand in OOP_win_map:
                    if OOP_total_map[hand] == 0:
                        self.gamestate.OOPvalues[hand] = 0
                    else:
                        OOP_win_percent = OOP_win_map[hand] / OOP_total_map[hand]
                        split_percent = OOPsplit_map[hand] / OOP_total_map[hand]
                        self.gamestate.OOPvalues[hand] = OOP_win_percent * self.gamestate.pot - ((OOP_total_map[hand] - OOP_win_map[hand]) / OOP_total_map[hand]) * self.gamestate.contribution['OOP'] + split_percent * (self.gamestate.pot / 2)

                for hand in self.gamestate.IPRange.hands:
                    if hand not in self.gamestate.IPvalues or self.gamestate.IPvalues[hand] is None:
                        self.gamestate.IPvalues[hand] = 0

                for hand in self.gamestate.OOPRange.hands:
                    if hand not in self.gamestate.OOPvalues or self.gamestate.OOPvalues[hand] is None:
                        self.gamestate.OOPvalues[hand] = 0
        else:
            if self.position == 'IP':
                #calculate IP values on IP node - we can use the frequences depending on the hand
                for hand in self.gamestate.IPRange.hands:
                    action_values = []
                    for i in range(3):
                        if self.children[i].gamestate.IPvalues[hand] is None:
                            self.children[i].calc_values()
                        ip_val = self.children[i].gamestate.IPvalues.get(hand)
                        action_values.append(ip_val)
                    strategy_ev = sum(action_values[i] * self.gamestate.IPfreqs[hand][i] for i in range(3))
                    self.gamestate.IPvalues[hand] = strategy_ev
                    for i in range(3):
                        regret = action_values[i] - strategy_ev
                        self.gamestate.IPRegret[hand][i] = max(0, regret)
            
                # for calculating the OOP values on an IP node - we have to use the average of the frequences from IP hands
                # calculate average
                total = len(self.gamestate.IPfreqs)
                average_freqs = [0, 0, 0]
                for hand_freqs in self.gamestate.IPfreqs.values():
                    for i in range(len(hand_freqs)):
                        average_freqs[i] += hand_freqs[i]
                for i in range(len(average_freqs)):
                    average_freqs[i] = average_freqs[i]/total
                
                # calculate OOP value
                for hand in self.gamestate.OOPRange.hands:
                    action_values = []
                    for i in range(3):
                        if self.children[i].gamestate.OOPvalues[hand] is None:
                            self.children[i].calc_values()
                        oop_val = self.children[i].gamestate.OOPvalues.get(hand)
                        action_values.append(oop_val)
                    strategy_ev = sum(action_values[i] * average_freqs[i] for i in range(3))
                    self.gamestate.OOPvalues[hand] = strategy_ev
                    for i in range(3):
                        regret = action_values[i] - strategy_ev
                        self.gamestate.OOPRegret[hand][i] = max(0, regret)
                    
            else:      
                # calculate OOP value on OOP node
                for hand in self.gamestate.OOPRange.hands:
                    action_values = []
                    for i in range(3):
                        if self.children[i].gamestate.OOPvalues[hand] is None:
                            self.children[i].calc_values()
                        oop_val = self.children[i].gamestate.OOPvalues.get(hand)
                        action_values.append(oop_val)
                    strategy_ev = sum(action_values[i] * self.gamestate.OOPfreqs[hand][i] for i in range(3))
                    self.gamestate.OOPvalues[hand] = strategy_ev
                    for i in range(3):
                        regret = action_values[i] - strategy_ev
                        self.gamestate.OOPRegret[hand][i] = max(0, regret)
                
                # calculate average
                total = len(self.gamestate.OOPfreqs)
                average_freqs = [0, 0, 0]
                for hand_freqs in self.gamestate.OOPfreqs.values():
                    for i in range(len(hand_freqs)):
                        average_freqs[i] += hand_freqs[i]
                for i in range(len(average_freqs)):
                    average_freqs[i] = average_freqs[i]/total
                
                # calculate IP value on OOP node
                for hand in self.gamestate.IPRange.hands:
                    action_values = []
                    for i in range(3):
                        if self.children[i].gamestate.IPvalues[hand] is None:
                            self.children[i].calc_values()
                        ip_val = self.children[i].gamestate.IPvalues.get(hand)
                        action_values.append(ip_val)
                    strategy_ev = sum(action_values[i] * average_freqs[i] for i in range(3))
                    self.gamestate.IPvalues[hand] = strategy_ev
                    for i in range(3):
                        regret = action_values[i] - strategy_ev
                        self.gamestate.IPRegret[hand][i] = max(0, regret)

    def calc_new_strat(self):
        # base case
        if self.type == 'terminal':
            return

        # start forming new strategy values
        for hand in self.gamestate.IPfreqs:
            regret_sum = sum(self.gamestate.IPRegret[hand])
            if regret_sum > 0:
                self.gamestate.IPfreqs[hand] = [
                    self.gamestate.IPRegret[hand][0] / regret_sum,
                    self.gamestate.IPRegret[hand][1] / regret_sum,
                    self.gamestate.IPRegret[hand][2] / regret_sum
                    ]
            if regret_sum == 0:
                # if the regret sum is 0, we set the strategy to be uniform
                self.gamestate.IPfreqs[hand] = [1/3, 1/3, 1/3]
        
        for hand in self.gamestate.OOPfreqs:
            regret_sum = sum(self.gamestate.OOPRegret[hand])
            if regret_sum > 0:
                self.gamestate.OOPfreqs[hand] = [
                    self.gamestate.OOPRegret[hand][0] / regret_sum,
                    self.gamestate.OOPRegret[hand][1] / regret_sum,
                    self.gamestate.OOPRegret[hand][2] / regret_sum
                    ]
            if regret_sum == 0:
                # if the regret sum is 0, we set the strategy to be uniform
                self.gamestate.OOPfreqs[hand] = [1/3, 1/3, 1/3]

        # recurse over children
        for child in self.children:
            child.calc_new_strat()
    
    def remove_folded_hands(self, IPfolded_hands, OOPfolded_hands):
        if self.position == 'IP':
            # find if any hands have been folded
            for hand in self.gamestate.IPfreqs:
                if self.gamestate.IPfreqs[hand] is not None and self.gamestate.IPfreqs[hand][0] == 1.0:
                    IPfolded_hands.add(hand)
            
            # remove folded hands from the range
            for hand in IPfolded_hands:
                if hand in self.gamestate.IPRange.hands:
                    self.gamestate.IPRange.remove_hand(hand)   
        else:     
            for hand in self.gamestate.OOPfreqs:
                if self.gamestate.OOPfreqs[hand] is not None and self.gamestate.OOPfreqs[hand][0] == 1.0:
                    OOPfolded_hands.add(hand)

            for hand in OOPfolded_hands:
                if hand in self.gamestate.OOPRange.hands:
                    self.gamestate.OOPRange.remove_hand(hand)
            
        # recurese over children
        for child in self.children:
            child.remove_folded_hands(IPfolded_hands.copy(), OOPfolded_hands.copy())

    def to_string_tree(self, level=0):
        indent = "  " * level
        result = f"{indent}{self.position}, {self.type}, {len(self.gamestate.community_cards)}"
        for child in self.children:
            result += child.to_string_tree(level + 1)
        return result
    
    def __repr__(self):
        return f"Node(position={self.position}, type={self.type}, card_count={len(self.gamestate.community_cards)})"
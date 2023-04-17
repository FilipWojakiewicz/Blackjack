import tkinter as tk
from Deck import Deck
from Hand import Hand

class Player:
    def __init__(self, score):
        self.hand = Hand()
        self.img_hand = []
        self.split_hand = None
        self.img_split_hand = None
        self.score = score
        self.split = False
        self.game_over = {'hand' : False, 'split_hand': False}

    def add_card(self, deck):
        self.hand.add_card(deck.deal())

    def add_split_card(self, deck):
        self.split_hand.add_card(deck.deal())

    def add_img(self, path, split=False):
        if split == False:
            self.img_hand.append(tk.PhotoImage(file=path))
        else:
            self.img_split_hand.append(tk.PhotoImage(file=path)) 

    def set_split(self, split):
        self.split = split

    def change_score(self, value):
        self.score += value

    def get_cards(self, split = False):
        if split == False:
            return self.hand.get_cards()
        else:
            return self.split_hand.get_cards()

    def get_img(self, split = False):
        if split == False:
            return self.img_hand
        else:
            return self.img_split_hand
        
    def get_split(self):
        return self.split
    
    def get_value(self, split = False):
        if split == False:
            return self.hand.get_value()
        else:
            return self.split_hand.get_value()

    def get_score(self):
        return self.score
    
    def get_deal(self):
        return self.deal

    def clear_cards(self):
        for i in range(0,len(self.hand.get_cards())):
            self.hand.remove_card(self.hand.get_cards()[0])
        self.img_hand.clear()
        self.game_over['hand'] = False
        if self.split_hand != None:
            for i in range(0,len(self.split_hand.get_cards())):
                self.split_hand.remove_card(self.split_hand.get_cards()[0])
            self.img_split_hand.clear()
            self.game_over['split_hand'] = False

    def split_cards(self):
        self.split_hand = Hand()
        self.img_split_hand = []
        self.split_hand.add_card(self.hand.get_cards()[1])
        self.hand.remove_card(self.hand.get_cards()[1])
        #self.img_split_hand.append(self.get_img()[1])
        self.img_hand.remove(self.get_img()[1])
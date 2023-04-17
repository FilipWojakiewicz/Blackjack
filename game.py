import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sys

from Deck import Deck
#from Hand import Hand
from Player import Player
from Solution import Move

HIGH = 800
WIDTH = 1000


def return_window(window_now, window_new):
    window_now.pack_forget()
    window_new.pack()

def show_card(player, label_cards_player, i, x, y, split=False):
    if split == False:
        player.add_img(path=card_name(card=player.get_cards()[i]))
        label_cards_player.append(tk.Label(image=player.get_img()[i]))
        label_cards_player[i].img = player.get_img()[i]
        label_cards_player[i].pack()
        label_cards_player[i].place(x=x, y=y, anchor='center')
    else:
        player.add_img(path=card_name(card=player.get_cards(True)[i]), split=True)
        label_cards_player.append(tk.Label(image=player.get_img(True)[i]))
        label_cards_player[i].img = player.get_img(True)[i]
        label_cards_player[i].pack()
        label_cards_player[i].place(x=x, y=y, anchor='center')

def update_label(player, Label_player_value, Label_score, Label_player_value_split=None):
    if player.get_split() == False:
        Label_player_value.config(text=f"Player card value: {player.get_value()}")
        Label_score.config(text=f"Score: {player.get_score()}")
    else:
        Label_player_value.config(text=f"Player card_1 value: {player.get_value()}")
        Label_player_value_split.config(text=f"Player card_2 value: {player.get_value(True)}")

def clear(player, label_cards_player, dealer, label_cards_dealer, label_cards_player_split = None):
    for i in range (0, len(player.get_img())):
        label_cards_player[i].destroy()
    for i in range (0, len(dealer.get_img())):
        label_cards_dealer[i].destroy()
    if player.get_split() == True:
        if label_cards_player_split != None:
            for i in range (0, len(player.get_img(True))):
                label_cards_player_split[i].destroy()
            label_cards_player_split.clear()
        player.set_split(False)
    player.clear_cards()
    dealer.clear_cards()
    label_cards_player.clear()
    label_cards_dealer.clear()

def button_forget(list):
    for button in list:
        button.place_forget()

def card_name(card):
    rank = str(card.rank)
    if card.suit == 'Hearts ♥':
        suit = 'hearts'
    elif card.suit == 'Diamonds ♦':
        suit = 'diamonds'
    elif card.suit == 'Clubs ♣':
        suit = 'clubs'
    elif card.suit == 'Spades ♠':
        suit = 'spades'
    return 'GUI/cards/' + rank + '_of_' + suit + '.png' 

def prize_to_win(player_value, dealer_value):
    if player_value > dealer_value and player_value <= 21:
        prize = 10
    elif dealer_value > player_value and dealer_value <= 21:
        prize = -10   
    elif player_value > 21 and dealer_value <= 21:
        prize = -10
    elif player_value <= 21 and dealer_value > 21:
        prize = 10
    else:
        prize = 0
    return prize

def determine_winner(player, dealer):
    player_value = player.hand.get_value()
    dealer_value = dealer.hand.get_value()
    prize = prize_to_win(player_value, dealer_value)

    if player.game_over['hand'] == 'hit' or player.game_over['hand'] == 'stand':
        player.change_score(prize)
    elif player.game_over['hand'] == 'double':
        player.change_score(2*prize)
    elif player.game_over['hand'] == 'fold':
        player.change_score(-10)

    if player.get_split() == True:
        player_split_value = player.split_hand.get_value()
        prize = prize_to_win(player_split_value, dealer_value)
        if player.game_over['split_hand'] == 'hit' or player.game_over['split_hand'] == 'stand':
            player.change_score(prize)
        elif player.game_over['split_hand'] == 'double':
            player.change_score(2*prize)
        elif player.game_over['split_hand'] == 'fold':
            player.change_score(-10)

def dealer_turn(deck, player, dealer, label_cards_dealer):
    if player.get_split() == False:    
        while dealer.get_value() < 17:
            dealer.add_card(deck)
        label_cards_dealer[0].place(x=465, y=150, anchor='center')
        for i in range (1,len(dealer.get_cards())):
            show_card(dealer, label_cards_dealer, i, x=465+35*i, y=150)
        determine_winner(player, dealer)
    elif player.get_split() == True:
        if player.game_over['hand'] != False and player.game_over['split_hand'] != False:
            while dealer.get_value() < 17:
                dealer.add_card(deck)
            label_cards_dealer[0].place(x=465, y=150, anchor='center')
            for i in range (1,len(dealer.get_cards())):
                show_card(dealer, label_cards_dealer, i, x=465+35*i, y=150)
            determine_winner(player, dealer)

def double(deck, player, label_cards_player, dealer, label_cards_dealer, turn=1, label_cards_player_split=None):
    if player.get_split() == False:
        if len(player.get_cards()) == 2:
            if player.get_value() < 21:
                player.add_card(deck)
                tmpl = len(player.get_cards()) - 1
                show_card(player, label_cards_player, tmpl, x=465+35*tmpl, y=440)
                player.game_over['hand'] = 'double'
                dealer_turn(deck, player, dealer, label_cards_dealer)
    else:
        if turn == 1:
            if len(player.get_cards()) == 2:
                if player.get_value() < 21:
                    player.add_card(deck)
                    tmpl = len(player.get_cards()) - 1
                    show_card(player, label_cards_player, tmpl, x=340+35*tmpl, y=420)
                    player.game_over['hand'] = 'double'
        elif turn == 2:
            if len(player.get_cards(True)) == 2:
                if player.get_value(True) < 21:
                    player.add_split_card(deck)
                    tmpl = len(player.get_cards(True)) - 1
                    show_card(player, label_cards_player_split, tmpl, x=590+35*tmpl, y=420, split=True)
                    player.game_over['split_hand'] = 'double'

def hit(deck, player, label_cards_player, dealer, label_cards_dealer, turn=1, label_cards_player_split=None):
    if player.get_split() == False:
        if player.get_value() < 21:
            player.add_card(deck)
            tmpl = len(player.get_cards()) - 1
            show_card(player, label_cards_player, tmpl, x=465+35*tmpl, y=440)
        if player.get_value() >= 21:
            player.game_over['hand'] = 'hit'
            dealer_turn(deck, player, dealer, label_cards_dealer)
    else:
        if turn == 1:
            if player.get_value() < 21:
                player.add_card(deck)
                tmpl = len(player.get_cards()) - 1
                show_card(player, label_cards_player, tmpl, x=340+35*tmpl, y=420)
            if player.get_value() >= 21:
                player.game_over['hand'] = 'hit'
        elif turn == 2:
            if player.get_value(True) < 21:
                player.add_split_card(deck)
                tmpl = len(player.get_cards(True)) - 1
                show_card(player, label_cards_player_split, tmpl, x=590+35*tmpl, y=420, split=True)
            if player.get_value(True) >= 21:
                player.game_over['split_hand'] = 'hit'

def stand(deck, player, dealer, label_cards_dealer, turn=1):
    if player.split == False:
        if player.game_over['hand'] == False:
            if player.get_value() < 21:
                player.game_over['hand'] = 'stand'
                dealer_turn(deck, player, dealer, label_cards_dealer)
    else:
        if turn == 1:
            player.game_over['hand'] = 'stand'
        elif turn == 2:
            player.game_over['split_hand'] = 'stand'

def is_blackjack(player):
    card1 = player.get_cards()[0]
    card2 = player.get_cards()[1]
    if card1.value + card2.value == 21:
        return True
    else:
        return False 

def deal(new_game ,deck, player, label_cards_player, dealer, label_cards_dealer, label_cards_player_split = None):
    if new_game == True:
        clear(player, label_cards_player, dealer, label_cards_dealer , label_cards_player_split)
    player.add_card(deck)
    dealer.add_card(deck)
    player.add_card(deck)
    dealer.add_card(deck)
    if is_blackjack(player=player):
       prize = 15
       player.change_score(prize)
    for i in range (0,len(player.get_cards())):
        show_card(player, label_cards_player, i, x=465+35*i, y=440)
    show_card(dealer, label_cards_dealer, 0, x=500, y=150)    

def game(window_old):

    def split():
        if len(player.get_cards()) == 2:
            if player.get_cards()[0].rank == player.get_cards()[1].rank:
                label_cards_player_split = []
        
                button_forget([button_stand, button_hit, button_double, button_split, button_next_game])
        
                label_cards_player[1].place_forget()
        
                button_stand_1 = tk.Button(window_game, command=lambda: [stand(deck, player, dealer, label_cards_dealer), update_label(player, Label_player_value, Label_score, Label_player_value_split)],
                                            text='Stand_1', height='0', width='10', font=('timesnewroman', 18, 'bold'))
                button_stand_2 = tk.Button(window_game, command=lambda: [stand(deck, player, dealer, label_cards_dealer, 2), update_label(player, Label_player_value, Label_score, Label_player_value_split)],
                                            text='Stand_2', height='0', width='10', font=('timesnewroman', 18, 'bold'))
                button_hit_1 = tk.Button(window_game, command=lambda: [hit(deck, player, label_cards_player, dealer, label_cards_dealer), update_label(player, Label_player_value, Label_score, Label_player_value_split)],
                                        text='Hit_1', height='0', width='10', font=('timesnewroman', 18, 'bold'))
                button_hit_2 = tk.Button(window_game, command=lambda: [hit(deck, player, label_cards_player, dealer, label_cards_dealer, 2, label_cards_player_split), update_label(player, Label_player_value, Label_score, Label_player_value_split)],
                                        text='Hit_2', height='0', width='10', font=('timesnewroman', 18, 'bold'))
                button_double_1 = tk.Button(window_game, command=lambda: [double(deck, player, label_cards_player, dealer, label_cards_dealer), update_label(player, Label_player_value, Label_score, Label_player_value_split)],
                                           text='Double_1', height='0', width='10', font=('timesnewroman', 18, 'bold'))
                button_double_2 = tk.Button(window_game, command=lambda: [double(deck, player, label_cards_player, dealer, label_cards_dealer, 2, label_cards_player_split), update_label(player, Label_player_value, Label_score, Label_player_value_split)],
                                           text='Double_2', height='0', width='10', font=('timesnewroman', 18, 'bold'))
                button_dealer_turn = tk.Button(window_game, command=lambda: [dealer_turn(deck, player, dealer, label_cards_dealer), Label_dealer_value.config(text=f"Dealer card value: {dealer.get_value()}")],
                                             text='Dealer turn', height='2', width='10', font=('timesnewroman', 18, 'bold'))
                button_next_game_split = tk.Button(window_game, command=lambda: [clear_screen(elements), buttons(button_stand, button_hit, button_double, button_split, button_next_game),
                                                                                 deal(True, deck, player, label_cards_player, dealer, label_cards_dealer, label_cards_player_split), update_label(player, Label_player_value, Label_score), Label_dealer_value.config(text="")],
                                                    text='Next game', height='2', width='10', font=('timesnewroman', 18, 'bold'))
                
                button_stand_1.pack()
                button_stand_1.place(x=100, y=HIGH-100, anchor='center')
                button_stand_2.pack()
                button_stand_2.place(x=100, y=HIGH-50, anchor='center')
                button_hit_1.pack()
                button_hit_1.place(x=300, y=HIGH-100, anchor='center')
                button_hit_2.pack()
                button_hit_2.place(x=300, y=HIGH-50, anchor='center')
                button_double_1.pack()
                button_double_1.place(x=500, y=HIGH-100, anchor='center')
                button_double_2.pack()
                button_double_2.place(x=500, y=HIGH-50, anchor='center')
                button_dealer_turn.pack()
                button_dealer_turn.place(x=700, y=HIGH-75, anchor='center')
                button_next_game_split.pack()
                button_next_game_split.place(x=900, y=HIGH-75, anchor='center')
        
                label_cards_player.pop(1)
                player.split_cards()
                player.add_card(deck)
                player.add_split_card(deck)
        
                label_cards_player[0].place(x=340, y=420, anchor='center')
                show_card(player, label_cards_player, 1, x=340+35*1, y=420)
                    
                for i in range (0,len(player.get_cards(True))):
                    show_card(player, label_cards_player_split, i, x=590+35*i, y=420, split=True)
        
                Label_player_value.config(text=f"Player card_1 value: {player.get_value()}")
                Label_player_value_split = tk.Label(window_game, text=f"Player card_2 value: {player.get_value(True)}", font = ("timesnewroman", 18, "bold"))
        
                Label_player_value.pack()
                Label_player_value.place(x=20, y=620, anchor="w")
                Label_dealer_value.pack()
                Label_dealer_value.place(x=980, y=620, anchor="e")
                Label_player_value_split.pack()
                Label_player_value_split.place(x=500, y=620, anchor="center")
                
                elements = [button_stand_1, button_stand_2, button_hit_1, button_hit_2, button_double_1, button_double_2, button_dealer_turn, button_next_game_split, Label_player_value_split]


    window_old.pack_forget()
    window_game = tk.Frame(window, height=str(HIGH), width=str(WIDTH))

    #preper game
    deck = Deck()
    deck.shuffle()
    player = Player(100)
    dealer = Player(None)

    label_cards_player = []
    label_cards_dealer = []

    
    
    button_stand = tk.Button(window_game, command=lambda: [stand(deck, player, dealer, label_cards_dealer), update_label(player, Label_player_value, Label_score), Label_dealer_value.config(text=f"Dealer card value: {dealer.get_value()}")],
                             text='Stand', height='2', width='10', font=('timesnewroman', 18, 'bold'))
    button_hit = tk.Button(window_game, command=lambda: [hit(deck, player, label_cards_player, dealer, label_cards_dealer), update_label(player, Label_player_value, Label_score), Label_dealer_value.config(text=f"Dealer card value: {dealer.get_value()}")],
                            text='Hit', height='2', width='10', font=('timesnewroman', 18, 'bold'))
    button_double = tk.Button(window_game, command=lambda: [double(deck, player, label_cards_player, dealer, label_cards_dealer), update_label(player, Label_player_value, Label_score), Label_dealer_value.config(text=f"Dealer card value: {dealer.get_value()}")],
                               text='Double', height='2', width='10', font=('timesnewroman', 18, 'bold'))
    button_split = tk.Button(window_game, command=lambda: [player.set_split(True), split()], text='Split', height='2', width='10', font=('timesnewroman', 18, 'bold'))
    button_next_game = tk.Button(window_game, command=lambda: [deal(True, deck, player, label_cards_player, dealer, label_cards_dealer), update_label(player, Label_player_value, Label_score), Label_dealer_value.config(text="")],
                                 text='Next game', height='2', width='10', font=('timesnewroman', 18, 'bold'))
    
    button_stand.pack()
    button_stand.place(x=100, y=HIGH-70, anchor='center')
    button_hit.pack()
    button_hit.place(x=300, y=HIGH-70, anchor='center')
    button_double.pack()
    button_double.place(x=500, y=HIGH-70, anchor='center')
    button_split.pack()
    button_split.place(x=700, y=HIGH-70, anchor='center')
    button_next_game.pack()
    button_next_game.place(x=900, y=HIGH-70, anchor='center')

    img_table = tk.PhotoImage(file="GUI/table.png")
    label_table = tk.Label(image=img_table)
    label_table.img = img_table
    label_table.pack()
    label_table.place(x=0, y=0, anchor='nw')

    deal(False ,deck, player, label_cards_player, dealer, label_cards_dealer)
    
    Label_player_value = tk.Label(window_game, text=f"Player card value: {player.get_value()}", font = ("timesnewroman", 18, "bold"))
    Label_dealer_value = tk.Label(window_game, font = ("timesnewroman", 18, "bold"))
    Label_score = tk.Label(window_game, text=f"Score: {player.get_score()}", font = ("timesnewroman", 18, "bold"))
   
    Label_player_value.pack()
    Label_player_value.place(x=50, y=620, anchor="w")
    Label_dealer_value.pack()
    Label_dealer_value.place(x=950, y=620, anchor="e")
    Label_score.pack()
    Label_score.place(x=500, y=620, anchor="center")
    
    def clear_screen(list_of_elements):
        for element in list_of_elements:
            element.destroy()
    
    def buttons(button_stand, button_hit, button_double, button_split, button_next_game):
        button_stand.pack()
        button_stand.place(x=100, y=HIGH-70, anchor='center')
        button_hit.pack()
        button_hit.place(x=300, y=HIGH-70, anchor='center')
        button_double.pack()
        button_double.place(x=500, y=HIGH-70, anchor='center')
        button_split.pack()
        button_split.place(x=700, y=HIGH-70, anchor='center')
        button_next_game.pack()
        button_next_game.place(x=900, y=HIGH-70, anchor='center')


    
    window_game.pack()
        


def menu():

    window_menu = tk.Frame(window, height=str(HIGH), width=str(WIDTH))
    window_old = window_menu
    
    #Creating elements
    text_menu = tk.Label(window_menu, text='Menu gry', height='30', width='100', font=('timesnewroman', 30, 'bold'))
    button_game = tk.Button(window_menu, command=lambda: game(window_old), text='Graj', height='0', width='20', font=('timesnewroman', 18, 'bold'))
    button_exit = tk.Button(window_menu, command=lambda: sys.exit(0), text='Zamknij aplikacje', height='0', width='20', font=('timesnewroman', 18, 'bold'))
    
    #Placing elements
    text_menu.pack()
    text_menu.place(x=WIDTH/2, y=80, anchor='center')
    button_game.pack()
    button_game.place(x=WIDTH/2, y=HIGH-500, anchor='center')
    button_exit.pack()
    button_exit.place(x=WIDTH/2, y=HIGH-400, anchor='center')

    window_menu.pack()

if __name__ == '__main__':
    #Creating window
    window = tk.Tk()
    window.title('Blackjack')
    window.minsize(height=str(HIGH), width=str(WIDTH))
    window.maxsize(height=str(HIGH), width=str(WIDTH))
    
    menu()

    window.mainloop()
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sys
from BlackjackGame import BlackjackGame

HIGH = 800
WIDTH = 1200


def return_window(window_now, window_new):
    window_now.pack_forget()
    window_new.pack()

def start_game(window_old):

    game = BlackjackGame()

    window_old.pack_forget()
    window_game = tk.Frame(window, height=str(HIGH), width=str(WIDTH))

    
    img_table = tk.PhotoImage(file="GUI/table.png")
    label_table = tk.Label(image=img_table)
    label_table.pack()
    label_table.img = img_table
    label_table.place(x=0, y=0, anchor='nw')
    window_game.pack()
    game.play()

def menu():

    window_menu = tk.Frame(window, height=str(HIGH), width=str(WIDTH))
    window_old = window_menu
    
    #Creating elements
    text_menu = tk.Label(window_menu, text='Menu gry', height='30', width='100', font=('timesnewroman', 30, 'bold'))
    button_game = tk.Button(window_menu, command=lambda: start_game(window_old), text='Graj', height='0', width='20', font=('timesnewroman', 18, 'bold'))
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
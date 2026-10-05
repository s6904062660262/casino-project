from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import random

#== Functions =================================================
def load_balance():
    try:
        with open("balance.txt", "r", encoding="utf-8") as f:
            return int(f.read())
    except:
        return 1000

def save_balance():
    with open("balance.txt", "w", encoding="utf-8") as f:
        f.write(str(balance))

def update_balance():
    try:
        global blackjack_bet
        blackjack_bet = blackjack_bet
    except:
        blackjack_bet = None
    user_balance_label.config(text=f"Balance: {balance}$")
    slot_balance_label.config(text=f"Balance: {balance}$")
    blackjack_balance_label.config(text=f"Balance: {balance}$ | Bet: {blackjack_bet}$")

def load_history(history_name):
    try:
        with open(history_name+"-history.txt", "r", encoding="utf-8") as f:
            return f.readlines()
    except:
        return []

def save_history(history_name, new_history):
    with open(history_name+"-history.txt", "w", encoding="utf-8") as f:
        f.writelines(new_history)

def get_formatted_history(history_list):
    win_money = 0
    win_count = 0
    lose_money = 0
    lose_count = 0
    for h in history_list:
        try:
            outcome, money = h.strip().split("! ")
            if outcome == "WIN":
                win_money += int(money)
                win_count += 1
            elif outcome == "LOSE":
                lose_money += int(money)
                lose_count += 1
        except:
            continue
    return [win_money, win_count, lose_money, lose_count]

def update_history():
    # slot history
    slot_played.config(text=f"Played : {len(slot_new_history)}")
    slot_formatted_history = get_formatted_history(slot_new_history)
    slot_pl.config(text=f"P&L : {slot_formatted_history[0] + slot_formatted_history[2]}")
    slot_wins.config(text=f"Wins : {slot_formatted_history[1]}")
    slot_loses.config(text=f"Loses : {slot_formatted_history[3]}")
    slot_history_scroll.config(state="normal")
    slot_history_scroll.delete("1.0", "end")
    for h in slot_new_history:
        slot_history_scroll.insert("end", h)
    slot_history_scroll.config(state="disabled")
    # blackjack history
    blackjack_played.config(text=f"Played : {len(blackjack_new_history)}")
    blackjack_formatted_history = get_formatted_history(blackjack_new_history)
    blackjack_pl.config(text=f"P&L : {blackjack_formatted_history[0] + blackjack_formatted_history[2]}")
    blackjack_wins.config(text=f"Wins : {blackjack_formatted_history[1]}")
    blackjack_loses.config(text=f"Loses : {blackjack_formatted_history[3]}")
    blackjack_history_scroll.config(state="normal")
    blackjack_history_scroll.delete("1.0", "end")
    for h in blackjack_new_history:
        blackjack_history_scroll.insert("end", h)
    blackjack_history_scroll.config(state="disabled")

balance = load_balance()
slot_new_history = load_history("slot")
blackjack_new_history = load_history("blackjack")

def on_closing():
    save_balance()
    save_history("slot", slot_new_history)
    save_history("blackjack", blackjack_new_history)
    window.destroy()

def ask_mom():
    global balance
    if balance > 0:
        user_result_label.config(text="0 money required.")
        return
    balance = 1000
    user_result_label.config(text="Your mom gave you +1000")
    update_balance()

#== GUI ========================================================
window = Tk()
window.title("Casino Game")
window.geometry("500x450")
window.minsize(500, 450)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

window.protocol("WM_DELETE_WINDOW", on_closing)

tab_control = ttk.Notebook(window)
tab_control.columnconfigure(0, weight=1)
tab_control.rowconfigure(0, weight=1)
tab_control.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

#-- Slot ---------------------------------------------------------
def spin_slot():
    global balance
    
    try:
        bet = int(slot_bet_entry.get())
    except ValueError:
        slot_result_label.config(text="Invalid bet! Bet must be integer.")
        return

    if bet <= 0:
        slot_result_label.config(text="Bet must greater than 0!")
        return
    
    if balance <= 0:
        slot_result_label.config(text="You ran out of money! Ask mom for it.")
        return

    if bet > balance:
        slot_result_label.config(text="Can not bet more than Balance!")
        return

    values = ('🍉', '🍇', '🍈')
    n1 = random.choice(values)
    n2 = random.choice(values)
    n3 = random.choice(values)

    slot_label.config(text=f"[ {n1} ]  [ {n2} ]  [ {n3} ]")

    mutiplier = {
        '🍉': 4,
        '🍇': 8,
        '🍈': 2
    }
    
    if n1 == n2 == n3:
        win = bet * mutiplier[n1]
        balance += win
        result = f"WIN! +{win}"
    else:
        balance -= bet
        result = f"LOSE! -{bet}"

    slot_result_label.config(text=result)
    slot_new_history.append(result+'\n')

    update_balance()
    update_history()

slot_tab = Frame(tab_control)
slot_tab.columnconfigure((0,1), weight=1)
slot_tab.rowconfigure((0,1,2,3,4,5), weight=1)

tab_control.add(slot_tab, text='Slot')

slot_balance_label = Label(slot_tab, text=f"Balance: {balance}", font=("Arial", 18, "bold"))
slot_balance_label.grid(row=0, column=0, columnspan=2, pady=15)

bet_label = Label(slot_tab, text="Bet Amount:", font=("Arial", 14))
bet_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

slot_bet_entry = Entry(slot_tab, justify="center", width=8, font=("Arial", 14))
slot_bet_entry.insert(0, "50")
slot_bet_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

slot_label = Label(slot_tab, text="[ ? ]  [ ? ]  [ ? ]", font=("Arial", 26, "bold"))
slot_label.grid(row=2, column=0, columnspan=2, pady=20)

spin_btn = Button(slot_tab, text="SPIN", command=spin_slot, width=12, font=("Arial", 14, "bold"))
spin_btn.grid(row=3, column=0, columnspan=2, pady=10)

slot_result_label = Label(slot_tab, text="...", font=("Arial", 14))
slot_result_label.grid(row=4, column=0, columnspan=2, pady=15)

#-- Black Jack ---------------------------------------------------
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["♥", "♦", "♣", "♠"]

deck, player, dealer = [], [], []

def card_value(hand):
    total, aces = 0, 0
    for r, s in hand:
        if r in ["J", "Q", "K"]:
            total += 10
        elif r == "A":
            total += 11
            aces += 1
        else:
            total += int(r)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def card_text(hand):
    return "  ".join([f"[{r}{s}]" for r, s in hand])

def updateCard(show_dealer=True):
    player_label.config(text=f"Player: {card_text(player)}\npoint: {card_value(player)}")
    if show_dealer:
        dealer_label.config(text=f"Dealer: {card_text(dealer)}\npoint: {card_value(dealer)}")
    else:
        dealer_label.config(text=f"Dealer: [ ? ]  {card_text(dealer[1:])}")

def new_game():
    global deck, player, dealer, balance, blackjack_bet
    try:
        b = int(blackjack_bet_entry.get())
    except:
        blackjack_result_label.config(text="Invalid bet!")
        return

    if b <= 0:
        blackjack_result_label.config(text="Bet must greater than 0!")
        return
    
    if b > balance:
        blackjack_result_label.config(text="Can not bet more than Balance!")
        return

    if balance <= 0:
        slot_result_label.config(text="You ran out of money! Ask mom for it.")
        return

    if len(deck) > 0:
        blackjack_result_label.config(text="The game is running!")
        return
    
    blackjack_bet = b
    balance -= blackjack_bet
    update_balance()
    deck = [(r, s) for s in suits for r in ranks]
    random.shuffle(deck)
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    blackjack_result_label.config(text="")
    btn_hit.config(state="normal")
    btn_stay.config(state="normal")
    updateCard(show_dealer=False)

def end_round(text, win_amount):
    global balance, deck, blackjack_bet
    balance += win_amount
    blackjack_result_label.config(text=text)
    blackjack_new_history.append(text+'\n')
    update_balance()
    update_history()
    btn_hit.config(state="disabled")
    btn_stay.config(state="disabled")
    deck.clear()
    blackjack_bet = None
    updateCard(show_dealer=True)

def hit():
    player.append(deck.pop())
    updateCard(show_dealer=False)
    if card_value(player) > 21:
        end_round(f"EXCEED! -{blackjack_bet}", 0)

def stay():
    while card_value(dealer) < 17:
        dealer.append(deck.pop())
    p, d = card_value(player), card_value(dealer)
    if d > 21 or p > d:
        end_round(f"WIN! +{blackjack_bet*2}", blackjack_bet*2)
    elif p < d:
        end_round(f"LOSE! -{blackjack_bet}", 0)
    else:
        end_round("TIED! +0", blackjack_bet)

blackjack_tab = Frame(tab_control)
blackjack_tab.columnconfigure(0, weight=1)
blackjack_tab.rowconfigure((1,2), weight=1)

tab_control.add(blackjack_tab, text='BlackJack')

blackjack_balance_label = Label(blackjack_tab, text="", font=("Arial", 18, "bold"))
blackjack_balance_label.grid(row=0, column=0, pady=10, sticky="nsew")

dealer_label = Label(blackjack_tab, text="", font=("Arial", 22), bg="#e8f5e9", relief="ridge")
dealer_label.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

player_label = Label(blackjack_tab, text="", font=("Arial", 22), bg="#e3f2fd", relief="ridge")
player_label.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

blackjack_result_label = Label(blackjack_tab, text="...", font=("Arial", 18, "bold"))
blackjack_result_label.grid(row=3, column=0, pady=5, sticky="nsew")

control = Frame(blackjack_tab)
control.grid(row=4, column=0, pady=10, sticky="nsew")
control.grid_columnconfigure((0,1,2,3), weight=1)

Label(control, text="Bet: $", font=("Arial", 16)).grid(row=0, column=0, sticky="e")
blackjack_bet_entry = Entry(control, font=("Arial", 16), justify="center")
blackjack_bet_entry.insert(0, "100")
blackjack_bet_entry.grid(row=0, column=1, sticky="ew", padx=5)

btn_hit = Button(control, text="Hit", font=("Arial", 16), command=hit)
btn_hit.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_stay = Button(control, text="Stay", font=("Arial", 16), command=stay)
btn_stay.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
btn_new = Button(control, text="New Game", font=("Arial", 16), command=new_game)
btn_new.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

#-- User ---------------------------------------------------
user_tab = Frame(tab_control)

tab_control.add(user_tab, text="User Info")
user_balance_label = Label(user_tab, text=f"Balance: {balance}", font=("Arial", 18, "bold"))
user_balance_label.pack()

Label(user_tab, text="Statistics:", font=("Arial", 13, "bold")).pack(anchor="w", padx=20)

ask_mom_btn = Button(user_tab, text="Ask mom +1000", command=ask_mom)
ask_mom_btn.pack(anchor="sw", side="bottom")

user_result_label = Label(user_tab, text="...", font=("Arial", 14))
user_result_label.pack(side="bottom", pady=10)

history_tab_control = ttk.Notebook(user_tab)
history_tab_control.pack(fill="both", expand=True, anchor="center", padx=20)

history_bg_color = "#E9E9E9"

# Slot History -----------
slot_history_tab = Frame(history_tab_control)
slot_history_tab.pack_configure(anchor="w")

history_tab_control.add(slot_history_tab, text="Slot")

slot_statistics_frame = Frame(slot_history_tab, bg=history_bg_color)
slot_statistics_frame.columnconfigure((1, 2), weight=1)
slot_statistics_frame.rowconfigure((1, 2, 3), weight=1)
slot_statistics_frame.pack(fill="both", expand=True)

Label(slot_statistics_frame, font=("Arial", 1)).grid(row=1)

slot_played = Label(slot_statistics_frame, text="Played : ", bg=history_bg_color)
slot_played.grid(row=2, column=1, sticky="w", padx=20)

slot_pl = Label(slot_statistics_frame, text="P&L : ", bg=history_bg_color)
slot_pl.grid(row=3, column=1, sticky="w", padx=20)

slot_wins = Label(slot_statistics_frame, text="Wins : ", bg=history_bg_color)
slot_wins.grid(row=2, column=2, sticky="w")

slot_loses = Label(slot_statistics_frame, text="Loses : ", bg=history_bg_color)
slot_loses.grid(row=3, column=2, sticky="w")

Label(slot_statistics_frame, font=("Arial", 1)).grid(row=4)

Label(
    slot_statistics_frame,
    text="History:",
    bg=history_bg_color,
    font=("Arial", 9, "bold")
).grid(row=5, column=1, sticky="sw")

slot_history_scroll = ScrolledText(slot_history_tab, bg=history_bg_color, wrap = WORD, state="disabled")
slot_history_scroll.pack(fill="both", expand=True)

# BlackJack History ------
blackjack_history_tab = Frame(history_tab_control)
blackjack_history_tab.pack_configure(anchor="w")

history_tab_control.add(blackjack_history_tab, text="BlackJack")

blackjack_statistics_frame = Frame(blackjack_history_tab, bg=history_bg_color)
blackjack_statistics_frame.columnconfigure((1, 2), weight=1)
blackjack_statistics_frame.rowconfigure((1, 2, 3), weight=1)
blackjack_statistics_frame.pack(fill="both", expand=True)

Label(blackjack_statistics_frame, font=("Arial", 1)).grid(row=1)

blackjack_played = Label(blackjack_statistics_frame, text="Played : ", bg=history_bg_color)
blackjack_played.grid(row=2, column=1, sticky="w", padx=20)

blackjack_pl = Label(blackjack_statistics_frame, text="P&L : ", bg=history_bg_color)
blackjack_pl.grid(row=3, column=1, sticky="w", padx=20)

blackjack_wins = Label(blackjack_statistics_frame, text="Wins : ", bg=history_bg_color)
blackjack_wins.grid(row=2, column=2, sticky="w")

blackjack_loses = Label(blackjack_statistics_frame, text="Loses : ", bg=history_bg_color)
blackjack_loses.grid(row=3, column=2, sticky="w")

Label(blackjack_statistics_frame, font=("Arial", 1)).grid(row=4)

Label(
    blackjack_statistics_frame,
    text="History:",
    bg=history_bg_color,
    font=("Arial", 9, "bold")
).grid(row=5, column=1, sticky="sw")

blackjack_history_scroll = ScrolledText(blackjack_history_tab, bg=history_bg_color, wrap = WORD, state="disabled")
blackjack_history_scroll.pack(fill="both", expand=True)

update_balance()
update_history()
window.mainloop()

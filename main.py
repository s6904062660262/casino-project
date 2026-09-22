from tkinter import *
from tkinter import ttk
import random

file_path = "data.csv"

#== Functions =================================================
def loadBalance():
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return int(f.read())
    except:
        return 1000

def saveBalance():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(balance))

def updateBalance():
    balanceLabel.config(text=f"Balance: {balance}")
    balance_label.config(text=f"เงิน: ${balance} | เดิมพัน: ${bet_entry.get()}")

def onClosing():
    saveBalance()
    window.destroy()

balance = loadBalance()

def spinSlot():
    global balance
    
    try:
        bet = int(betEntry.get())
    except ValueError:
        resultLabel.config(text="Invalid bet! Bet must be integer.")
        return

    if bet <= 0:
        resultLabel.config(text="Bet must greater than 0!")
        return
    
    if balance <= 0:
        resultLabel.config(text="You ran out of money! Ask mom for it.")
        return

    if bet > balance:
        resultLabel.config(text="Can not bet more than Balance!")
        return

    values = ('🍉', '🍇', '🍈')
    n1 = random.choice(values)
    n2 = random.choice(values)
    n3 = random.choice(values)

    slotLabel.config(text=f"[ {n1} ]  [ {n2} ]  [ {n3} ]")

    mutiplier = {
        '🍉': 4,
        '🍇': 8,
        '🍈': 2
    }
    
    if n1 == n2 == n3:
        win = bet * mutiplier[n1]
        balance += win
        resultLabel.config(text=f"WIN! +{win}")
    else:
        balance -= bet
        resultLabel.config(text=f"LOSE! -{bet}")

    updateBalance()
    saveBalance()

def askMom():
    global balance
    if balance > 0:
        resultLabel.config(text="0 money required.")
        return
    balance = 1000
    resultLabel.config(text="Your mom gave you +1000")
    updateBalance()
    saveBalance()

#== GUI ========================================================
window = Tk()
window.title("Casino Game")
window.geometry("500x450")
window.minsize(500, 450)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

window.protocol("WM_DELETE_WINDOW", onClosing)

tabControl = ttk.Notebook(window)
tabControl.columnconfigure(0, weight=1)
tabControl.rowconfigure(0, weight=1)
tabControl.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

#-- Slot ---------------------------------------------------------
tab1 = ttk.Frame(tabControl)
tab1.columnconfigure((0,1), weight=1)
tab1.rowconfigure((0,1,2,3,4,5), weight=1)

tabControl.add(tab1, text='Slot')

balanceLabel = Label(tab1, text=f"Balance: {balance}", font=("Arial", 18, "bold"))
balanceLabel.grid(row=0, column=0, columnspan=2, pady=15)

betLabel = Label(tab1, text="Bet Amount:", font=("Arial", 14))
betLabel.grid(row=1, column=0, padx=5, pady=5, sticky="e")

betEntry = Entry(tab1, justify="center", width=8, font=("Arial", 14))
betEntry.insert(0, "50")
betEntry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

slotLabel = Label(tab1, text="[ ? ]  [ ? ]  [ ? ]", font=("Arial", 26, "bold"))
slotLabel.grid(row=2, column=0, columnspan=2, pady=20)

spinButton = Button(tab1, text="SPIN", command=spinSlot, width=12, font=("Arial", 14, "bold"))
spinButton.grid(row=3, column=0, columnspan=2, pady=10)

resultLabel = Label(tab1, text="...", font=("Arial", 14))
resultLabel.grid(row=4, column=0, columnspan=2, pady=15)

askMomButton = Button(tab1, text="Ask mom +1000", command=askMom)
askMomButton.grid(row=5, column=0, padx=15, pady=15, sticky="sw")

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
    balance_label.config(text=f"เงิน: ${balance} | เดิมพัน: ${bet_entry.get()}")

def update(show_dealer=True):
    player_label.config(text=f"Player: {card_text(player)}\nแต้ม: {card_value(player)}")
    if show_dealer:
        dealer_label.config(text=f"Dealer: {card_text(dealer)}\nแต้ม: {card_value(dealer)}")
    else:
        dealer_label.config(text=f"Dealer: [ ? ]  {card_text(dealer[1:])}")

def new_game():
    global deck, player, dealer, balance, bet
    try:
        b = int(bet_entry.get())
    except:
        result_label.config(text="ใส่ bet เป็นตัวเลขก่อน!")
        return
    if b <= 0 or b > balance:
        result_label.config(text="bet ไม่ถูกต้อง!")
        return
    bet = b
    balance -= bet
    updateBalance()
    deck = [(r, s) for s in suits for r in ranks]
    random.shuffle(deck)
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    result_label.config(text="")
    btn_hit.config(state="normal")
    btn_stay.config(state="normal")
    update(show_dealer=False)

def end_round(text, win_amount):
    global balance
    balance += win_amount
    result_label.config(text=text)
    updateBalance()
    btn_hit.config(state="disabled")
    btn_stay.config(state="disabled")
    update(show_dealer=True)

def hit():
    player.append(deck.pop())
    update(show_dealer=False)
    if card_value(player) > 21:
        end_round("แตก! เสียเดิมพัน", 0)

def stay():
    while card_value(dealer) < 17:
        dealer.append(deck.pop())
    p, d = card_value(player), card_value(dealer)
    if d > 21 or p > d:
        end_round(f"ชนะ! +${bet*2}", bet*2)
    elif p < d:
        end_round("แพ้! เสียเดิมพัน", 0)
    else:
        end_round("เสมอ! คืนเงิน", bet)

tab2 = ttk.Frame(tabControl)
tab2.columnconfigure(0, weight=1)
tab2.rowconfigure((1,2), weight=1)

tabControl.add(tab2, text='BlackJack')

balance_label = Label(tab2, text="", font=("Arial", 18, "bold"))
balance_label.grid(row=0, column=0, pady=10, sticky="nsew")

dealer_label = Label(tab2, text="", font=("Arial", 22), bg="#e8f5e9", relief="ridge")
dealer_label.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

player_label = Label(tab2, text="", font=("Arial", 22), bg="#e3f2fd", relief="ridge")
player_label.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

result_label = Label(tab2, text="", font=("Arial", 20, "bold"))
result_label.grid(row=3, column=0, pady=5, sticky="nsew")

control = Frame(tab2)
control.grid(row=4, column=0, pady=10, sticky="nsew")
control.grid_columnconfigure((0,1,2,3), weight=1)

Label(control, text="Bet: $", font=("Arial", 16)).grid(row=0, column=0, sticky="e")
bet_entry = Entry(control, font=("Arial", 16), justify="center")
bet_entry.insert(0, "100")
bet_entry.grid(row=0, column=1, sticky="ew", padx=5)

btn_hit = Button(control, text="Hit", font=("Arial", 16), command=hit)
btn_hit.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_stay = Button(control, text="Stay", font=("Arial", 16), command=stay)
btn_stay.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
btn_new = Button(control, text="New Game", font=("Arial", 16), command=new_game)
btn_new.grid(row=1, column=2, sticky="ew", padx=5, pady=5)

updateBalance()

window.mainloop()

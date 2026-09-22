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

    balanceLabel.config(text=f"Balance: {balance}")
    saveBalance()

def askMom():
    global balance
    if balance > 0:
        resultLabel.config(text="0 money required.")
        return
    balance = 1000
    balanceLabel.config(text=f"Balance: {balance}")
    resultLabel.config(text="Your mom gave you +1000")
    saveBalance()

#== GUI ========================================================
window = Tk()
window.title("Casino Game")
window.geometry("400x370")
window.minsize(400, 370)
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
tab2 = ttk.Frame(tabControl)
tab2.columnconfigure(0, weight=1)
tab2.rowconfigure(0, weight=1)

tabControl.add(tab2, text='BlackJack')

window.mainloop()

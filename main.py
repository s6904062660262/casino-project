import tkinter as tk
from tkinter import messagebox
import random
import os

# ชื่อไฟล์สำหรับบันทึกข้อมูล
SAVE_FILE = "casino_save.txt"

# ---------------- ฟังก์ชันอ่าน/บันทึกไฟล์ ----------------
def load_balance():
    """ โหลดเงินจากไฟล์ หากไม่มีไฟล์ให้เริ่มที่ 1000 """
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 1000
    return 1000

def save_balance():
    """ บันทึกเงินลงไฟล์ """
    with open(SAVE_FILE, "w") as f:
        f.write(str(balance))

def on_closing():
    """ เซฟข้อมูลอัตโนมัติเมื่อกดปิดหน้าต่างโปรแกรม (ปุ่ม X) """
    save_balance()
    root.destroy()

# ---------------- เริ่มต้นค่าเงิน ----------------
balance = load_balance()

# ---------------- ฟังก์ชันหมุนสล็อต ----------------
def play_slot():
    global balance
    
    # 1. ตรวจสอบเงินเดิมพัน
    try:
        bet = int(bet_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number")
        return

    if bet <= 0 or bet > balance:
        messagebox.showwarning("Warning", "Invalid bet amount")
        return

    # 2. สุ่มผลลัพธ์ (เลข 1-3)

    value = ('🍉','🍇','🍈')
    n1 = value[random.randint(0, 2)]
    n2 = value[random.randint(0, 2)]
    n3 = value[random.randint(0, 2)]

    slot_label.config(text=f"[ {n1} ]  [ {n2} ]  [ {n3} ]")

    # 3. คิดเงิน
    mutipile = {
        '🍉':4,
        '🍇':8,
        '🍈':2

    }
    if n1 == n2 == n3:
        win = bet * mutipile[n1]
        balance += win
        result_label.config(text=f"WIN! +{win}")
    else:
        balance -= bet
        result_label.config(text=f"LOSE! -{bet}")

    # 4. อัปเดตเงินบนหน้าจอ + บันทึกข้อมูล
    balance_label.config(text=f"Balance: {balance}")
    save_balance()

    # ตรวจสอบเงินหมด
    if balance <= 0:
        messagebox.showerror("Game Over", "You ran out of money!")
        balance = 1000  # รีเซ็ตเงินกลับเป็น 1000 ถ้าแพ้จนหมด
        save_balance()
        root.destroy()

# ---------------- สร้างหน้าต่าง GUI ----------------
root = tk.Tk()
root.title("Casino Game")
root.geometry("300x340")

# ดักจับ event เมื่อผู้ใช้กดปิดหน้าต่าง (ปุ่ม X)
root.protocol("WM_DELETE_WINDOW", on_closing)

balance_label = tk.Label(root, text=f"Balance: {balance}", font=("Arial", 14))
balance_label.pack(pady=10)

tk.Label(root, text="Bet Amount:").pack()
bet_entry = tk.Entry(root, justify="center")
bet_entry.insert(0, "50")
bet_entry.pack(pady=5)

slot_label = tk.Label(root, text="[ ? ]  [ ? ]  [ ? ]", font=("Arial", 20, "bold"))
slot_label.pack(pady=20)

play_button = tk.Button(root, text="SPIN", font=("Arial", 12), command=play_slot)
play_button.pack(pady=10)

result_label = tk.Label(root, text="Good Luck!", font=("Arial", 11))
result_label.pack(pady=10)

root.mainloop()

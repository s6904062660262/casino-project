import tkinter as tk
from tkinter import messagebox
import random

# ชื่อไฟล์สำหรับบันทึกข้อมูล
SAVE_FILE = "casino_save.txt"

# ---------------- ฟังก์ชันอ่าน/บันทึกไฟล์ (ไม่ใช้ os) ----------------
def load_balance():
    """ โหลดเงินจากไฟล์ หากไม่มีไฟล์ให้เริ่มที่ 1000 """
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 1000
    except:
        return 1000

def save_balance():
    """ บันทึกเงินลงไฟล์ """
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
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

    # 2. สุ่มผลลัพธ์ Emoji
    value = ('🍉', '🍇', '🍈')
    n1 = random.choice(value)
    n2 = random.choice(value)
    n3 = random.choice(value)

    slot_label.config(text=f"[ {n1} ]  [ {n2} ]  [ {n3} ]")

    # 3. คิดเงินตามตัวคูณ
    mutipile = {
        '🍉': 4,
        '🍇': 8,
        '🍈': 2
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

# ---------------- สร้างหน้าต่าง GUI (Grid Only) ----------------
root = tk.Tk()
root.title("Casino Game")
root.geometry("400x380") # ปรับขยายขนาดหน้าต่างรองรับข้อความใหญ่

# กำหนดขนาดคอลัมน์ให้ขยายกลางหน้าจอ
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

# ดักจับ event เมื่อผู้ใช้กดปิดหน้าต่าง (ปุ่ม X)
root.protocol("WM_DELETE_WINDOW", on_closing)

# จัดวาง Widget ด้วย grid() พร้อมปรับขนาดตัวอักษร (font)
balance_label = tk.Label(root, text=f"Balance: {balance}", font=("Arial", 18, "bold"))
balance_label.grid(row=0, column=0, columnspan=2, pady=15)

bet_title_label = tk.Label(root, text="Bet Amount:", font=("Arial", 14))
bet_title_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

bet_entry = tk.Entry(root, justify="center", width=8, font=("Arial", 14))
bet_entry.insert(0, "50")
bet_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

slot_label = tk.Label(root, text="[ ? ]  [ ? ]  [ ? ]", font=("Arial", 26, "bold"))
slot_label.grid(row=2, column=0, columnspan=2, pady=20)

play_button = tk.Button(root, text="SPIN", command=play_slot, width=12, font=("Arial", 14, "bold"))
play_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(root, text="Good Luck!", font=("Arial", 14))
result_label.grid(row=4, column=0, columnspan=2, pady=15)

root.mainloop()
import tkinter as tk
from tkinter import messagebox

def umrechnen():

    euro = float(entry_euro.get())
    kurs = 1.08 
    dollar = euro * kurs
    label_result.config(text=f"{dollar:.2f} USD", fg="green")

root = tk.Tk()
root.title("Währungsrechner")
root.geometry("300x200")

tk.Label(root, text="Betrag in Euro (€):", font=("Arial", 10)).pack(pady=10)
entry_euro = tk.Entry(root)
entry_euro.pack(pady=5)

btn_calc = tk.Button(root, text="Umrechnen", command=umrechnen, bg="blue", fg="white")
btn_calc.pack(pady=10)

label_result = tk.Label(root, text="0.00 USD", font=("Arial", 12, "bold"))
label_result.pack(pady=10)

root.mainloop()
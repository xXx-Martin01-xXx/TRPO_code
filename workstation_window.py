import tkinter as tk
from tkinter import font, messagebox
from tkinter import ttk

class WorkstationWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        master.title("Рабочие места")
        font1 = font.Font(family="Arial", size=12)

        frame = tk.Frame(master)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Таблица рабочих мест: Номер (ID) | Адрес | Кабинет
        columns = ("Number", "Address", "Cabinet")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.heading("Number", text="Номер")
        self.tree.heading("Address", text="Адрес")
        self.tree.heading("Cabinet", text="Кабинет")
        self.tree.column("Number", width=80)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Форма ввода без поля номера (id автогенерация)
        entry_frame = tk.Frame(master)
        entry_frame.pack(padx=10, pady=5)

        tk.Label(entry_frame, text="Адрес:").grid(row=0, column=0)
        self.entry_address = tk.Entry(entry_frame, font=font1)
        self.entry_address.grid(row=0, column=1)

        tk.Label(entry_frame, text="Кабинет:").grid(row=1, column=0)
        self.entry_cabinet = tk.Entry(entry_frame, font=font1)
        self.entry_cabinet.grid(row=1, column=1)

        tk.Button(entry_frame, text="Добавить рабочее место", command=self.add_workstation, font=font1, bg="lightgreen").grid(row=2, columnspan=2, pady=5)
        tk.Button(master, text="Удалить выбранное рабочее место", command=self.delete_workstation, font=font1, bg="lightcoral").pack(pady=5)

        self.populate()

    def populate(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for ws in self.db.get_workstations():
            self.tree.insert("", tk.END, iid=ws["id"], values=(ws["id"], ws["address"], ws["cabinet"]))

    def add_workstation(self):
        addr = self.entry_address.get().strip()
        cab = self.entry_cabinet.get().strip()
        if not (addr and cab):
            messagebox.showwarning("Ошибка", "Заполните все поля.")
            return
        self.db.add_workstation(addr, cab)
        self.entry_address.delete(0, tk.END)
        self.entry_cabinet.delete(0, tk.END)
        self.populate()

    def delete_workstation(self):
        sel = self.tree.selection()
        if not sel:
            return
        self.db.delete_workstation(sel[0])
        self.populate()
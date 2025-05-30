import tkinter as tk
from tkinter import font, messagebox
from tkinter import ttk

class ComponentWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        master.title("Комплектующие")
        font1 = font.Font(family="Arial", size=12)

        frame = tk.Frame(master)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        columns = ("Number", "Name", "Quantity")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.heading("Number", text="Номер")
        self.tree.heading("Name", text="Наименование")
        self.tree.heading("Quantity", text="Количество")
        self.tree.column("Number", width=80)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        entry_frame = tk.Frame(master)
        entry_frame.pack(padx=10, pady=5)

        tk.Label(entry_frame, text="Наименование:").grid(row=0, column=0)
        self.entry_name = tk.Entry(entry_frame, font=font1)
        self.entry_name.grid(row=0, column=1)

        tk.Label(entry_frame, text="Количество:").grid(row=1, column=0)
        self.entry_qty = tk.Entry(entry_frame, font=font1)
        self.entry_qty.grid(row=1, column=1)

        tk.Button(entry_frame, text="Добавить", command=self.add_component, font=font1, bg="lightyellow").grid(row=2, columnspan=2, pady=5)
        tk.Button(master, text="Удалить выбранное", command=self.delete_component, font=font1, bg="lightcoral").pack(pady=5)

        self.populate()

    def populate(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for comp in self.db.get_components():
            self.tree.insert("", tk.END, iid=comp["id"], values=(comp["id"], comp["name"], comp["quantity"]))

    def add_component(self):
        name = self.entry_name.get().strip()
        qty = self.entry_qty.get().strip()
        if not name or not qty.isdigit():
            messagebox.showwarning("Ошибка", "Введите наименование и целое число для количества.")
            return
        self.db.add_component(name, int(qty))
        self.entry_name.delete(0, tk.END)
        self.entry_qty.delete(0, tk.END)
        self.populate()

    def delete_component(self):
        sel = self.tree.selection()
        if not sel:
            return
        self.db.delete_component(sel[0])
        self.populate()
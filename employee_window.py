import tkinter as tk
from tkinter import font, messagebox
from tkinter import ttk

class EmployeeWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        master.title("Сотрудники")
        font1 = font.Font(family="Arial", size=12)

        frame = tk.Frame(master)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Таблица сотрудников: Номер | Фамилия | Имя | Отчество
        columns = ("Номер","Фамилия","Имя","Отчество")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Поля ввода
        entry_frame = tk.Frame(master)
        entry_frame.pack(padx=10, pady=5)
        tk.Label(entry_frame, text="Фамилия:").grid(row=0, column=0)
        self.entry_surname = tk.Entry(entry_frame, font=font1)
        self.entry_surname.grid(row=0, column=1)
        tk.Label(entry_frame, text="Имя:").grid(row=1, column=0)
        self.entry_name = tk.Entry(entry_frame, font=font1)
        self.entry_name.grid(row=1, column=1)
        tk.Label(entry_frame, text="Отчество:").grid(row=2, column=0)
        self.entry_patronymic = tk.Entry(entry_frame, font=font1)
        self.entry_patronymic.grid(row=2, column=1)
        tk.Button(entry_frame, text="Добавить сотрудника", command=self.add_employee, font=font1, bg="lightblue").grid(row=3, columnspan=2, pady=5)

        tk.Button(master, text="Удалить выбранного сотрудника", command=self.delete_employee, font=font1, bg="lightcoral").pack(pady=5)

        self.populate()

    def populate(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for emp in self.db.get_employees():
            self.tree.insert("", tk.END, iid=emp["id"], values=(emp["id"], emp["surname"], emp["name"], emp["patronymic"]))

    def add_employee(self):
        surname = self.entry_surname.get().strip()
        name = self.entry_name.get().strip()
        patronymic = self.entry_patronymic.get().strip()
        if not (surname and name and patronymic):
            messagebox.showwarning("Ошибка", "Заполните все поля фамилии, имени и отчества.")
            return
        self.db.add_employee(surname, name, patronymic)
        self.entry_surname.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_patronymic.delete(0, tk.END)
        self.populate()

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            return
        emp_id = selected[0]
        self.db.delete_employee(emp_id)
        self.populate()
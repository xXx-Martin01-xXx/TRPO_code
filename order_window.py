import tkinter as tk
from tkinter import font, messagebox
from tkinter import ttk

class OrderWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        master.title("Заказы")
        font1 = font.Font(family="Arial", size=12)

        # Вспомогательная функция для сокращения ФИО
        def format_fio(surname, name, patronymic):
            return f"{surname} {name[0]}. {patronymic[0]}."

        # Фрейм для таблицы заказов
        frame = tk.Frame(master)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Настройка столбцов: Номер | Рабочее место | Компонент | Ответственный | Дата
        columns = ("Number", "Workstation", "Component", "Responsible", "Date")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        self.tree.heading("Number", text="Номер")
        self.tree.heading("Workstation", text="Рабочее место")
        self.tree.heading("Component", text="Компонент")
        self.tree.heading("Responsible", text="Ответственный")
        self.tree.heading("Date", text="Дата")
        self.tree.column("Number", width=80)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Фрейм для формы создания заказа
        form = tk.Frame(master)
        form.pack(padx=10, pady=5)

        # Получаем данные из БД для выпадающих списков
        workstations = self.db.get_workstations()
        components = self.db.get_components()
        employees = self.db.get_employees()

        # Рабочее место
        tk.Label(form, text="Рабочее место:").grid(row=0, column=0)
        self.ws_var = tk.StringVar()
        self.ws_cb = ttk.Combobox(form, textvariable=self.ws_var, font=font1, state="readonly")
        ws_list = [f"{w['address']}, кабинет {w['cabinet']}" for w in workstations]
        self.ws_map = {disp: w['id'] for w, disp in zip(workstations, ws_list)}
        self.ws_cb['values'] = ws_list
        self.ws_cb.grid(row=0, column=1)

        # Компонент
        tk.Label(form, text="Компонент:").grid(row=1, column=0)
        self.comp_var = tk.StringVar()
        self.comp_cb = ttk.Combobox(form, textvariable=self.comp_var, font=font1, state="readonly")
        comp_list = [f"{c['name']}, кол-во {c['quantity']}" for c in components]
        self.comp_map = {disp: c['id'] for c, disp in zip(components, comp_list)}
        self.comp_cb['values'] = comp_list
        self.comp_cb.grid(row=1, column=1)

        # Ответственный
        tk.Label(form, text="Ответственный:").grid(row=2, column=0)
        self.emp_var = tk.StringVar()
        self.emp_cb = ttk.Combobox(form, textvariable=self.emp_var, font=font1, state="readonly")
        emp_list = [format_fio(e['surname'], e['name'], e['patronymic']) for e in employees]
        self.emp_map = {disp: e['id'] for e, disp in zip(employees, emp_list)}
        self.emp_cb['values'] = emp_list
        self.emp_cb.grid(row=2, column=1)

        # Кнопки
        tk.Button(form, text="Создать заказ", command=self.add_order, font=font1, bg="lightgrey").grid(row=3, columnspan=2, pady=5)
        tk.Button(master, text="Удалить выбранное", command=self.delete_order, font=font1, bg="lightcoral").pack(pady=5)

        # Первичное заполнение таблицы
        self.populate()

    def populate(self):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Заполняем новыми данными
        for o in self.db.get_orders():
            ws = f"{o['address']}, кабинет {o['cabinet']}"
            comp = f"{o['comp_name']}, кол-во {o['comp_quantity']}"
            resp = f"{o['emp_surname']} {o['emp_name'][0]}. {o['emp_patronymic'][0]}."
            self.tree.insert("", tk.END, iid=o['id'], values=(o['id'], ws, comp, resp, o['created_at']))
            
    def add_order(self):
        ws_disp = self.ws_var.get()
        comp_disp = self.comp_var.get()
        emp_disp = self.emp_var.get()
        if not (ws_disp and comp_disp and emp_disp):
            messagebox.showwarning("Ошибка", "Заполните все поля.")
            return
        ws_id = self.ws_map[ws_disp]
        comp_id = self.comp_map[comp_disp]
        emp_id = self.emp_map[emp_disp]
        self.db.add_order(ws_id, comp_id, emp_id)
        self.populate()

    def delete_order(self):
        sel = self.tree.selection()
        if not sel:
            return
        self.db.delete_order(sel[0])
        self.populate()
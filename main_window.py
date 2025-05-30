import tkinter as tk
from tkinter import font, messagebox
from employee_window import EmployeeWindow
from workstation_window import WorkstationWindow
from component_window import ComponentWindow
from order_window import OrderWindow

class MainWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        font1 = font.Font(family="Arial", size=12)

        tk.Button(master, text="Сотрудники", command=self.open_employee, font=font1, bg="lightblue").pack(fill=tk.X)
        tk.Button(master, text="Рабочие места", command=self.open_workstation, font=font1, bg="lightgreen").pack(fill=tk.X)
        tk.Button(master, text="Комплектующие", command=self.open_component, font=font1, bg="lightyellow").pack(fill=tk.X)
        tk.Button(master, text="Заказы", command=self.open_order, font=font1, bg="lightgrey").pack(fill=tk.X)

    def open_employee(self):
        EmployeeWindow(tk.Toplevel(self.master), self.db)

    def open_workstation(self):
        WorkstationWindow(tk.Toplevel(self.master), self.db)

    def open_component(self):
       ComponentWindow(tk.Toplevel(self.master), self.db)

    def open_order(self):
        OrderWindow(tk.Toplevel(self.master), self.db)
import tkinter as tk
from database import Database
from main_window import MainWindow

def main():
    db =  Database("sysadmin.db")
    
    root = tk.Tk()
    root.title("Заказ комплектующих")
    root.geometry('600x400')
    
    MainWindow(root, db)
    root.mainloop()
    
if __name__ == "__main__":
    main()
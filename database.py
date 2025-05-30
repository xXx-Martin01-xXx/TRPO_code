import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.migrate_components()

    def create_tables(self):
        # Таблица сотрудников
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS employees (
                   id INTEGER PRIMARY KEY,
                   surname TEXT NOT NULL,
                   name TEXT NOT NULL,
                   patronymic TEXT NOT NULL
               )''')
        # Таблица рабочих мест
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS workstations (
                   id INTEGER PRIMARY KEY,
                   address TEXT NOT NULL,
                   cabinet TEXT NOT NULL
               )''')
        # Таблица комплектующих
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS components (
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL
               )''')
        # Таблица заказов с ответственным сотрудником
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS orders (
                   id INTEGER PRIMARY KEY,
                   workstation_id INTEGER NOT NULL,
                   component_id INTEGER NOT NULL,
                   employee_id INTEGER NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY(workstation_id) REFERENCES workstations(id),
                   FOREIGN KEY(component_id) REFERENCES components(id),
                   FOREIGN KEY(employee_id) REFERENCES employees(id)
               )''')
        self.conn.commit()

    def migrate_components(self):
        cols = [row['name'] for row in self.cursor.execute("PRAGMA table_info(components)")]
        if 'quantity' not in cols:
            self.cursor.execute("ALTER TABLE components ADD COLUMN quantity INTEGER DEFAULT 0")
            self.conn.commit()

    # CRUD для сотрудников
    def add_employee(self, surname, name, patronymic):
        self.cursor.execute(
            "INSERT INTO employees (surname, name, patronymic) VALUES (?, ?, ?)",
            (surname, name, patronymic)
        )
        self.conn.commit()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees ORDER BY id")
        return self.cursor.fetchall()

    def delete_employee(self, emp_id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        self.conn.commit()
        rows = self.get_employees()
        self.cursor.execute("DELETE FROM employees")
        for idx, row in enumerate(rows, start=1):
            self.cursor.execute(
                "INSERT INTO employees (id, surname, name, patronymic) VALUES (?, ?, ?, ?)",
                (idx, row["surname"], row["name"], row["patronymic"])
            )
        self.conn.commit()

    # CRUD для рабочих мест
    def add_workstation(self, address, cabinet):
        self.cursor.execute(
            "INSERT INTO workstations (address, cabinet) VALUES (?, ?)",
            (address, cabinet)
        )
        self.conn.commit()

    def get_workstations(self):
        self.cursor.execute("SELECT * FROM workstations ORDER BY id")
        return self.cursor.fetchall()

    def delete_workstation(self, ws_id):
        self.cursor.execute("DELETE FROM workstations WHERE id=?", (ws_id,))
        self.conn.commit()
        rows = self.get_workstations()
        self.cursor.execute("DELETE FROM workstations")
        for idx, row in enumerate(rows, start=1):
            self.cursor.execute(
                "INSERT INTO workstations (id, address, cabinet) VALUES (?, ?, ?)",
                (idx, row["address"], row["cabinet"])
            )
        self.conn.commit()

    # CRUD для комплектующих
    def add_component(self, name, quantity):
        self.cursor.execute(
            "INSERT INTO components (name, quantity) VALUES (?, ?)",
            (name, quantity)
        )
        self.conn.commit()
        
    def get_components(self):
        self.cursor.execute("SELECT * FROM components ORDER BY id")
        return self.cursor.fetchall()

    def delete_component(self, comp_id):
        self.cursor.execute("DELETE FROM components WHERE id=?", (comp_id,))
        self.conn.commit()
        rows = self.get_components()
        self.cursor.execute("DELETE FROM components")
        for idx, row in enumerate(rows, start=1):
            self.cursor.execute(
                "INSERT INTO components (id, name, quantity) VALUES (?, ?, ?)",
                (idx, row["name"], row["quantity"])
            )
        self.conn.commit()

    # CRUD для заказов с ответственным
    def add_order(self, workstation_id, component_id, employee_id):
        self.cursor.execute(
            "INSERT INTO orders (workstation_id, component_id, employee_id) VALUES (?, ?, ?)",
            (workstation_id, component_id, employee_id)
        )
        self.conn.commit()

    def get_orders(self):
        self.cursor.execute(
            '''SELECT o.id,
                      w.address,
                      w.cabinet,
                      c.name AS comp_name,
                      c.quantity AS comp_quantity,
                      e.surname AS emp_surname,
                      e.name AS emp_name,
                      e.patronymic AS emp_patronymic,
                      o.created_at
               FROM orders o
               JOIN workstations w ON o.workstation_id=w.id
               JOIN components c ON o.component_id=c.id
               JOIN employees e ON o.employee_id=e.id
               ORDER BY o.id'''
        )
        return self.cursor.fetchall()

    def delete_order(self, order_id):
        # Удаляем заказ и переиндексируем id
        self.cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
        self.conn.commit()
        rows = self.get_orders()
        # Удаляем все записи
        self.cursor.execute("DELETE FROM orders")
        # Вставляем заново с новыми id
        for idx, row in enumerate(rows, start=1):
            # Извлекаем поля из результата get_orders
            address = row['address']
            cabinet = row['cabinet']
            comp_name = row['comp_name']
            comp_qty = row['comp_quantity']
            sur = row['emp_surname']
            nm = row['emp_name']
            pat = row['emp_patronymic']
            created = row['created_at']
            # Определяем component_id и employee_id
            comp_id = next((c['id'] for c in self.get_components() if c['name'] == comp_name and c['quantity'] == comp_qty), None)
            emp_id = next((e['id'] for e in self.get_employees() if e['surname'] == sur and e['name'] == nm and e['patronymic'] == pat), None)
            # workstation_id сохраняем как оригинальный порядок
            ws_id = next((w['id'] for w in self.get_workstations() if w['address'] == address and w['cabinet'] == cabinet), None)
            self.cursor.execute(
                "INSERT INTO orders (id, workstation_id, component_id, employee_id, created_at) VALUES (?, ?, ?, ?, ?)",
                (idx, ws_id, comp_id, emp_id, created)
            )
        self.conn.commit()
        rows = self.get_orders()
        self.cursor.execute("DELETE FROM orders")
        for idx, row in enumerate(rows, start=1):
            address, cabinet, comp_name, comp_qty, sur, nm, pat, created = (
                row['address'], row['cabinet'], row['name'], row['quantity'],
                row['surname'], row['name'], row['patronymic'], row['created_at']
            )
            # find component_id and employee_id by matching name, quantity, and full fio mapping
            comp_id = next((c['id'] for c in self.get_components() if c['name']==comp_name and c['quantity']==comp_qty), None)
            emp_id = next((e['id'] for e in self.get_employees()
                            if e['surname']==sur and e['name']==nm and e['patronymic']==pat), None)
            ws_id = idx  # assume workstations unchanged order
            self.cursor.execute(
                "INSERT INTO orders (id, workstation_id, component_id, employee_id, created_at) VALUES (?, ?, ?, ?, ?)",
                (idx, ws_id, comp_id, emp_id, created)
            )
        self.conn.commit()
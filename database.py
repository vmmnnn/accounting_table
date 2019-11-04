import sqlite3

class DB_people:
    def __init__(self):
        self.conn = sqlite3.connect('data/people.db')
        self.c = self.conn.cursor()    # to have an opportunity to change add etc
        self.c.execute('''CREATE TABLE IF NOT EXISTS people (id_client integer primary key, link text, FIO text)''')
        self.conn.commit()

    def insert_data(self, link, FIO):
        self.c.execute('''INSERT INTO people (link, FIO) VALUES (?, ?)''', (link, FIO))
        self.conn.commit()



class DB_products:
    def __init__(self):
        self.conn = sqlite3.connect('data/products.db')
        self.c = self.conn.cursor()    # to have an opportunity to change add etc
        self.c.execute('''CREATE TABLE IF NOT EXISTS products (id_product integer primary key, name text, prime_cost integer)''')   # prime_cost - себестоимость
        self.conn.commit()

    def insert_data(self, name, prime_cost):
        self.c.execute('''INSERT INTO products (name, prime_cost) VALUES (?, ?)''', (name, prime_cost))
        self.conn.commit()


class DB_order:
    def __init__(self):
        self.conn = sqlite3.connect('data/orders.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS orders (id_order integer primary key, id_client integer, shipping real, payment real, net real, order_date text, shipping_date text, shipping_way text)''')
        self.conn.commit()

    def insert_data(self, id_client, shipping, payment, net, order_date, shipping_date, shipping_way):
        self.c.execute('''INSERT INTO orders (id_client, shipping, payment, net, order_date, shipping_date, shipping_way) VALUES (?, ?, ?, ?, ?, ?, ?)''', (id_client, shipping, payment, net, order_date, shipping_date, shipping_way))
        self.conn.commit()


class DB_cart:
    def __init__(self):
        self.conn = sqlite3.connect('data/cart.db')
        self.c = self.conn.cursor()    # to have an opportunity to change add etc
        self.c.execute('''CREATE TABLE IF NOT EXISTS cart (id_order integer, id_product integer, quantity integer)''')
        self.conn.commit()

    def insert_data(self, id_order, id_product, quantity):
        self.c.execute('''INSERT INTO cart (id_order, id_product, quantity) VALUES (?, ?, ?)''', (id_order, id_product, quantity))
        self.conn.commit()

#class DB:
#    def __init__(self):
#        self.conn = sqlite3.connect('data/tablichka.db')
#        self.c = self.conn.cursor()    # to have an opportunity to change add etc
#        self.c.execute('''CREATE TABLE IF NOT EXISTS tablichka (id integer primary key, id_client integer, shipping real, product text, payment real, net real, order_date text, shipping_date text, shipping_way text)''')
#        self.conn.commit()

#    def insert_data(self, id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way):
#        self.c.execute('''INSERT INTO tablichka (id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way))
#        self.conn.commit()

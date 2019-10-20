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


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('data/tablichka.db')
        self.c = self.conn.cursor()    # to have an opportunity to change add etc
        self.c.execute('''CREATE TABLE IF NOT EXISTS tablichka (id integer primary key, id_client integer, shipping real, product text, payment real, net real, order_date text, shipping_date text, shipping_way text)''')
        self.conn.commit()

    def insert_data(self, id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way):
        self.c.execute('''INSERT INTO tablichka (id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way))
        self.conn.commit()

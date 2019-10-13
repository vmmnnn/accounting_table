from consts import *
import autocomplete

import tkinter as tk
from tkinter import ttk   # widget Treeview for table
import sqlite3
from tkinter import messagebox as mb


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.db_people = db_people
        self.view_records()

    def init_main(self):       ##############                D R A W I N G        S C R E E N
        self.toolbar = tk.Frame(bg='white', bd=2)   # bd - border       Add, Edit, Delete
        self.toolbar.pack(side=tk.TOP, fill=tk.X)   # toolbar is on the top
        self.draw_toolbar()
                                        #      T A B L E
        self.tree = ttk.Treeview(self, columns=('ID', 'shipping', 'link', 'FIO', 'product', 'payment', 'net', 'order_date', 'shipping_date', 'shipping_way'), height=TABLE_HEIGHT, show='headings') # show=... - not to show 0 columns
        self.draw_scrollbar()
        self.draw_columns()

        self.tree.pack()

    def draw_columns(self):
        self.tree.column('ID', width=0, anchor=tk.CENTER) # where the text should be in column
        self.tree.column('shipping', width=SHIPPING_COLUMN, anchor=tk.CENTER)
        self.tree.column('link', width=LINK_COLUMN, anchor=tk.CENTER)
        self.tree.column('FIO', width=FIO_COLUMN, anchor=tk.CENTER)
        self.tree.column('product', width=PRODUCT_COLUMN, anchor=tk.CENTER)
        self.tree.column('payment', width=PAYMENT_COLUMN, anchor=tk.CENTER)
        self.tree.column('net', width=NET_COLUMN, anchor=tk.CENTER)
        self.tree.column('order_date', width=ORDER_DATE_COLUMN, anchor=tk.CENTER)
        self.tree.column('shipping_date', width=SHIPPING_DATE_COLUMN, anchor=tk.CENTER)
        self.tree.column('shipping_way', width=SHIPPING_WAY_COLUMN, anchor=tk.CENTER)

        self.tree.heading('ID', text='')
        self.tree.heading('shipping', text='Доставка')
        self.tree.heading('link', text='Ссылка')
        self.tree.heading('FIO', text='ФИО')
        self.tree.heading('product', text='Товар')
        self.tree.heading('payment', text='Сумма')
        self.tree.heading('net', text='Чистыми')
        self.tree.heading('order_date', text='Дата заказа')
        self.tree.heading('shipping_date', text='Дата отправки')
        self.tree.heading('shipping_way', text='Способ отправки')

    def draw_scrollbar(self):
        w, h = SCREEN
        self.toolbar.update()
        self.toolbar_height = self.toolbar.winfo_screenheight()
        scrollbar_x, scrollbar_y = SCROLLBAR_COORDINATES
        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        vsb.place(x=scrollbar_x, y=scrollbar_y, height=SCROLLBAR_HEIGHT)
        self.tree.configure(yscrollcommand=vsb.set)


    def draw_toolbar(self):                                 ####### B U T T O N S
        self.add_img = tk.PhotoImage(file='buttons_pct/add.gif')    # button add
        btn_open_dialog = tk.Button(self.toolbar, text='Добавить позицию', command=self.open_dialog, bg='white', bd=0, compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='buttons_pct/update.gif')    # button edit
        btn_edit_dialog = tk.Button(self.toolbar, text='Редактировать', bg='white', bd=0, image=self.update_img, compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='buttons_pct/delete.gif')    # button delete
        btn_delete = tk.Button(self.toolbar, text='Удалить', bg='white', bd=0, image=self.delete_img, compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.to_excel_img = tk.PhotoImage(file='buttons_pct/to_excel.gif')    # button add
        btn_to_excel = tk.Button(self.toolbar, text='Выгрузить в excel', command=self.to_excel, bg='white', bd=0, compound=tk.TOP, image=self.to_excel_img)
        btn_to_excel.pack(side=tk.LEFT)


    def records(self, shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way):
        self.db.insert_data(shipping, product, payment, net, order_date, shipping_date, shipping_way)
        self.db_people.insert_data(link, FIO)
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM tablichka''')
        self.db_people.c.execute('''SELECT * FROM people''')

        people_data = self.db_people.c.fetchall()
        num_record = 1
        for row in self.db.c.fetchall():
            i = 0
            res_row = [str(num_record)]    # Номер записи в таблице
            num_record += 1
            res_row.append(str(row[1]))   # shipping
            res_row.append(str((people_data[i])[0]))  # link
            res_row.append(str((people_data[i])[1]))  # FIO
            i += 1
            j = -1
            for t in row:
                j += 1
                if j == 0 or j == 1:
                    continue
                res_row.append(str(t))
            [self.tree.delete(i) for i in self.tree.get_children()]  # clean, because we don't need double lines
            [self.tree.insert('', 'end', values = res_row)]  # new value is after previous


    def update_record(self, shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way):   # to change values: UPDATE changes them. Then description...=? - what to change, WHERE ID - which line
        self.db.c.execute('''UPDATE tablichka SET shipping=?, link=?, FIO=?, product=?, payment=?, net=?, order_date=?, shipping_date=?, shipping_way=? WHERE ID=?''', (shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way, self.tree.set(self.tree.selection()[0], '#1')))  # #1 - column №1 - ID
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        answ = mb.askyesno(title="Подтверждение", message="Удалить данные?")
        if answ == True:
            sel = self.tree.selection()
            for selection_item in sel:   # selection returns numers of all chosen records
                self.db.c.execute('''DELETE FROM tablichka WHERE id=?''', (self.tree.set(selection_item, '#1')))   # #1 - column from which we should take a number (column 1 because id is at this column)
            self.db.conn.commit()    # To save all results
            self.view_records()      # To show

    def to_excel(self):     # Выгрузить данные в excel
        FILENAME = "data/data.csv"
        self.db.c.execute('''SELECT shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way FROM tablichka''')
        component = self.db.c.fetchall()
        main_list = []
        for row in component:
            list1 = list(row)
            main_list.append(list1)
        out = open(FILENAME, 'w')
        for row in main_list:
            for column in row:
                out.write('%s;' % str(column))
            out.write('\n')
        out.close()

    def open_delete_dialog(self):
        Delete()

    def open_dialog(self):
        Child()

    def open_update_dialog(self):  # thiss function will be called after pushing the edit button
        Update()


            # window for adding new line
class Child(tk.Toplevel):    # child window
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def btn_add_reaction(self, event):
        self.view.records(self.entry_shipping.get(),
                          self.entry_link.get(),
                          self.entry_FIO.get(),
                          self.entry_product.get(),
                          self.entry_payment.get(),
                          self.entry_net.get(),
                          self.entry_order_date.get(),
                          self.entry_shipping_date.get(),
                          self.entry_shipping_way.get())
        self.destroy()


    def init_child(self):
        self.title('Добавить')
        self.geometry('400x400+400+100')  # first 2 numbers - size; second - place
        self.resizable(False, False)

        label_shipping = tk.Label(self, text='Доставка')  # names of text fields
        label_shipping.place(x=50, y=50)

        label_link = tk.Label(self, text='Ссылка')
        label_link.place(x=50, y=80)

        label_FIO = tk.Label(self, text='ФИО')
        label_FIO.place(x=50, y=110)

        label_product = tk.Label(self, text='Товар')
        label_product.place(x=50, y=140)

        label_payment = tk.Label(self, text='Сумма')
        label_payment.place(x=50, y=170)

        label_net = tk.Label(self, text='Чистыми')
        label_net.place(x=50, y=200)

        label_order_date = tk.Label(self, text='Дата заказа')
        label_order_date.place(x=50, y=230)

        label_shipping_date = tk.Label(self, text='Дата отправки')
        label_shipping_date.place(x=50, y=260)

        label_shipping_way = tk.Label(self, text='Способ отправки')
        label_shipping_way.place(x=50, y=290)


        self.entry_shipping = ttk.Entry(self)   # make a place where to write new positions
        self.entry_shipping.place(x=200, y=50)

        self.entry_link = ttk.Entry(self)
        self.entry_link.place(x=200, y=80)

        self.entry_FIO = ttk.Entry(self)
        self.entry_FIO.place(x=200, y=110)


#        self.entry_product = ttk.Entry(self)               # ADD AUTOCOMPLETE FROM https://gist.github.com/uroshekic/11078820
        autocomplete_list = products_list()
        self.entry_product = autocomplete.AutocompleteEntry(autocomplete_list, self, self, listboxLength=6, width=20, matchesFunction=autocomplete.matches)
        self.entry_product.place(x=200, y=140)

        self.entry_payment = ttk.Entry(self)
        self.entry_payment.place(x=200, y=170)

        self.entry_net = ttk.Entry(self)
        self.entry_net.place(x=200, y=200)

        self.entry_order_date = ttk.Entry(self)
        self.entry_order_date.place(x=200, y=230)

        self.entry_shipping_date = ttk.Entry(self)
        self.entry_shipping_date.place(x=200, y=260)

        self.entry_shipping_way = ttk.Entry(self)
        self.entry_shipping_way.place(x=200, y=290)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=350)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=350)
        self.btn_ok.bind('<Button-1>', self.btn_add_reaction)


        self.grab_set()   # so we can't use main window until this window is open
        self.focus_set()

class Update(Child):   # window for changing values. Child because windows are almost the same: another title and button 'edit' instead of 'Ok'
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def btn_edit_reaction(self, event):
        self.view.update_record(self.entry_shipping.get(),
                                self.entry_link.get(),
                                self.entry_FIO.get(),
                                self.entry_product.get(),
                                self.entry_payment.get(),
                                self.entry_net.get(),
                                self.entry_order_date.get(),
                                self.entry_shipping_date.get(),
                                self.entry_shipping_way.get())
        self.destroy()

    #def btn_close_reaction(self, event):

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=350)

        btn_edit.bind('<Button-1>', self.btn_edit_reaction)
        btn_edit.bind('<Return>', self.btn_edit_reaction)
        #btn_edit.bind('<Escape>', self.destroy)
        self.btn_ok.destroy()   # Because we have button 'edit' insead of 'Ok'

class DB_people:
    def __init__(self):
        self.conn = sqlite3.connect('data/people.db')
        self.c = self.conn.cursor()    # to have an opportunity to change add etc
        self.c.execute('''CREATE TABLE IF NOT EXISTS people (link text primary key, FIO text)''')
        self.conn.commit()

    def insert_data(self, link, FIO):
        self.c.execute('''INSERT INTO people (link, FIO) VALUES (?, ?)''', (link, FIO))
        self.conn.commit()

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('data/tablichka.db')
        self.c = self.conn.cursor()    # to have an opportunity to change add etc
        self.c.execute('''CREATE TABLE IF NOT EXISTS tablichka (id integer primary key, shipping real, product text, payment real, net real, order_date text, shipping_date text, shipping_way text)''')
        self.conn.commit()

    def insert_data(self, shipping, product, payment, net, order_date, shipping_date, shipping_way):
        self.c.execute('''INSERT INTO tablichka (shipping, product, payment, net, order_date, shipping_date, shipping_way) VALUES (?, ?, ?, ?, ?, ?, ?)''', (shipping, product, payment, net, order_date, shipping_date, shipping_way))
        self.conn.commit()


#class DB:
#    def __init__(self):
#        self.conn = sqlite3.connect('data/tablichka.db')
#        self.c = self.conn.cursor()    # to have an opportunity to change add etc
#        self.c.execute('''CREATE TABLE IF NOT EXISTS tablichka (id integer primary key, shipping real, link text, FIO text, product text, payment real, net real, order_date text, shipping_date text, shipping_way text)''')
#        self.conn.commit()

#    def insert_data(self, shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way):
#        self.c.execute('''INSERT INTO tablichka (shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way))
#        self.conn.commit()


def products_list():
    return ['арбуз', 'армия', 'болото', 'борщ', 'ворота', 'вино', 'вода', 'гармошка', 'град', 'голубь', 'дерево', 'дом', 'декорация', 'pen', 'pencil', 'pa', 'po', 'pu', 'pppp', 'pep', 'ptr', 'book', 'ручка', 'рюмка']

root = tk.Tk()
db = DB()
db_people = DB_people()
app = Main(root)
app.pack()

root.title("Database")
w, h = SCREEN
root.geometry("%dx%d+%d+%d" % (w, h, 0, 0))
root.mainloop()

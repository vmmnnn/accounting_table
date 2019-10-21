from consts import *
from database import *
import autocomplete

import tkinter as tk
from tkinter import ttk   # widget Treeview for table
from tkinter import messagebox as mb
from tkinter import filedialog as fd

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.db_people = db_people
        self.db_products = db_products
        self.view_records()

    def init_main(self):       ##############                D R A W I N G        S C R E E N
        self.toolbar = tk.Frame(bg='white', bd=2)   # bd - border       Add, Edit, Delete
        self.toolbar.pack(side=tk.TOP, fill=tk.X)   # toolbar is on the top
        self.draw_toolbar()
                                        #      T A B L E
        self.tree = ttk.Treeview(self, columns=('ID', 'num', 'shipping', 'link', 'FIO', 'product', 'payment', 'net', 'order_date', 'shipping_date', 'shipping_way'), height=TABLE_HEIGHT, show='headings') # show=... - not to show 0 columns
        self.draw_scrollbar()
        self.draw_columns()

        self.tree.pack()

    def draw_columns(self):
        self.tree.column('ID', width=0, anchor=tk.CENTER) # where the text should be in column
        self.tree.column('num', width=NUM_COLUMN, anchor=tk.CENTER) # where the text should be in column
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
        self.tree.heading('num', text='№')
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

        self.products_img = tk.PhotoImage(file='buttons_pct/products.gif')    # button add
        btn_products = tk.Button(self.toolbar, text='Товары', command=self.open_products, bg='white', bd=0, compound=tk.TOP, image=self.products_img)
        btn_products.pack(side=tk.LEFT)


    def records(self, shipping, new_link, new_FIO, product, payment, net, order_date, shipping_date, shipping_way):
        self.db_people.c.execute('''SELECT id_client FROM people WHERE link = ? AND FIO = ?''', (new_link, new_FIO))
        list_res = self.db_people.c.fetchall()
        if list_res:    # we already have this client
            new_id_client = list_res[0][0]
        else:
            self.db_people.insert_data(new_link, new_FIO)    # write new client
            self.db_people.c.execute('''SELECT id_client FROM people WHERE link = ? AND FIO = ?''', (new_link, new_FIO))
            new_id_client = self.db_people.c.fetchall()[0][0]
        self.db.insert_data(new_id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way)
        self.view_records()

    def view_records(self):
        self.db_people.c.execute('''SELECT * FROM people''')
        self.db.c.execute('''SELECT ID, id_client, shipping_way FROM tablichka''')

        [self.tree.delete(i) for i in self.tree.get_children()]  # clean, because we don't need double lines

        num_record = 0
        self.db.c.execute('''SELECT * FROM tablichka''')
        for row in self.db.c.fetchall():
            self.db_people.c.execute('''SELECT * FROM people WHERE id_client = ?''', (row[1],))
            person = self.db_people.c.fetchall()[0]
            res_row = [str(row[0]), str(num_record + 1)]
            num_record += 1
            res_row.append(str(row[2]))   # shipping
            res_row.append(str(person[1]))  # link
            res_row.append(str(person[2]))  # FIO

            col = -1
            for t in row:    # other columns (date etc)
                col += 1
                if col in range(3):
                    continue
                res_row.append(str(t))
            [self.tree.insert('', 'end', values = res_row)]  # new value is after previous

    def update_record(self, shipping, link, FIO, product, payment, net, order_date, shipping_date, shipping_way):   # to change values: UPDATE changes them. Then description...=? - what to change, WHERE ID - which line
        self.db.c.execute('''SELECT id_client FROM tablichka WHERE ID=?''', (self.tree.set(self.tree.selection()[0], '#1')))  # #1 - column №1 - ID
        id_client = self.db.c.fetchall()[0][0]

        self.db.c.execute('''SELECT COUNT(*) FROM tablichka WHERE id_client=?''', (id_client,))
        orders = int(self.db.c.fetchall()[0][0])

        if orders == 1:   # there is no more orders with this client => we can change
            self.db_people.c.execute('''UPDATE people SET link=?, FIO=? WHERE id_client=?''', (link, FIO, id_client))
        else:
            self.db_people.c.execute('''INSERT INTO people (link, FIO) VALUES (?, ?)''', (link, FIO))
            self.db_people.c.execute('''SELECT id_client FROM people WHERE link = ? AND FIO = ?''', (link, FIO))
            id_client = self.db_people.c.fetchall()[0][0]
        self.db_people.conn.commit()

        self.db.c.execute('''UPDATE tablichka SET id_client=?, shipping=?, product=?, payment=?, net=?, order_date=?, shipping_date=?, shipping_way=? WHERE ID=?''', (id_client, shipping, product, payment, net, order_date, shipping_date, shipping_way, self.tree.set(self.tree.selection()[0], '#1')))  # #1 - column №1 - ID
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        answ = mb.askyesno(title="Подтверждение", message="Удалить данные?")
        if answ == True:
            sel = self.tree.selection()
            for selection_item in sel:   # selection returns numers of all chosen records
                self.db.c.execute('''SELECT id_client FROM tablichka WHERE id=?''', (self.tree.set(selection_item, '#1')))
                id_to_delete = self.db.c.fetchall()[0][0]
                self.db.c.execute('''SELECT COUNT(*) FROM tablichka WHERE id_client=?''', (id_to_delete,))    # if this client had only one order => delete from people
                orders = self.db.c.fetchall()[0][0]
                if orders == 1:   # delete from people
                    self.db_people.c.execute('''DELETE FROM people WHERE id_client = ?''', (id_to_delete,))
                self.db.c.execute('''DELETE FROM tablichka WHERE id = ?''', (self.tree.set(selection_item, '#1')))   # #1 - column from which we should take a number (column 1 because id is at this column)
            self.db.conn.commit()    # To save all results
            self.db_people.conn.commit()
            self.view_records()      # To show

    def to_excel(self):     # Выгрузить данные в excel
        FILENAME = "data/data.csv"
        self.db.c.execute('''SELECT * FROM tablichka''')
        table = self.db.c.fetchall()

        num_record = 0
        main_list = [["ID", "Num", "Shipping", "Link", "Name", "Order", "Sum", "Net", "order_date", "shipping_date", "shipping_way"]]

        for row in table:
            num_record += 1
            cur_list = [row[0], num_record, row[2]]    # row[1] - id_client

            self.db_people.c.execute('''SELECT link, FIO FROM people WHERE id_client=?''', (row[0],))
            person = self.db_people.c.fetchall()

            cur_list.append(person[0][0])
            cur_list.append(person[0][1])

            col = -1
            for t in row:    # other columns (date etc)
                col += 1
                if col in range(3):
                    continue
                cur_list.append(str(t))
            main_list.append(cur_list)

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

    def open_update_dialog(self):  # this function will be called after pushing the edit button
        Update()

    def open_products(self):   # To open a new window - table with products
        Products_window()


class Products_window(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_products()
        self.db = db
        self.db_people = db_people
        self.db_products = db_products
        self.view_records()

    def init_products(self):
        self.title('Товары')
        self.geometry('400x400+400+100')  # first 2 numbers - size; second - place
        self.resizable(False, False)

        self.draw_menu()

        self.toolbar = tk.Frame(self, bg='white', bd=2)   # bd - border       Add, Edit, Delete
        self.toolbar.pack(side=tk.TOP, fill=tk.X)   # toolbar is on the top
        self.draw_toolbar()
                                        #      T A B L E
        self.tree = ttk.Treeview(self, columns=('ID', 'num', 'name', 'prime_cost'), height=380, show='headings') # show=... - not to show 0 columns
        self.draw_scrollbar()
        self.draw_columns()

        self.tree.pack()

        self.focus_set()

    def records(self, name, prime_cost):
        self.db_products.insert_data(str(name), int(prime_cost))
        self.view_records()

    def view_records(self):
        self.db_products.c.execute('''SELECT * FROM products''')
        [self.tree.delete(i) for i in self.tree.get_children()]  # clean, because we don't need double lines
        num_record = 0
        for row in self.db_products.c.fetchall():
            num_record += 1
            res_row = [row[0], num_record, row[1], row[2]]
            [self.tree.insert('', 'end', values = res_row)]  # new value is after previous

    def update_record(self, name, prime_cost):   # to change values: UPDATE changes them. Then description...=? - what to change, WHERE ID - which line
        self.db_products.c.execute('''UPDATE products SET name=?, prime_cost=? WHERE id_product=?''', (name, prime_cost, self.tree.set(self.tree.selection()[0], '#1')))  # #1 - column №1 - ID
        self.db_products.conn.commit()
        self.view_records()


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

    def draw_menu(self):
        mainmenu = tk.Menu(self)
        self.config(menu=mainmenu)
        filemenu = tk.Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="Выгрузить в excel", command=self.to_excel)
        filemenu.add_command(label="Догрузить из excel", command=self.from_excel)
        mainmenu.add_cascade(label="Excel", menu=filemenu)

    def draw_columns(self):
        self.tree.column('ID', width=0, anchor=tk.CENTER) # where the text should be in column
        self.tree.column('num', width=NUM_COLUMN, anchor=tk.CENTER) # where the text should be in column
        self.tree.column('name', width=NAME_PRODUCT_COLUMN, anchor=tk.CENTER)
        self.tree.column('prime_cost', width=PRIME_COST_PRODUCT_COLUMN, anchor=tk.CENTER)

        self.tree.heading('ID', text='')
        self.tree.heading('num', text='№')
        self.tree.heading('name', text='Название')
        self.tree.heading('prime_cost', text='Себестоимость')

    def draw_scrollbar(self):
        self.toolbar.update()
        toolbar_height = self.toolbar.winfo_screenheight()
        scrollbar_x, scrollbar_y = 345, toolbar_height % 10 + 23
        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        vsb.place(x=scrollbar_x, y=scrollbar_y, height=302)
        self.tree.configure(yscrollcommand=vsb.set)

    def to_excel(self):     # Выгрузить данные в excel
        FILENAME = "data/products.csv"
        self.db_products.c.execute('''SELECT * FROM products''')
        table = self.db_products.c.fetchall()

        num_record = 0
        main_list = [["ID", "Num", "Name", "Prime cost"]]

        for row in table:
            num_record += 1
            cur_list = [row[0], num_record, row[1], row[2]]
            main_list.append(cur_list)

        out = open(FILENAME, 'w')
        for row in main_list:
            for column in row:
                out.write('%s;' % str(column))
            out.write('\n')
        out.close()

    def from_excel(self):
        file_name = fd.askopenfilename()
        f = open(file_name)
        num_s = True
        s = f.read()
        new_products = s.split('\n')
        for row in new_products:
            if num_s:
                num_s = False
                continue
            if not row:
                break
            name, prime_cost = row.split(';')
            self.db_products.c.execute('''SELECT * FROM products WHERE name=?''', (name,))
            if not self.db_products.c.fetchall():    # we haven't had this product yet
                self.db_products.insert_data(str(name), int(prime_cost))
        self.view_records()
        #text.insert(1.0, s)
        f.close()


    def open_dialog(self):
        Child_product(self)

    def open_update_dialog(self):  # this function will be called after pushing the edit button
        Update_product(self)

    def delete_records(self):
        pass



class Child_product(tk.Toplevel):    # child window for product
    def __init__(self, products):
        super().__init__(root)
        self.init_child()
        self.view = products

    def btn_add_reaction(self, event):
        self.view.records(self.entry_name.get(),
                          self.entry_prime_cost.get())
        self.destroy()


    def init_child(self):
        self.title('Добавить товар')
        self.geometry('400x160+400+100')  # first 2 numbers - size; second - place
        self.resizable(False, False)

        label_name = tk.Label(self, text='Название')  # names of text fields
        label_name.place(x=50, y=50)

        label_prime_cost = tk.Label(self, text='Себестоимость')
        label_prime_cost.place(x=50, y=80)


        self.entry_name = ttk.Entry(self)   # make a place where to write new positions
        self.entry_name.place(x=200, y=50)

        self.entry_prime_cost = ttk.Entry(self)
        self.entry_prime_cost.place(x=200, y=80)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=110)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=110)
        self.btn_ok.bind('<Button-1>', self.btn_add_reaction)

        self.grab_set()   # so we can't use main window until this window is open
        self.focus_set()


class Update_product(Child_product):   # window for changing products. Child because windows are almost the same: another title and button 'edit' instead of 'Ok'
    def __init__(self, products):
        super().__init__(products)
        self.init_edit()
        self.view = products

    def btn_edit_reaction(self, event):
        self.view.update_record(self.entry_name.get(),
                                self.entry_prime_cost.get())
        self.destroy()

    def init_edit(self):
        self.title('Редактировать товар')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=110)

        btn_edit.bind('<Button-1>', self.btn_edit_reaction)
        btn_edit.bind('<Return>', self.btn_edit_reaction)
        self.btn_ok.destroy()   # Because we have button 'edit' insead of 'Ok'



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

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=350)

        btn_edit.bind('<Button-1>', self.btn_edit_reaction)
        btn_edit.bind('<Return>', self.btn_edit_reaction)
        self.btn_ok.destroy()   # Because we have button 'edit' insead of 'Ok'


def products_list():
    return ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'D1', 'D2', 'pen', 'pencil', 'pa', 'po', 'pu', 'pppp', 'pep', 'ptr', 'book', 'ручка', 'рюмка']

root = tk.Tk()
db = DB()
db_people = DB_people()
db_products = DB_products()
app = Main(root)
app.pack()

#products = Products_window()
#products.destroy()

root.title("Database")
w, h = SCREEN
root.geometry("%dx%d+%d+%d" % (w, h, 0, 0))
root.mainloop()

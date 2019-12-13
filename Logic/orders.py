from Logic.connector import connector
import random

class customer():
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def commit(self):
        try:
            conn = connector()
            conn.session.sql('insert into customer (name, phone, email) values(\''
                             +str(self.name)+'\', '
                             '\'' + str(self.phone)+'\','
                             ' \''+ str(self.email)+'\');').execute()
        except:
            print('Mistake on commit', __class__)


class book_order():
    def __init__(self, book_id, quantity):
        self.book = book_id
        self.quantity = quantity


    def get_id(self):
        conn = connector()
        try : x = conn.session.sql('select order_id from orders order by order_id DESC limit 1').execute().fetch_all()[0][0]
        except: x = 1
        return x

    def check_availability(self):
        conn = connector()
        if conn.session.sql('select exists (select * from book where book_id='+str(self.book)+' and quantity>='+str(self.quantity)+');').execute().fetch_all()[0][0]:
            return True
        return False

    def commit(self, id):
        try:
            conn = connector()
            if self.check_availability():
                    temp = 'True'
            else: temp = 'False'
            conn.session.sql(
                    'INSERT INTO orders_book (order_id, book_id, quantity, fullfilled) values (' + str(id) + ', '
                    + str(self.book) + ', '
                    + str(self.quantity) + ', '
                    + temp + ');').execute()
            if temp=='True':
                conn.session.sql(
                        'UPDATE book set quantity=quantity-'
                        + str(self.quantity) +
                        ' where book_id='
                        + str(self.book) + ';').execute()
        except Exception as e:
            print('Mistake on commit', __class__, e)






class order():

    def __init__(self, books, quantities, customer, step):
        self.books = [book_order(books[i],quantities[i]) for i in range(len(books))]
        self.customer = customer
        self.step = step

    def commit_order(self):
        self.fullfill()
        self.check_other_orders()
        conn = connector()
        conn.session.sql('INSERT INTO orders (cust_id, step, executed) values ('+str(self.customer)+', '
                         + str(self.step)+ ', False'
                         ')').execute()
        id = conn.session.sql('select order_id from orders order by order_id DESC limit 1;').execute().fetch_all()[0][0]
        for i in self.books: i.commit(id)
        if conn.session.sql('select avg(fullfilled) from orders_book where order_id='+str(id)+' group by order_id ;').execute().fetch_all()[0][0]==1:
            conn.session.sql('update orders set executed=True where order_id='+str(id)+';').execute()
            conn.session.sql('update orders set step='+ str(self.step)+' where order_id=' + str(id) + ';').execute()

    def check_other_orders(self):
        try:
            conn = connector()
            x = conn.session.sql('select order_id from orders where executed=False;').execute().fetch_all()
            un = []
            for i in x:
                un.append(i[0])
            for i in un:
                if conn.session.sql('select avg(fullfilled) from orders_book where order_id=' + str(
                    i) + ' group by order_id ;').execute().fetch_all()[0][0] == 1:
                    conn.session.sql('update orders set executed=True where order_id=' + str(i) + ';').execute()
                    conn.session.sql(
                        'update orders set step=' + str(self.step) + ' where order_id=' + str(i) + ';').execute()
        except: pass

    def fullfill(self):
        try:
            conn = connector()
            x = conn.session.sql('select book_id, quantity, order_id from orders_book where fullfilled=False;').execute().fetch_all()
            b = []
            q = []
            id = []
            for i in x:
                b.append(i[0])
                q.append(i[1])
                id.append(i[2])

            for i in range(len(b)):
                if book_order(b[i], q[i]).check_availability():
                    conn.session.sql('update orders_book set fullfilled=True where book_id='+str(b[i])+'&& order_id='+str(id[i])+';').execute()
                    conn.session.sql('UPDATE book set quantity=quantity-' + str(q[i]) + ' where book_id=' + str(b[i]) + ';').execute()
        except: print(self.__class__)



class publisher_order():
    def __init__(self, publisher, quantity, book, exec_time, step):
        self.quantity = quantity
        self.book = book
        self.exec = exec_time
        self.step = step


    def commit_p_order(self):
        conn = connector()
        conn.session.sql('INSERT INTO publisher_orders (quantity, exec_time, book_id, step) values ('+
                         str(self.quantity) + ', '+
                         str(self.exec) + ', '+
                         str(self.book) + ', '+
                         str(self.step)
                         +')').execute()

class total_order():
    def __init__(self, step,s ):
        self.step = step
        self.s = s

    def template(self):
        self.update_books()
        x, y, z = self.check_books()
        for i in range(len(x)):
            if z[i]==0:
                t = 10
            else:
                t = random.randint(10+round(z[i] * 200*0.75), 10+round(z[i] * 200*1.25))
            temp = publisher_order(y[i], t, x[i], random.randint(1, 5), self.step)
            temp.commit_p_order()

    def update_books(self):
        conn = connector()
        conn.session.sql(
            'update publisher_orders set exec_time=exec_time-' + str(self.s) + ' where exec_time >0').execute()
        try:
            x = conn.session.sql('select book_id, quantity from publisher_orders where exec_time=0;').execute().fetch_all()
            update_list = []
            q_list = []
            for i in x:
                update_list.append(i[0])
                q_list.append(i[1])
            for i in range(len(update_list)):
                conn.session.sql('update book set quantity=quantity + '+str(q_list[i])+' where book_id='+str(update_list[i])+';').execute()
            conn.session.sql('update publisher_orders set exec_time=-1 where exec_time=0;').execute()
        except: pass


    def check_books(self):
        conn = connector()
        orders = []
        publishers = []
        rating = []
        x = conn.session.sql(
            'select book_id, publ_id, popularity from book where quantity < 5;').execute().fetch_all()
        if  len(conn.session.sql('select book_id from publisher_orders where exec_time > -1;').execute().fetch_all())!=0:
            z = []
            t = conn.session.sql('select book_id from publisher_orders where exec_time > -1;').execute().fetch_all()
            for i in t:
                z.append(i[0])
        else: z = []
        for i in x:
            if i[0] not in z:
                orders.append(i[0])
                publishers.append(i[1])
                rating.append(i[2][0])
        return orders, publishers, rating







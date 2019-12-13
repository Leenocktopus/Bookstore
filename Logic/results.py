from Logic.connector import connector


class results():
    def __init__(self):
        self.connector = connector()

    def popular_book(self, step):
        return self.connector.session.sql(
            'select book_name from (select book_name, sum(quantity) as x from orders_customers_view where step='+str(step)+' group by book_name) as Y where x=(select max(x) from (select book_name, sum(quantity) as x from orders_customers_view where step='+str(step)+' group by book_name) as E);').execute().fetch_all()[0][0]

    def popular_book_all(self):
        return self.connector.session.sql('select book_name from (select book_name, sum(quantity) as x from orders_customers_view group by book_name) as Y where x=(select max(x) from (select book_name, sum(quantity) as x from orders_customers_view group by book_name) as E);').execute().fetch_all()[0][0]

    def popular_theme(self, step):
        return self.connector.session.sql(
            'select theme from (select theme, sum(quantity) as x from orders_customers_view where step='+str(step)+' group by theme) as Y where x=(select max(x) from (select theme, sum(quantity) as x from orders_customers_view where step='+str(step)+' group by theme) as E);').execute().fetch_all()[0][0]


    def publ_step(self, step):
        return self.connector.session.sql(
            'select '
            'count(p_id) '
            'from publisher_orders where '
            'step = ' + str(step) + ';'
        ).execute().fetch_all()[0][0]


    def publ_all(self):
        return self.connector.session.sql(
            'select '
            ' count(p_id) '
            ' from publisher_orders;'
        ).execute().fetch_all()[0][0]

    def popular_theme_all(self):
        return self.connector.session.sql('select theme from (select theme, sum(quantity) as x from orders_customers_view group by theme) as Y where x=(select max(x) from (select theme, sum(quantity) as x from orders_customers_view group by theme) as E);').execute().fetch_all()[0][0]


    def popular_customer(self, step):
        return self.connector.session.sql(
            'select c from (select customer as c, sum(quantity) as s from orders_customers_view where step=' +str(step)+' group by customer) as W where s=(select max(s) from (select customer as c, sum(quantity) as s from orders_customers_view where step='+str(step)+' group by customer) as W);').execute().fetch_all()[
            0][0]

    def popular_customer_all(self):
        return self.connector.session.sql('select c from (select customer as c, sum(quantity) as s from orders_customers_view group by customer) as W where s=(select max(s) from (select customer as c, sum(quantity) as s from orders_customers_view group by customer) as W);').execute().fetch_all()[0][0]





    def popular_publisher(self, step):
        return self.connector.session.sql(
            'select company from (select company, sum(quantity) as s from order_publisher where step ='+str(step)+' group by id ) as Y where s=(select max(s) from (select company, sum(quantity) as s from order_publisher where step ='+str(step)+'  group by id) as Z);').execute().fetch_all()[
            0][0]

    def popular_publisher_all(self):
        return self.connector.session.sql(
            'select company from (select company, sum(quantity) as s from order_publisher group by id) as Y where s=(select max(s) from (select company, sum(quantity) as s from order_publisher group by id) as Z);').execute().fetch_all()[
            0][0]



    def popular_author(self, step):
        return self.connector.session.sql(
            'select author from (select author, sum(quantity) as s from order_publisher where step ='+str(step)+' group by aid) as Y where s=(select max(s) from (select author, sum(quantity) as s from order_publisher where step ='+str(step)+' group by aid) as Z);').execute().fetch_all()[
            0][0]

    def popular_author_all(self):
        return self.connector.session.sql('select author from (select author, sum(quantity) as s from order_publisher group by aid) as Y where s=(select max(s) from (select author, sum(quantity) as s from order_publisher group by aid) as Z);').execute().fetch_all()[0][0]



    def sold(self, step):
        return self.connector.session.sql('select sum(quantity) from orders_customers_view where executed_order=True and step='+str(step)+';').execute().fetch_all()[0][0]

    def sold_all(self):
        return self.connector.session.sql(
            'select sum(quantity) from orders_customers_view where executed_order=True;').execute().fetch_all()[0][0]


    def executed_step(self,step, x):
        if x:
            return self.connector.session.sql(
                'select count(step) from orders where executed=true and step = '+str(step)+';').execute().fetch_all()[0][0]
        else:
            return self.connector.session.sql(
                'select count(step) from orders where executed=false and step = '+str(step)+';').execute().fetch_all()[0][0]
    def executed_all(self, x):
        if x:
            return self.connector.session.sql(
                'select count(step) from orders where executed=true;').execute().fetch_all()[0][0]
        else:
            return self.connector.session.sql(
                'select count(step) from orders where executed=false;').execute().fetch_all()[0][0]



    def income(self, step, mult, new_mult):
        total = 0
        new =[]
        x = self.connector.session.sql('select book_id from (select book.book_id, max(book.year) from book inner join author_book on book.book_id=author_book.book_id group by author_id) as O;').execute().fetch_all()
        for i in x:
           new.append(i[0])
        z = self.connector.session.sql('select book_id, price*s as sum from (select book_id as bid, sum(quantity) as s from orders_customers_view where executed_order=true and step='+str(step)+' group by book_id) as U inner join book on book.book_id=bid group by book_id;').execute().fetch_all()
        for i in z:
            if i[0] in new:
                total = total + (float(i[1])* float(new_mult))
            else:
                total = total + (float(i[1]) * float(mult))
        return round(total,2)

    def total_income(self, mult,new_mult):
        total = 0
        new = []
        x = self.connector.session.sql(
            'select book_id from (select book.book_id, max(book.year) from book inner join author_book on book.book_id=author_book.book_id group by author_id) as O;').execute().fetch_all()
        for i in x:
            new.append(i[0])
        z = self.connector.session.sql(
            'select book_id, price*s as sum from (select book_id as bid, sum(quantity) as s from orders_customers_view where executed_order=true group by book_id) as U inner join book on book.book_id=bid group by book_id;').execute().fetch_all()

        if self.connector.session.sql('select exists (select* from publisher_orders where exec_time<0);').execute().fetch_all()[0][0]:
            minus = self.connector.session.sql('select sum(total) from (select book_id, price*s as total from (select book_id as bid, sum(quantity) as s from publisher_orders where exec_time<0 group by book_id) as W inner join book on bid=book.book_id) as I;').execute().fetch_all()[0][0]
        else: minus = 0
        for i in z:
            if i[0] in new:
                total = total + (float(i[1]) * float(new_mult))
            else:
                total = total + (float(i[1]) * float(mult))
        return round(total-float(minus), 2)



    def assortment(self):
            z = self.connector.session.sql('select * from book_view;').execute().fetch_all()
            result = []
            k=-1
            for i in z:
                k+=1
                result.append([])
                for j in i:
                    if type(j)==tuple:
                        result[k].append(round(j[0]))
                    else:
                        result[k].append(j)
            return result


    def orders(self, x):
        z = self.connector.session.sql('select id, book_name, author_name, theme, quantity, customer, phone, step, executed_order, executed_part from orders_customers_view where step='+str(x)+';').execute().fetch_all()
        result = []
        k = -1
        for i in z:
            k += 1
            result.append([])
            for j in i:
                if type(j) == tuple:
                    result[k].append(round(j[0]))
                else:
                    result[k].append(j)
        return result

    def publisher_orders(self):
        z = self.connector.session.sql('select * from view_porder order by p_id;').execute().fetch_all()
        result = []
        k = -1
        for i in z:
            k += 1
            result.append([])
            for j in i:
                if type(j) == tuple:
                    result[k].append(round(j[0]))
                else:
                    result[k].append(j)
        return result



    def book_by_parameter(self, x):
        if x=='author':
            z = self.connector.session.sql(
                ' select author_name, sum(quantity) from orders_customers_view group by author_name;').execute().fetch_all()
        elif x=='name':
            z = self.connector.session.sql(
                'select book_name, sum(quantity) from orders_customers_view group by book_id;').execute().fetch_all()
        elif x=='publisher':
            z = self.connector.session.sql(
                'select company, sum(quantity) from order_publisher group by company;').execute().fetch_all()
        elif x=='theme':
            z = self.connector.session.sql(
                'select theme, sum(quantity) from orders_customers_view group by theme;').execute().fetch_all()
        elif x=='customer':
            z = self.connector.session.sql(
                'select customer, sum(quantity) from orders_customers_view group by customer;').execute().fetch_all()
        result = []
        k = -1
        for i in z:
            k += 1
            result.append([])
            for j in i:
                    result[k].append(j)
        return result




    def books_by_order(self):
        conn = connector()
        orders = conn.session.sql('select count(s) from (select count(order_id) as s from orders_book group by order_id) as G;').execute().fetch_all()[0][0]
        books = conn.session.sql('select sum(quantity) as s from orders_book;').execute().fetch_all()[0][0]
        return round(float(books)/float(orders),2)



    def price_by_order(self):
        conn =connector()
        x = conn.session.sql('select id, sum(orders_customers_view.quantity*price) from orders_customers_view inner join book on book.book_id=orders_customers_view.book_id group by id;').execute().fetch_all()
        ids = []
        prices = []
        for i in x:
            ids.append(i[0])
            prices.append(i[1])

        return ids, prices, round(float(sum(prices)/len(prices)),2)




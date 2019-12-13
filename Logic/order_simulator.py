import random
from Logic.connector import connector, metadata
from Logic.orders import order,total_order

class order_simulator():
   def __init__(self, step, mult,new_mult):
       self.step = step
       self.mult = mult
       self.new_mult = new_mult
       self.connector = connector()
       self.metadata = metadata()
       self.author_count = self.metadata.select_authors_count()
       self.book_count = self.metadata.select_books_count()
       self.cust_count = self.metadata.select_customers_count()
       self.total_step = 0



   def simulate(self):
       self.total_step = self.total_step + self.step
       for day in range(self.step):
           books_in_day = random.randint(round(self.book_count*0.75),round(self.book_count*1.25))
           for i in range(books_in_day):
               cust_id = random.randint(1, self.cust_count)
               x = self.order_parameters()
               book_s = []
               quantities = []
               for i in x:
                   author = random.randint(1, self.author_count)
                   books = self.metadata.select_by_author(author)
                   books.append('new')
                   books.append('new')
                   random_book = books[random.randint(0, len(books)-1)]
                   if random_book=='new':
                       book_id = self.metadata.newest_book(author)
                   else:
                       book_id = random_book
                   book_s.append(book_id)
                   quantities.append(i)
               c = order(book_s, quantities, cust_id, self.total_step)
               c.commit_order()
       self.set_popularity()
       total_o = total_order(self.total_step , self.step)
       total_o.template()

   def order_parameters(self):
       one_order = [1] * 20
       two_orders = [2] * 3
       three_orders = [3] * 1
       total = (one_order + two_orders + three_orders)
       total_ids = total[random.randint(0, len(total) - 1)]
       total_books = [total[random.randint(0, len(total) - 1)] for i in range(total_ids)]
       return total_books


   def stop_simulation(self):
       self.connector.session.sql('SET FOREIGN_KEY_CHECKS = 0;').execute()
       self.connector.session.sql('TRUNCATE TABLE orders;').execute()
       self.connector.session.sql('TRUNCATE TABLE orders_book').execute()
       self.connector.session.sql('TRUNCATE TABLE publisher_orders').execute()
       self.connector.session.sql('SET FOREIGN_KEY_CHECKS = 1;').execute()

   def set_popularity(self):
        x = self.connector.session.sql('select book_id, sum(quantity) from orders_book group by book_id;').execute().fetch_all()
        z = self.connector.session.sql('select sum(quantity) from orders_book;').execute().fetch_all()[0][0]
        if z ==None:

            self.connector.session.sql('update book set popularity='+str(0.0)+';').execute()
        else:
            for i in x:
                self.connector.session.sql('update book set popularity='+str(i[1]/z)+'where book_id='+str(i[0])+';').execute()








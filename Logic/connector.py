import mysqlx


class connector():
    def __init__(self):
        self.session = self.connect()

    def connect(self):
        session = mysqlx.get_session({
            'host': 'localhost',
            'port': 33060,
            'user': 'root',
            'password': 'root'})
        session.sql('use bookshelf;').execute()
        return session

class metadata():
    def __init__(self):
        self.conn = connector()

    def select_books_count(self):
        return self.conn.session.sql('select COUNT(book_id) from book;').execute().fetch_all()[0][0]

    def select_authors_count(self):
        return self.conn.session.sql('select COUNT(author_id) from author;').execute().fetch_all()[0][0]

    def select_by_author(self, s):
        result = []
        x = self.conn.session.sql('select book_id from author_book where author_id='+str(s)+';').execute().fetch_all()
        for row in range(len(x)):
            result.append(x[row][0])
        return result

    def newest_book(self, s):
        return self.conn.session.sql('select book.book_id, max(book.year) from book inner join author_book on book.book_id=author_book.book_id where author_book.author_id='+str(s)+';').execute().fetch_all()[0][0]

    def select_customers_count(self):
        return self.conn.session.sql('select COUNT(cust_id) from customer;').execute().fetch_all()[0][0]










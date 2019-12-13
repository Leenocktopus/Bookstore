from Logic.connector import connector

class author:
    def __init__(self, name):
        self.name = name


    def commit(self):
        try:
            conn = connector()
            conn.session.sql('insert ignore into author (name) values(\''+self.name+'\');').execute()
        except:
            print('Mistake on commit', __class__)

    def get(self):
        try:
            conn = connector()
            return conn.session.sql('select author_id from author where name=\''+str(self.name)+'\';').execute().fetch_all()[0][0]
        except:
            print('Mistake on get', __class__)

class publisher:
    def __init__(self, name):
        self.company_name = name

    def commit(self):
        try:
            conn = connector()
            conn.session.sql('insert ignore into publisher(company_name) values(\''+self.company_name+'\');').execute()
        except:
            print('Mistake on commit', __class__)
    def get(self):
        try:
            conn = connector()
            return conn.session.sql('select publ_id from publisher where company_name=\''+str(self.company_name)+'\';').execute().fetch_all()[0][0]
        except:
            print('Mistake on get', __class__)


class theme:
    def __init__(self, name):
        self.theme_name=name

    def commit(self):
        try:
            conn = connector()
            conn.session.sql('insert ignore into genre(name) values (\''+self.theme_name+'\');').execute()
        except:
            print('Mistake on commit', __class__)

    def get(self):
        try:
            conn = connector()
            return conn.session.sql('select genre_id from genre where name=\''+str(self.theme_name)+'\';').execute().fetch_all()[0][0]
        except:
            print('Mistake on get', __class__)


class book:
    def __init__(self, author_names, name, year, pages,theme1, price, publisher_name, quantity):
        self.authors = [author(i) for i in author_names]
        self.name = name
        self.year = year
        self.pages = pages
        self.theme = theme(theme1)
        self.price = price
        self.publisher = publisher(publisher_name)
        self.quantity = quantity


    def commit(self):
            for i in self.authors:
                i.commit()
            ids = [i.get() for i in self.authors]
            conn = connector()
            self.theme.commit()
            self.publisher.commit()
            print('all_ok')
            conn.session.sql('INSERT IGNORE INTO book (name, year, pages, price, publ_id, genre_id, quantity) VALUES( \''+str(self.name)+'\', \''+
                             str(self.year) + '\', ' +str(self.pages) + ' , ' + str(self.price) + ' , ' + str(self.publisher.get())+ ' , ' +str(self.theme.get())+' , ' +str(self.quantity) +
                             ');').execute()
            id = self.get()
            if conn.session.sql('select exists(select book_id from author_book where book_id='+str(id)+');').execute().fetch_all()[0][0]==0:
                for i in ids:
                    conn.session.sql('INSERT  INTO author_book(author_id, book_id) values ('+str(i)+','+str(id)+');').execute()


    def get(self):
        try:
            conn = connector()
            return conn.session.sql(
                'select book_id from book where name=\'' + str(self.name) + '\';').execute().fetch_all()[0][0]
        except:
            print('Mistake on get', __class__)




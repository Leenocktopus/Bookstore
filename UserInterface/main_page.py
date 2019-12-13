from tkinter import *
from tkinter import messagebox
from Logic.order_simulator import order_simulator
from Logic.results import results
from Logic.book import book
import matplotlib.pyplot as plt
import threading

class Main_window():
    def __init__(self, controller):
        self.controller = controller
        controller.title('Book store simulation')
        controller.geometry('700x500')

        simulator = 0
        menubar = Menu(controller)
        menubar.add_command(label="Додати книгу", command= lambda : new_window())
        menubar.add_command(label="Асортимент", command=lambda: assort())
        menubar.add_command(label="Замовлення покупців", command=lambda: orders())
        menubar.add_command(label="Замовлення в видаництво", command=lambda: publisher_orders())
        stats = Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Статистика", menu=stats)
        stats.add_command(label="Книги/Книги", command=lambda: book_book('name'))
        stats.add_command(label="Книги/Автор", command=lambda: book_book('author'))
        stats.add_command(label="Книги/Тематика", command=lambda: book_book('theme'))
        stats.add_command(label="Книги/Видавництво", command=lambda: book_book('publisher'))
        stats.add_command(label="Книги/Покупець", command=lambda: book_book('customer'))
        stats.add_command(label="Ціна/Замовлення", command=lambda: plot())
        controller.config(menu=menubar)
        self.step_variable = IntVar()
        self.day_variable = IntVar()
        self.f_b = Frame(controller)
        self.f_side = Frame(controller)

        self.l_multipl = Label(controller, text='Роздрібна націнка')
        self.l_new_mult = Label(controller, text='Націнка на новий товар')
        self.simulation_step = Label(controller, text='Крок симуляції')

        self.e1 = Entry(controller)
        self.e2 = Entry(controller)


        self.r1 = Radiobutton(controller, text='1 День', variable = self.step_variable, value=1)
        self.r2 = Radiobutton(controller, text='2 Дні', variable = self.step_variable, value=2)
        self.r3 = Radiobutton(controller, text='3 Дні', variable = self.step_variable, value=3)
        self.begin = Button(controller, text='Почати симуляцію', command= lambda : start())
        self.reset = Button(controller, text='Закінчити симуляцію', command=lambda: reset())
        self.step = Button(controller, text='Крок', command=lambda: step())

        self.l1 = Label(controller, text='Загальний результат')
        self.l2 = Label(controller, text='Результати на поточному кроці')
        self.l3 = Label(controller, textvariable=self.day_variable)
        self.l4 = Label(controller, text='День Симуляції:')

        Label(self.f_b, text='Виконананих замовлень:').grid(row=0, column=0, sticky=W)
        Label(self.f_b, text='Затриманих замовлень:').grid(row=1, column=0, sticky=W)
        Label(self.f_b, text='Всього замовлень:').grid(row=2, column=0, sticky=W)
        Label(self.f_b, text='Всього книг:').grid(row=3, column=0, sticky=W)
        Label(self.f_b, text='Замовлень в видавництва:').grid(row=4, column=0, sticky=W)
        Label(self.f_b, text='Найпопулярніша книга:').grid(row=5, column=0, sticky=W)
        Label(self.f_b, text='Найпопулярніший автор:').grid(row=6, column=0, sticky=W)
        Label(self.f_b, text='Найпопулярніше видавництво:').grid(row=7, column=0, sticky=W)
        Label(self.f_b, text='Найактивніший покупець:').grid(row=8, column=0, sticky=W)
        Label(self.f_b, text='Найпопулярніша тематика:').grid(row=9, column=0, sticky=W)
        Label(self.f_b, text='Отримано прибутку:').grid(row=10, column=0, sticky=W)


        self.step1 = Label(self.f_b,width=15, anchor=W)
        self.step2 = Label(self.f_b,width=15, anchor=W)
        self.step3 = Label(self.f_b,width=15, anchor=W)
        self.step4 = Label(self.f_b,width=15, anchor=W)
        self.step5 = Label(self.f_b,width=15, anchor=W)
        self.step6 = Label(self.f_b,width=15, anchor=W)
        self.step7 = Label(self.f_b,width=15, anchor=W)
        self.step8 = Label(self.f_b,width=15, anchor=W)
        self.step9 = Label(self.f_b, width=15,anchor=W)
        self.step10 = Label(self.f_b,width=15, anchor=W)
        self.step11 = Label(self.f_b,width=15, anchor=W)

        self.step1.grid(row=0, column=1, sticky=W)
        self.step2.grid(row=1, column=1, sticky=W)
        self.step3.grid(row=2, column=1, sticky=W)
        self.step4.grid(row=3, column=1, sticky=W)
        self.step5.grid(row=4, column=1, sticky=W)
        self.step6.grid(row=5, column=1, sticky=W)
        self.step7.grid(row=6, column=1, sticky=W)
        self.step8.grid(row=7, column=1, sticky=W)
        self.step9.grid(row=8, column=1, sticky=W)
        self.step10.grid(row=9, column=1, sticky=W)
        self.step11.grid(row=10, column=1, sticky=W)

        Label(self.f_side, text='Виконананих замовлень:').grid(row=0, column=0, sticky=W)
        Label(self.f_side, text='Затриманих замовлень:').grid(row=1, column=0, sticky=W)
        Label(self.f_side, text='Всього замовлень:').grid(row=2, column=0, sticky=W)
        Label(self.f_side, text='Всього книг:').grid(row=3, column=0, sticky=W)
        Label(self.f_side, text='Замовлень в видавництва:').grid(row=4, column=0, sticky=W)
        Label(self.f_side, text='Найпопулярніша книга:').grid(row=5, column=0, sticky=W)
        Label(self.f_side, text='Найпопулярніший автор:').grid(row=6, column=0, sticky=W)
        Label(self.f_side, text='Найпопулярніше видавництво:').grid(row=7, column=0, sticky=W)
        Label(self.f_side, text='Найактивніший покупець:').grid(row=8, column=0, sticky=W)
        Label(self.f_side, text='Найпопулярніша тематика:').grid(row=9, column=0, sticky=W)
        Label(self.f_side, text='Поточний бюджет:').grid(row=10, column=0, sticky=W)
        Label(self.f_side, text='Книг в замовленні:').grid(row=11, column=0, sticky=W)
        Label(self.f_side, text='Ціна замовлення:').grid(row=12, column=0, sticky=W)

        self.total1 = Label(self.f_side,width=15, anchor=W)
        self.total2 = Label(self.f_side,width=15, anchor=W)
        self.total3 = Label(self.f_side,width=15, anchor=W)
        self.total4 = Label(self.f_side,width=15, anchor=W)
        self.total5 = Label(self.f_side,width=15, anchor=W)
        self.total6 = Label(self.f_side,width=15, anchor=W)
        self.total7 = Label(self.f_side,width=15, anchor=W)
        self.total8 = Label(self.f_side,width=15, anchor=W)
        self.total9 = Label(self.f_side,width=15, anchor=W)
        self.total10 = Label(self.f_side,width=15, anchor=W)
        self.total11 = Label(self.f_side,width=15, anchor=W)
        self.total12 = Label(self.f_side, width=15, anchor=W)
        self.total13 = Label(self.f_side, width=15, anchor=W)

        self.total1.grid(row=0, column=1, sticky=W)
        self.total2.grid(row=1, column=1, sticky=W)
        self.total3.grid(row=2, column=1, sticky=W)
        self.total4.grid(row=3, column=1, sticky=W)
        self.total5.grid(row=4, column=1, sticky=W)
        self.total6.grid(row=5, column=1, sticky=W)
        self.total7.grid(row=6, column=1, sticky=W)
        self.total8.grid(row=7, column=1, sticky=W)
        self.total9.grid(row=8, column=1, sticky=W)
        self.total10.grid(row=9, column=1, sticky=W)
        self.total11.grid(row=10, column=1, sticky=W)
        self.total12.grid(row=11, column=1, sticky=W)
        self.total13.grid(row=12, column=1, sticky=W)

        self.l_multipl.grid(row=0, column=0, sticky=W)
        self.l_new_mult.grid(row=1, column=0, sticky=W)

        self.simulation_step.grid(row=2, column=0, sticky=W)
        self.e1.grid(row=0, column=1, sticky=W)
        self.e2.grid(row=1, column=1, sticky=W)
        self.r1.grid(row=2, column=1, sticky=W)
        self.r2.grid(row=3, column=1, sticky=W)
        self.r3.grid(row=4, column=1, sticky=W)
        self.begin.grid(row=5, column=0, sticky=(W,E,S,N))
        self.reset.grid(row=5, column=1, sticky=(W,E,S,N))
        self.step.grid(row=5, column=2)
        self.l3.grid(row=0, column=4, sticky=W)
        self.l4.grid(row=0, column=3, sticky=W)
        self.l1.grid(row=1, column=3, columnspan=2, sticky=W)
        self.l2.grid(row=7, column=0, sticky=W)

        self.f_b.grid(row=8, column=0, columnspan=3,sticky=W)
        self.f_side.grid(row=2, column=3, columnspan=3, rowspan=7, sticky=W+N)

        self.reset.config(state='disabled')
        self.step.config(state='disabled')



        def plot():
            if self.day_variable.get()!=0:
                self.res = results()
                x,y,r = self.res.price_by_order()
                plt.plot(sorted(x),y)
                plt.show()

        def update_step_result():
            global simulator
            self.res = results()
            self.step1.configure(text=self.res.executed_step(self.day_variable.get(), 1 ))
            self.step2.configure(text=self.res.executed_step(self.day_variable.get(), 0))
            self.step3.configure(text=self.res.executed_step(self.day_variable.get(), 0)+self.res.executed_step( self.day_variable.get(), 1))
            self.step4.configure(text=self.res.sold(self.day_variable.get()))
            self.step5.configure(text=self.res.publ_step(self.day_variable.get()))
            self.step6.configure(text=self.res.popular_book(self.day_variable.get()))
            self.step7.configure(text=self.res.popular_author(self.day_variable.get()))
            self.step8.configure(text=self.res.popular_publisher(self.day_variable.get()))
            self.step9.configure(text=self.res.popular_customer(self.day_variable.get()))
            self.step10.configure(text=self.res.popular_theme(self.day_variable.get()))
            self.step11.configure(text=self.res.income(self.day_variable.get(), self.e1.get(), self.e2.get()))

            self.total1.configure(text=self.res.executed_all(1))
            self.total2.configure(text=self.res.executed_all(0))
            self.total3.configure(text=self.res.executed_all(1)+self.res.executed_all(0))
            self.total4.configure(text=self.res.sold_all())
            self.total5.configure(text=self.res.publ_all())
            self.total6.configure(text=self.res.popular_book_all())
            self.total7.configure(text=self.res.popular_author_all())
            self.total8.configure(text=self.res.popular_publisher_all())
            self.total9.configure(text=self.res.popular_customer_all())
            self.total10.configure(text=self.res.popular_theme_all())
            self.total11.configure(text=self.res.total_income(self.e1.get(), self.e2.get()))
            self.total12.configure(text=self.res.books_by_order())
            x,y, middle = self.res.price_by_order()
            self.total13.configure(text=middle)
            simulator.set_popularity()

        def start():
            global simulator
            if self.step_variable.get()!=0 and self.e1.get()!='' and self.e2.get()!='':
                simulator = order_simulator(self.step_variable.get(), self.e1.get(), self.e2.get())
                self.begin.config(state='disabled')
                self.reset.config(state='normal')
                self.step.config(state='normal')
            else:
                messagebox.showerror("Помилка", "Введених параметрів недостатньо для симуляції або вони неправильні!")

        def assort():
            re = results()
            res = re.assortment()
            app2 = Toplevel()
            Label(app2, text='Назва книги', bg='gray', anchor='w').grid(row=0, column=0, sticky=(S,W,E,N))
            Label(app2, text='Автор', bg='gray', anchor='w').grid(row=0, column=1, sticky=(S,W,E,N))
            Label(app2, text='Видавництво', bg='gray', anchor='w').grid(row=0, column=2, sticky=(S,W,E,N))
            Label(app2, text='Кількість сторінок', bg='gray', anchor='w').grid(row=0, column=3, sticky=(S,W,E,N))
            Label(app2, text='Рік видання', bg='gray', anchor='w').grid(row=0, column=4, sticky=(S,W,E,N))
            Label(app2, text='Популярність (%)',bg='gray', anchor='w').grid(row=0, column=6, sticky=(S,W,E,N))
            Label(app2, text='Книг в магазині', bg='gray', anchor='w').grid(row=0, column=5, sticky=(S, W, E, N))
            for i in range(len(res)):
                for j in range(len(res[i])):
                    Label(app2, text=res[i][j], bg='white', anchor='w').grid(row=i+1, column=j, sticky=(S,W,E,N))

        def orders():
            re = results()
            if self.day_variable.get()==0:
                res = re.orders(1)
            else: res = re.orders(self.day_variable.get())
            app3 = Toplevel()
            Label(app3, text='Номер', bg='gray', anchor='w').grid(row=0, column=0, sticky=(S, W, E, N))
            Label(app3, text='Назва книги', bg='gray', anchor='w').grid(row=0, column=1, sticky=(S, W, E, N))
            Label(app3, text='Автор', bg='gray', anchor='w').grid(row=0, column=2, sticky=(S, W, E, N))
            Label(app3, text='Тематика', bg='gray', anchor='w').grid(row=0, column=3, sticky=(S, W, E, N))
            Label(app3, text='Кількість', bg='gray', anchor='w').grid(row=0, column=4, sticky=(S, W, E, N))
            Label(app3, text='Ім\'я покупця', bg='gray', anchor='w').grid(row=0, column=5, sticky=(S, W, E, N))
            Label(app3, text='Телефон', bg='gray', anchor='w').grid(row=0, column=6, sticky=(S, W, E, N))
            Label(app3, text='День', bg='gray', anchor='w').grid(row=0, column=7, sticky=(S, W, E, N))
            Label(app3, text='Виконання замовлення', bg='gray', anchor='w').grid(row=0, column=8, sticky=(S, W, E, N))
            Label(app3, text='Наявність книги', bg='gray', anchor='w').grid(row=0, column=9, sticky=(S, W, E, N))
            for i in range(len(res)):
                for j in range(len(res[i])):
                    if j==8 or j==9:
                        if res[i][j]==1:
                            res[i][j]='Done'
                        if res[i][j]==0:
                            res[i][j]='Waiting'
                    Label(app3, text=res[i][j], bg='white', anchor='w').grid(row=i+1, column=j, sticky=(S,W,E,N))

        def publisher_orders():
            re = results()
            res = re.publisher_orders()
            app3 = Toplevel()
            Label(app3, text='Номер', bg='gray', anchor='w').grid(row=0, column=0, sticky=(S, W, E, N))
            Label(app3, text='Кількість', bg='gray', anchor='w').grid(row=0, column=1, sticky=(S, W, E, N))
            Label(app3, text='Видавництво', bg='gray', anchor='w').grid(row=0, column=2, sticky=(S, W, E, N))
            Label(app3, text='Назва книги', bg='gray', anchor='w').grid(row=0, column=3, sticky=(S, W, E, N))
            Label(app3, text='День', bg='gray', anchor='w').grid(row=0, column=4, sticky=(S, W, E, N))
            Label(app3, text='Днів до виконання', bg='gray', anchor='w').grid(row=0, column=5, sticky=(S, W, E, N))
            for i in range(len(res)):
                for j in range(len(res[i])):
                    if res[i][j]==-1 or res[i][j]==-2 or res[i][j]==-3:
                        res[i][j]='Done'
                    Label(app3, text=res[i][j], bg='white', anchor='w').grid(row=i + 1, column=j, sticky=(S, W, E, N))

        def book_book(x):
            re = results()
            res = re.book_by_parameter(x)
            app4 = Toplevel()
            Label(app4, text='Параметр', bg='gray', anchor='w').grid(row=0, column=0, sticky=(S, W, E, N))
            Label(app4, text='Кількість', bg='gray', anchor='w').grid(row=0, column=1, sticky=(S, W, E, N))
            for i in range(len(res)):
                for j in range(len(res[i])):
                    Label(app4, text=res[i][j], bg='white', anchor='w').grid(row=i + 1, column=j, sticky=(S, W, E, N))


        def step():
            global simulator
            simulator.simulate()
            self.day_variable.set(self.day_variable.get()+self.step_variable.get())
            update_step_result()



        def reset():
            global simulator
            simulator.stop_simulation()
            self.reset.config(state='disabled')
            self.begin.config(state='normal')
            self.step.config(state='disabled')
            self.day_variable.set(0)
            self.step1.configure(text='')
            self.step2.configure(text='')
            self.step3.configure(text='')
            self.step4.configure(text='')
            self.step5.configure(text='')
            self.step6.configure(text='')
            self.step7.configure(text='')
            self.step8.configure(text='')
            self.step9.configure(text='')
            self.step10.configure(text='')
            self.step11.configure(text='')

            self.total1.configure(text='')
            self.total2.configure(text='')
            self.total3.configure(text='')
            self.total4.configure(text='')
            self.total5.configure(text='')
            self.total6.configure(text='')
            self.total7.configure(text='')
            self.total8.configure(text='')
            self.total9.configure(text='')
            self.total10.configure(text='')
            self.total11.configure(text='')
            self.total12.configure(text='')
            self.total13.configure(text='')

            simulator.set_popularity()

        def new_window():
            app1 = Toplevel()
            app1.geometry('244x214')
            app1.resizable(width=False, height=False)
            app1.title('Додати книгу')
            var1 = StringVar()
            var2 = StringVar()
            var1.set('Orelly')
            var2.set("Science")
            option1 = OptionMenu(app1, var1, 'Orelly','Springer','Willey','Oxford UP', 'Pearson Ed.', 'Egmont')
            option2 = OptionMenu(app1, var2, "Biography", "Science" ,"Science Fiction" ,"Fantasy" ,"Fairy Tale", "Drama" ,"Romance")
            cancel = Button(app1, text='Відмінити', command = lambda : app1.destroy())
            ok = Button(app1, text='Додати Книгу ', command = lambda : add_book())
            e1 = Entry(app1)
            e2 = Entry(app1)
            e3 = Entry(app1)
            e4 = Entry(app1)
            e5 = Entry(app1)
            e6 = Entry(app1)
            Label(app1, text='Автор:').grid(row=0, column=0, sticky=E)
            Label(app1, text='Назва:').grid(row=1, column=0, sticky=E)
            Label(app1, text='Рік видання:').grid(row=2, column=0, sticky=E)
            Label(app1, text='Кількість сторінок:').grid(row=3, column=0, sticky=E)
            Label(app1, text='Початкова кількість:').grid(row=4, column=0, sticky=E)
            Label(app1, text='Ціна:').grid(row=6, column=0, sticky=E)
            Label(app1, text='Видання:').grid(row=7, column=0, sticky=E)
            Label(app1, text='Тематика:').grid(row=8, column=0, sticky=E)
            option1.grid(row=7, column=1, sticky=W)
            option2.grid(row=8, column=1, sticky=W)
            e1.grid(row=0, column=1, sticky=E)
            e2.grid(row=1, column=1, sticky=E)
            e3.grid(row=2, column=1, sticky=E)
            e4.grid(row=3, column=1, sticky=E)
            e5.grid(row=4, column=1, sticky=E)
            e6.grid(row=6, column=1, sticky=E)
            cancel.grid(row=9, column=0, sticky=(W,E,S,N))
            ok.grid(row=9, column=1, sticky=(W,E,S,N))


            def add_book():
                if e1.get!='' and e2.get()!='' and e3.get()!='' and e4.get()!='' and e5.get()!='':
                    authors  = e1.get().split(',')
                    name     = e2.get()
                    year     = e3.get()
                    pages    = e4.get()
                    quantity = e5.get()
                    price    = e6.get()
                    publisher = var1.get()
                    theme = var2.get()
                    b = book(authors, name, year, pages,theme,price, publisher, quantity)
                    b.commit()
                    app1.destroy()
                else:
                    messagebox.showerror("Помилка",
                                         "Неправильно введені параметри!")
                    print(var2.get())
                    print(var1.get())




app = Tk()
gui = Main_window(app)
app.mainloop()
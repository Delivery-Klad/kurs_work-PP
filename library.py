# coding=utf8
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import tkinter as tk
import database

databaseName = 'dataBase.db'
who = 0
currentUserID = 0
currentTable = 0
root = tk.Tk()
var1 = IntVar()
var2 = IntVar()
var3 = IntVar()

# region tables
frame = ttk.Treeview(root)
frame.place(relx=0.15, rely=0.05, relwidth=0.33, relheight=0.89)
frame2 = ttk.Treeview(root)
frame2.place(relx=0.65, rely=0.05, relwidth=0.33, relheight=0.89)
frame["columns"] = ("ID", "Название", "Автор", "Год издания", "Кол-во")
frame.column("#0", width=0, stretch=tk.NO)
frame.column("ID", width=40, stretch=tk.NO)
frame.column("Название", width=200, stretch=tk.NO)
frame.column("Автор", width=200, stretch=tk.NO)
frame.column("Год издания", width=80, stretch=tk.NO)
frame.column("Кол-во", width=50, stretch=tk.NO)

frame.heading("ID", text="ID", anchor=tk.W)
frame.heading("Название", text="Название", anchor=tk.W)
frame.heading("Автор", text="Автор", anchor=tk.W)
frame.heading("Год издания", text="Год издания", anchor=tk.W)
frame.heading("Кол-во", text="Кол-во", anchor=tk.W)

frame2["columns"] = ("ID", "Название", "Автор", "Год издания", "Идентификатор")
frame2.column("#0", width=0, stretch=tk.NO)
frame2.column("ID", width=40, stretch=tk.NO)
frame2.column("Название", width=200, stretch=tk.NO)
frame2.column("Автор", width=150, stretch=tk.NO)
frame2.column("Год издания", width=80, stretch=tk.NO)
frame2.column("Идентификатор", width=100, stretch=tk.NO)

frame2.heading("ID", text="ID", anchor=tk.W)
frame2.heading("Название", text="Название", anchor=tk.W)
frame2.heading("Автор", text="Автор", anchor=tk.W)
frame2.heading("Год издания", text="Год издания", anchor=tk.W)
frame2.heading("Идентификатор", text="Идентификатор", anchor=tk.W)


# endregion


def fill_LibTable():
    try:
        frame.delete(*frame.get_children())
        books = database.fill_libTable()
        for i in books:
            frame.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def fill_on_hand_table():
    global currentTable
    try:
        currentTable = 0
        button_take.configure(state='normal')
        button_give.configure(state='normal')
        frame2.heading("Идентификатор", text="Идентификатор", anchor=tk.W)
        button_sortCount2.configure(text='Идентификатору')
        frame2.delete(*frame2.get_children())
        books = database.fill_onHandTableLib(currentUserID, who)
        for i in books:
            frame2.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def fill_middle_time():
    global currentTable
    try:
        currentTable = 1
        button_take.configure(state='disabled')
        button_give.configure(state='disabled')
        frame2.heading("Идентификатор", text="Среднее время", anchor=tk.W)
        button_sortCount2.configure(text='Времени')
        frame2.delete(*frame2.get_children())
        books = database.fill_middle()
        for i in books:
            frame2.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def fill_frequency():
    global currentTable
    try:
        currentTable = 2
        button_take.configure(state='disabled')
        button_give.configure(state='disabled')
        frame2.heading("Идентификатор", text="Частота выдачи", anchor=tk.W)
        button_sortCount2.configure(text='Частоте')
        frame2.delete(*frame2.get_children())
        books = database.fill_frequency()
        for i in books:
            frame2.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def sort_frame(byWhat):
    try:
        frame.delete(*frame.get_children())
        books = database.sort1(byWhat)
        for i in books:
            frame.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def sort_frame2(byWhat):
    try:
        frame2.delete(*frame2.get_children())
        books = database.sort2(byWhat, who, currentUserID, currentTable)
        for i in books:
            frame2.insert('', 'end', values=i)
    except Exception as e:
        print(e)


def add_book():
    try:
        if len(entry_id.get()) != 0 and len(entry_title.get()) != 0 and len(entry_author.get()) != 0 and \
                len(entry_year.get()) != 0 and len(entry_count.get()) != 0:
            if not database.check_id(int(entry_id.get())):
                messagebox.showerror("TypeError", "Введенный Id уже существует")
                return
            data = [entry_id.get(), entry_title.get(), entry_author.get(), entry_year.get(), entry_count.get()]
            if not data[0].isdigit():
                messagebox.showerror("TypeError", "Id должен быть указан числом")
                return
            if not data[3].isdigit():
                messagebox.showerror("TypeError", "Год издания должен быть указан числом")
                return
            if not data[4].isdigit():
                messagebox.showerror("TypeError", "Кол-во экземпляров должно быть указано числом")
                return
            frame.insert('', 'end', values=data)
            database.add_to_database(data)
        else:
            messagebox.showerror("InputError", "Все поля должны быть заполнены")
    except Exception as e:
        print(e)


def del_book():
    try:
        i = frame.selection()[0]
        book = frame.item(i).values()
        frame.delete(i)
        book = str(book).split()
        ID = book[2][1:-1]
        database.del_from_database(ID)
    except IndexError:
        messagebox.showerror('error', 'Вы не выбрали книгу')


def replace_book(table):
    try:
        if table == "Library":
            button_take.configure(state='normal')
            button_give.configure(state='normal')
            i = frame.selection()[0]
            book = frame.item(i).values()
            book = str(book).split()
            ID = book[2][1:-1]
            if database.give_book(int(ID), currentUserID) > 1:
                frame.item(i, values=database.get_book(ID))
                frame2.insert('', 'end', values=database.get_book_onHand(ID))
            else:
                frame2.insert('', 'end', values=database.get_book_onHand(ID))
                frame.delete(i)
        elif table == "NotInLibrary":
            i = frame2.selection()[0]
            book = frame2.item(i).values()
            book = str(book).split()
            ID = book[2][1:-1]
            print('ID ' + str(ID))
            takeID = book[len(book) - 3][:-2]
            print('takeID ' + str(takeID))
            database.take_book(ID, takeID)
            database.get_middleTime(ID)
            database.get_frequency(ID)
            frame2.delete(i)
            fill_LibTable()
        else:
            print('Где-то закралась ошибочка')
    except IndexError:
        messagebox.showerror('error', 'Вы не выбрали книгу')


def add_count(count):
    try:
        i = frame.selection()[0]
        book = frame.item(i).values()
        book = str(book).split()
        ID = book[2][1:-1]
        database.add_countBooks(ID, count)
        fill_LibTable()
    except IndexError:
        messagebox.showerror('error', 'Вы не выбрали книгу')


def all_disabled():
    button_middle.configure(state='disabled')
    button_add.configure(state='disabled')
    button_del.configure(state='disabled')
    button_take.configure(state='disabled')
    button_give.configure(state='disabled')
    button_plusOne.configure(state='disabled')
    button_plusTwo.configure(state='disabled')
    button_plusFive.configure(state='disabled')
    button_plusTen.configure(state='disabled')
    button_plusFT.configure(state='disabled')
    button_plusTwenty.configure(state='disabled')
    button_sortID.configure(state='disabled')
    button_sortID2.configure(state='disabled')
    button_sortName.configure(state='disabled')
    button_sortName2.configure(state='disabled')
    button_sortAuthor.configure(state='disabled')
    button_sortAuthor2.configure(state='disabled')
    button_sortYear.configure(state='disabled')
    button_sortYear2.configure(state='disabled')
    button_sortCount.configure(state='disabled')
    button_sortCount2.configure(state='disabled')
    button_frequency.configure(state='disabled')


def login():
    global who
    global currentUserID
    all_disabled()
    if len(entry_userId.get()) != 0 and len(entry_pass.get()) != 0:
        userID = database.check_user(entry_userId.get(), entry_pass.get())
        if userID:
            if userID == "0":
                who = 0
                button_take.configure(state='normal')
                button_give.configure(state='normal')
            elif userID == "1":
                who = 1
                button_middle.configure(state='normal')
                button_add.configure(state='normal')
                button_del.configure(state='normal')
                button_take.configure(state='normal')
                button_give.configure(state='normal')
                button_frequency.configure(state='normal')
                button_onHand.configure(state='normal')
            elif userID == "2":
                who = 2
                button_middle.configure(state='normal')
                button_add.configure(state='normal')
                button_del.configure(state='normal')
                button_take.configure(state='normal')
                button_give.configure(state='normal')
                button_plusOne.configure(state='normal')
                button_plusTwo.configure(state='normal')
                button_plusFive.configure(state='normal')
                button_plusTen.configure(state='normal')
                button_plusFT.configure(state='normal')
                button_plusTwenty.configure(state='normal')
                button_frequency.configure(state='normal')
                button_onHand.configure(state='normal')
        else:
            messagebox.showerror('error', 'Пользователь не найден')
    var1.set(0)
    var2.set(0)
    var3.set(0)
    if len(entry_userId.get()) != 0:
        currentUserID = entry_userId.get()
    fill_on_hand_table()
    entry_userId.delete(0, 'end')
    entry_pass.delete(0, 'end')
    button_sortID.configure(state='normal')
    button_sortID2.configure(state='normal')
    button_sortName.configure(state='normal')
    button_sortName2.configure(state='normal')
    button_sortAuthor.configure(state='normal')
    button_sortAuthor2.configure(state='normal')
    button_sortYear.configure(state='normal')
    button_sortYear2.configure(state='normal')
    button_sortCount.configure(state='normal')
    button_sortCount2.configure(state='normal')
    button_exit.configure(state='normal')
    button_enter.configure(state='disabled')
    button_reg.configure(state='disabled')


def reg():
    if len(entry_userId.get()) != 0 and len(entry_pass.get()) != 0:
        if var1.get() == 1 and var2.get() == 0 and var3.get() == 0:
            if database.reg_user(entry_userId.get(), entry_pass.get(), "0"):
                messagebox.showinfo('Успех', 'Регистрация прошла успешно')
                login()
            else:
                messagebox.showerror('error', 'Введенный логин уже существует')
        elif var1.get() == 0 and var2.get() == 1 and var3.get() == 0:
            if database.reg_user(entry_userId.get(), entry_pass.get(), "1"):
                messagebox.showinfo('Успех', 'Регистрация прошла успешно')
                login()
            else:
                messagebox.showerror('error', 'Введенный логин уже существует')
        elif var1.get() == 0 and var2.get() == 0 and var3.get() == 1:
            if database.reg_user(entry_userId.get(), entry_pass.get(), "2"):
                messagebox.showinfo('Успех', 'Регистрация прошла успешно')
                login()
            else:
                messagebox.showerror('error', 'Введенный логин уже существует')
        else:
            messagebox.showerror('error', 'Необходимо выбрать один из типов пользователей')
    else:
        messagebox.showerror('error', 'Необходимо указать логин и пароль для регистрации')


def Exit():
    global who
    global currentUserID
    who = 0
    currentUserID = 0
    all_disabled()
    button_enter.configure(state='normal')
    button_reg.configure(state='normal')


fill_LibTable()
# region UI создание графического интерфейса
button_add = tk.Button(root, text="Добавить", bg='#BDBDBD', command=lambda: add_book(), state='disabled')
button_add.place(relx=0.045, rely=0.40, relwidth=0.1, relheight=0.05)
button_del = tk.Button(root, text="Удалить", bg='#BDBDBD', command=lambda: del_book(), state='disabled')
button_del.place(relx=0.045, rely=0.46, relwidth=0.1, relheight=0.05)
button_give = tk.Button(root, text="->Взять книгу->", bg='#BDBDBD', command=lambda: replace_book("Library"),
                        state='disabled')
button_give.place(relx=0.52, rely=0.05, relwidth=0.1, relheight=0.05)
button_take = tk.Button(root, text="<-Вернуть книгу<-", bg='#BDBDBD', command=lambda: replace_book("NotInLibrary"),
                        state='disabled')
button_take.place(relx=0.52, rely=0.11, relwidth=0.1, relheight=0.05)
button_middle = tk.Button(root, text="Среднее время на руках", bg='#BDBDBD', command=lambda: fill_middle_time(),
                          state='disabled')
button_middle.place(relx=0.52, rely=0.32, relwidth=0.1, relheight=0.05)
button_frequency = tk.Button(root, text="Частота выдачи", bg='#BDBDBD', command=lambda: fill_frequency(),
                             state='disabled')
button_frequency.place(relx=0.52, rely=0.38, relwidth=0.1, relheight=0.05)
button_onHand = tk.Button(root, text="Список книг на руках", bg='#BDBDBD', command=lambda: fill_on_hand_table(),
                          state='disabled')
button_onHand.place(relx=0.52, rely=0.44, relwidth=0.1, relheight=0.05)
button_sortID = tk.Button(root, text="ID", bg='#BDBDBD', command=lambda: sort_frame("ID"), state='disabled')
button_sortID.place(relx=0.22, rely=0.945, relwidth=0.03, relheight=0.05)
button_sortName = tk.Button(root, text="Названию", bg='#BDBDBD', command=lambda: sort_frame("Name"), state='disabled')
button_sortName.place(relx=0.255, rely=0.945, relwidth=0.05, relheight=0.05)
button_sortAuthor = tk.Button(root, text="Автору", bg='#BDBDBD', command=lambda: sort_frame("Author"), state='disabled')
button_sortAuthor.place(relx=0.31, rely=0.945, relwidth=0.05, relheight=0.05)
button_sortYear = tk.Button(root, text="Году", bg='#BDBDBD', command=lambda: sort_frame("Year"), state='disabled')
button_sortYear.place(relx=0.365, rely=0.945, relwidth=0.05, relheight=0.05)
button_sortCount = tk.Button(root, text="Количеству", bg='#BDBDBD', command=lambda: sort_frame("Count"),
                             state='disabled')
button_sortCount.place(relx=0.42, rely=0.945, relwidth=0.05, relheight=0.05)
button_sortID2 = tk.Button(root, text="ID", bg='#BDBDBD', command=lambda: sort_frame2("ID"), state='disabled')
button_sortID2.place(relx=0.72, rely=0.945, relwidth=0.03, relheight=0.05)
button_sortName2 = tk.Button(root, text="Названию", bg='#BDBDBD', command=lambda: sort_frame2("Name"), state='disabled')
button_sortName2.place(relx=0.755, rely=0.945, relwidth=0.05, relheight=0.05)
button_sortAuthor2 = tk.Button(root, text="Автору", bg='#BDBDBD', command=lambda: sort_frame2("Author"),
                               state='disabled')
button_sortAuthor2.place(relx=0.81, rely=0.945, relwidth=0.05, relheight=0.05)
button_sortYear2 = tk.Button(root, text="Году", bg='#BDBDBD', command=lambda: sort_frame2("Year"), state='disabled')
button_sortYear2.place(relx=0.865, rely=0.945, relwidth=0.05, relheight=0.05)
button_sortCount2 = tk.Button(root, text="Идентификатору", bg='#BDBDBD', command=lambda: sort_frame2("takeID"),
                              state='disabled')
button_sortCount2.place(relx=0.92, rely=0.945, relwidth=0.06, relheight=0.05)
button_plusOne = tk.Button(root, text="+1", bg='#BDBDBD', command=lambda: add_count(1), state='disabled')
button_plusOne.place(relx=0.52, rely=0.6, relwidth=0.03, relheight=0.05)
button_plusTwo = tk.Button(root, text="+2", bg='#BDBDBD', command=lambda: add_count(2), state='disabled')
button_plusTwo.place(relx=0.555, rely=0.6, relwidth=0.03, relheight=0.05)
button_plusFive = tk.Button(root, text="+5", bg='#BDBDBD', command=lambda: add_count(5), state='disabled')
button_plusFive.place(relx=0.59, rely=0.6, relwidth=0.03, relheight=0.05)
button_plusTen = tk.Button(root, text="+10", bg='#BDBDBD', command=lambda: add_count(10), state='disabled')
button_plusTen.place(relx=0.52, rely=0.665, relwidth=0.03, relheight=0.05)
button_plusFT = tk.Button(root, text="+15", bg='#BDBDBD', command=lambda: add_count(15), state='disabled')
button_plusFT.place(relx=0.555, rely=0.665, relwidth=0.03, relheight=0.05)
button_plusTwenty = tk.Button(root, text="+20", bg='#BDBDBD', command=lambda: add_count(20), state='disabled')
button_plusTwenty.place(relx=0.59, rely=0.665, relwidth=0.03, relheight=0.05)
button_enter = tk.Button(root, text="Вход", bg='#BDBDBD', command=lambda: login())
button_enter.place(relx=0.08, rely=0.85, relwidth=0.05, relheight=0.05)
button_reg = tk.Button(root, text="Регистрация", bg='#BDBDBD', command=lambda: reg())
button_reg.place(relx=0.025, rely=0.85, relwidth=0.05, relheight=0.05)
button_exit = tk.Button(root, text="Выход", bg='#BDBDBD', command=lambda: Exit(), state='disabled')
button_exit.place(relx=0.025, rely=0.915, relwidth=0.105, relheight=0.05)

entry_id = tk.Entry(root, font=12)
entry_id.place(relx=0.045, rely=0.05, relwidth=0.1, relheight=0.05)
entry_userId = tk.Entry(root, font=12)
entry_userId.place(relx=0.025, rely=0.6, relwidth=0.1, relheight=0.05)
entry_pass = tk.Entry(root, font=12)
entry_pass.place(relx=0.025, rely=0.66, relwidth=0.1, relheight=0.05)
entry_title = tk.Entry(root, font=12)
entry_title.place(relx=0.045, rely=0.12, relwidth=0.1, relheight=0.05)
entry_author = tk.Entry(root, font=12)
entry_author.place(relx=0.045, rely=0.19, relwidth=0.1, relheight=0.05)
entry_year = tk.Entry(root, font=12)
entry_year.place(relx=0.045, rely=0.26, relwidth=0.1, relheight=0.05)
entry_count = tk.Entry(root, font=12)
entry_count.place(relx=0.045, rely=0.33, relwidth=0.1, relheight=0.05)

label_id = tk.Label(root, font=12, text="Id:", fg='black')
label_id.place(relx=0.023, rely=0.05)
label_title = tk.Label(root, font=12, text="Назв:", fg='black')
label_title.place(relx=0.01, rely=0.12)
label_author = tk.Label(root, font=12, text="Автор:", fg='black')
label_author.place(relx=0.005, rely=0.19)
label_year = tk.Label(root, font=12, text="Год:", fg='black')
label_year.place(relx=0.015, rely=0.26)
label_count = tk.Label(root, font=12, text="Кол-во:", fg='black')
label_count.place(relx=0.005, rely=0.33)
label_sort = tk.Label(root, font=12, text="Сортировка по:", fg='black')
label_sort.place(relx=0.148, rely=0.945)
label_sort2 = tk.Label(root, font=12, text="Сортировка по:", fg='black')
label_sort2.place(relx=0.647, rely=0.945)
label_fill = tk.Label(root, font=12, text="Пополнение", fg='black')
label_fill.place(relx=0.52, rely=0.55, relwidth=0.1, relheight=0.05)
label_func = tk.Label(root, font=12, text="Формирование отчетов", fg='black')
label_func.place(relx=0.52, rely=0.27, relwidth=0.1, relheight=0.05)
label_func = tk.Label(root, font=12, text="Тип пользователя", fg='black')
label_func.place(relx=0.036, rely=0.55)

user = Checkbutton(root, font=12, text="Пользователь", fg='black', variable=var1)
user.place(relx=0.011, rely=0.72, relwidth=0.1, relheight=0.05)
lib_worker = Checkbutton(root, font=12, text="Библиотекарь", fg='black', variable=var2)
lib_worker.place(relx=0.01, rely=0.76, relwidth=0.1, relheight=0.05)
admin = Checkbutton(root, font=12, text="Админ", fg='black', variable=var3)
admin.place(relx=0.0195, rely=0.8, relwidth=0.05, relheight=0.05)
# endregion
if __name__ == "__main__":
    root.title("Библиотека")
    root.geometry("1750x500")
    root.resizable(False, False)
    root.mainloop()

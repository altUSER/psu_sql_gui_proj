from main import main
import os

from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showerror

DB_PATH = ''

root = Tk()
root.title('Подключение к БД')
root.geometry('250x200')

def update_label():
    global DB_PATH
    db_path_label.config(text=DB_PATH)

def open_db():
    global DB_PATH
    db_path = filedialog.askopenfilename(filetypes=[('sqlite', '*.sqlite')])
    DB_PATH = db_path
    update_label()

def start():
    global DB_PATH
    main(DB_PATH)
    root.destroy()


db_path_label = ttk.Label()
db_path_label.grid(row=0, column=0, columnspan=2)

db_open_btn = Button(text='Открыть БД', command=open_db)
db_open_btn.grid(row=1, column=0)

db_create_btn = Button(text='Создать БД')
db_create_btn.grid(row=1, column=1)

start_btn = Button(text='НАчать работу', command=start)
start_btn.grid(row=2, column=0, columnspan=2)

root.mainloop()
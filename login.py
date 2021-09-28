from tkinter import *
import sqlite3
import subprocess

root=Tk()

def run_game():
    root.destroy()
    subprocess.call(["python","game.py"])

def run_login():
    root.destroy()
    subprocess.call(["python","login.py"])

def login_username():
    conn = sqlite3.connect('login.db')
    c = conn.cursor()

    c.execute('SELECT 1 FROM register_table WHERE username = ? AND password = ?', (u_name.get(), password.get()))



    user = c.fetchone()

    if user >0:

        run_game()



    else:
        run_login()


u_name_label = Label(root, text='User Name')
u_name_label.grid(row=0, column=0)
password_label = Label(root, text='Password')
password_label.grid(row=4, column=0)


u_name = Entry(root, width=30)
u_name.grid(row=0, column=1, padx=20)
password=Entry(root, width=30)
password.grid(row=4, column=1)

insert_btn = Button(root, text="Register", command=login_username)
insert_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

root.mainloop()
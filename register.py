from tkinter import *
import sqlite3
import subprocess

root=Tk()
root.title('register')


def run_login():
    root.destroy()
    subprocess.call(["python","login.py"])

conn=sqlite3.connect("login.db")
c=conn.cursor()

# c.execute(""" CREATE TABLE register_table (
#     user_name String,
#     first_name String,
#     last_name String,
#     password String
#
#     )""")


conn.commit()
conn.close()

def register_username():
    conn = sqlite3.connect('login.db')

    c = conn.cursor()


    c.execute("INSERT INTO register_table VALUES(:user_name,  :first_name, :last_name, :password)",
              {

                  "user_name": u_name.get(),
                  "first_name": f_name.get(),
                  "last_name": l_name.get(),
                  "password": password.get(),
              }
              )


    run_login()

    conn.commit()
    conn.close()

u_name = Entry(root, width=30)
u_name.grid(row=0, column=1, padx=20)

f_name = Entry(root, width=30)
f_name.grid(row=1, column=1)

l_name = Entry(root, width=30)
l_name.grid(row=2, column=1)



password=Entry(root, width=30)
password.grid(row=4, column=1)

u_name_label = Label(root, text='User Name')
u_name_label.grid(row=0, column=0)

f_name_label = Label(root, text='First Name')
f_name_label.grid(row=1, column=0)

l_name_label = Label(root,text='Last Name')
l_name_label.grid(row=2, column=0)


password_label = Label(root, text='Password')
password_label.grid(row=4, column=0)

insert_btn = Button(root, text="Register", command=register_username)
insert_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)



root.mainloop()
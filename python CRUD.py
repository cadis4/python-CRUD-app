from tkinter import Tk, Button, Label, Scrollbar, Listbox, StringVar, Entry, W, E, N, S, END
from tkinter import ttk
from tkinter import messagebox
import pypyodbc as pyo
from sqlserver_config import dbConfig

#define cursor obj
con = pyo.connect(**dbConfig)
cursor = con.cursor()

class Bookdb: 
    def __init__(self):
        self.con = pyo.connect(**dbConfig)
        self.cursor = self.con.cursor()
        print("You have connected to the db")
        print(self.con)
        
    #destructor
    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return rows
      
    def insert(self, title, author, cod):
        sql = "INSERT INTO books(title, author, cod) VALUES (?, ?, ?)"
        values = [title, author, cod]
        self.cursor.execute(sql, values)
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="New book added to the database")

    def update(self, id, title, author, cod):
        tsql = 'UPDATE books SET title = ?, author = ?, cod = ? WHERE id = ?'
        self.cursor.execute(tsql, [title, author, cod, id])
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="Book updated")

    def delete(self, id):
        delquery = 'DELETE FROM books WHERE id = ?'
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="Book Database", message="Book deleted")

db = Bookdb()

def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)
    title_entry.delete(0, 'end')
    title_entry.insert('end', selected_tuple[1]) 
    author_entry.delete(0, 'end')
    author_entry.insert('end', selected_tuple[2])
    cod_entry.delete(0, 'end')
    cod_entry.insert('end', selected_tuple[3])

def view_records():
    list_bx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)

def add_book():
    db.insert(title_text.get(), author_text.get(), cod_text.get())
    list_bx.delete(0, 'end')
    list_bx.insert('end', (title_text.get(), author_text.get(), cod_text.get()))
    title_entry.delete(0, "end")
    author_entry.delete(0, "end")
    cod_entry.delete(0, "end")

def delete_records():
    db.delete(selected_tuple[0])

def clear_screen():
    list_bx.delete(0, 'end')
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    cod_entry.delete(0, 'end')

def update_records():
    db.update(selected_tuple[0], title_text.get(), author_text.get(), cod_text.get())
    title_entry.delete(0, 'end')
    author_entry.delete(0, 'end')
    cod_entry.delete(0, 'end')

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

#define app window 
root = Tk() 
root.title("Book App")
root.configure(background="light blue")
root.geometry("850x500")
root.resizable(width=False, height=False)

# create labels
title_table = ttk.Label(root, text="Book:", background="light blue", font=("TkDefaultFont", 16))
title_table.grid(row=0, column=0, sticky=W)
title_text = StringVar()
title_entry = ttk.Entry(root, width=24, textvariable=title_text)
title_entry.grid(row=0, column=1, sticky=W)

author_table = ttk.Label(root, text="Author:", background="light blue", font=("TkDefaultFont", 16))
author_table.grid(row=0, column=2, sticky=W)
author_text = StringVar()
author_entry = ttk.Entry(root, width=24, textvariable=author_text)
author_entry.grid(row=0, column=3, sticky=W)

cod_table = ttk.Label(root, text="Code:", background="light blue", font=("TkDefaultFont", 16))
cod_table.grid(row=0, column=4, sticky=W)
cod_text = StringVar()
cod_entry = ttk.Entry(root, width=24, textvariable=cod_text)
cod_entry.grid(row=0, column=5, sticky=W)

#create buttons 
add_bttn = Button(root, text="Add book", bg="black", fg="white", font="helvetica 10 bold", command=add_book)
add_bttn.grid(row=0, column=6, sticky=W)

list_bx = Listbox(root, height=16, width=40, font="helvetica 13", bg="white")
list_bx.grid(row=3, column=1, columnspan=14, sticky=W + E, pady=40, padx=15)
list_bx.bind('<<ListboxSelect>>', get_selected_row)

scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1, column=8, rowspan=14, sticky=W)

list_bx.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=list_bx.yview)

modify_bttn = Button(root, text="Modify record", bg="black", fg="white", font="helvetica 10 bold", command=update_records)
modify_bttn.grid(row=15, column=4)

delete_bttn = Button(root, text="Delete record", bg="black", fg="white", font="helvetica 10 bold", command=delete_records)
delete_bttn.grid(row=15, column=5)

view_bttn = Button(root, text="View record", bg="black", fg="white", font="helvetica 10 bold", command=view_records)
view_bttn.grid(row=15, column=1)

clear_bttn = Button(root, text="Clear record", bg="black", fg="white", font="helvetica 10 bold", command=clear_screen)
clear_bttn.grid(row=15, column=2)

exit_bttn = Button(root, text="Exit record", bg="black", fg="white", font="helvetica 10 bold", command=root.destroy)
exit_bttn.grid(row=15, column=3)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

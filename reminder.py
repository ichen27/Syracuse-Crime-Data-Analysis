from tkinter import *
import sqlite3

root = Tk()
root.title('Reminders App')
root.geometry("400x600")

conn = sqlite3.connect('reminders.db')
c = conn.cursor()


'''
c.execute("""CREATE TABLE reminders (
    item text
    )""")
'''

#add to database
#refresh the screen
def submit():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()

    c.execute("INSERT INTO reminders VALUES (:item1)",
    {
        'item1': item.get()
    })

    conn.commit()
    conn.close()

    item.delete(0, END)
    printout()

def printout():
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 1:
            widget.destroy()

    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM reminders WHERE item IS NOT NULL AND item != ''")
    records = c.fetchall()


    count = 2
    print(records)

    for record in records:

        checkbox = Button(root,text="check",command=lambda id=record[1]: button_click(id))
        checkbox.grid(row=count, column=0, sticky='w', padx=(15,0))
        reminderText = Label(root, text=record[0])
        reminderText.grid(row=count, column=0, sticky='w', padx=(90,0))
        count += 1

    conn.commit()
    conn.close()

#detect what button is click,
def button_click(button_id):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    print(button_id)
    c.execute("DELETE from reminders WHERE oid=" + str(button_id))

    conn.commit()
    conn.close()


    printout()


title = Label(root, text="To Do List", font=("Arial", 20))
title.grid(row=0, column=0)

item = Entry(root, width=30,)
item.grid(row=1, column=0, columnspan=2, padx=(15,0), pady=(15,0))

add = Button(root, text="+", command=submit)
add.grid(row=1, column=4,pady=(15,0))
printout()


conn.commit()
conn.close()


root.mainloop()
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
import sqlite3

mainicon = os.getcwd() +  "\\mainicon.ico"

def convertDataToList(data, list):
    for i in data:
        list.append(i[0])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def openDoctorWindow(combo, dData, dList):
    g = Toplevel()
    g.attributes('-topmost', 'true')
    g.geometry("400x400+700+100")
    g.resizable(False,False)
    g.iconbitmap(mainicon)
    g.lift()
    g.grab_set()
    emptyLabel = Label(g, text='')
    doctorvar = StringVar()
    doctorEntry = Entry(g, width=23,font=("tajawal", 14), textvariable=doctorvar)
    addDoctorBtn = ttk.Combobox(g, width=9,font=("tajawal", 14))
    addDoctorBtn = Button(g, text='Add doctor', width=10, bg='light green')
    drtv = ttk.Treeview(g, height=20)
    drtv['columns'] = ('doctors')
    drtv.column("#0", width=0, anchor=CENTER, stretch=NO)
    drtv.column("#1", width=350, minwidth=25, anchor=CENTER)
    drtv.heading("#1", text='doctors')
    emptyLabel.pack(pady=10)
    doctorEntry.place(x=24, y=30)
    addDoctorBtn.place(x=295, y=30)
    drtv.pack(pady=30)

    def addDoctor(event=None):
        con = sqlite3.connect("proj1.db")
        c = con.cursor()
        records = c.execute("SELECT * FROM doctors").fetchall()
        fetchedDoctors = []
        convertDataToList(records, fetchedDoctors)
        if doctorEntry.get() == "":
            messagebox.showinfo("Warning", "Doctor input cant be empty", parent=g)
            return
        if doctorEntry.get() in fetchedDoctors:
            messagebox.showinfo("Warning", "Doctor already exists", parent=g)
            return
        if has_numbers(doctorEntry.get()) == True:
            messagebox.showinfo("Warning", "Doctor name cant have numbers", parent=g)
            return
        if doctorEntry.get() != "" and doctorEntry.get() not in fetchedDoctors:
            c.execute("INSERT into doctors(doctor)Values(?)",(doctorEntry.get(),))
            doctorEntry.delete(0, END)
        con.commit()
        refreshDoctors()
        con.close()

    def refreshDoctors():
        for item in drtv.get_children():
            drtv.delete(item)
        placeDoctors()

    def placeDoctors():
        con = sqlite3.connect('proj1.db')
        c = con.cursor()
        records = c.execute("SELECT * FROM doctors").fetchall()
        rowId = c.execute("SELECT rowid FROM doctors").fetchall()
        fetchedrowId = []
        convertDataToList(rowId, fetchedrowId)
        con.commit()
        con.close()
        count = 0
        for record in records:
            if count % 2 == 0:
                drtv.insert(parent='', index='end', iid=count, text=fetchedrowId[count], values=(record), tags=('evenrow',))
            else:
                drtv.insert(parent='', index='end', iid=count, text=fetchedrowId[count], values=(record), tags=('oddrow',))
            count += 1

    def deleteDoctor(event=None):
        try:
            con = sqlite3.connect('proj1.db')
            c = con.cursor()
            ds = drtv.item(drtv.selection())['text']
            c.execute("DELETE FROM doctors WHERE rowid =?", (ds,)).fetchall()
            con.commit()
            con.close()        
            refreshDoctors()
        except:
            return

    def refreshCombo():
        conn = sqlite3.connect("proj1.db")
        cur = conn.cursor()
        select = cur.execute("SELECT * FROM doctors")
        dData = select.fetchall()
        dList = []
        convertDataToList(dData, dList)
        conn.close()
        combo['completevalues'] = dList
        g.destroy()

    placeDoctors()
    g.bind("<BackSpace>", deleteDoctor)
    g.bind("<Delete>", deleteDoctor)
    drtv.bind("<Double-Button-1>", deleteDoctor)
    g.bind("<Return>", addDoctor)
    addDoctorBtn.config(command=addDoctor)
    g.protocol('WM_DELETE_WINDOW', refreshCombo)
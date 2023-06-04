import os
import sqlite3
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox

def convertDataToList(data, list):
    for i in data:
        list.append(i[0])


mainicon = os.getcwd() +  "\\mainicon.ico"

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def openEditWin(dcombo):
    win = Toplevel()
    win.geometry("935x500")
    win.resizable(False, False)
    win.iconbitmap(mainicon)
    win.title("Edit saved drugs")
    win.grab_set()
    win.lift()
    label = Label(win, text='Edit drug data', font=('tajawal', 15), justify=CENTER)
    drugLabel = Label(win, text='Drug name:', justify=CENTER)
    typeLabel = Label(win, text='Drug type:', justify=CENTER)
    doseLabel = Label(win, text='Dose:', justify=CENTER)
    useLabel = Label(win, text='Use:', justify=CENTER)
    priceLabel = Label(win, text='Price:', justify=CENTER)
    addDrugBtn = Button(win, text='Add drug', width=10, bg='light green')

    # cboDrg = AutocompleteCombobox(win, width=22, font=("tajawal", 14), completevalues=drugList, textvariable=cbo)

    typeCombolst = ['Tablet', 'Capsule', 'Syrup', 'Ointment', 'Drops']
    doseCombolst = ['5 mg', '10 mg', '50 mg', '100 mg', '250 mg', '500 mg', '1000 mg']
    useCombolst = ['1 x 1', '1 x 2', '1 x 3', '2 x 2', '2 x 3']

    cboDrg = Entry(win, width=21, font=("tajawal", 16), highlightbackground='grey', highlightthickness=1, border=0)
    typeCombo = AutocompleteCombobox(win, width=9,font=("tajawal", 14), completevalues=typeCombolst)
    doseCombo = AutocompleteCombobox(win, width=9,font=("tajawal", 14), completevalues=doseCombolst)
    useCombo = AutocompleteCombobox(win, width=9,font=("tajawal", 14), completevalues=useCombolst)
    priceEntry = Entry(win, width=8,font=("tajawal", 14), highlightbackground='grey', highlightthickness=1, border=0)

    IQDLabel = Label(win, text='IQD', font=("tajawal", 10))

    prtv = ttk.Treeview(win, height=16)
    prtv['columns'] = ('ID', 'Drug', 'Type', 'Dose', 'Use', 'Price')
    prtv.column("#0", width=0, stretch=NO)
    prtv.column("#1", width=12, minwidth=25,  anchor=CENTER)
    prtv.column("#2", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#3", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#4", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#5", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#6", width=169, minwidth=25, anchor=CENTER)

    prtv.heading("#1", text='id')
    prtv.heading("#2", text='Drug')
    prtv.heading("#3", text='Type')
    prtv.heading("#4", text='Dose')
    prtv.heading("#5", text='Use')
    prtv.heading("#6", text='Price')
    # label.pack(pady=20)
    label.place        (x=421, y=14)
    drugLabel.place    (x=40 , y=59)
    cboDrg.place       (x=40 , y=82)
    typeLabel.place    (x=301, y=59)
    typeCombo.place    (x=301, y=82)
    doseLabel.place    (x=428, y=59)
    doseCombo.place    (x=428, y=82)
    useLabel.place     (x=555, y=59)
    useCombo.place     (x=555, y=82)
    priceLabel.place   (x=682, y=59)
    priceEntry.place   (x=682, y=82)
    IQDLabel.place     (x=778, y=84)
    addDrugBtn.place   (x=818, y=81)
    prtv.place         (x=39 , y=120)
    prtv.tag_configure('oddrow', background='light grey')
    prtv.tag_configure('evenrow', background='#f0f0f0')

    def clearDrugEntrys():
        cboDrg.delete(0, END)
        doseCombo.delete(0, END)
        typeCombo.delete(0, END)
        useCombo.delete(0, END)
        priceEntry.delete(0, END)

    def refreshDrugs():
        for item in prtv.get_children():
            prtv.delete(item)
        placeDrugs()

    def addDrug():
        con = sqlite3.connect("proj1.db")
        c = con.cursor()
        drgs = c.execute("SELECT drug FROM drugs").fetchall()
        fetchedrgs = []
        convertDataToList(drgs, fetchedrgs)
        for i in range(len(fetchedrgs)):
            fetchedrgs[i] = fetchedrgs[i].upper()

        if cboDrg.get() == "":
            messagebox.showerror("Error", "Drug name cant be empty", parent=win)
            return
        if typeCombo.get() == "":
            messagebox.showerror("Error", "Drug type cant be empty", parent=win)
            return
        if doseCombo.get() == "":
            messagebox.showerror("Error", "Drug dose cant be empty", parent=win)
            return
        if useCombo.get() == "":
            messagebox.showerror("Error", "Drug use cant be empty", parent=win)
            return
        if has_numbers(priceEntry.get()) == False:
            messagebox.showerror("Error", "Drug price must be a number", parent=win)
            return
        if cboDrg.get().upper() in fetchedrgs:
            ask = messagebox.askyesno("Warning", "this name already exists, do you want to add another one?", parent=win)
            if ask == 0:
                return
            if ask == 1:
                con = sqlite3.connect("proj1.db")
                c = con.cursor()
                c.execute("INSERT into drugs(drug, type, dose, use, price)Values(?,?,?,?,?)",(cboDrg.get().capitalize(), typeCombo.get(), doseCombo.get(), useCombo.get(), priceEntry.get()))
                con.commit()
                con.close()
                clearDrugEntrys()
        else:
            con = sqlite3.connect("proj1.db")
            c = con.cursor()
            c.execute("INSERT into drugs(drug, type, dose, use, price)Values(?,?,?,?,?)",(cboDrg.get().capitalize(), typeCombo.get(), doseCombo.get(), useCombo.get(), priceEntry.get()))
            con.commit()
            con.close()
            clearDrugEntrys()


    def placeDrugs():
        con = sqlite3.connect('proj1.db')
        c = con.cursor()
        records = c.execute("SELECT * FROM drugs").fetchall()
        rowId = c.execute("SELECT rowid FROM drugs").fetchall()
        fetchedRowId = []
        convertDataToList(rowId, fetchedRowId)
        count = 0
        for record in records:
            if count % 2 == 0:
                prtv.insert(parent='', index='end', iid=count, text=fetchedRowId[count], values=(count+1, record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                prtv.insert(parent='', index='end', iid=count, text=fetchedRowId[count], values=(count+1, record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            # increment counter
            count += 1
        con.commit()
        con.close()
    placeDrugs()


    def deleteRecord(e):
        try:
            ds = prtv.item(prtv.selection())['text']
            con = sqlite3.connect('proj1.db')
            c = con.cursor()
            c.execute("DELETE FROM drugs WHERE rowid =?", (ds,))
            con.commit()
            con.close()
            refreshDrugs()
        except:
            return

    def deselect(e):
        if len(prtv.selection()) > 0:
            prtv.selection_remove(prtv.selection()[0])

    def handle_click(event):
        if prtv.identify_region(event.x, event.y) == "separator":
            return "break"

    def refreshList():
        con = sqlite3.connect('proj1.db')
        c = con.cursor()
        drugData = c.execute("SELECT * FROM drugs").fetchall()
        drugList = []
        convertDataToList(drugData, drugList)
        con.close()
        dcombo['completevalues'] = drugList
        win.destroy()
        
    win.bind("<BackSpace>", deleteRecord)
    win.bind("<Delete>", deleteRecord)
    prtv.bind('<Button-1>', handle_click)
    win.bind("<Escape>", deselect)
    win.bind("<Return>", lambda e:[addDrug(), refreshDrugs()])
    addDrugBtn.config(command=lambda:[addDrug(), refreshDrugs()])
    win.protocol("WM_DELETE_WINDOW", refreshList)
    win.mainloop()
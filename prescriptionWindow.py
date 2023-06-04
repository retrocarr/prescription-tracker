from tkinter import Toplevel, Label, Button, CENTER, StringVar, END, Entry, NO
from fpdf import FPDF
import os
from tkinter import ttk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from drugedit import openEditWin
import sqlite3

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def convertDataToList(data, list):
    for n in data:
        list.append(n[0])

mainicon = os.getcwd() +  "\\mainicon.ico"

def openPresWindow(TREEVIEW, TREEVIEW2):
    for line in TREEVIEW.selection():
        x = TREEVIEW.item(line)['values'][0]

    for line in TREEVIEW2.selection():
        H = TREEVIEW2.item(line)['values'][0]

    for line in TREEVIEW2.selection():
        visitDate = TREEVIEW2.item(line)['values'][2]

    conn = sqlite3.connect("proj1.db")
    c = conn.cursor()
    c.execute("SELECT * FROM patientList WHERE ID =?", (x,))
    name = c.fetchall()
    J = c.execute("SELECT * FROM visits").fetchall()
    conn.commit()
    drugWin = Toplevel()
    drugWin.iconbitmap(mainicon)
    drugWin.geometry("940x500+100+50")
    drugWin.resizable(False, False)
    drugWin.grab_set()
    drugWin.lift()
    label = Label(drugWin, text=name[0][1].strip() + " " + visitDate, font=('tajawal', 15), justify=CENTER)
    drugWin.title(name[0][1].strip() + " " + visitDate)
    editDrugs = Button(drugWin, text='Edit drugs', bg='light grey', font=('tajawal', 7))
    drugLabel = Label(drugWin, text='Drug name:', justify=CENTER)
    typeLabel = Label(drugWin, text='Drug type:', justify=CENTER)
    doseLabel = Label(drugWin, text='Dose:', justify=CENTER)
    useLabel = Label(drugWin, text='Use:', justify=CENTER)
    priceLabel = Label(drugWin, text='Price:', justify=CENTER)
    addDrugBtn = Button(drugWin, text='Add drug', width=10, bg='light green')
    printVisitBtn = Button(drugWin, text='Print visit', bg='#97e8e7', width=10)
    drugData = c.execute("SELECT * FROM drugs").fetchall()
    drugList = []
    convertDataToList(drugData, drugList)
    cbo = StringVar()
    def data(cbo):
        placeDrugData()
    cbo.trace("w", lambda name, index, mode, cbo=cbo: data(cbo))


    cboDrg = AutocompleteCombobox(drugWin, width=22, font=("tajawal", 14), completevalues=drugList, textvariable=cbo)

    typeCombolst = ['Tablet', 'Capsule', 'Syrup', 'Ointment', 'Drops']
    typeCombo = AutocompleteCombobox(drugWin, width=9,font=("tajawal", 14), completevalues=typeCombolst)

    doseCombo = AutocompleteCombobox(drugWin, width=9,font=("tajawal", 14))
    doseCombo['values'] = ['5 mg', '10 mg', '50 mg', '100 mg', '250 mg', '500 mg', '1000 mg']

    useCombolst = ['1/2 x 1', '1 x 1', '1 x 2', '1 x 3', '2 x 2', '2 x 3']
    useCombo = AutocompleteCombobox(drugWin, width=9,font=("tajawal", 14), completevalues=useCombolst)

    priceEntry = Entry(drugWin, width=8,font=("tajawal", 14), highlightbackground='grey', highlightcolor='grey', highlightthickness=1)
    IQDLabel = Label(drugWin, text='IQD', font=("tajawal", 10))

    prtv = ttk.Treeview(drugWin, height=16)
    prtv['columns'] = ('ID', 'Drug', 'Type', 'Dose', 'Use', 'Price', 'rowid')
    prtv.column("#0", width=0, stretch=NO)
    prtv.column("#1", width=12, minwidth=25,  anchor=CENTER)
    prtv.column("#2", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#3", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#4", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#5", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#6", width=169, minwidth=25, anchor=CENTER)
    prtv.column("#7", width=0, anchor=CENTER, stretch=NO)

    prtv.heading("#1", text='id')
    prtv.heading("#2", text='Drug')
    prtv.heading("#3", text='Type')
    prtv.heading("#4", text='Dose')
    prtv.heading("#5", text='Use')
    prtv.heading("#6", text='Price')
    prtv.heading("#7", text='')
    label.pack(pady=20)
    # label.place        (x=350, y=14)
    drugLabel.place    (x=40 , y=59)
    editDrugs.place    (x=40 , y=35)
    cboDrg.place       (x=40 , y=82)
    typeLabel.place    (x=310, y=59)
    typeCombo.place    (x=310, y=82)
    doseLabel.place    (x=437, y=59)
    doseCombo.place    (x=437, y=82)
    useLabel.place     (x=564, y=59)
    useCombo.place     (x=564, y=82)
    priceLabel.place   (x=691, y=59)
    priceEntry.place   (x=691, y=82)
    IQDLabel.place     (x=787, y=84)
    addDrugBtn.place   (x=819, y=81)
    printVisitBtn.place(x=819, y=50)
    prtv.place         (x=40 , y=120)

    prtv.tag_configure('oddrow', background='light grey')
    prtv.tag_configure('evenrow', background='#f0f0f0')

    def addDrug():
        if cboDrg.get() == "":
            messagebox.showerror("Error", "Drug name cant be empty", parent=drugWin)
            return
        if typeCombo.get() == "":
            messagebox.showerror("Error", "Drug type cant be empty", parent=drugWin)
            return
        if doseCombo.get() == "":
            messagebox.showerror("Error", "Drug dose cant be empty", parent=drugWin)
            return
        if useCombo.get() == "":
            messagebox.showerror("Error", "Drug use cant be empty", parent=drugWin)
            return
        if has_numbers(priceEntry.get()) == False:
            messagebox.showerror("Error", "Drug price must be a number", parent=drugWin)
            return
        if cboDrg.get() != "" and doseCombo.get() != "" and typeCombo.get() != "" and useCombo.get() != "":
            con = sqlite3.connect("proj1.db")
            c = con.cursor()
            c.execute("INSERT into prescriptions(ID, drug, type, dose, use, price)Values(?,?,?,?,?,?)",(H, cboDrg.get(), typeCombo.get(), doseCombo.get(), useCombo.get(), priceEntry.get()))
            con.commit()
            con.close()
            saveDrugData()
            clearDrugEntrys()

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
        
    def placeDrugs():
        con = sqlite3.connect('proj1.db')
        c = con.cursor()
        records = c.execute("SELECT * FROM prescriptions WHERE ID =?", (H,)).fetchall()
        drugid = c.execute("SELECT rowid FROM prescriptions WHERE ID =?", (H,)).fetchall()
        fetcheddid = []
        convertDataToList(drugid, fetcheddid)
        count = 0
        for record in records:
            if count % 2 == 0:
                prtv.insert(parent='', index='end', iid=count, text='', values=(count+1, record[1], record[2], record[3], record[4], record[5], fetcheddid[count]), tags=('evenrow',))
            else:
                prtv.insert(parent='', index='end', iid=count, text='', values=(count+1, record[1], record[2], record[3], record[4], record[5], fetcheddid[count]), tags=('oddrow',))
            # increment counter
            count += 1
        con.commit()
        con.close()
    placeDrugs()

    def saveDrugData(): 
        con = sqlite3.connect("proj1.db")
        c = con.cursor()

        drgs = c.execute("SELECT drug FROM drugs").fetchall()
        fetchedrgs = []
        convertDataToList(drgs, fetchedrgs)
        for i in range(len(fetchedrgs)):
            fetchedrgs[i] = fetchedrgs[i].lower()

        if cboDrg.get() != "" and cboDrg.get().lower() in fetchedrgs:
            c.execute("""UPDATE drugs SET
            type = :type,
            dose = :dose,
            use = :use,
            price = :price
            WHERE drug = :drugname""",
            {
                'type': typeCombo.get(),
                'dose': doseCombo.get(),
                'use': useCombo.get(),
                'price': priceEntry.get(),
                'drugname': cboDrg.get().lower()
            }
            )
            con.commit()
            con.close()
        # if cboDrg.get() != "" and cboDrg.get().upper() not in fetchedrgs:
        else:
            c.execute("INSERT into drugs(drug, type, dose, use, price)Values(?,?,?,?,?)",(cboDrg.get().lower(), typeCombo.get(), doseCombo.get(), useCombo.get(), priceEntry.get()))
            con.commit()
            con.close()

    def placeDrugData():
        try:
            conn = sqlite3.connect("proj1.db")
            cc = conn.cursor()
            dRow = cc.execute("SELECT * FROM drugs WHERE drug =?", (cboDrg.get(),)).fetchall()[0]
            typeCombo.delete(0, END)
            doseCombo.delete(0, END)
            useCombo.delete(0, END)
            priceEntry.delete(0, END)
            typeCombo.insert(1,  dRow[1])
            doseCombo.insert(1,  dRow[2])
            useCombo.insert(1,   dRow[3])
            priceEntry.insert(1, dRow[4])
            conn.close()
        except:
            return

    def handle_click(event):
        if prtv.identify_region(event.x, event.y) == "separator":
            return "break"

    def printVisit():
        # try:
            if len(prtv.get_children()) > 0:
                for line in prtv.get_children():
                    tvLen = prtv.item(line)['values'][0]
                con = sqlite3.connect("proj1.db")
                c = con.cursor()
                pname = c.execute("SELECT * FROM patientList WHERE ID =?", (x,)).fetchall()
                record = c.execute("SELECT * FROM prescriptions WHERE ID =?", (H,)).fetchall()
                con.commit()
                con.close()

                pdf = FPDF('P', 'mm', 'A5')
                pdf.add_page()
                pdf.set_font('courier', 'B', 10)

                pdf.cell(0, 35, "", ln=1)

                pdf.cell(12, 5, "Name:", border=1)
                pdf.set_font('courier', '', 10)
                pdf.cell(64, 5, pname[0][1].strip(), border=1, align='C')
                pdf.cell(3, 0, "")
                pdf.set_font('courier', 'B', 10)
                pdf.cell(10, 5, "Age:", border=1)
                pdf.set_font('courier', '', 10)
                pdf.cell(8, 5, pname[0][2], border=1, align='C')
                pdf.cell(3, 0, "")
                pdf.set_font('courier', 'B', 10)
                pdf.cell(12, 5, "Date:", border=1)
                pdf.set_font('courier', '', 10)
                pdf.cell(23, 5, visitDate, border=1, ln=1, align='C')

                pdf.set_font('courier', 'B', 10)
                pdf.cell(5, 10, "", "B")
                pdf.cell(57, 10, "Drug", "B")
                pdf.cell(23, 10, "type", "B")
                pdf.cell(23, 10, "dose", "B")
                pdf.cell(23, 10, "use", "B", ln=1,)
                pdf.cell(23, 0.1, "", ln=1,)
                pdf.set_font('courier', '', 10)

                for index in range(tvLen):
                    if index % 2 == 0:
                        pdf.set_fill_color(255, 255, 255)
                    else:
                        pdf.set_fill_color(211, 211, 211)
                    pdf.cell(5 , 7, str(index + 1), fill=1)
                    pdf.cell(57, 7, record[index][1], fill=1)
                    pdf.cell(23, 7, record[index][2], fill=1)
                    pdf.cell(23, 7, record[index][3], fill=1)
                    pdf.cell(23, 7, record[index][4], ln=1, fill=1)
                    index += 1
                global pdfName
                pdfName = pname[0][1].strip().replace(" ", "_") + "-" + visitDate.replace("/", ".") +'.pdf'
                pdf.output(pdfName)
                os.system (pdfName)
            else:
                messagebox.showerror("Error", "Visit has no prescriptions")
        # except:
        #     return
                
            
    def delpdf():
        try:
            os.remove(pdfName)
            drugWin.destroy()
        except:
            drugWin.destroy()
    def deselect(e):
        if len(prtv.selection()) > 0:
            prtv.selection_remove(prtv.selection()[0])
    
    def delpre(e):
        try:
            drugid = c.execute("SELECT rowid FROM prescriptions WHERE ID =?", (H,)).fetchall()
            fetcheddid = []
            convertDataToList(drugid, fetcheddid)
            ds = prtv.item(prtv.selection())['values'][6]
            con = sqlite3.connect('proj1.db')
            cc = con.cursor()
            cc.execute("DELETE FROM prescriptions WHERE rowid =?", (ds,))
            con.commit()
            con.close()
            refreshDrugs()
        except:
            return
        else:
            return

    def refreshvisits():
        try:
            for line in TREEVIEW.selection():
                s = TREEVIEW.item(line)['values'][0]
            con = sqlite3.connect('proj1.db')
            c = con.cursor()
            records = c.execute("SELECT * FROM visits WHERE ptid =?", (s,)).fetchall()
            for item in TREEVIEW2.get_children():
                TREEVIEW2.delete(item)

            ids = []
            for i in records:
                ids.append(i[0])
            patientTotalPayments = []
            for hh in range(len(ids)):
                prices = c.execute("SELECT price FROM prescriptions WHERE ID =?", (ids[hh],)).fetchall()
                vtp = 0
                for q in range(len(prices)):
                    vtp += int(prices[q][0])
                patientTotalPayments.append(vtp)

            count = 0
            for record in records:
                if count % 2 == 0:
                    TREEVIEW2.insert(parent='', index='end', iid=count, text="", values=(record[0], count+1, record[2], record[3] ,patientTotalPayments[count]), tags=('evenrow',))
                else:
                    TREEVIEW2.insert(parent='', index='end', iid=count, text="", values=(record[0], count+1, record[2], record[3] ,patientTotalPayments[count]), tags=('oddrow',))
                # increment counter
                count += 1
            con.commit()
            con.close()
            for line in TREEVIEW.selection():
                S = TREEVIEW.item(line)['values'][3]
        except:
           return


    prtv.bind('<Button-1>', handle_click)
    drugWin.bind("<Return>", lambda e:[addDrug(), refreshDrugs()])
    prtv.bind("<BackSpace>", delpre)
    prtv.bind("<Delete>", delpre)
    cboDrg.bind("<<ComboboxSelected>>", lambda e: placeDrugData())

    printVisitBtn.config(command=printVisit)
    addDrugBtn.config(command=lambda:[addDrug(), refreshDrugs()])
    def PEW():
        openEditWin(cboDrg)

    editDrugs.config(command=PEW)

    drugWin.protocol("WM_DELETE_WINDOW", lambda:[delpdf(), refreshvisits()])
    drugWin.bind("<Escape>", deselect)

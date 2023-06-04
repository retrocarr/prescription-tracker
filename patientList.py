import os
from datetime import datetime
import sqlite3
from tkcalendar import DateEntry
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from doctorWindow import openDoctorWindow
from prescriptionWindow import openPresWindow
from dataBaseSettings import projconnect
from printWindow import openPrintWindow

projcon = projconnect()

def convertDataToList(data, list):
    for i in data:
        list.append(i[0])
def has_numbers(inputString):
    return any(c.isalpha() for c in inputString) != True
    # return any(char.isdigit() for char in inputString)
def character_limit(entry_text):
    if len(entry_text.get()) > 3:
        entry_text.set(entry_text.get()[:-1])

mainicon = os.getcwd() +  "\\mainicon.ico"
print(mainicon)
# [[[[[[[[[[[[[ CREATE MAIN WINDOW ]]]]]]]]]]]]
root = Tk()
root.geometry('1340x722+50+17')
root.title('patient list')
root.iconbitmap(mainicon)
root.configure(background="silver")
# root.resizable(False,False)
fillerFrame = Frame(bg='light grey')
fillerFrame.pack(fill=X)
title = Label(root, text='PRESCRIPTION', bg='#3498DB', font=('tajawal 16 bold'), fg='white', highlightbackground="light grey", highlightthickness=2, height=1)
title.pack(fill=X)

# [[[[[[[[[[[[ CREATE INPUTS FRAME ]]]]]]]]]]]]
Manage_Frame = Frame(root, bg="white", highlightbackground="light grey", highlightthickness=2, height=1)
Manage_Frame.pack(fill=BOTH, side='left', expand=1)

conn = sqlite3.connect("proj1.db")
cur = conn.cursor()
select = cur.execute("SELECT * FROM doctors")
doctors = select.fetchall()
docotrList = ["None"]
convertDataToList(doctors, docotrList)
conn.close()

addReffButton = Button(Manage_Frame, text='+', height=0)

def searchOnPress(nv):
    searchNameEntry()
nv = StringVar()
nv.trace("w", lambda name, index, mode, nv=nv: searchOnPress(nv))

lbl_nameF = Frame(Manage_Frame,    bg='white', width=187, height=24)
lbl_ageF = Frame(Manage_Frame,     bg='white', width=187, height=24)
lbl_phoneF = Frame(Manage_Frame,   bg='white', width=187, height=24)
lbl_addressF = Frame(Manage_Frame, bg='white', width=187, height=24)

agevar = StringVar()
lbl_name = Label(lbl_nameF, text='Name', bg='white', font=("tajawal 12"), anchor='w')
name_Entry = Entry(Manage_Frame, bd='2', justify='center', font=('tajawal 13'), textvariable=nv)
lbl_age = Label(lbl_ageF, text='Age', bg='white', font=("tajawal 12"), anchor='w')
age_Entry = Entry(Manage_Frame , bd='2', justify='center', font=('tajawal 13'), textvariable=agevar)
lbl_phone = Label(lbl_phoneF, text='Phone number', bg='white', font=("tajawal 12"), anchor='w')
phone_Entry = Entry(Manage_Frame, bd='2', justify='center', font=('tajawal 13'))
lbl_address = Label(lbl_addressF, text='address', bg='white', font=("tajawal 12"), anchor='w')
address_Entry = Entry(Manage_Frame,bd='2', justify='center', font=('tajawal 13'))
# lbl_name.pack(pady=(10, 2), padx=5, fill=X)
lbl_nameF.pack(pady=(10, 2), padx=5)
name_Entry.pack(pady=2, padx=4)
lbl_name.pack(fill=X)
# lbl_age.pack(pady=2, padx=5, fill=X)
lbl_ageF.pack(pady=2)
age_Entry.pack(pady=2, padx=4)
lbl_age.pack(fill=X)
# lbl_phone.pack(pady=2, padx=5, fill=X)
lbl_phoneF.pack(pady=2, padx=5)
phone_Entry.pack(pady=2, padx=4)
lbl_phone.pack(fill=X)
# lbl_address.pack(pady=2, padx=5, fill=X)
lbl_addressF.pack(pady=2, padx=5)
address_Entry.pack(pady=2, padx=4)
lbl_address.pack(fill=X)
lbl_nameF.pack_propagate(0)
lbl_ageF.pack_propagate(0)
lbl_phoneF.pack_propagate(0)
lbl_addressF.pack_propagate(0)

#============= Buttons===========
frm = Frame(Manage_Frame)
add_btn = Button   (frm,          width=9,  text='Add',    bg='#8c8c8c', fg='white', font=("tajawal 12 bold"), height=1)
update_btn = Button(frm,          width=9,  text='Change', bg='#8c8c8c', fg='white', font=("tajawal 12 bold"), height=1)
clear_btn = Button (Manage_Frame, width=20, text='Clear',  bg='#8c8c8c', fg='white', font=("tajawal 12 bold"), height=1)
about_btn = Button (Manage_Frame, width=20, text='About',  bg='#8c8c8c', fg='white', font=("tajawal 12 bold"), height=1)
frm.pack(pady=(30, 2), padx=3)
add_btn.pack   (side='right', fill=X, padx=4)
update_btn.pack(side='left', fill=X, padx=4)
# add_btn.pack(pady=(30, 9))
# update_btn.pack(pady=9)
clear_btn.pack(pady=3)
# about_btn.pack(pady=3)
# ========== Search manage ========= 
search_Frame=Frame(root,bg='white', height=50, highlightbackground="light grey", highlightthickness=2)
search_Frame.pack(side='top', fill=X)
search_FrameFrame = Frame(search_Frame, bg='white')
search_FrameFrame.pack(fill=X, side='left', pady=8)

#===============combobox=================
searchLabel = Label(search_FrameFrame, text='Search:', bg='white', font=('tajawal 12'))
searchLabel.pack(side='left')
combo_search=ttk.Combobox(search_FrameFrame,justify='center', width=6, state="readonly", font=("tajawal 10"))
combo_search['value']=['ID','Name','Phone']
combo_search.pack(fill=BOTH, side='left', padx=5)
# combo_search.pack(side="left", padx=(10,2), pady=11)
combo_search.current(1)
combo_search.insert(0, 'Name')
#========== search Entry ===============
def callback(sv):
    search()
sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
search_Entry = Entry(search_FrameFrame, justify='left', bd='2', textvariable=sv, font=("tajawal 11"), border=0, highlightbackground='grey', highlightthickness=1)
search_Entry.pack(side='left', fill=BOTH, padx=5)
# search_Entry.pack(side="left", padx=5, pady=11)
#==========search button ================
xIcon = PhotoImage(file= os.getcwd() +  "\\delete-icon.png")
printIcon = PhotoImage(file= os.getcwd() +  "\\print-icon.png")

del_btn = Button(search_FrameFrame, text='t', image=xIcon , fg='white', height=20, width=20)
del_btn.pack(side='left', fill=BOTH, padx=5)
# del_btn.pack(side="left", padx=5, pady=11)

printTodayBtn = Button(search_FrameFrame, text=' Print', image=printIcon, fg='black', height=20, width=53, compound='left')
printTodayBtn.pack(side='left', fill=BOTH, padx=5)





#=============List student===============
details_Frame=Frame(root,bg='#f2f4f4')

scroll_x=Scrollbar(details_Frame,orient=HORIZONTAL)
scroll_y=Scrollbar(details_Frame,orient=VERTICAL)








# [[[[[[[[[[[[[[[[SECONDARY TREEVIEW]]]]]]]]]]]]]]]]
vtvFrameFrame = Frame(root, highlightbackground="light grey", highlightthickness=2, width=1)
vtvFrame = Frame(vtvFrameFrame, highlightbackground="black", highlightthickness=2, bg='white')
vtv=ttk.Treeview(vtvFrame,
columns=('#hiddenId', '#id', '#date', '#doctor', '#price'),
xscrollcommand=scroll_x.set,
yscrollcommand=scroll_y.set, height=200)
vtv['show']='headings'
vtv.column("#price", minwidth=0, width=100, anchor=CENTER)
vtv.heading('#price',text='Price')
vtv.column("#date", minwidth=0, width=100, anchor=CENTER)
vtv.heading('#date',text='Date')
vtv.column("#doctor", minwidth=0, width=160, anchor=CENTER)
vtv.heading('#doctor',text='Doctor')
vtv.column("#id", minwidth=0, width=20, anchor=CENTER)
vtv.heading('#id',text='')
vtv.column("#hiddenId", stretch=NO, width=0, anchor=CENTER)
vtv.heading('#hiddenId',text='HIDDEN')
text = StringVar()
pnl = Label(vtvFrame, bg='#3498DB', fg='white', font=('tajawal',12), textvariable=text, width=1)
pnl.pack(fill=X)
text.set('Visits')
vtvBtnFrame = Frame(vtvFrame, bg='white')
doctorFrame = Frame(vtvBtnFrame, bg='white')
dateFrame = Frame(vtvBtnFrame, bg='white', width=180, height=50)
dateFrame.pack_propagate(0)
vtvFrameFrame.pack(side='right')
vtvBtnFrame.pack()
vtvFrame.pack   ()
vtv.pack(fill=BOTH)
lbl = Label(doctorFrame, bg='white', text='Doctor', font=('tajawal 11 bold'))
lbl.pack()
docEntry = AutocompleteCombobox(doctorFrame, width=14, completevalues=docotrList, font=('tajawal 13'), justify='center')
docEntry['state'] = 'readonly'
if len(docotrList) != 0:
    docEntry.current(0)
docEntry.pack(side='left', padx=(0,6), pady=(1,0))
newDoctorBtn = Button(doctorFrame, text="+", font=("tahawal 9 bold"), width=2)
newDoctorBtn.pack(side="right", pady=1)
calLbl = Label(dateFrame, text='Date', bg='white', font=('tajawal 11 bold'))
calLbl.pack()
currYear = int(datetime.today().strftime('%Y'))
currMonth = int(datetime.today().strftime('%m'))
currDay = int(datetime.today().strftime('%d'))
cal = DateEntry(dateFrame, justify=CENTER, selectmode="day", year=currYear, month=currMonth, day=currDay, font=('tajawal 11'), date_pattern='y/mm/dd')
cal['state'] = 'readonly'
cal.pack(fill=X)
doctorFrame.pack(pady=5)
dateFrame.pack(pady=1)
addVisitButton = Button(vtvBtnFrame, text='Add visit', bg='light green', font=("tajawal 12 bold"), height=1)
addVisitButton.pack(pady=20, fill=X)

# [[[[[[[[[[[[[MAIN TREEVIEW]]]]]]]]]]]]]
tvFrame = Frame(root, highlightbackground="light grey", highlightthickness=2)
tv=ttk.Treeview(tvFrame,
columns=('#id', '#name', '#age', '#phone', '#address'),
xscrollcommand=scroll_x.set,
yscrollcommand=scroll_y.set)
# tv.place(x=451,y=-4, width=686, height=641)
tvFrame.pack(side="right", fill=BOTH, expand=1)
tv.pack(side="right", fill=BOTH, expand=1)
tv['show']='headings'
tv.column("#address", minwidth=22, width=230, anchor='w')
tv.heading('#address',text='Address', anchor='w')
tv.column("#phone", minwidth=22, width=200, anchor='n')
tv.heading('#phone',text='Phone')      
tv.column("#age", minwidth=22, width=100, stretch=NO, anchor='n')
tv.heading('#age',text='Age')       
tv.column("#name", minwidth=22, width=250, anchor='w')
tv.heading('#name',text='Name', anchor='w')
tv.column("#id", minwidth=2, width=30, stretch=NO, anchor=CENTER)
tv.heading('#id',text='')

style = ttk.Style()
style.configure("Treeview.Heading", font=("None 12 bold"))
style.configure("Treeview",         font=("None 11"))
vtv.tag_configure('oddrow', background='light grey')
vtv.tag_configure('evenrow', background='#f0f0f0')
tv.tag_configure('oddrow', background='light grey')
tv.tag_configure('evenrow', background='#f0f0f0')
style.map('Treeview', background=[('selected', '#3498DB')])

def placeData():
    cursor=projcon.ListRequest()
    num = 0
    for row in cursor:
        if num % 2 == 0:
            tv.insert(parent='', index='end', iid=num, text='', values=(row[0], row[1], row[2], row[3], row[4]), tags=('evenrow',))
        else:
            tv.insert(parent='', index='end', iid=num, text='', values=(row[0], row[1], row[2], row[3], row[4]), tags=('oddrow',))
        num += 1

con = sqlite3.connect("proj1.db")
c = con.cursor()
ptnameList = c.execute("SELECT * FROM patientList").fetchall()
fetchedPtList = []
for i in range(len(ptnameList)):
    fetchedPtList.append(ptnameList[i][1])


def fetchPatients():
    global fetchedPtList
    con = sqlite3.connect("proj1.db")
    c = con.cursor()
    ptnameList = c.execute("SELECT * FROM patientList").fetchall()
    fetchedPtList = []
    for i in range(len(ptnameList)):
        fetchedPtList.append(ptnameList[i][1])

def BuSaveData():
    fetchPatients()
    if name_Entry.get() == "":
        messagebox.showerror("Error", "Name cant be empty")
        return

    if has_numbers(name_Entry.get()) == True:
        messagebox.showerror("Error", "Patinet name cant include numbers")
        return
    if age_Entry.get() != "":
        if has_numbers(age_Entry.get()) == False:
            messagebox.showerror("Error", "Patient age must be a number")
            return
    if phone_Entry.get() != "":
        if has_numbers(phone_Entry.get()) == False:
            messagebox.showerror("Error", "Patinet phone must be number")
            return

    if name_Entry.get().upper() in (i.upper() for i in fetchedPtList):
        messagebox.showerror("Error", name_Entry.get().strip() + " already exists")
        return
    if name_Entry.get() != "" and name_Entry.get().upper() not in (i.upper() for i in fetchedPtList):
        msg = projcon.Add(name_Entry.get().capitalize().strip(), age_Entry.get(), phone_Entry.get(), address_Entry.get().strip())
        messagebox.showinfo(title="add info", message = msg)
        clearEntrys()
        return

def refreshTable():
    for item in tv.get_children():
        tv.delete(item)
    placeData()

def deleteFromDb(event=None):
    # try:
        con = sqlite3.connect("proj1.db")
        c = con.cursor()

        for line in tv.selection():
            name = tv.item(line)['values'][1]

        warn = messagebox.askokcancel("warning", "are you sure you want to delete " + name.strip() + "'s" + " record" + " and all of its data?")
    

        if warn == 0:
            con.close()
            return
        if warn == 1:
            for line in tv.selection():
                ptSelection = tv.item(line)['values'][0]

            for i in vtv. get_children():
                c.execute("DELETE FROM prescriptions WHERE ID =" + str(vtv.item(i)['values'][0]))
            c.execute("DELETE FROM visits WHERE ptid =" + str(ptSelection))
            c.execute("SELECT * FROM patientList")
            c.execute("DELETE FROM patientList WHERE ID =" + str(ptSelection))

            con.commit()
            con.close()
            refreshTable()
            deselect()
            clearEntrys()
            search_Entry.delete(0, END)
    # except:
    #     return
    

def deleteVisit(e):
    if len(vtv.selection()) > 0:
        try:
            warn = messagebox.askokcancel("Warning", "Are you sure you want to delete this vist")
            if warn == 0:
                return
            if warn == 1:
                visitSelection = (vtv.item(int(vtv.selection()[0]))['values'][0])
                conne = sqlite3.connect("proj1.db")
                c = conne.cursor()
                c.execute("DELETE FROM visits WHERE ID = ?", (visitSelection,))
                conne.commit()
                conne.close()
                placeVisits()
        except:
            return


def clearEntrys(event=None):
    name_Entry.delete(0, END)
    age_Entry.delete(0, END)
    phone_Entry.delete(0, END)
    address_Entry.delete(0, END)

def get_cursor(event=None):


    def updateRecord(event=None):
        # global cname_Entry, cage_Entry, cphone_Entry, caddress_Entry
        if cname_Entry.get() == "":
            messagebox.showerror("Error", "Name cant be empty")
            return

        if has_numbers(cname_Entry.get()) == True:
            messagebox.showerror("Error", "Patinet name cant include numbers")
            return
        if cage_Entry.get() != "":
            if has_numbers(cage_Entry.get()) == False:
                messagebox.showerror("Error", "Patient age must be a number")
                return
        if cphone_Entry.get() != "":
            if has_numbers(cphone_Entry.get()) == False:
                messagebox.showerror("Error", "Patinet phone must be number")
                return
        for line in tv.selection():
            Uid = tv.item(line)['values'][0]
        con = sqlite3.connect("proj1.db")
        c= con.cursor()
        c.execute("""UPDATE patientList SET
        name = :name,
        age = :age,
        phone = :phone,
        address = :address
        WHERE ID = :id""",
        {
            'name': cname_Entry.get().strip(),
            'age': cage_Entry.get(),
            'phone': cphone_Entry.get(),
            'address': caddress_Entry.get().strip(),
            'id': Uid
        }
        )
        con.commit()
        con.close()
        clearEntrys()
        refreshTable()
        q.destroy()
        return

    if len(tv.selection()) != 0:
        for line in tv.selection():
            name = tv.item(line)['values'][1]

        cagevar = StringVar()
        cagevar.trace("w", lambda *args: character_limit(cagevar))
        q = Toplevel()
        q.iconbitmap(mainicon)
        q.attributes('-topmost', 'true')
        # q.geometry("350x490+700+100")
        q.title(name.strip())
        q.resizable(False,False)
        q.lift()
        q.grab_set()
        # global cname_Entry, cage_Entry, cphone_Entry, caddress_Entry
        mainFrame = Frame(q)
        mainLbl = Label(mainFrame, text='Change record details for:', font=("tajawal 12"))
        mainLbl2 = Label(mainFrame, text=name.strip(), font=("tajawal 12 bold"))
        clbl_name = Label(q, text='Name:', width=30, font=("tajawal 10"))
        cname_Entry = Entry(q, bd='2', justify='center', width=20, font=('tajawal 14'))
        clbl_age = Label(q, text='Age:', width=30, font=("tajawal 10"))
        cage_Entry = Entry(q , bd='2', justify='center', width=20, font=('tajawal 14'), textvariable=cagevar)
        clbl_phone = Label(q, text='Phone number:', width=30, font=("tajawal 10"))
        cphone_Entry = Entry(q, bd='2', justify='center', width=20, font=('tajawal 14'))
        clbl_address = Label(q, text='Address:', width=38, font=("tajawal 10"))
        caddress_Entry = Entry(q,bd='2', justify='center', width=20, font=('tajawal 14'))

        changeButton = Button(q, text='Change', width=10, bg='light green', command=updateRecord)

        mainFrame.pack(pady=(10,5))
        mainLbl.pack()
        mainLbl2.pack()
        clbl_name.pack(pady=4)
        cname_Entry.pack(pady=4)
        clbl_age.pack(pady=4)
        cage_Entry.pack(pady=4)
        clbl_phone.pack(pady=4)
        cphone_Entry.pack(pady=4)
        clbl_address.pack(pady=4)
        caddress_Entry.pack(pady=4)
        changeButton.pack(pady=15)

        try:
            cursor_row = tv.focus()
            contents = tv.item(cursor_row)
            row = contents['values']
            clearEntrys()
            cname_Entry.insert(1, row[1])
            cage_Entry.insert(1, row[2])
            cphone_Entry.insert(1, row[3])
            caddress_Entry.insert(1, row[4])
        except:
            return
        q.bind("<Return>", updateRecord)
        cname_Entry.focus()


def deselect(event=None):
    try:
        if len(tv.selection()) > 0:
            tv.selection_remove(tv.selection()[0])
        if len(vtv.selection()) > 0:
            vtv.selection_remove(vtv.selection()[0])
        for item in vtv.get_children():
            vtv.delete(item)
        text.set('Visits')
    except:
        return

def OPW(event=None):
    if len(vtv.selection()) != 0:
        openPresWindow(tv, vtv)

def searchNameEntry(event=None):
    for item in tv.get_children():
        tv.delete(item)
    lookup_record = name_Entry.get()
    con = sqlite3.connect('proj1.db')
    c = con.cursor()
    c.execute("SELECT rowid, * FROM patientList WHERE name LIKE ?", ("%"+lookup_record+"%",))
    records = c.fetchall()
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            tv.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2] ,record[3], record[4], record[5]), tags=('evenrow',))
        else:
            tv.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2] ,record[3], record[4], record[5]), tags=('oddrow',))
        count += 1
        con.commit()
    con.close()
    try:
        if len(tv.selection()) > 0:
            tv.selection_remove(tv.selection()[0])
        if len(vtv.selection()) > 0:
            vtv.selection_remove(vtv.selection()[0])
        for item in vtv.get_children():
            vtv.delete(item)
        text.set('Visits')
    except:
        return

def search(event=None):
    for item in tv.get_children():
        tv.delete(item)
    lookup_record = search_Entry.get()
    con = sqlite3.connect('proj1.db')
    c = con.cursor()
    if combo_search.get() == 'ID':
        c.execute("SELECT rowid, * FROM patientList WHERE ID LIKE ?", ("%"+lookup_record+"%",))
    if combo_search.get() == 'Name':
        c.execute("SELECT rowid, * FROM patientList WHERE name LIKE ?", ("%"+lookup_record+"%",))
    if combo_search.get() == 'Phone':
        c.execute("SELECT rowid, * FROM patientList WHERE phone LIKE ?", ("%"+lookup_record+"%",))
    records = c.fetchall()
    global count
    count = 0
    for record in records:
        if count % 2 == 0:
            tv.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2] ,record[3], record[4], record[5]), tags=('evenrow',))
        else:
            tv.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2] ,record[3], record[4], record[5]), tags=('oddrow',))
        count += 1
        con.commit()
    con.close()

def ADDPATIENT(event=None):
    BuSaveData()
    refreshTable()
    name_Entry.focus()

def placeVisits(event=None):
    try:
        for line in tv.selection():
            s = tv.item(line)['values'][0]
        con = sqlite3.connect('proj1.db')
        c = con.cursor()
        records = c.execute("SELECT * FROM visits WHERE ptid =?", (s,)).fetchall()
        for item in vtv.get_children():
            vtv.delete(item)

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
                vtv.insert(parent='', index='end', iid=count, text="", values=(record[0], count+1, record[2], record[3] ,patientTotalPayments[count]), tags=('evenrow',))
            else:
                vtv.insert(parent='', index='end', iid=count, text="", values=(record[0], count+1, record[2], record[3] ,patientTotalPayments[count]), tags=('oddrow',))
            # increment counter
            count += 1
        con.commit()
        con.close()
        placeName()
    except:
        return


def addVisit():
    for line in tv.selection():
        h = tv.item(line)['values'][0]
    con = sqlite3.connect('proj1.db')
    cc = con.cursor()
    cc.execute("INSERT INTO visits(ptid, date, doctor)Values(?,?,?)",(h, cal.get_date(), docEntry.get()))
    con.commit()
    con.close()
    placeVisits()

def checkForRepeatedVisit():
    # try:
        for line in tv.selection():
            h = tv.item(line)['values'][0]
        con = sqlite3.connect('proj1.db')
        cc = con.cursor()
        dates = cc.execute("SELECT * FROM visits WHERE ptid=?", (h,)).fetchall()
        fetchedDates = []
        for date in dates:
            fetchedDates.append(date[2])
        con.commit()
        con.close()
        if str(cal.get_date()) in fetchedDates:
            ask = messagebox.askyesno("warning", "theres already a visit with that date, do you want to add another?")
            if ask == 0:
                return
            if ask == 1:
                addVisit()
        else:
            addVisit()
    # except:
    #     return

def placeName():
    for line in tv.selection():
        S = tv.item(line)['values'][1]
    text.set(S.strip() + "'s" + ' Vists')

def handle_click(event):
    if tv.identify_region(event.x, event.y) == "separator":
        return "break"
def handle_click1(event):
    if vtv.identify_region(event.x, event.y) == "separator":
        return "break"

def ODW(event=None):
    openDoctorWindow(docEntry, docotrList, docotrList)

def vtvs(e):
    try: 
        vtv.selection_remove(vtv.selection()[0]) 
    except:
        return

agevar.trace("w", lambda *args: character_limit(agevar))

tv.bind('<Button-1>', handle_click)
vtv.bind('<Button-1>', handle_click1)
tv.bind("<ButtonRelease-1>", placeVisits)
tv.bind("<Double-Button-1>", get_cursor)
tv.bind("<BackSpace>", deleteFromDb)
tv.bind("<Delete>", deleteFromDb)
vtv.bind("<BackSpace>", deleteVisit)
vtv.bind("<Delete>", deleteVisit)
vtv.bind('<Double-Button-1>', OPW)
search_Frame.bind("<ButtonRelease-1>", deselect)
Manage_Frame.bind("<ButtonRelease-1>", deselect)
root.bind("<Escape>", deselect)
vtvBtnFrame.bind("<ButtonRelease-1>", vtvs)
combo_search.bind("<<ComboboxSelected>>", search)
# docEntry.bind('<Double-Button-1>', ODW)
newDoctorBtn.config(command=ODW)
root.bind("<Control_L>f", lambda e: search_Entry.focus())
root.bind("<Control_L>F", lambda e: search_Entry.focus())

root.bind("<Return>", ADDPATIENT)
addVisitButton.config(command=checkForRepeatedVisit)
add_btn.config(command=ADDPATIENT)
clear_btn.config(command=clearEntrys)
del_btn.config(command=deleteFromDb)
update_btn.config(command=get_cursor)
printTodayBtn.config(command=openPrintWindow)
placeData()
root.mainloop()
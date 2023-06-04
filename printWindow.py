from tkinter import Tk, Frame, Label, Button, Toplevel
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3
import os
from fpdf import FPDF

mainicon = os.getcwd() +  "\\mainicon.ico"

def convertDataToList(data, list):
    for i in data:
        list.append(i[0])

def character_limit(entry_text):
    if len(entry_text.get()) > 2:
        entry_text.set(entry_text.get()[:-1])

def yearLimit(entry_text):
    if len(entry_text.get()) > 4:
        entry_text.set(entry_text.get()[:-1])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def openPrintWindow():
    printWin = Toplevel()
    printWin.iconbitmap(mainicon)
    printWin.geometry("370x180+500+250")
    printWin.resizable(False, False)
    printWin.grab_set()
    printWin.lift()

    dFrame = Frame(printWin)

    lbl1 = Label(dFrame, text='From:')
    lbl2 = Label(dFrame, text='To:')
    DE1 = DateEntry(dFrame, date_pattern='y/mm/dd')
    DE2 = DateEntry(dFrame, date_pattern='y/mm/dd')
    printButton = Button(printWin, text='Print selection')
    printToday = Button(printWin, text='Print today')

    dFrame.pack(pady=30, padx=(0, 20))
    lbl1.pack(side='left')
    DE1.pack(side='left', padx=(0, 40))
    lbl2.pack(side='left')
    DE2.pack(side='right')
    printButton.pack(pady=5)
    printToday.pack(pady=5)

    def caldate():
        con = sqlite3.connect('proj1.db')
        c = con.cursor()
        v = c.execute("SELECT ptid, date, ID FROM visits").fetchall()
        p = c.execute("SELECT ID FROM visits").fetchall()

        pdf = FPDF('P', 'mm', 'A5')
        pdf.add_page()
        pdf.set_font('courier', 'B', 10)
        pdf.cell(0, 35, "", ln=1)
        pdf.cell(0, 10, 'All visits from: ' + DE1.get().replace('-', '/') + ' to: ' + DE2.get().replace('-', '/') , ln=1)
        pdf.cell(35, 10, 'Date', 'B')
        pdf.cell(55, 10, 'Patient name', 'B')
        pdf.cell(35, 10, 'Total price', 'B', ln=1)
        pdf.set_font('courier', '', 10)

        index = 0
        for i in v:
            dateobject = datetime.strptime(i[1], '%Y-%m-%d').date()
            name = c.execute("SELECT name FROM patientList WHERE ID =?", (i[0],)).fetchall()[0][0]
            priceData = c.execute("SELECT price FROM prescriptions WHERE ID =?", (i[2],)).fetchall()
            prices = []
            convertDataToList(priceData, prices)
            P = 0
            for u in prices:
                P += u
            if  DE1.get_date() <= dateobject <= DE2.get_date():
                if index % 2 == 0:
                    pdf.set_fill_color(255, 255, 255)
                else:
                    pdf.set_fill_color(211, 211, 211)
                pdf.cell(35, 10, str(dateobject).replace('-', '/'))
                pdf.cell(55, 10, str(name))
                pdf.cell(35, 10, str(P), ln=1)
                index += 1

        global pdfName
        pdfName = "temporaryReport.pdf"
        pdf.output(pdfName)
        os.system (pdfName)

    def PT():
        con = sqlite3.connect('proj1.db')
        c = con.cursor()
        v = c.execute("SELECT ptid, date, ID FROM visits").fetchall()
        p = c.execute("SELECT ID FROM visits").fetchall()

        pdf = FPDF('P', 'mm', 'A5')
        pdf.add_page()
        pdf.set_font('courier', 'B', 10)
        pdf.cell(0, 35, "", ln=1)
        pdf.cell(0, 10, 'All visits for: ' + str(datetime.today().date()) , ln=1)
        pdf.cell(35, 10, 'Date', 'B')
        pdf.cell(55, 10, 'Patient name', 'B')
        pdf.cell(35, 10, 'Total price', 'B', ln=1)
        pdf.set_font('courier', '', 10)

        index = 0
        for i in v:
            dateobject = datetime.strptime(i[1], '%Y-%m-%d').date()
            name = c.execute("SELECT name FROM patientList WHERE ID =?", (i[0],)).fetchall()[0][0]
            priceData = c.execute("SELECT price FROM prescriptions WHERE ID =?", (i[2],)).fetchall()
            prices = []
            convertDataToList(priceData, prices)
            P = 0
            for u in prices:
                P += u
            if  dateobject == datetime.today().date():
                if index % 2 == 0:
                    pdf.set_fill_color(255, 255, 255)
                else:
                    pdf.set_fill_color(211, 211, 211)
                pdf.cell(35, 10, str(dateobject).replace('-', '/'))
                pdf.cell(55, 10, str(name))
                pdf.cell(35, 10, str(P), ln=1)
                index += 1
        global pdfName
        pdfName = "temporaryReport.pdf"
        pdf.output(pdfName)
        os.system (pdfName)

    def delpdf():
        try:
            os.remove(pdfName)
            printWin.destroy()
        except:
            printWin.destroy()

    printButton.config(command=caldate)
    printWin.bind("<Return>", lambda e:caldate)
    printToday.config(command=PT)
    printWin.protocol("WM_DELETE_WINDOW", delpdf)
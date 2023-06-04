import sqlite3
class projconnect:
    def __init__(self):
        con = self._db=sqlite3.connect("proj1.db")
        self._db.row_factory=sqlite3.Row
        self._db.execute("CREATE table if not exists patientList(ID integer primary key autoincrement,name text, age text, phone integer, address text)")
        self._db.execute("CREATE table if not exists prescriptions(ID integer, drug text,type text, dose text, use text, price integer)")
        self._db.execute("CREATE table if not exists visits(ID integer primary key autoincrement, ptid integer, date text, doctor text, price text)")
        self._db.execute("CREATE table if not exists doctors(doctor text)")
        self._db.execute("CREATE table if not exists drugs(drug text, type text, dose text, use text, price int)")
        self._db.commit()
    def Add(self, name, age, phone, address):
        self._db.execute("INSERT into patientList(name, age, phone, address)Values(?,?,?,?)",(name, age, phone, address))
        self._db.commit()
        return "Request is submitted"
    def ListRequest(self):
        cursor=self._db.execute("select * from patientList")
        return cursor;
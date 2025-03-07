import string
import random
from traits.trait_types import Password, Title
import sqlite3
class main:
    def connect(self):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS accounts(
        Id INTEGER PRIMARY KEY,
        UserName TEXT NOT NULL UNIQUE ,
        Password TEXT NOT NULL UNIQUE ,
        RestoreKey TEXT NOT NULL UNIQUE 
        )''')
        conn.commit()
        conn.close()

    def insert(self,UserName, Password):
        RSKey = "".join(random.choices(string.digits+ string.ascii_letters + "!@#$%^&*",k=22))
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO accounts VALUES (NULL,?, ?,?)", (UserName,Password,RSKey))
        conn.commit()
        conn.close()

    def view(self):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts ")
        rows = cur.fetchall()
        conn.close()
        return rows

    def search(self,UserName,Password):
        try:
            conn = sqlite3.connect('Accounts.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM accounts WHERE UserName=? AND Password=?", (UserName, Password))
            rows = cur.fetchall()
            conn.close()
            return rows
        except:
            return False

    def delete(self,id):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM accounts WHERE Id=?", (id,))
        conn.commit()
        conn.close()

    def update(self,UserName,Password,RestorKey):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute("UPDATE accounts SET UserName=?,Password=? WHERE RestoreKey=?", (UserName,Password,RestorKey))
        conn.commit()
        conn.close()

    def getRestoreKey(self, userName, Password):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute("""
            SELECT RestoreKey FROM accounts 
            WHERE UserName=? AND Password=?
        """, (userName, Password))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    def RestoreAcc(self,RestoreKey):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE RestoreKey=?",(RestoreKey,))
        row = cur.fetchone()
        conn.close()
        return row

class Account:
    def __init__(self,UserName,Password,RestorKey):
        if not UserName:
            raise ValueError("Error: Username is None!")
        self.UserName = UserName
        self.Password = Password
        self.RestorKey = RestorKey
    def CreateDB(self):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.UserName}(id INTEGER PRIMARY KEY,title TEXT,UserName TEXT,Password TEXT)")
        conn.commit()
        conn.close()
    def Insert(self,Title,UserName,Password):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"INSERT INTO {self.UserName} VALUES (NULL,?,?,?)",(Title,UserName,Password))
        conn.commit()
        conn.close()

    def View(self):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"SELECT title, UserName FROM {self.UserName}")
        rows = cur.fetchall()
        conn.close()
        return rows

    def Search(self,Title=''):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {self.UserName} WHERE title=?", (Title,))
        rows = cur.fetchall()
        conn.close()
        return rows
    def Delete(self,id):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {self.UserName} WHERE Id=?", (id,))
        conn.commit()
        conn.close()
    def Update(self,id,Title,UserName,Password):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"UPDATE {self.UserName} SET title=?,UserName=?,Password=? WHERE id=?", (id,Title,UserName, Password))
        conn.commit()
        conn.close()
    def getId(self,Title):
        if not Title:
            return None
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM {self.UserName} WHERE title=?", (Title,))
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    def getItem(self, Title):
        conn = sqlite3.connect('Accounts.db')
        cur = conn.cursor()
        cur.execute(f"SELECT title, UserName, Password FROM {self.UserName} WHERE title=?", (Title,))
        row = cur.fetchone()
        conn.close()
        return row if row else None


Main = main()
Main.connect()
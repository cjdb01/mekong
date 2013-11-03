#!/usr/bin/python -u

import sqlite3 as lite
import re
import sys

def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

con = lite.connect('test.db')

users = (
         ("cjdb", "12345", "cjdb01@hotmail.com", "Christopher", "DB", "12/05/1993", "123 Fake Street", "Springfield", "NSW", "2560", "0212345678", "M"),
         ("tjdb", "12345", "tjdb01@hotmail.com", "Taylor", "DB", "30/04/1999", "123 Fake Street", "Springfield", "NSW", "2560", "0212345678", "F")
        )

with con:
    con.create_function("REGEXP", 2, regexp)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Users")
    cur.execute("CREATE TABLE Users(Id TEXT, Password TEXT, Email TEXT, FirstName TEXT, LastName TEXT, DateOfBirth TEXT, StreetAddress TEXT, Suburb TEXT, State TEXT, Postcode TEXT, ContactPhone TEXT, Sex TEXT)")
    cur.executemany("INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", users)
    cur.execute("SELECT * FROM Users WHERE Password REGEXP ?", '123')
    
    while True:
        row = cur.fetchone()
        if row == None:
            break
        
        for i in row:
            print i,
            
        print
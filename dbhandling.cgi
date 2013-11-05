#!/usr/bin/python -u

import cgi
import hashlib
import re
import sqlite3 as lite
import sys

error = ""

def good():
    global error
    error = ""
    return True

def legal_username(username):
    global error    
    length = len(username)
    
    error = "Invalid username '" + username + "': usernames must"
    
    if not re.match('[A-Za-z_]\w+', username):
        error += "start with a letter and only contain letters, numbers and underscores."
    elif length < 3 or length > 8:
        error += "be 3 - 8 characters long."
    else:
        return good()
    return False
    
def legal_password(password, username, first_name, last_name):
    global error
    length = password
    reg = re.compile(password)
    
    error = "Invalid password: passwords must "
    
    if length < 6 or length > 64:
        error += "be 6 - 64 characters long."
    elif not reg.search("[A-Z]"):
        error += "contain at least one upper case letter."
    elif not reg.search("[a-z]"):
        error += "contain at least one lower case letter."
    elif not reg.search("\d"):
        error += "contain at least one numeral."
    elif not reg.search("\W"):
        error += "contain at least one special character."
    elif reg.search(username) or reg.search(first_name) or reg.search(last_name):
        error += "not contain usernames, first names, or last names."
    else:
        return good()
    return False
    
def legal_isbn(isbn):
    global error
    
    if not re.match("\d{9} (\d|X)", isbn):
        error = "Invalid ISBN '" + isbn + "': an ISBN must be exactly 10 digits."
        return False
    else:
        return good()
        
def legal_credit_card_number(number):
    global error
    
    if not re.match("\d{16}", number):
        error = "Invalid credit card number: a credit card number has exactly 16 digits."
        return False
    else:
        return good()
        
def legal_expiry_date(mm, yy):
    global error
    if datetime.date.year > yy or (datetime.date.year == yy and datetime.date.month > mm):
        error = "Invalid expiry date."
        return False
    else:
        return good()
        
def total_books(db):
    total_price = 0
    
    for isbn in basket:
        db.execute("SELECT price FROM Books WHERE isbn = :isbn", {"isbn": isbn})
        row = db.fetchone()
        
        if row:
            total_price += float(row["price"])
        
    return total_price
            
def authenticate(username, password, db):
    global error
    global login
    
    error = "Authentication error: "
    
    if login:
        error = "A user is already logged in."
    elif legal_username(username):
        db.execute("SELECT * FROM Users WHERE username = :uname", {"uname": username})
        
        row = db.fetchone()        
        if not row:
            error += "username '" + username + "' does not exist."
        elif password != row["password"]:
            error += "incorrect username or password."
        else:
            login = row
            login["password"] = ""
            return good()
    else:
        error += "incorrect username or password."
    return False
    
def search_books(criteria, category, db):
    booklist = []
    
    if (category == "isbn" and legal_isbn(criteria)):
        db.execute("SELECT * FROM Books WHERE isbn = :criteria", {"criteria": criteria})
    else:
        db.execute("SELECT * FROM Books WHERE :cat REGEXP :crit", {"cat": category, "crit": cirteria})

    while True:
        row = db.fetchone()
        if row:
            booklist.append(row)
        else:
            break
    return booklist
    
def read_basket(db):
    global basket
    
    db.execute("SELECT * FROM :login", { "login": login["username"] })
    
    while True:
        row = db.fetchone()
        if row:
            basket[row["isbn"]] = row["quantity"]
        else:
            break
            
def write_basket(db):
    db.execute("DROP TABLE IF EXISTS :user", { "user": login["username"] })
    db.execute("CREATE TABLE :user(isbn TEXT PRIMARY KEY, quantity INT)", { "user": login["username"]})
    
    for k, v in basket:
        db.execute("INSERT INTO :user VALUES(:isbn, :quantity)", { "user": login["username"], "isbn": k, "quantity": v })

def delete_basket(isbn, db):
    global basket
    try:
        basket[isbn] -= 1
        if basket[isbn] <= 0:
            basket.remove(isbn)
        write_basket(db)
    except Exception:
        error = "Not in basket"
        
def add_basket(isbn, db):
    global basket
    try:
        basket[isbn] += 1
    except Exception:
        basket[isbn] = 1
        
    write_basket(db)
    
def count_basket():
    items = 0
    for i in basket:
        items += i
    return items
    
import render

render.html_header("Mekong", {"username": "cjdb"}, {"12345": 1})
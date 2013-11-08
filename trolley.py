import database as dbase
import sqlite3 as lite

import books

basket_db = "data/main.db"

def read_basket(username, order, asc):
    db = dbase.db_init(basket_db)
    rows = None
    
    with db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("SELECT * FROM Baskets WHERE username = ? ORDER BY (SELECT %s FROM Books WHERE Books.isbn = isbn) %s" % (dbase.sanitise(order), dbase.sanitise(asc)), [username])
        
        rows = cursor.fetchall()
    return rows
    

def delete_basket(username, isbn, quantity):
    db = dbase.db_init(basket_db)
    
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Baskets WHERE username = ? AND isbn = ?", [username, isbn])
        
        book = cursor.fetchone()
        if book:
            new_quantity = book["quantity"] - quantity
            if new_quantity > 0:
                cursor.execute("UPDATE Baskets SET quantity = ? WHERE username = ? AND isbn = ?", [new_quantity, username, isbn])
            else:
                cursor.execute("DELETE FROM Baskets WHERE username = ? AND isbn = ?", [username, isbn])
        
def add_basket(username, isbn, quantity):
    db = dbase.db_init(basket_db)
    
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Baskets WHERE username = ? AND isbn = ?", [username, isbn])
        
        book = cursor.fetchone()
        if book:
            cursor.execute("UPDATE Baskets SET quantity = ? WHERE username = ? AND isbn = ?", [book["quantity"] + quantity, username, isbn])
        else:
            cursor.execture("INSERT INTO Baskets VALUES(?, ?, ?)", [username, isbn, quantity])
            
def set_basket(username, isbn, quantity):
    db = dbase.db_init(basket_db)
    
    with db:
        cursor = db.cursor()
       
        book = cursor.fetchone()
       
        if book:
            if quantity > 0:
                cursor.execute("UPDATE Baskets SET quantity = ? WHERE username = ? AND isbn = ?", [quantity, username, isbn])
            else:
                cursor.execute("DELETE FROM Baskets WHERE username = ? AND isbn = ?", [username, isbn])
        else:
            if quantity > 0:
                cursor.execute("INSERT INTO Baskets VALUES(?, ?, ?)", [username, isbn, quantity])
    
def count_basket(username):
    items = 0
    
    db = dbase.db_init(basket_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Baskets WHERE username = ?", [username])
        
        trolley = cursor.fetchall()
        
        for item in trolley:
            items += item["quantity"]
            
    return items
    
def total_basket(username):
    total_price = 0.00
    
    db = dbase.db_init(basket_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Baskets WHERE username = ?", [username])
        
        trolley = cursor.fetchall()
        
        for item in trolley:
            cursor.execute("SELECT price FROM Books WHERE isbn = ?", [item["isbn"]])
            book = cursor.fetchone()
            total_price += book["price"]
            
        return total_price
        
def quick_trolley(username):
    basket = read_basket(username, "price", "DESC")
    for isbn in basket:
        book = books.present_books(isbn["isbn"], "isbn", "price", "ASC")

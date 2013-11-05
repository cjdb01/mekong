import database as dbase
import sqlite3 as lite
import re

books_db = 'main.db'
    
def legal_isbn(isbn):
    global error
    
    if not re.match("\d{9} (\d|X)", isbn):
        error = "Invalid ISBN '" + isbn + "': an ISBN must be exactly 10 digits."
        return False
    else:
        return good()

def total_books(basket):
    total_price = 0
    db = dbase.db_init(books_db)
    
    with db:
        cursor = db.cursor()
        for isbn in basket:
            cursor.execute("SELECT price FROM Books WHERE isbn = :isbn", {"isbn": isbn})
            row = cursor.fetchone()
            
            if row:
                price = row[0].split('$')
                total_price += float(price[1])
        
    return total_price

def search_books(criteria, category):
    db = dbase.db_init(books_db)
    
    with db:
        cursor = db.cursor()
        if (category == "isbn" and legal_isbn(criteria)):
            cursor.execute("SELECT * FROM Books WHERE isbn = :criteria", {"criteria": criteria})
        else:
            cursor.execute("SELECT * FROM Books WHERE title REGEXP :criteria", {"criteria": criteria})

        booklist = cursor.fetchall()
    return booklist
    
def present_books(criteria, category):
    booklist = search_books(criteria, category)
    
    if not booklist:
        print "No items match your search."
    
    for book in booklist:
        
        print book["title"], "...", book["price"]
        print "Author(s):", book["authors"]
        print "Pages:", book["numpages"], " ; ISBN:", book["isbn"]
        print "Publisher:", book["publisher"], " ; Publication date:", book["publication_date"]
        print "Catalogue:", book["catalog"], " ; Binding:", book["binding"]
        print
        print
        print re.sub(r"<[^>]+>(.*)", r"\1", book["productdescription"])
        print
        print
        print
        print
        print
import re
import sqlite as lite

file = open(books.json)

db = lite.connect("books.db")

def regexp(expr, item):
    expr = re.escape(expr)
    reg = re.compile(expr)
    return reg.search(item) is not None

with db:
    con.create_function("REGEXP", 2, regexp)
    cursor = db.cursor()
    cursor.execute("CREATE TABLE Books(isbn TEXT PRIMARY KEY, ean TEXT, catalog TEXT, binding TEXT, num_pages INT, smallimageurl TEXT, mediumimagewidth INT, publicationdate TEXT, productdescription TEXT, publisher TEXT, authors TEXT, largeimageheight INT, mediumimageheight INT, largeimagewidth INT, salesrank INT, smallimageheight INT, smallimagewidth INT, price TEXT, title TEXT, year TEXT)")
    
    book = {}
    collecting = False
    for line in file:
        line.rstrip('\n')
        
        if re.match("\s*\"([^\"]+)\"\s*:\s*\"(.*)\",?\s*", line):
            field = re.sub(r"\s*\"([^\"]+)\"\s*:\s*\"(.*)\",?\s*", r"\1", line)
            book[field] = re.sub(r"\s*\"([^\"]+)\"\s*:\s*\"(.*)\",?\s*", r"\2", line)
        elif re.match("\s*\"([^\"]+)\"\s*:\s*\[\s*", line):
            field = re.sub(r"\s*\"([^\"]+)\"\s*:\s*\[\s*", r"\1", line)
            collecting = True
        elif collecting == True and re.match("\s*\"(.*)\"\s*,?\s*", line):
            books[isbn][field].append(re.sub(r"\s*\"(.*)\"\s*,?\s*", r"\1"))
        elif collecting == True and re.match("\s*\]\s*,?\s*"):
            collecting = False
        elif re.match("\s*},", line):
            cursor.execute("INSERT INTO Books VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [book["isbn"], book["ean"], book["catalog"], book["binding"], book["num_pages"], book["smallimageurl"], book["mediumimagewidth"], book["publicationdate"], book["productdescription"], book["publisher"], book["authors"], book["largeimageheight"], book["mediumimageheight"], book["largeimagewidth"], book["salesrank"], book["smallimageheight"], book["smallimagewidth"], book["price"], book["title"], book["year"]])
            
    cursor.execute("SELECT isbn FROM Books WHERE title REXEXP :Harry", {"Harry": "Harry"})
    
    while True:
        rows = cursor.fetchone()
        if not row:
            break
        else:
            print row["isbn"]
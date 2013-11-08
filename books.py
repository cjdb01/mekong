import database as dbase
import sqlite3 as lite
import re

books_db = 'data/main.db'

def legal_isbn(isbn):
    global error
    
    if not re.match("\d{9} (\d|X)", isbn):
        error = "Invalid ISBN '" + isbn + "': an ISBN must be exactly 10 digits."
        return False
    else:
        return good()

def search_books(criteria, category, order, asc):
    db = dbase.db_init(books_db)
    
    with db:
        cursor = db.cursor()
        if (category == "isbn" and legal_isbn(criteria)):
            cursor.execute("SELECT * FROM Books WHERE isbn = ?", [criteria])
        else:
            cursor.execute("SELECT * FROM Books WHERE " + dbase.sanitise(category) + " REGEXP ? ORDER BY " + dbase.sanitise(order) + " " + dbase.sanitise(asc), [criteria])

        booklist = cursor.fetchall()
    return booklist
    
def present_books(criteria, category, order, asc, account):
    booklist = search_books(criteria, category, order, asc)
    
    if not booklist:
        print "No items match your search."
    
    for book in booklist:
        print """
                        <div class="media">
                          <a class="pull-left" href="#">
                            <img class="media-object alt="No picture to display" src="%s">
                          </a>
                          <div class="media-body">
                            <div class="row">
                              <div class="col-md-9">
                                <h3 class="media-heading">%s</h3>
                              </div>
                              <div class="col-md-2" align="right">
                                <h3 class="media-heading">$%.2f</h3>
                              </div>
                            </div>
  
                            <div class="row">
                              <div class="col-md-6">
                                <strong>%s</strong>
                              </div>
                              <div class="col-md-6" align="right">
                                <strong>Published by %s</strong>
                              </div>
                            </div>
    
                            %s
                          </div>
                          <br/>
                        </div>
""" % (book["mediumimageurl"], book["title"], book["price"], book["authors"], book["publisher"], book["productdescription"])
        if account:
            print """
                        <div class="media">
                          <form action="mekong.cgi?page=search" method="post">
                            <div class="row">
                              <div class="col-md-9"></div>
                              <div class="col-md-1">
                                <input type="text" class="form-control" name="qty" placeholder="1" style="width: 60px;">
                                <input type="hidden" name="isbn" value="%s">
                                <input type="hidden" name="criteria" value="%s">
                                <input type="hidden" name="category" value="%s">
                                <input type="hidden" name="order" value="%s">
                                <input type="hidden" name="asc" value="%s">
                              </div>
                              <div class="col-md-1">
                                <button type="submit" class="btn btn-success" name="isbn-to-add">Add to trolley</button>
                              </div>
                            </div>
                          </form>
                        </div>
                        <br />
                        <br />
""" % (book["isbn"], criteria, category, order, asc)

def quick_trolley_books(isbn, qty):
    book = search_books(isbn, "isbn", "price", "asc")
    
    print """
                        <div class="media">
                          <a class="pull-left" href="#">
                            <img class="media-object alt="No picture to display" src="%s">
                          </a>
                          <div class="media-body">
                            <div class="row">
                              <div class="col-md-9">
                                <h4 class="media-heading">%s</h4>
                              </div>
                              <div class="col-md-2" align="right">
                                <h4 class="media-heading">$%.2f</h4>
                              </div>
                            </div>
  
                            <div class="row">
                              <div class="col-md-6">
                                <strong>%s</strong>
                              </div>
                              <div class="col-md-6" align="right">
                                <strong>In basket: %d</strong>
                              </div>
                            </div>
                          </div>
                          <br/>
                        </div>
""" % (book["smallimageurl"], book["title"], book["price"], book["authors"], qty)
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
    
def product_description(criteria, category, order, asc, account, book):
    str = """
<div id="%s" class="modal fade" tabindex="-1" style="display: none; min-width: 80%%; left: 23%%; right: 30%%;">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Product description</h4>
      </div>
      <div class="modal-body">
        <div class="panel-body">
          <div class="media">
              <a class="pull-left" href="#">
                
                <img class="media-object alt="No picture to display" src="%s" style="max-width:500px;">
              </a>
              <div class="media-body">
                <div class="row">
                  <div class="col-md-10">
                    <h3 class="media-heading">%s</h3>
                  </div>
                  <div class="col-md-1" align="right">
                    <h3 class="media-heading">$%.2f</h3>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-10">
                    <strong>Authors</strong>
                  </div>
                  <div class="col-md-2">
                    <strong>Publisher</strong>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-10">
                    %s
                  </div>
                  <div class="col-md-2">%s</div>
                </div>
                <br/>
                <div class="row">
                  <div class="col-md-10">
                    <strong>
                      Pages
                    </strong>
                  </div>
                  <div class="col-md-2">
                    <strong>
                      Publication date
                    </strong>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-10">
                    %d
                  </div>
                  <div class="col-md-2">
                    %s
                  </div>
                </div>
                <br/>
                <div class="row">
                  <div class="col-md-10">
                    <strong>
                      ISBN
                    </strong>
                  </div>
                  <div class="col-md-2">
                    <strong>
                      Current rank
                    </strong>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-10">
                    %s
                  </div>
                  <div class="col-md-2">
                    %s
                  </div>
                </div>
                <br/>
                <div class="row">
                  <div class="col-md-10">
                    <strong>
                      Product description
                    </strong>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-10">
                    %s
                  </div>
                </div>
              <br/>
            </div>
        </div>
      </div>
      <div class="modal-footer">
        <form action="mekong.cgi?page=search" method="post">
          <button type="button" class="btn btn-default" data-dismiss="modal">
            Close
          </button>
""" % (book["isbn"], book["largeimageurl"], book["title"], book["price"], book["authors"], book["publisher"], book["numpages"], book["publication_date"], book["isbn"], book["salesrank"], book["productdescription"])
    if account:
        str += """
  <input type="hidden" name="isbn" value="%s">
  <input type="hidden" name="criteria" value="%s">
  <input type="hidden" name="category" value="%s">
  <input type="hidden" name="order" value="%s">
  <input type="hidden" name="asc" value="%s">
  <button type="submit" class="btn btn-success" name="qty" value="1">Add to trolley</button>
""" % (book["isbn"], criteria, category, order, asc)
    str += """
    </form>
      </div>
    </div><!-- /.modal-content -->
  </div>
</div>
"""
    return str
    
def present_books(criteria, category, order, asc, account, firstlook):
    if not "criteria":
        print "No items match your search"
        return
    if not firstlook:
        booklist = search_books(criteria, category, order, asc)
    else:
        booklist = first_look()
    
    if not booklist:
        print "No items match your search."
    
    for book in booklist:
        if len(book["productdescription"]) > 30:
            description = ' '.join(book["productdescription"].split(' ')[:30]) + "..."
        else:
            description = book["productdescription"]
        print """
                        <div class="media-body">
                            <div class="row">
                              <div class="col-md-2">
                                <center>
                                  <a href="#%s" data-toggle="modal">
                                    <img class="media-object alt="No picture to display" src="%s">
                                  </a>
                                </center>
                              </div>
                              <div class="col-md-8">
                                <a href="#%s" data-toggle="modal">
                                  <h3 class="media-heading">%s</h3>
                                </a>
                              </div>
                              <div class="col-md-2" align="right">
                                <h3 class="media-heading">$%.2f</h3>
                              </div>
                              </br>
                              <div class="col-md-7">
                                <strong>%s</strong>
                              </div>
                              <div class="col-md-3" align="right">
                                <strong>Published by %s</strong>
                              </div>
                              <br/>
                              <div class="col-md-10">
                              %s
                              </div>
                            </div>
                          </div>
                        
                        
""" % (book["isbn"], book["mediumimageurl"], book["isbn"], book["title"], book["price"], book["authors"], book["publisher"], description)
        if account:
            print """
                        <div class="media">
                          <form action="mekong.cgi?page=search" method="post">
                            <div class="row">
                              <div class="col-md-9"></div>
                              <div class="col-md-1">
                                <input type="text" class="form-control" name="qty" placeholder="1" style="width: 60px;" value="1" pattern="\d+">
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
""" % (book["isbn"], criteria, category, order, asc)
        print "<hr/>"

    for book in booklist:
        print product_description(criteria, category, order, asc, account, book)
        
        
def first_look():
    db = dbase.db_init(books_db)
    random_books = []
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Books WHERE salesrank <= 10 ORDER BY salesrank ASC")
       
        books = cursor.fetchall()
        
        for i in range(1, 10):
            random_books.append(books[i])
            
    return random_books
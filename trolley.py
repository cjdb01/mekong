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
        cursor.execute("SELECT * FROM Baskets WHERE username = ? AND isbn = ?;", [username, isbn])
        book = cursor.fetchone()
       
        if book:
            cursor.execute("UPDATE Baskets SET quantity = ? WHERE username = ? AND isbn = ?;", [quantity, username, isbn])
            cursor.execute("DELETE FROM Baskets WHERE quantity <= 0;")
        else:
            if quantity > 0:
                cursor.execute("INSERT INTO Baskets VALUES(?, ?, ?);", [username, isbn, quantity])
    
def count_basket(username):
    items = 0
    
    db = dbase.db_init(basket_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Baskets WHERE username = ?;", [username])
        
        trolley = cursor.fetchall()
        
        for item in trolley:
            items += item["quantity"]
            
    return items
    
def total_basket(username):
    total_price = 0.00
    
    db = dbase.db_init(basket_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Baskets WHERE username = ?;", [username])
        
        trolley = cursor.fetchall()
        
        for item in trolley:
            cursor.execute("SELECT price FROM Books WHERE isbn = ?;", [item["isbn"]])
            book = cursor.fetchone()
            total_price += (book["price"] * book["quantity"])
            
        return total_price

def product_description(book, qty):
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
                  <div class="col-md-2">
                    <strong>Quantity:</strong>
                  </div>
                </div>
                
                <div class="row">
                  <div class="col-md-10">
                    %s
                  </div>
                  <div class="col-md-2">
                    %d
                  </div>
                </div>
              <br/>
            </div>
        </div>
      </div>
      <div class="modal-footer">
        <form action="mekong.cgi?page=trolley" method="post">
        <button type="button" class="btn btn-default" data-dismiss="modal">
          Close
        </button>
    <input type="hidden" name="isbn" value="%s">
    <button type="submit" class="btn btn-success" name="qty" value="1">Add to trolley</button>
    <button type="submit" class="btn btn-danger" name="qty" value="0">Remove from trolley</button>
      </form>
      </div>
    </div><!-- /.modal-content -->
  </div>
</div>
""" % (book["isbn"], book["largeimageurl"], book["title"], book["price"], book["authors"], book["publisher"], book["numpages"], book["publication_date"], book["isbn"], book["salesrank"], book["productdescription"], qty, book["isbn"])
    return str
        
def present_trolley(username):
    str = ""
    db = dbase.db_init(basket_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Baskets WHERE username = ?;", [username])
        
        trolley = cursor.fetchall()
        
        for item in trolley:
            cursor.execute("SELECT * FROM Books WHERE isbn = ?;", [item["isbn"]])
            
            book = cursor.fetchone()
            
            str += """
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
          <h4 class="media-heading">%s</h4>
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
    </div>
  </div>
<div class="media">
  <form action="mekong.cgi?page=trolley" method="post">
    <div class="row">
      <div class="col-md-7"></div>
      <div class="col-md-1"><strong>Quantity:</strong></div>
      <div class="col-md-1">
        <input type="text" class="form-control" name="qty" placeholder="%d" style="width: 60px;" />
        <input type="hidden" name="isbn" value="%s" />
      </div>
      <div class="col-md-1">
        <button type="submit" class="btn btn-success" name="isbn-to-add">Update</button>
      </div>
      <div class="col-md-1">
        <button type="submit" class="btn btn-danger" name="remove" onclick="document.getElementsByName('qty')[0].value = 0;">Remove</button>
      </div>
    </div>
  </form>
</div>
<hr/>
""" % (book["isbn"], book["smallimageurl"], book["isbn"], book["title"], book["price"], book["authors"], book["publisher"], item["quantity"], book["isbn"])
            
            str += product_description(book, item["quantity"])
    str += """
<div class="col-md-8"></div>
<div class="col-md-2">
  <h4>Total price: $%.2f</h4>
</div>
<div class="mod-md-2">
  <form action="mekong.cgi?page=checkout" method="post">
    <button type="submit" class="btn btn-info">
      Proceed to checkout
    </button>
  </form>
</div>
""" % total_basket(username)
    return str
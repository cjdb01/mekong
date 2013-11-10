import database as dbase
import re

order_db = "data/main.db"

error = ""

def have_orders(username):
    db = dbase.db_init(order_db)
    
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Orders WHERE username = ?", [username])
        
        orders = cursor.fetchall()
        
        if not orders:
            error = "You haven't made any purchases. Make one today!"
            return False
        else:
            return True

def retrieve_orders(account):
    db = dbase.db_init(order_db)
    
    with db:
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM Orders WHERE username = ? ORDER BY order_number DESC", [account["username"]])
        
        orders = cursor.fetchall()

        for order in orders:
            isbn_list = order["isbns"].split(';')

            books = ""
            for i in isbn_list:
                isbn = re.sub(r"(.{10})\*\d+", r"\1", i)
                qty = re.sub(r".{10}\*(\d+)", r"\1", i)
                cursor.execute("SELECT * FROM Books WHERE isbn = ?", [isbn])
                book = cursor.fetchone()
                print isbn
                if book:
                    books += """
<div class="row">
  <div class="col-md-2">
    %s
  </div>
  <div class="col-md-2">
    %s
  </div>
  <div class="col-md-2">
    %s
  </div>
  <div class="col-md-2">
    %s
  </div>
  <div class="col-md-2">
    $%s
  </div>
  <div class="col-md-1">
    %s
  </div>
</div>
<hr/>
""" % (book["title"], book["authors"], book["publisher"], isbn, book["price"], qty)
            str = """
div class="panel-group" id="accordion">
  <div class="panel panel-default">
    <div class="panel-heading">
      <h4 class="panel-title">
        <a data-toggle="collapse" data-parent="#accordion" href="#collapseOne">
            Order #%d
        </a>
      </h4>
    </div>
    <div id="collapseOne" class="panel-collapse collapse in">
      <div class="panel-body">
        <div class="row">
          <div class="col-md-3">
            <label>Order placed</label><br/>
            %s
            <hr/>
            <label>Total price</label><br/>
            $%.2f
            <hr/>
            <label>Credit card</label><br/>
            XXXX XXXX XXXX %s<br/><br/>
            <label>Expires</label><br/>
            %s
            <hr/>
            <label>Shipped to</label><br/>
            %s %s,<br/>
            %s,<br/>
            %s %s, %s
          </div>
          <div class="col-md-9">
            <div class="row">
              <div class="col-md-2">
                <label>Title</label>
              </div>
              <div class="col-md-2">
                <label>Author</label>
              </div>
              <div class="col-md-2">
                <label>Publisher</label>
              </div>
              <div class="col-md-2">
                <label>ISBN</label>
              </div>
              <div class="col-md-2">
                <label>Price</label>
              </div>
              <div class="col-md-1">
                <label>Quantity</label>
              </div>
            </div>
            %s
          </div>
        </div>
      </div>
    </div>
  </div>
  
</div>
""" % (order["order_number"], order["date_of_order"], order["total_price"], order["last_four"], order["expiry"], account["firstname"],\
                     account["lastname"], account["address"], account["suburb"], account["state"], account["postcode"], books)
            print str

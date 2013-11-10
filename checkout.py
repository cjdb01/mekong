import database as dbase
import hashlib
import trolley
from datetime import date
from datetime import datetime

error = ""

checkout_db = "data/main.db"

def print_checkout(account):
    return """
<form action="mekong.cgi?page=order-submitted" method="post">
  <div class="form-group">
    <label for="credit-card">
      Credit card
    </label>
    <input name="credit-card" class="form-control" type="number" placeholder="1234 1234 1234 1234" pattern="(\d{4} ){3}\d{4}" style="width: 185px;" required/>
  </div>
  <div class="row">
    <div class="col-md-2">
      <label>
        Expiry Date
      </label>
    </div>
  </div>
  <div class="row">
    <div class="form-group">
      <div class="col-md-1">
        <select class="form-control" style="width: 80px;" name="month">
          <option value="1">Jan</option>
          <option value="2">Feb</option>
          <option value="3">Mar</option>
          <option value="4">Apr</option>
          <option value="5">May</option>
          <option value="6">Jun</option>
          <option value="7">Jul</option>
          <option value="8">Aug</option>
          <option value="9">Sep</option>
          <option value="10">Oct</option>
          <option value="11">Nov</option>
          <option value="12">Dec</option>
        </select>
      </div>
      <div class="col-md-1">
        <select class="form-control" style="width: 90px;" name="year">
          <option value="2013">2013</option>
          <option value="2014">2014</option>
          <option value="2015">2015</option>
          <option value="2016">2016</option>
          <option value="2017">2017</option>
          <option value="2018">2018</option>
          <option value="2019">2019</option>
          <option value="2020">2020</option>
          <option value="2021">2021</option>
          <option value="2022">2022</option>
          <option value="2023">2023</option>
          <option value="2024">2024</option>
        </select>
      </div>
    </div>
  </div>
  <br/>
  <div class="form-group">
    <label>Post to:</label><br/>
    %s %s<br/>
    %s,<br/>
    %s, %s, %s<br/>
  </div>

  <div class="row">
    <div class="col-md-2">
      <label>
        Postage
      </label>
    </div>
  </div>
  <div class="form-group">
    <select class="form-control" style="width: 320px;" name="postage">
      <option value="1">Standard (3 to 5 working days)</option>
      <option value="2">Registered (3 to 5 working days)</option>
      <option value="3">Express (1 to 2 working days)</option>
      <option value="4">Registered Express (1 to 2 working days)</option>
    </select>
  </div>


  <button type="submit" class="btn btn-success">Submit order</button>
  </form>
""" % (account["firstname"], account["lastname"], account["address"], account["suburb"], account["state"], account["postcode"])

def execute_order(account, month, year, credit_card, postage):
    global error
    if year == date.today().year and month < date.today().month:
        error = "Your card has expired."
    else:
        db = dbase.db_init(checkout_db)
        
        with db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Baskets WHERE username = ?;", [account["username"]])
            
            books = cursor.fetchall()
            if books:
                isbn = ""
                hash = hashlib.sha512(credit_card)
                last_four = credit_card[-4:]
                now = datetime.now()
                for b in books:
                   isbn += "%s*%d;" % (b["isbn"], b["quantity"])
                
                cursor.execute("INSERT INTO Orders(username, credit_card, expiry, last_four, isbns, date_of_order, postage, total_price) VALUES(?, ?, ?, ?, ?, ?, ?, ?);",\
                                             [account["username"], hash.hexdigest(), "%s/%s" % (str(month), str(year)), last_four, isbn, now, postage, trolley.total_basket(account["username"])])
                cursor.execute("DELETE FROM Baskets WHERE username = ?;", account["username"])
                return True
            else:
                error = "Your trolley is empty!"
    return False
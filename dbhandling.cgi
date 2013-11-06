#!/usr/bin/python -u

import cgi
import cgitb
import datetime
import hashlib
import re
import sqlite3 as lite
import sys

account = {}

##################################################################################################################################################
# Database code
def regexp(expr, item):
    expr = re.escape(expr)
    reg = re.compile(expr)
    return reg.search(item) is not None
    
def sanitise(expr):
    return re.escape(expr)

def db_init(path):
    db = lite.connect(path)
    
    try:
        db.create_function("REGEXP", 2, regexp)
        db.row_factory = lite.Row
    except Exception:
        sys.exit("Couldn't establish a connection with database.")
    
    return db

##################################################################################################################################################
# Login code
login_db = "main.db"


def legal_username(username):
    length = len(username)
    
    error = "Invalid username '" + username + "': usernames must"
    
    if not re.match('[A-Za-z_]\w+', username):
        error += "start with a letter and only contain letters, numbers and underscores."
    elif length < 3 or length > 8:
        error += "be 3 - 8 characters long."
    else:
        return ""
    return error
    
def unique_username(username):
#    db = db_init(login_db)
#    with db:
#        cursor = db.cursor()
#        cursor.execute("SELECT * FROM Users WHERE username = ?", [username])
#        
#        rows = cursor.fetchone()
#        
#    return rows is None
    return True
    
def legal_password(password, username, first_name, last_name):
    length = len(password)
    
    error = "Invalid password: passwords must "
    
    if length < 6 or length > 64:
        error += "be 6 - 64 characters long."
    elif not re.search("[A-Z]", password):
        error += "contain at least one upper case letter."
    elif not re.search("[a-z]", password):
        error += "contain at least one lower case letter."
    elif not re.search("\d", password):
        error += "contain at least one numeral."
    elif not re.search("\W", password):
        error += "contain at least one special character."
    elif re.search(username, password, re.IGNORECASE) or re.search(first_name, password, re.IGNORECASE) or re.search(last_name, password, re.IGNORECASE):
        error += "not contain usernames, first names, or last names."
    else:
        return ""
    return error
    
def authenticate_user(username, password):
    error = "Authentication error: "
    
    if account:
        error = "A user is already logged in."
    elif legal_username(username):
        db = db_init(login_db)
    
        with db:
            cursor = db.cursor()
            db.execute("SELECT * FROM Users WHERE username = :uname", {"uname": username})
            
            row = db.fetchone()        
            if not row:
                error += "username '" + username + "' does not exist."
            elif password != row["password"]:
                error += "incorrect username or password."
            else:
                account = row
                return ""
    else:
        error += "incorrect username or password."
    return error
    
def create_account(user):
    error = legal_username(user["username"])
    if not error:
        if not unique_username(user["username"]):
            error = "Create account error: username is not unique"
        else:
            error = legal_password(user["password"], user["username"], user["firstname"], user["lastname"])
            if not error:
                db = db_init(login_db)
        
                with db:
                    cursor = db.cursor()
                
                    hash = hashlib.sha512()
                    hash.update(user["password"])
                    pwd = hash.hexdigest()
                
                    cursor.execute("INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [user["username"], pwd, user["firstname"], user["lastname"],\
                                            user["address"], user["suburb"], user["state"], user["postcode"], user["dob"], user["email"], user["phone"], user["sex"], False])
                    # TODO: send confirmation email
    return error
    
def change_password(username, current_password, new_password):
    hash = hashlib.sha512()
    hash.update(current_password)
    
    db = db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users")
        
        row = cursor.fetchone()
        
        error = legal_password(new_password, row["username"], row["firstname"], row["lastname"])
        if row["password"] == hash.hexdigest() and not error:
            hash = hashlib.sha512()
            hash.update(new_password)
            
            if hash.hexdigest() != row["password"]:
                cursor.execute("UPDATE Users SET password = ? WHERE username = ? AND password = ?", [hash.hexdigest(), username, row["password"]])
            else:
                error = "Password update error: new password cannot match old password."
        elif row["password"] != hash.hexdigest():
            error = "Password update error: incorrect password."
                
    return error

def reset_password(username):
    return 0 # TODO

##################################################################################################################################################
# Render code

def login_details():
    print """
              <ul class="nav navbar-nav navbar-right">
              <!-- TODO: FIX SO THAT IT SAYS YOUR USERNAME AND TAKES YOU TO A PAGE IF YOU CLICK ON IT! -->
                <li id="fat-menu" class="dropdown">
                  <a id="drop3" class="dropdown-toggle" data-toggle="dropdown" role="button" href="#">
                    Login
                    <b class="caret"></b>
                  </a>
                  <div class="dropdown-menu" style="padding: 15px; padding-bottom: 0px; width: 250px;" aria-labelledby="drop3" role="menu">
                    <form>
                      <label for="login">Login</label>
                      <input type="text" id="username" class="form-control" placeholder="Enter username" style="margin-bottom: 5px;"></input>
                      <input type="password" id="password" class="form-control" placeholder="Enter password" style="margin-bottom: 10px;"></input>
                      <div class="checkbox">
                        <label>
                          <input id="remember-me" type="checkbox"> Remember me
                        </label>
                      </div>
                      <input type="submit" id="login" class="btn btn-primary" style="margin-bottom: 10px; width: 215px" value="Login"></input>
                      <button type="submit" id="forgot" class="btn btn-danger" style="margin-bottom: 10px; width: 215px">Forgot Password</button>
                      <button type="submit" id="create" class="btn btn-warning" style="margin-bottom: 10px; width: 215px">Create account</button>
                    </form>
                  </div>
                </li> 
              </ul>
"""

def print_header():
    print "Content-type: text/html"
    print # Do not remove
    print """
    <!DOCTYPE html>
    <html lang="en">
    <!-- Code taken from Bootstrap website -->
    <html>
      <head>
        <title>Mekong Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- Bootstrap -->
        <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">

        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
          <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
          <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
        <![endif]-->
      </head>
      <body>
        <div class="navbar navbar-inverse navbar-fixed-top">
          <div class="container">
            <nav class="collapse navbar-collapse navbar-collapse" role="navigation">
              <ul class="nav navbar-nav">
                <li><a href="#">Home</a></li>
                <li><a href="#">Recommendations</a></li>
                <li><a href="#">Trolley</a></li>
                <li><a href="#">Checkout</a></li>
              </ul>
              <form class="navbar-form navbar-left" role="search">
                <div class="form-group">
                    <input type="text" class="form-control" style="width: 300px;" placeholder="Quick title search"></input>
                </div>
                <button type="submit" class="btn btn-default">Search</button>
              </form>
              <ul class="nav navbar-nav">
                <li><a href="#">Advanced search</a></li>
              </ul>
"""
    login_details()
    print """
            </nav>
          </div>
        </div>

        <div id="content" class="container">
          <div class="jumbotron">
            <h1>mekong.com.au</h1>
            <p>Welcome to mekong.com.au</p>
          </div>
        </div>
        
        <div class="bs-old-docs">
            <p><br></p>
        </div>
"""

def print_body_search():
    print """
        <div class="container bs-docs-container">
          <div class="row">
            <div class="col-md-3">
              <div class="panel panel-info" style="min-height: 300px;">
                <div class="panel-heading">
                    <h3 class="panel-title">
                      <strong>Quick trolley</strong><br>
                      <div class="row">
                        <div class="col-md-6">
                          0 items
                        </div>
                        <div class="col-md-6" align="right">
                          $0.00
                        </div>
                      </div> 
                    </h3>
                </div>
                <div class="panel-body">
                    Your trolley is empty...
                </div>
              </div>
            </div>
            <div class="col-md-9" role="main">
              <div class="panel panel-info fixed-left" style="min-height: 300px;">
                <div class="panel-heading">
                  <h3 class="panel-title">Search results</h3>
                </div>
                <div class="panel-body">
                  No results to display.
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://code.jquery.com/jquery.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="js/bootstrap.js"></script>
        
      </body>
    </html>
"""

form = cgi.FieldStorage()

print_header()
print_body_search()
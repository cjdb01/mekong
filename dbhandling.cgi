#!/usr/bin/python -u

from os import environ

import cgi
import cgitb
import datetime
import hashlib
import re
import sqlite3 as lite
import sys

error = ""
login = {}

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
    
    
#############################################

def login_details():
    print """
                <ul class="nav navbar-nav navbar-right">
                    <li id="fat-menu" class="dropdown">
                        <a id="drop3" class="dropdown-toggle" data-toggle="dropdown" role="button" href="#">
"""
    if not login:
        print "Login"
    else:
        print login["username"]

    print """
                            <b class="caret"></b>
                        </a>
"""

    if not login:
        print """
                        <div class="dropdown-menu" style="padding: 15px; padding-bottom: 0px; width: 250px;" aria-labelledby="drop3" role="menu">
                            <form action="mekong.cgi" method="post">
                                <label for="login">Login</label>
                                <input type="text" id="username" class="form-control" placeholder="Enter username" style="margin-bottom: 5px;"></input>
                                <input type="password" id="password" class="form-control" placeholder="Enter password" style="margin-bottom: 10px;"></input>
                                <div class="checkbox">
                                    <label>
                                        <input id="remember-me" type="checkbox"> Remember me
                                    </label>
                                </div>
                                <button type="submit" id="login" class="btn btn-primary" style="margin-bottom: 10px; width: 215px">Login</button>
                                <button type="submit" id="login" class="btn btn-danger" style="margin-bottom: 10px; width: 215px">Forgot Password</button>
                                <button type="submit" id="create" class="btn btn-warning" style="margin-bottom: 10px; width: 215px">Create account</button>
                            </form>
                        </div>
"""
    else:
        print """
                        <ul class="dropdown-menu" aria-labelledby="drop3" role="menu">
                            <li role="presentation">
                                <a href="mekong.cgi?myaccount">Account</a>
                            </li>
                            <li role="presentation">
                                <a href="mekong.cgi?myhistory">History</a>
                            </li>
                            <li role="presentation">
                                <a href="mekong.cgi?mysettings">Settings</a>
                            </li>
                        </ul>
"""
    print """
                    </li> 
                </ul>
"""

def cookie_output(form):
    username = form.getvalue("username")
    password = form.getvalue("password")
    remember = form.getvalue("remember")
    
    expires = ""
    if remember:
        expires = "Monday, 31-Dec-2040 23:59:59 GMT"
    else:
        expires = datetime.datetime.fromtimestamp(time.time()).strftime('%A, %d-%m-%Y ' + str(datetime.datetime.now().hour + 1) + ':%M:%S GMT')
    
    to_print = 'Set-Cookie: UserID=' + username + '; Password=' + password + '; Exipres=' + expires + '; Set-Cookie-Domain=www.cse.unsw.edu.au/~chrisdb/mekong.cgi'
    print to_print

def html_header(title, form):

    print "Content-Type: text-html"
    cookie_output(form)

    cookie_username = ""
    cookie_password = ""
    authenticated = -1
    if environ.haskey('HTTP_COOKIE'):
        for cookie in map(strip, split(environ['HTTP_COOKIE'], ';')):
            (key, value) = split(cookie, '=')
                if key == 'UserID':
                    cookie_username = value
                elif key == 'Password':
                    cookie_passowrd = value
    if cookie_username != "" and cookie_password != "":
        authenticated = int(authenticate(cookie_username, cookie_password)
    
    print
    print """
<!DOCTYPE html>
<html lang="en">
<!-- Code taken from Bootstrap website -->
<html>
  <head>
    <title>
"""
    print title
    print """
    </title>
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
                    <li><a href="mekong.cgi">Home</a></li>
                    <li><a href="mekong.cgi?recommendations">Recommendations</a></li>
                    <li><a href="mekong.cgi?trolley">Trolley</a></li>
                    <li><a href="mekong.cgi?checkout">Checkout</a></li>
                </ul>
                <form class="navbar-form navbar-left" role="search" action="mekong.cgi" method="post">
                    <div class="form-group">
                        <input type="text" class="form-control" style="width: 300px;" placeholder="Quick title search"></input>
                    </div>
                    <button type="submit" class="btn btn-default">Search</button>
                </form>
                <ul class="nav navbar-nav">
                    <li>
                        <a href="mekong.cgi?advanced-search">Advanced search</a>
                    </li>
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
"""
    if authenticated == 0:
        print """
        <div class="alert alert-danger fade in">
            <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
                ×
            </button>
            <strong>
"""
        print error
        print """
            </strong>
        </div>
"""
    elif authenticated == 1 and not form.getvalue("prevlogin"):
        print """
        <div class="alert alert-danger fade in">
            <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
                ×
            </button>
            <strong>Welcome,
"""
        print login["username"] + "!"
        print """
            </strong>
"""
    print """
    </div>
    
    <div class="bs-old-docs">
        <p><br></p>
    </div>
    
    <div class="container bs-docs-container">
        <div class="row">
            <div class="col-md-3">
                <div class="panel panel-info" style="min-height: 300px;">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <strong>Quick trolley</strong><br>
                            <div class="row">
                                <div class="col-md-6">
"""
    items = count_basket()
    if items == 1:
        print "1 item"
    else:
        print items, "items"
    print """  
                                </div>
                                <div class="col-md-6" align="right">
"""
    if items == 0:
        print "$0.00"
    else:
        print "$%.2f" % total_books()
    print """
                                </div>
                            </div> 
                        </h3>
                    </div>
                    <div class="panel-body">
"""
    if items == 0:
        print "Your trolley is empty..."
    else:
        print_cart()
    print """
                    </div>
                </div>
            </div>
            <div class="col-md-9" role="main">
                <div class="panel panel-info fixed-left" style="min-height: 300px;">
                    <div class="panel-heading">
                        <h3 class="panel-title">Search results</h3>
                    </div>
                    <div class="panel-body">
"""
    if not results:
        print "No results to display."
    else:
        print_results(results)
    print """
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://code.jquery.com/jquery.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>

"""

form = cgi.FieldStorage()
html_header("Mekong", form)
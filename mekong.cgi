#!/usr/bin/env python2.7

from os import environ
from datetime import datetime
import cgi, cgitb; cgitb.enable()
import hashlib
import re
import sqlite3 as lite
import sys

import books
import login
import trolley


account = {}

##################################################################################################################################################
# Render code

def alert_message(type, strong, normal):
        print """
        <div class="alert alert-%s fade in">
            <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
                x
            </button>
            <strong>
              %s
            </strong>
            %s
        </div>
""" % (type, strong, normal)

def login_details():
    global account
    print """
              <ul class="nav navbar-nav navbar-right">
                <li id="fat-menu" class="dropdown">
                  <a id="drop3" class="dropdown-toggle" data-toggle="dropdown" role="button" href="#">
"""
    if not account:
        print """
                    Login
                    <b class="caret"></b>
                  </a>
                  <div class="dropdown-menu" style="padding: 15px; padding-bottom: 0px; width: 250px;" aria-labelledby="drop3" role="menu">
                    <form action="mekong.cgi?page=login" method="post">
                      <label for="login">Login</label>
                      <input type="text" name="username" class="form-control" placeholder="Enter username" style="margin-bottom: 5px;"></input>
                      <input type="password" name="password" class="form-control" placeholder="Enter password" style="margin-bottom: 10px;"></input>
                      <div class="checkbox">
                        <label>
                          <input name="remember-me" type="checkbox"> Remember me
                        </label>
                      </div>
                      <button type="submit" id="login" class="btn btn-primary" style="margin-bottom: 10px; width: 215px">Login</button>
                    </form>
                    <form>
                      <button type="submit" id="forgot" class="btn btn-danger" style="margin-bottom: 10px; width: 215px">Forgot Password</button>
                    </form>
                    <form action="mekong.cgi?page=create-account" method="post">
                      <button type="submit" id="create" class="btn btn-warning" style="margin-bottom: 10px; width: 215px">Create account</button>
                    </form>
"""
    else:
        print account["username"]
        print """
                    <ul class="dropdown-menu" aria-labelledby="drop3" role="menu">
                      <li role="presentation">
                        <a href="mekong.cgi?page=myaccount">Account</a>
                      </li>
                      <li role="presentation">
                        <a href="mekong.cgi?page=myhistory">History</a>
                      </li>
                      <li role="presentation">
                        <a href="mekong.cgi?page=mysettings">Settings</a>
                      </li>
                      <li role="presentation">
                        <a href="mekong.cgi?page=logout">Log out</a>
                      </li>
                    </ul>
"""
    print """
                  </div>
                </li> 
              </ul>
"""

def print_registration():
    print """
                      <form action="mekong.cgi?page=application-submitted" method="post">
                        <div class="form-group">
                          <label for="username-reg">
                            Username
                          </label>
                          <input name="username-reg" class="form-control" type="text" placeholder="Enter username"></input>
                        </div>
                        <div class="form-group">
                          <label for="password-reg">
                            Password
                          </label>
                          <input name="password-reg" class="form-control" type="password" placeholder="Enter password"></input>
                        </div>
                        <div class="form-group">
                          <label for="confirmpass-reg">
                            Confirm password
                          </label>
                          <input name="confirmpass-reg" class="form-control" type="password" placeholder="Enter password" ></input>
                        </div>
                        <div class="form-group">
                          <label for="email-reg">
                            Email
                          </label>
                          <input name="email-reg" class="form-control" type="email" placeholder="Enter email"></input>
                        </div>
                        <div class="form-group">
                          <label for="firstname-reg">
                            First name
                          </label>
                          <input name="firstname-reg" class="form-control" type="text" placeholder="e.g. John"></input>
                        </div>
                        <div class="form-group">
                          <label for="lastname-reg">
                            Last name
                          </label>
                          <input name="lastname-reg" class="form-control" type="text" placeholder="e.g. Smith"></input>
                        </div>
                        <div class="form-group">
                          <label for="address-reg">
                            Street address
                          </label>
                          <input name="address-reg" class="form-control" type="text" placeholder="e.g. 1 George Street"></input>
                        </div>
                        <div class="form-group">
                          <div class="row">
                            <div class="col-md-3">
                              <label for="suburb-reg">
                                Suburb
                              </label>
                              <input name="suburb-reg" class="form-control" type="text" placeholder="e.g. Sydney" style="width: 200px"></input>
                            </div>
                            <div class="col-md-2">
                              <label for="state-reg">
                                State
                              </label>
                              <select class="form-control" name="state-reg">
                                <option>NSW</option>
                                <option>QLD</option>
                                <option>VIC</option>
                                <option>ACT</option>
                                <option>TAS</option>
                                <option>WA</option>
                                <option>SA</option>
                                <option>NT</option>
                              </select>
                            </div>
                            <div class="col-md-3">
                              <label for="postcode-reg">
                                Postcode
                              </label>
                              <input name="postcode-reg" class="form-control" type="number" placeholder="e.g. 2000" style="width: 200px" maxlength="4"></input>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label for="phone-reg">
                            Contact phone
                          </label>
                          <input name="phone-reg" class="form-control" type="text" placeholder="e.g. 0012345678"></input>
                        </div>
                        <div class="form-group">
                          <div class="row">
                            <div class="col-md-4">
                              <label for="btn-group">
                                Sex
                              </label>
                              <br />
                              <div class="btn-group" data-toggle="buttons">
                                <label class="btn btn-primary">
                                  <input type="radio" name="sex-reg" id="male"> Male
                                </label>
                                <label class="btn btn-primary">
                                  <input type="radio" name="sex-reg" id="female"> Female
                                </label>
                                <label class="btn btn-primary">
                                  <input type="radio" name="sex-reg" id="undisclosed"> Undisclosed
                                </label>
                              </div>
                            </div>
                            <div class="col-md-3">
                              <label for="suburb-reg">
                                Date of birth
                              </label>
                              <input name="dob-reg" class="form-control" type="text" placeholder="DD/MM/YYYY" style="width: 200px" maxlength="10"></input>
                            </div>
                          </div>
                        </div>
                        <div class="form-group">
                          <label class="checkbox-inline">
                            <input type="checkbox" id="certificate"> By registering I understand my details may be used for in-house marketing purposes
                          </label>
                        </div>
                        <div class="form-group">
                          <button type="submit" class="btn btn-success" name="create-account">Create account</button>
                        </div>
                      </form>
"""

def print_header(title, form):
    global account
    
    username = form.getvalue("username")
    password = form.getvalue("password")
    
    if username and password:
        account = login.authenticate_user(username, password)
    if form.getvalue("page") == "login" and account and username and password:
        print "Set-Cookie:username=%s;" % (username)
        print "Set-Cookie:password=%s;" % (password)
        
        if form.getvalue("remember-me"):
            print "Set-Cookie:Expires=Thursday, 31-Dec-2099 23:59:59 GMT;"
        else:
            print "Set-Cookie:Expires=%s;" % (datetime.now().strftime('%A, %d-%m-%Y ' + str(datetime.now().hour + 1) + ':%M:%S GMT'))
        print "Set-Cookie:Domain=www.cse.unsw.edu.au/~chrisdb/mekong.cgi;"
    elif form.getvalue("page") == "logout":
        print "Set-Cookie:username=;"
        print "Set-Cookie:password=;"
        print "Set-Cookie:Expires=Wednesday, 12-05-1993 00:00:00 GMT;"
        print "Location: mekong.cgi?page=logout-complete"
    
    print "Content-type: text/html"
    print # Do not remove
    
    if environ.has_key('HTTP_COOKIE'):
        username = ""
        password = ""
        myenv = re.sub(r"\s", r"", environ['HTTP_COOKIE'])
        for cookie in myenv.split(';'):
            (key, value) = cookie.split('=')
            if key == "username":
                username = value
            elif key == "password":
                password = value
                
        if username and password:
            account = login.authenticate_user(username, password)
    
    print """
    <!DOCTYPE html>
    <html lang="en">
    <!-- Code taken from Bootstrap website -->
      <head>
        <title>"""
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
                <li><a href="mekong.cgi?page=recommendations">Recommendations</a></li>
                <li><a href="mekong.cgi?page=trolley">Trolley</a></li>
                <li><a href="mekong.cgi?page=checkout">Checkout</a></li>
              </ul>
              <form class="navbar-form navbar-left" role="search" action="mekong.cgi?page=search" method="post">
                <div class="form-group">
                    <input type="text" class="form-control" style="width: 300px;" placeholder="Quick title search" name="criteria">
                    <input type="hidden" name="category" value="title">
                    <input type="hidden" name="order" value="salesrank">
                    <input type="hidden" name="asc" value="DESC">
                </div>
                <button type="submit" class="btn btn-default">Search</button>
              </form>
              <ul class="nav navbar-nav">
                <li><a href="mekong.cgi?page=advanced-search">Advanced search</a></li>
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
    if not account and login.error:
        alert_message("danger", login.error, "")
        
    if form.getvalue("qty") and int(form.getvalue("qty")) > 0 and account:
        trolley.set_basket(account["username"], form.getvalue("isbn"), form.getvalue("qty"))
        alert_message("success", "", "Item added to cart")
        
    if form.getvalue("page") == "application-submitted":
        if form.getvalue("password-reg") == form.getvalue("confirmpass-reg"):
            user = {}
            user["username"] = form.getvalue("username-reg")
            user["password"] = form.getvalue("password-reg")
            user["firstname"] = form.getvalue("firstname-reg")
            user["lastname"] = form.getvalue("lastname-reg")
            user["address"] = form.getvalue("address-reg")
            user["suburb"] = form.getvalue("suburb-reg")
            user["state"] = form.getvalue("state-reg")
            user["postcode"] = form.getvalue("postcode-reg")
            user["email"] = form.getvalue("email-reg")
            user["phone"] = form.getvalue("phone-reg")
            user["dob"] = form.getvalue("dob-reg")
            user["sex"] = form.getvalue("sex-reg")
            
            if not login.create_account(user):
                alert_message("danger", login.error, "")
            else:
                alert_message("success", "Account successfully created.", "A confirmation email has been sent to %s. Before logging in, please confirm your account." % (user["email"]))
        else:
            alert_message("danger", "Your password and your confirm password entries do not match!", "")
    print """
          </div>
"""
    print """
        </div>
        <div class="bs-old-docs">
            <p><br></p>
        </div>
"""

def print_body_search(form):
    global account
    print """
        <div class="container bs-docs-container" style="min-width: 600px">
          <div class="row">
            <div class="col-md-3">
              <div class="panel panel-info" data-spy="affix" style="min-height: 300px; min-width: 260px;">
                <div class="panel-heading">
                    <h3 class="panel-title">
                      <strong>Quick trolley</strong><br>
                      <div class="row">
                        <div class="col-md-6">
"""
    if account:
        basket_size = trolley.count_basket(account["username"])
    else:
        basket_size = 0
    print basket_size, "items"
    print """
                        </div>
                        <div class="col-md-6" align="right">
"""
    if account:
        print "$%.2f" % (trolley.total_basket(account["username"]))
    else:
        print "$0.00"
    print """
                        </div>
                      </div> 
                    </h3>
                </div>
                <div class="panel-body">
"""
    if basket_size == 0:
        print "Your trolley is empty..."
    else:
        t = trolley.read_basket(account["username"], "price", "DESC")
        for i in t:
            book = books.search_books(i["isbn"], "isbn", "price", "ASC")
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
""" % (book["smallimageurl"], book["title"], book["price"], book["authors"], i["qty"])
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
    if form.getvalue("page") == "search":
        books.present_books(form.getvalue("criteria"), form.getvalue("category"), form.getvalue("order"), form.getvalue("asc"), account)
    elif form.getvalue("page") == "create-account":
        print_registration()
        
    print """
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

print_header("Mekong", form)
print_body_search(form)

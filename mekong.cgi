#!/usr/bin/env python2.7

import cgi, cgitb; cgitb.enable()
import datetime
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
                    <form action="mekong.cgi" method="post">
                      <label for="login">Login</label>
                      <input type="text" id="username" class="form-control" placeholder="Enter username" style="margin-bottom: 5px;"></input>
                      <input type="password" id="password" class="form-control" placeholder="Enter password" style="margin-bottom: 10px;"></input>
                      <div class="checkbox">
                        <label>
                          <input id="remember-me" type="checkbox"> Remember me
                        </label>
                      </div>
                      <input type="submit" id="login" class="btn btn-primary" style="margin-bottom: 10px; width: 215px" value="Login"></input>
                    </form>
                      <button type="submit" id="forgot" class="btn btn-danger" style="margin-bottom: 10px; width: 215px">Forgot Password</button>
                    <form action="mekong.cgi?page=create-account" method="post">
                      <button type="submit" id="create" class="btn btn-warning" style="margin-bottom: 10px; width: 215px">Create account</button>
                    </form>
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

def print_header(title):
    print "Content-type: text/html"
    print # Do not remove
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
              <form class="navbar-form navbar-left" role="search" action="mekong.cgi?page=quicksearch" method="post">
                <div class="form-group">
                    <input type="text" class="form-control" style="width: 300px;" placeholder="Quick title search" name="searchbar"></input>
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
    if form.getvalue("username") and form.getvalue("password"):
        error_msg = login.authenticate_user(form.getvalue("username"), form.getvalue("password"), account)
        if error_msg:
            print """
        <div class="alert alert-danger fade in">
            <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
                x
            </button>
            <strong>
"""
            print error_msg
            print """
            </strong>
"""
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
            
            error_msg = login.create_account(user)
            
            if error_msg:
                print """
          <div class="alert alert-danger fade in">
            <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
                x
            </button>
            <strong>
"""
                print error_msg
            else:
                print """
                <div class="alert alert-danger fade in">
            <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
                x
            </button>
            <strong>
"""
                print "Account successfully created. An confirmation email has been sent to", user["email"] + ". Before logging in, please confirm your account."
        else:
            print """
          <div class="alert alert-danger fade in">
            <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
                x
            </button>
            <strong>
                Your password and your confirm password entries do not match!
"""
        print """
            </strong>
"""
    print """
        </div>
    </div>
"""
    print """
        </div>
"""
#    if form.getvalue("isbn-to-add"):
        #basket.quick_basket(account["username"])
      
    print """
        
        <div class="bs-old-docs">
            <p><br></p>
        </div>
"""

def print_body_search(form):
    print """
        <div class="container bs-docs-container">
          <div class="row">
            <div class="col-md-3">
              <div class="panel panel-info" data-spy="affix" style="min-height: 300px; min-width: 260px">
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
"""
    if form.getvalue("page") == "quicksearch":
        books.present_books(form.getvalue("searchbar"), "title", "salesrank", "DESC")
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

print_header("Mekong")
print_body_search(form)

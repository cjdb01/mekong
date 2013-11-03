#!/usr/bin/python -u

import cgi
import re

error = ""
login = {}
books = {}
basket = {}

i_username = "username"
i_password = "password"
i_givename = "givename"
i_lastname = "lastname"
i_street_address = "street_address"
i_suburb = "suburb"
i_state = "state"
i_postcode = "postcode"
i_gender = "gender"
i_phone_number = "phone_number"
i_credit_card = "credit_card"

# Return true
def legal_username(username):
    global error
    if re.match("[A-Za-z_]\w+", username) == None:
        error = "Invalid username '" + username + "': usernames must start with a letter and only contain letters, numbers and underscores."
    elif len(username) < 3 or len(username) > 8:
        error = "Invalid username '" + username + "': usernames must be 3 - 8 characters long."
    else:
        return True
    return False
    
def legal_password(password, username, first_name, surname):
    global error
    if len(password) < 6 or len(password) > 64:
        error = "Invalid password: passwords must be 6 - 64 characters long."
    elif re.search("[A-Z]", password) == None:
        error = "Invalid password: passwords must contain at least one upper case character."
    elif re.search("[a-z]", password) == None:
        error = "Invalid password: passwords must contain at least one lower case character."
    elif re.search("\d", password) == None:
        error = "Invalid password: passwords must contain at least one digit."
    elif re.search("\W", password) == None:
        error = "Invalid password: passwords must contain at least one special character."
    elif re.search(username, password) != None:
        error = "Invalid password: passwords cannot contain your username."
    elif re.search(username, first_name) != None:
        error = "Invalid password: passwords cannot contain your first name."
    elif re.search(username, surname) != None:
        error = "Invalid password: passwords cannot contain your last name."
    else:
        return True
    return False

def legal_isbn(isbn):
    global error
    if re.match("\d{9} (\d|X)") == None:
        error = "Invalid ISBN '" + isbn + "': an ISBN must be exactly 10 digits."
        return False
    else:
        return True
        
def legal_credit_card_number(number):
    global error
    if re.match("\d{16}", number) == None:
        error = "Invalid credit card number: a credit card number has exactly 16 digits."
        return False
    return True

def legal_expiry_date(mm, yy):
    global error
    if datetime.date.year > yy or (datetime.date.year == yy and datetime.date.month > mm):
        error = "Invalid expiry date."
        return False
    else:
        return True
        
def total_books(isbns):
    total = 0
    for isbn in isbns:
        if books.get(isbn) == None:
            sys.exit("Internal error: unknown ISBN '" + isbn + "'in total_books")
        else:
            total += books[isbn][price] 
    return total
    
def authenticate(username, password):
    global login
    global error
    if not login:
        error = "User is already logged in."
    elif legal_username(username) == True:
        try:
            file = open(user_directory + "/" + username, 'r')
            
            for line in file:
                line.rstrip('\n')
                line = re.escape(line)
                key = re.sub(r"(.+?) = (.+?)", r"\1", line)
                
            file.close()
            
            if login[i_password] != password:
                error = "Incorrect username or password."
            else:
                return True
        except IOError:
            error = "Authentication error: username '" + username + "' does not exist."
    else:
        error = "Incorrect username or password."
    return False
    
def read_books(filename):
    global books
    try:
        file = open(filename)
        isbn = ""
        field = ""
        collecting = False
        for line in file:
            line.rstrip('\n')
            line = re.escape(line)
            
            if re.match("\s*\"(\d+X?)\"\s*:\s*{\s*", line):
                isbn = re.sub(r"\s*\"(\d+X?)\"\s*:\s*{\s*", r"\1", line)
                continue
            if isbn == "":
                continue
            elif re.match("\s*\"([^\"]+)\"\s*:\s*\"(.*)\",?\s*", line):
                field = re.sub(r"\s*\"([^\"]+)\"\s*:\s*\"(.*)\",?\s*", r"\1", line)
                books[isbn][field] = re.sub(r"\s*\"([^\"]+)\"\s*:\s*\"(.*)\",?\s*", r"\2", line)
            elif re.match("\s*\"([^\"]+)\"\s*:\s*\[\s*", line):
                field = re.sub(r"\s*\"([^\"]+)\"\s*:\s*\[\s*", r"\1", line)
                collecting = True
            elif collecting == True and re.match("\s*\"(.*)\"\s*,?\s*", line):
                books[isbn][field].append(re.sub(r"\s*\"(.*)\"\s*,?\s*", r"\1"))
            elif collecting == True and re.match("\s*\]\s*,?\s*"):
                collecting = False
        file.close()
    except IOError:
        sys.exit("Cannot open book database '" + filename + "'.")

def search_books(criteria, category):
    global error
    criteria = re.sub(r"^\s*(.*?)\s*$", r"\1", criteria)
    booklist = []
    
    if category == "isbn" and legal_isbn(criteria) and books.get(criteria):
        booklist.append(books[criteria])
    else:
        for i in books:
            line = re.escape(line)
            
            if i.get(category) and re.search(criteria, i.get(category)):
                booklist.append(i)
                
    return booklist

def read_basket():
    global basket
    try:
        file = open(login[i_username], "r")
        for line in file:
            line.rstrip('\n')
            isbn = re.sub(r"\s*(\d{9} (\d|X)) = (\d+)", r"\1", line)
            if books.get(isbn):
                basket[isbn] = re.sub(r"\s*(\d{9} (\d|X)) = (\d+)", r"\3", line)
            
        file.close()
    except IOError:
        error = "Basket is empty!"
    
def write_basket():
    try:
        file = open(login[i_username], "w")
        for i in basket:
            file.writeLine(i)
            
        file.close()
    except Exception:
        error = "Unsure what to put here..."
    
def delete_basket(isbn):
    global basket
    try:
        basket[isbn] -= 1
        if basket[isbn] <= 0:
            basket.remove(isbn)
        write_basket()
    except Exception:
        error = "Not in basket"

def add_basket(isbn):
    global basket
    try:
        basket[isbn] += 1
    except Exception:
        basket[isbn] = 1
        
    write_basket()
    
def finalise_order(login, credit_card, expiry_date):
    order_number = 0
    
    try:
        file = open("orders/next_order_number", "r+")
        for line in file:
            line.rstrip('\n')
            order_number = int(line)
            line = str(order_number + 1)
    except Exception:
        sys.exit("Missing orders/next_order_number")
    finally:
        file.close()
        

def login_form():
    print '<p>\n\
<center>\n\
<form>\n\
Username: <input type="text" name="username" size=16></input>\n\
Password: <input type="password" name="password" size=16></input>\n\
</form>\n\
</center>\n\
<p>\n'
        
print 'Content-Type: text-html\n\n\
<!DOCTYPE html>\n\
<html lang="en">\n\
<head>\n\
<title>mekong.com.au</title>\n\
<link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css" rel="stylesheet">\n\
<script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js"></script>\n\
</head>\n\
<body>\n\
<p>\n\
<div class="container">\n'

login_form()

print '</div>\n\
<body>\n\
</html>\n'
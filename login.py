import database as dbase
from datetime import datetime
import hashlib
import os
import re
import smtplib

login_db = "data/main.db"

error = ""

def send_mail(destination, subject, body):
    SENDMAIL = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % SENDMAIL, "w")
    p.write("""
From: accounts@mekong.com.au  
To: %s
Subject: %s

%s
""" % (destination, subject, body)
    sts = p.close()
    if sts != 0:
        error = "Sendmail exit status %s" % (sts)
        return False
    error = ""
    return True

def legal_username(username):
    global error

    length = len(username)
    
    error = "Invalid username '" + username + "': usernames must"
    
    if not re.match('[A-Za-z_]\w+', username):
        error += "start with a letter and only contain letters, numbers and underscores."
    elif length < 3 or length > 8:
        error += "be 3 - 8 characters long."
    else:
        error = ""
        return True
    return False
    
def unique_username(username):
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [username])
        
        rows = cursor.fetchone()
        
    return rows is None
    
def legal_password(password, username, first_name, last_name):
    global error
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
        error = ""
        return True
    return False
    
def authenticate_user(username, password):
    global error
    error = "Authentication error: "
    
    if legal_username(username):
        db = dbase.db_init(login_db)
    
        with db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = :uname", {"uname": username})
            
            row = cursor.fetchone()
            
            hash = hashlib.sha512()
            hash.update(password)
            password = hash.hexdigest()
            
            if not row:
                error += "username '" + username + "' does not exist."
            elif password != row["password"]:
                error += "incorrect username or password."
            elif row["confirmed"]: # a value here means that they haven't clicked on the link yet!
                error += "please confirm your registration prior to logging in."
            else:
                error = ""
                return row
    else:
        error += "incorrect username or password."
    return None
    
def create_account(user):
    global error
    if legal_username(user["username"]):
        if not unique_username(user["username"]):
            error = "Create account error: username is not unique"
        else:
            if legal_password(user["password"], user["username"], user["firstname"], user["lastname"]):
                db = dbase.db_init(login_db)
        
                with db:
                    cursor = db.cursor()
                
                    hash = hashlib.sha512()
                    hash.update(user["password"])
                    pwd = hash.hexdigest()
                    
                    hash = hashlib.sha512()
                    hash.update(user["username"])
                    hash.update(user["firstname"])
                    hash.update(datetime.now().strftime('%A, %d-%m-%Y ' + str(datetime.now().hour + 1) + ':%M:%S GMT'))
                    
                    confirmation = hash.hexdigest()
                    
                    if not send_mail(user["email"], "Mekong.com.au: Account activation", "Dear %s %s,\n\nThis email is to confirm that you have requested an account with mekong.com.au.\n\nIf you created the account, please click on the following link http://www.cse.unsw.edu.au/~chrisdb/%s.\n\nIf you did not create the account, please send an email to webmaster@mekong.com.au to rectify the issue.\n\nKind regards,\n\nMekong staff" % (user["firstname"], user["lastname"], confirmation)):
                        return False
                    
                    cursor.execute("INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [user["username"], pwd, user["firstname"], user["lastname"],\
                                            user["address"], user["suburb"], user["state"], user["postcode"], user["dob"], user["email"], user["phone"], user["sex"], confirmation, "", ""])
                    return True
    return False
    
def change_password(username, current_password, new_password):
    global error
    hash = hashlib.sha512()
    hash.update(current_password)
    
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users")
        
        row = cursor.fetchone()
        if row["password"] == hash.hexdigest() and legal_password(new_password, row["username"], row["firstname"], row["lastname"]):
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
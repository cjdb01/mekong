import database as dbase
from datetime import datetime
import hashlib
import os
import re
import smtplib

login_db = "data/main.db"

error = ""

def send_mail(destination, subject, body):
    # Code from http://www.yak.net/fqa/84.html
    SENDMAIL = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % SENDMAIL, "w")
    p.write("From: accounts@mekong.com.au\n")
    p.write("To: %s\n" % (destination))
    p.write("Subject: %s\n" % (subject))
    p.write("\n\n%s\n" % (body))

    sts = p.close()
    if sts:
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
    rows = None
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [username])
        
        rows = cursor.fetchone()
        
    return rows is None
    
def unique_email(email):
    db = dbase.db_init(login_db)
    rows = None
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE email = ?", [email])
        
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
            cursor.execute("SELECT * FROM Users WHERE username = ?", [username])
            
            user = cursor.fetchone()
            
            hash = hashlib.sha512()
            hash.update(password)
            password = hash.hexdigest()
            
            if not user:
                error += "username '" + username + "' does not exist."
            elif password != user["password"]:
                error += "incorrect username or password."
            elif user["confirmed"]: # a value here means that they haven't clicked on the link yet!
                error += "please confirm your registration prior to logging in."
            else:
                error = ""
                return user
    else:
        error += "incorrect username or password."
    return None
    
def create_account(user):
    global error
    if legal_username(user["username"]):
        if not unique_username(user["username"]):
            error = "Create account error: username is not unique"
        if not unique_email(user["email"]):
            error = "Create account error: e-mail is not unique"
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
                    hash.update(str(datetime.now()))
                    hash.update(os.urandom(20))
                    
                    confirmation = hash.hexdigest()
                    
                    if not send_mail(user["email"], "Mekong.com.au: Account activation", "Dear %s,\n\nThis email is to confirm that you have requested an account with mekong.com.au.\n\nIf you created the account, please click on the following link http://www.cse.unsw.edu.au/~chrisdb/mekong.cgi?page=confirm-account&link=%s.\n\nIf you did not create the account, please send an email to webmaster@mekong.com.au to rectify the issue.\n\nKind regards,\n\nMekong staff" % (user["firstname"], confirmation)):
                        return False
                    
                    cursor.execute("INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [user["username"], pwd, user["firstname"], user["lastname"],\
                                            user["address"], user["suburb"], user["state"], user["postcode"], user["dob"], user["email"], user["phone"], user["sex"], confirmation, "", ""])
                    return True
    return False
    
def change_password_backend(username, current_password, new_password):
    global error
    
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?;", [username, current_password])
        
        user = cursor.fetchone()
        
        if user:
            if legal_password(new_password, user["username"], user["firstname"], user["lastname"]):
                hash = hashlib.sha512()
                hash.update(new_password)
            
                if hash.hexdigest() != user["password"]:
                    cursor.execute("UPDATE Users SET password = ? WHERE username = ? AND password = ?;", [hash.hexdigest(), username, user["password"]])
                    error = ""
                    return True
                else:
                    error = "Password update error: new password cannot match old password."
        else:
            error = "Password update error: incorrect password." 
                
    return False
    
def confirm_account(link):
    global error
    
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE confirmed = ?;", [link])
        
        user = cursor.fetchone()
        
        if user:
            cursor.execute("UPDATE Users SET confirmed = '' WHERE confirmed = ?;", [link])
            return True
        else:
            error = """
Accounts can only be confirmed once, so you might have already confirmed your account. If this is the case please log in using the form at the top of the page.<br/>
If you haven't confirmed your account yet, please ensure that you copied the URL from your email correctly.<br/>Queries may be sent to accounts@mekong.com.au.<br/>
"""
            return False

def reset_password_request(username, email):
    global error
    
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [username])
        
        user = cursor.fetchone()
        
        if user:
            if user["email"] != email:
               error = "The e-mail address you provided does not match the one in our database."
               return False
        
            dtime = datetime.now()
            hash = hashlib.sha512()
            hash.update(username)
            hash.update(str(datetime.now()))
            hash.update(os.urandom(20))
            
            cursor.execute("UPDATE Users SET password_reset_link = ?, password_reset_date = ? WHERE username = ?;", [hash.hexdigest(), dtime, username])
            
            if send_mail(user["email"], "Mekong.com.au: Reset password request", "Dear %s,\n\nWe have received a request to reset your password.\n\nBefore resetting your password, it is our policy to request that you click the following link, http://www.cse.unsw.edu.au/~chrisdb/mekong.cgi?page=reset-password&link=%s.\n\nIf you did not authorise this request, you may choose to ignore this email.\n\nIf you didn't create an account with Mekong, please contact us at webmaster@mekong.com.au immediately. Do not provide personal details in this email." % (user["firstname"], hash.hexdigest())):
                return True
        else:
            error = "Could not find username '%s'" % (username)
        return False
        
def reset_password(link, password):
    global error
    
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE password_reset_link = ?", [link])
        
        user = cursor.fetchone()
        
        if user:
            if change_password_backend(user["username"], user["password"], password):
                cursor.execute("UPDATE Users SET password_reset_link = '', password_reset_date = '' WHERE username = ?;", [user["username"]])
                return True
        else:
          error = "User does not exist."
          return False
    error += '<br/><a href="mekong.cgi?page=reset-password&link=%s">Click here</a> to try again' % (link)
    return False

def reset_password_validate(link):
    global error
    
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE password_reset_link = ?;", [link])
        
        user = cursor.fetchone()
        
        if user:
            now = datetime.now()
            then = user["password_reset_date"]
#            time_difference = now - then
#            if time_difference.total_seconds() < (60 * 60 * 24 * 2): # seconds/minute * minutes/hour * hours/day * max days before timeout
            print """
<div class="bs-callout bs-callout-info">
  <h4>Nearly there!</h4>
  <p>Just enter your new password into the boxes below and press the button to reset your password!</p>
</div>

                
<form class="form-group" action="mekong.cgi?page=validate-password" method="post">
  <div class="control-group">
    <label for="username">
      New password
    </label>
    <div class="controls">
      <input name="password" class="form-control" type="password" required />
      <p class="help-block"></p>
    </div>
  </div>
  <div class="form-group">
    <label for="email">
      Confirm new password
    </label>
    <input name="confirm-password" class="form-control" type="password" required />
  </div>
  <div class="controls">
    <input type="hidden" name="userid" value="%s" />
    <button type="submit" class="btn btn-info">Reset my password</button>
  </div>
</form>
""" % (link)
            return True
#            else:
#                error = "The link timed out. You only have two days to reset your password."
#                return False
        else:
            error = "Invalid link"
            return False
    return False
    
            
def print_forgot_password():
    print """
<div class="bs-callout bs-callout-info">
  <h4>Oops!</h4>
  <p>We've all forgotten our passwords at one point. Don't worry, just enter your username and e-mail and we'll be able to recover it for you.</p>
</div>

<form class="form-group" action="mekong.cgi?page=forgot-password-sent" method="post">
  <div class="control-group">
    <label for="username">
      Username
    </label>
    <div class="controls">
      <input name="username" class="form-control" type="text" required />
      <p class="help-block"></p>
    </div>
  </div>
  <div class="form-group">
    <label for="email">
      Email
    </label>
    <input name="email" class="form-control" type="email" placeholder="Enter e-mail" required />
  </div>
  <div class="controls">
    <button type="submit" class="btn btn-info" name="reset-password">Email me</button>
  </div>
</form>
"""
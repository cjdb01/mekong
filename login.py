import database as dbase
import hashlib
import re

login_db = "data/main.db"


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
    db = dbase.db_init(login_db)
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ?", [username])
        
        rows = cursor.fetchone()
        
    return rows is None
    
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
    
def authenticate_user(username, password, login):
    error = "Authentication error: "
    
    if login:
        error = "A user is already logged in."
    elif not legal_username(username):
        db = dbase.db_init(login_db)
    
        with db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = :uname", {"uname": username})
            
            row = cursor.fetchone()
            
            if not row:
                error += "username '" + username + "' does not exist."
            elif password != row["password"]:
                error += "incorrect username or password."
            elif not row["confirmed"]:
                error += "please confirm your registration prior to logging in."
            else:
                login = row
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
                db = dbase.db_init(login_db)
        
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
    
    db = dbase.db_init(login_db)
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
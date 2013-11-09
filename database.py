import os
import smtplib
import sqlite3 as lite
import re

def regexp(expr, item):
    expr = re.escape(expr)
    reg = re.compile(expr)
    return reg.search(item, re.IGNORECASE) is not None
    
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

def send_mail(destination, subject, body):
    SENDMAIL = "/usr/sbin/sendmail" # sendmail location

    FROM = "cjdb01@hotmail.com"
    TO = ["chrisdb@cse.unsw.edu.au"] # must be a list

    SUBJECT = "Hello!"

    TEXT = "This message was sent via sendmail."

    # Prepare actual message

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail

    import os

    p = os.popen("%s -t -i" % SENDMAIL, "w")
    p.write(message)
    status = p.close()
    if status:
        print "Sendmail exit status", status
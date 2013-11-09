import os
import smtplib
import sqlite3 as lite
import re

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

def send_mail(destination, subject, body):
    message = """
From: accounts@mekong.com.au
To: %s
Subject: %s

%s
""" % (destination, subject, body)

  postbox = os.popen("/usr/sbin/sendmail -t -i", "w")
  postbox.write(message)
  return postbox.close()
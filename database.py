import sqlite3 as lite
import re

def regexp(expr, item):
    expr = re.escape(expr)
    reg = re.compile(expr, re.IGNORECASE)
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


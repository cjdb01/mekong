import sqlite3 as lite
import re

def regexp(expr, item):
    expr = re.escape(expr)
    reg = re.compile(expr)
    return reg.search(item) is not None

def db_init(path):
    db = lite.connect(path)
    
    try:
        db.create_function("REGEXP", 2, regexp)
        db.row_factory = lite.Row
    except Exception:
        sys.exit("Couldn't establish a connection with database.")
    
    return db
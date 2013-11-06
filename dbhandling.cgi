#!/usr/bin/python -u

from os import environ


import cgi
import cgitb

    
#############################################

def html_header(title):
    print "Content-type: text/html"
    print # Do not remove
    print """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello World</title>
  </head>
  <body>
    Hello World
  </body>
</html>
"""

html_header("Mekong")
import smtplib

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
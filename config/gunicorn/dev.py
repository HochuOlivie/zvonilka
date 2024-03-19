"""Gunicorn *development* config file"""

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "Parser.wsgi:application"
# The number of worker processes for handling requests
workers = 4
# The socket to bind
bind = "0.0.0.0:443"

threads=8
# Write access and error info to /var/log
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
# Redirect stdout/stderr to log file
capture_output = True

loglevel='debug'

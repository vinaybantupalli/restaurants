#!/bin/sh

flask db upgrade

# log level and reload are for local testing only
exec gunicorn --bind 0.0.0.0:80 "app:create_app()" --log-level=debug --reload
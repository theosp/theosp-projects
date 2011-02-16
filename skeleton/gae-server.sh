#!/bin/bash

# Don't forget to update /etc/hosts
# -a "0.0.0.0" enable access to the development server from other computers

/etc/init.d/memcached restart
./clean_pyc
./google_appengine/dev_appserver.py -a "0.0.0.0" -c -d -p 80 --allow_skipped_files . &

appengine_server_pid="$!"

trap "kill $appengine_server_pid; exit;" SIGINT SIGTERM

#sleep 5 
#
#curl 0.0.0.0/setup

wait

./clean_pyc

#!/bin/bash

gsmir # git submodule init recursive

make clean
make

./google_appengine/appcfg.py update .

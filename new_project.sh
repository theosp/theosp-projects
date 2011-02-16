#!/bin/bash

BASHRC_INTERACTIVE_MODE_INIT=1
. ~/.bashrc # source .bashrc to load my git aliases
shopt -s expand_aliases # needed for the git aliases to work properly

user_project_name_github="$1"

if [[ -z "$user_project_name_github" ]]; then
    echo "USAGE: ./new_project.sh github_user_name/project_name"
    exit 1
fi

gig "$user_project_name_github"

cp -r ../skeleton/* .

ga .

gcm "Add project skeleton"

gsmag theosp/theosp_common_build_tools build
gsmag theosp/theosp_common_js javascript/src/theosp_common_js
gsmag theosp/theosp_common_css style/src/theosp_common_css
gsmag theosp/headjs javascript/src/headjs

# app engine related submodules {{{
gsmag theosp/google_appengine google_appengine
gsmag theosp/appengine_django appengine_django
gsmag django/django django-dist 1 # 1 for readonly
ln -s django-dist django
# }}}

gsmir

ga .

gcm "Add submodules: theosp_common_build_tools, theosp_common_js, theosp_common_css, headjs"

gta "project_skeleton"

ghto

make

ga .

gcm "make"

ghoc

# vim:ft=bash:fdm=marker:fmr={{{,}}}:

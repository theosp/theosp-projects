#!/bin/bash

# initiations {{{
BASHRC_INTERACTIVE_MODE_INIT=1
. ~/.bashrc # source .bashrc to load my git aliases
shopt -s expand_aliases # needed for the git aliases to work properly
# }}}

# vars {{{
action="install" # install is the default option
user_project_name_github=""
path=""
submodules=(
   #"repository" "path" "readonly"
    "theosp/theosp_common_build_tools" "build" 0
    "theosp/theosp_common_js" "javascript/src/theosp_common_js" 0
    "theosp/theosp_common_css" "style/src/theosp_common_css" 0
    "theosp/headjs" "javascript/src/headjs" 0
)

submodules_names=()
n=${#submodules[*]}
for (( i=0; i < n; i += 2 )); do
    submodules_names+=( "${submodules[i]}" )
done
unset i n
submodules_names_string=${submodules_names[@]}
# }}}

# functions {{{

# show_help () {{{
show_help () {
    cat <<EOF
NAME
    new_project.sh - Initiate/Update web application projects

SYNOPSIS
    ./new_project.sh [--install | --update | --update-skeleton | --update-submodules] [--] <github-rep> [<path>]
    ./new_project.sh [-h] [--help]

OPTIONS
EOF
}
# }}}

# submodule {{{

# submodule_install (repository_path) {{{
submodule_install () {
    local path="$1"

    pushd . > /dev/null
    cd "$path"

    local i n=${#submodules[*]}
    for (( i=0; i < n; i += 3 )); do
        gsmag "${submodules[i]}" "${submodules[$((i + 1))]}" ${submodules[$((i + 2))]}
    done

    pwd
    gsmir

    popd > /dev/null
}
# }}}

# submodule_update (repository_path) {{{
submodule_update () {
    local path="$1"

    pushd . > /dev/null

    cd "$path"

    popd > /dev/null
}
# }}}

# }}}

# actions {{{

# action_install (github_project, path) {{{
action_install () {
    local github_project="$1"
    local path="$2"

    # init {{{
    gig "$github_project" "$path"
    # }}}

    # add skeleton files {{{
    action_update_skeleton "$github_project" "$path"

    pushd . > /dev/null
    cd "$path"

    ga .

    gcm "Add project base"

    popd > /dev/null
    # }}}
    
    # install submodules {{{
    submodule_install "$path"

    pushd . > /dev/null
    cd "$path"

    ga .

    gcm "Add submodules: $submodules_names_string"

    popd > /dev/null
    # }}}

    # tag and push tag {{{
    pushd . > /dev/null
    cd "$path"

    gta "project_skeleton"

    ghto

    popd > /dev/null
    # }}}
    
    # make {{{
    pushd . > /dev/null
    cd "$path"

    make

    ga .

    gcm "make"

    popd > /dev/null
    # }}}

    # push {{{
    pushd . > /dev/null
    cd "$path"

    ghoc

    popd > /dev/null
    # }}}
}
# }}}

# action_update_skeleton (github_project, path) {{{
action_update_skeleton () {
    local github_project="$1"
    local path="$2"

    cp -r skeleton/* "$path"
}
# }}}

# }}}

# }}}

# parse argv {{{

# load options {{{
# original: http://mywiki.wooledge.org/BashFAQ/035 (Manual Loop)
while [[ $1 == -* ]]; do
    case "$1" in
      -h|--help|-\?)
          show_help
          exit 0
      ;;
      --install)
          action="install"

          shift
      ;;
      --update)
          action="update"

          shift
      ;;
      --update-skeleton)
          action="update-skeleton"

          shift
      ;;
      --update-submodules)
          action="update-submodules"

          shift
      ;;
      --)
          shift
          break
      ;;
      -*)
          echo "invalid option: $1" 1>&2
          show_help
          exit 1
      ;;
    esac
done
# }}}

# load arguments {{{
if (($# > 0)); then
    user_project_name_github="$1"

    path="${2:-${user_project_name_github#*/}}"
else 
    echo "Please provide the github repository" 1>&2
    show_help

    exit 1
fi
# }}}

# }}}

# call action {{{
action_"${action/-/_}" "$user_project_name_github" "$path"
# }}}

# vim:ft=bash:fdm=marker:fmr={{{,}}}:

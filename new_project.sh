#!/bin/bash

# initiations {{{
BASHRC_INTERACTIVE_MODE_INIT=1
. ~/.bashrc # source .bashrc to load my git aliases
shopt -s expand_aliases # needed for the git aliases to work properly
# }}}

# vars {{{

# options {{{
option_action="install" # install is the default option
option_project_readable_name=""
# }}}

# arguments {{{
user_project_name_github="" # $1
path="" # $2
# }}}

# data {{{

# project submodules {{{
submodules=(
   #"repository" "path" "readonly"
    "theosp/theosp_common_build_tools" "build" 0
    "theosp/theosp_common_js" "javascript/src/theosp_common_js" 0
    "theosp/theosp_common_css" "style/src/theosp_common_css" 0
    "theosp/headjs" "javascript/src/headjs" 0
)

submodules_names=()
n=${#submodules[*]}
for (( i=0; i < n; i += 3 )); do
    submodules_names+=( "${submodules[i]}" )
done
unset i n
submodules_names_string=${submodules_names[@]}
# }}}

# }}}

# }}}

# functions {{{

# show_help () {{{
show_help () {
    cat <<EOF
NAME
    new_project.sh - Initiate/Update web application projects

SYNOPSIS
    ./new_project.sh [--install | --update | --update-skeleton | --update-submodules] [--project-readable-name readable_name] [--] <github-rep> [<path>]
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

# recursive_find_replace (path, search, replace) {{{
recursive_find_replace () {
    local path="$1"
    local search="$2"
    local replace="$3"

    find "$path" -type f -exec sed -i "s/$search/$replace/g" {} \;
}
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
    local project_readable_name="${option_project_readable_name:-${github_project#*/}}"

    cp -r skeleton/* "$path"

    recursive_find_replace "$path" "|project_readable_name|" "$project_readable_name"
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
          option_action="install"

          shift
      ;;
      --update)
          option_action="update"

          shift
      ;;
      --update-skeleton)
          option_action="update-skeleton"

          shift
      ;;
      --update-submodules)
          option_action="update-submodules"

          shift
      ;;
      --project-readable-name)
          if (($# > 1)); then
              option_project_readable_name="$2"
              shift 2
          else
              echo "--project-readable-name requires an argument" 1>&2
              exit 1
          fi
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
action_"${option_action/-/_}" "$user_project_name_github" "$path"
# }}}

# vim:ft=bash:fdm=marker:fmr={{{,}}}:

#!/usr/bin/make

# Notes:
#
#     * gcc stands for google clouser compiler

# Variables {{{

# General {{{
SHELL := /bin/bash

BUILD_DIR = "build"

CLOSURE_COMPILER = "${BUILD_DIR}/google-compiler-20100918.jar"
YUI_COMPRESSOR = "${BUILD_DIR}/yuicompressor-2.4.2.jar"

GCC_MIN_JAR ?= java -jar ${CLOSURE_COMPILER}
YUI_MIN_JAR ?= java -jar ${YUI_COMPRESSOR}

JS_DIR = javascript
CSS_DIR = style
JS_SRC_DIR = ${JS_DIR}/src
CSS_SRC_DIR = ${CSS_DIR}/src

PYTHON_API_DIR = apis
PYTHON_API_SETTINGS_DIR = ${PYTHON_API_DIR}/settings
# }}}

# base {{{

# javascript {{{
BASE_JS_FILE = ${JS_DIR}/base.js
BASE_JS_GOOGLE_COMPILED_FILE = ${JS_DIR}/base.gcc.min.js

BASE_JS_FILE_COMPONENTS = \
    ${JS_SRC_DIR}/theosp_common_js/theosp.js\
    ${JS_SRC_DIR}/theosp_common_js/query-string.js\
    ${JS_SRC_DIR}/theosp_common_js/url.js\
    ${JS_SRC_DIR}/theosp_common_js/event-emitter.js\
    ${JS_SRC_DIR}/theosp_common_js/modes_manager.js\
    ${JS_SRC_DIR}/theosp_common_js/json2.js\
    ${JS_SRC_DIR}/theosp_common_js/base64.js\
    ${JS_SRC_DIR}/theosp_common_js/date.format.js\
    ${JS_SRC_DIR}/razoss_common_js/javascript/razoss_api.js\
    ${JS_SRC_DIR}/headjs/src/core.js

FILES_GENERATED_FOR_BASE_JS = ${BASE_JS_FILE}\
                              ${BASE_JS_GOOGLE_COMPILED_FILE}
# }}}

# style {{{
BASE_CSS_FILE = ${CSS_DIR}/base.css
BASE_LESS_CSS_FILE = ${CSS_SRC_DIR}/base.css.less
BASE_CSS_YAHOO_COMPILED_FILE = ${CSS_DIR}/base.yui.min.css

FILES_GENERATED_FOR_BASE_STYLE = ${BASE_CSS_FILE}\
								 ${BASE_CSS_YAHOO_COMPILED_FILE}
# }}}

FILES_GENERATED_FOR_BASE = ${FILES_GENERATED_FOR_BASE_JS}\
						   ${FILES_GENERATED_FOR_BASE_STYLE}

# }}}

# apis {{{
APIS_SRC_DIR = ${JS_SRC_DIR}/apis

MINIFIED_APIS_DIR = ${JS_DIR}/apis

APIS_SRC_FILES = ${wildcard ${APIS_SRC_DIR}/*.js}
APIS_FILES = ${subst ${APIS_SRC_DIR},${MINIFIED_APIS_DIR},${APIS_SRC_FILES}}
MINIFIED_APIS_FILES = ${APIS_FILES:.js=.gcc.min.js}

APIS_GENERATED_FILES = ${APIS_FILES}\
					   ${MINIFIED_APIS_FILES}

APIS_GENERATED_DIRS = ${MINIFIED_APIS_DIR}
# }}}

# frontends {{{

FRONTENDS_JS_DIR = ${JS_DIR}/frontends
FRONTENDS_STYLE_DIR = ${CSS_DIR}/frontends
FRONTENDS_JS_SRC_DIR = ${JS_SRC_DIR}/frontends
FRONTENDS_STYLE_SRC_DIR = ${CSS_SRC_DIR}/frontends

# admin {{{

ADMIN_FRONTEND_JS_DIR = ${FRONTENDS_JS_DIR}/admin
ADMIN_FRONTEND_STYLE_DIR = ${FRONTENDS_STYLE_DIR}/admin
ADMIN_FRONTEND_JS_SRC_DIR = ${FRONTENDS_JS_SRC_DIR}/admin
ADMIN_FRONTEND_STYLE_SRC_DIR = ${FRONTENDS_STYLE_SRC_DIR}/admin

# javascript {{{
ADMIN_FRONTEND_JS_FILE = ${ADMIN_FRONTEND_JS_DIR}/admin.js
ADMIN_FRONTEND_JS_GOOGLE_COMPILED_FILE = ${ADMIN_FRONTEND_JS_FILE:.js=.gcc.min.js}

ADMIN_FRONTEND_JS_FILES = \
    ${JS_SRC_DIR}/apis/user.js\
    ${ADMIN_FRONTEND_JS_SRC_DIR}/sections_prototype.js

FILES_GENERATED_FOR_ADMIN_FRONTEND_JS = ${ADMIN_FRONTEND_JS_FILE}\
                                        ${ADMIN_FRONTEND_JS_GOOGLE_COMPILED_FILE}
# }}}

# style {{{
ADMIN_FRONTEND_CSS_FILE = ${ADMIN_FRONTEND_STYLE_DIR}/admin.lcc.css
ADMIN_FRONTEND_CSS_YAHOO_COMPILED_FILE = ${ADMIN_FRONTEND_CSS_FILE:.lcc.css=.yui.min.css}

ADMIN_FRONTEND_LESS_CSS_FILES = ${CSS_SRC_DIR}/theosp_common_css/reset.css.less\
								${ADMIN_FRONTEND_STYLE_SRC_DIR}/admin.css.less

FILES_GENERATED_FOR_ADMIN_FRONTEND_STYLE = ${ADMIN_FRONTEND_CSS_FILE}\
                                           ${ADMIN_FRONTEND_CSS_YAHOO_COMPILED_FILE}
# }}}

FILES_GENERATED_FOR_ADMIN_FRONTEND = ${FILES_GENERATED_FOR_ADMIN_FRONTEND_JS}\
									 ${FILES_GENERATED_FOR_ADMIN_FRONTEND_STYLE}
# }}}

FILES_GENERATED_FOR_FRONTENDS = ${FILES_GENERATED_FOR_ADMIN_FRONTEND}

# }}}

# Sums {{{
ALL_GENERATED_DIRS = ${FRONTENDS_JS_DIR}

ALL_GENERATED_FILES = ${FILES_GENERATED_FOR_BASE}\
					  ${FILES_GENERATED_FOR_FRONTENDS}
# }}}

# }}}

# Functions {{{

# MAKE_PATH_DIR(path) - create path's dir (recursively) if it doesn't exists
MAKE_PATH_DIR = \
	dir="$$(dirname "${1}")";\
\
	if [[ -n "$$dir" && ! -e "$$dir" ]]; then \
		mkdir -p "$$dir";\
	fi

# INSERT_PROD_FILES_HEADER(input_file, output_file, remove_original=[true|false]) - remove_original is true by default
INSERT_PROD_FILES_HEADER = \
    cat production_files_headers.txt "$1" | sed -e "s/|VERSION|/$$(git describe)/" | sed -e "s/|DATE|/$$(date +"%F %H:%M")/" >> "$2";\
\
	if [[ $3 ]]; then\
		rm -f "$1";\
	fi

# YUI_COMPILE(input_js_or_css_file_path, output_js_or_css_file_path) - YUI compiler
YUI_COMPILE = \
	${call MAKE_PATH_DIR,${2}};\
\
	rm -f "${2}";\
\
	${YUI_MIN_JAR} "${1}" -o "${2}.tmp" --charset "utf-8";\
\
	${call INSERT_PROD_FILES_HEADER,${2}.tmp,${2},true}

# GCC_COMPILE(input_js_file_path, output_js_file_path) - Google closure compiler
GCC_COMPILE = \
	${call MAKE_PATH_DIR,${2}};\
\
	rm -f "${2}";\
\
	${GCC_MIN_JAR} --js "${1}" --warning_level QUIET --js_output_file "${2}.tmp";\
\
	${call INSERT_PROD_FILES_HEADER,${2}.tmp,${2},true}

# LESS_CSS_COMPILE(input_less_css_file_path, output_less_css_file_path) - lessc compiler
LESS_CSS_COMPILE = \
	${call MAKE_PATH_DIR,${2}};\
\
	if [[ "${1}" != "${2}" ]]; then\
		rm -f "${2}";\
\
		lessc "${1}" "${2}";\
	fi
# }}}
# }}}

# all {{{
all: base_js base_style apis admin_frontend
	@@echo "Build complete"

# base {{{

# javascript {{{
base_js: ${BASE_JS_GOOGLE_COMPILED_FILE}
	@@echo "Building base js"

${BASE_JS_GOOGLE_COMPILED_FILE}: ${BASE_JS_FILE}
	@@${call GCC_COMPILE,${BASE_JS_FILE},${BASE_JS_GOOGLE_COMPILED_FILE}}

${BASE_JS_FILE}: ${BASE_JS_FILE_COMPONENTS} theosp_common_js_submodule
	@@echo "Building base js (${BASE_JS_FILE})"

	@@cat ${BASE_JS_FILE_COMPONENTS} > ${BASE_JS_FILE}

theosp_common_js_submodule:
	@@echo "Building theosp_common_js submodule"

	@@cd javascript/src/theosp_common_js; $(MAKE) $(MFLAGS)
# }}}

# style {{{
base_style: ${BASE_CSS_YAHOO_COMPILED_FILE}
	@@echo "Building base css"

${BASE_CSS_YAHOO_COMPILED_FILE}: ${BASE_CSS_FILE}
	@@${call YUI_COMPILE,${BASE_CSS_FILE},${BASE_CSS_YAHOO_COMPILED_FILE}}

${BASE_CSS_FILE}: ${BASE_LESS_CSS_FILE}
	@@${call LESS_CSS_COMPILE,${BASE_LESS_CSS_FILE},${BASE_CSS_FILE}}
# }}}

# }}}

# apis minification {{{
apis: ${MINIFIED_APIS_FILES}
	@@echo "apis minification completed"

${MINIFIED_APIS_FILES}: ${APIS_SRC_FILES}
	@@mkdir -p ${MINIFIED_APIS_DIR}

	@@for file in ${APIS_SRC_FILES}; do \
		output_file="$${file%.js}.gcc.min.js"; \
		output_file="$${output_file/${subst /,\/,${APIS_SRC_DIR}}/${MINIFIED_APIS_DIR}}"; \
\
		echo "Minifying api -> $${output_file}"; \
\
		${call GCC_COMPILE,$$file,$$output_file};\
	done
# }}}

# frontends {{{

# admin {{{
admin_frontend: admin_js admin_css
	@@echo "Done building admin frontend"

# javascript {{{
admin_js: ${ADMIN_FRONTEND_JS_FILE} ${ADMIN_FRONTEND_JS_GOOGLE_COMPILED_FILE}
	@@echo "Done building admin frontend javascript"

${ADMIN_FRONTEND_JS_FILE}: ${ADMIN_FRONTEND_JS_FILES}
	@@echo "Building admin frontend js (${ADMIN_FRONTEND_JS_FILE})"

	@@mkdir -p ${ADMIN_FRONTEND_JS_DIR};

	@@cat ${ADMIN_FRONTEND_JS_FILES} > ${ADMIN_FRONTEND_JS_FILE}

${ADMIN_FRONTEND_JS_GOOGLE_COMPILED_FILE}: ${ADMIN_FRONTEND_JS_FILE}
	@@${call GCC_COMPILE,${ADMIN_FRONTEND_JS_FILE},${ADMIN_FRONTEND_JS_GOOGLE_COMPILED_FILE}}
# }}}

# style {{{
admin_css: ${ADMIN_FRONTEND_CSS_FILE} ${ADMIN_FRONTEND_CSS_YAHOO_COMPILED_FILE}
	@@echo "Done building admin frontend css"

${ADMIN_FRONTEND_CSS_YAHOO_COMPILED_FILE}: ${ADMIN_FRONTEND_CSS_FILE}
	@@${call YUI_COMPILE,${ADMIN_FRONTEND_CSS_FILE},${ADMIN_FRONTEND_CSS_YAHOO_COMPILED_FILE}}

${ADMIN_FRONTEND_CSS_FILE}: ${ADMIN_FRONTEND_LESS_CSS_FILES}
	@@echo "Building admin frontend css (${ADMIN_FRONTEND_CSS_FILE})"

	@@mkdir -p ${ADMIN_FRONTEND_STYLE_DIR};

	@@for file in ${ADMIN_FRONTEND_LESS_CSS_FILES}; do \
		${call LESS_CSS_COMPILE,$$file,$${file/.css.less/.lcc.css}}; \
	done

	@@cat ${ADMIN_FRONTEND_LESS_CSS_FILES:.css.less=.lcc.css} > ${ADMIN_FRONTEND_CSS_FILE}
# }}}

# }}}

# }}}

# }}}

.PHONY: all\
		base_js theosp_common_js_submodule base_style\
		apis\
		admin_frontend admin_js admin_css

clean: 
	@@rm -f ${ALL_GENERATED_FILES}
	@@rm -rf ${ALL_GENERATED_DIRS}

# vim:ft=make:fdm=marker:fmr={{{,}}}:

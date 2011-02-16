#!/bin/bash

cat <<EOF
Generate a new api:

***Read tasks.txt when finished.***

EOF

camelcased_api_name="CamelCasedApiName"
camelcased_pluralized_api_name="CamelCasedPluralizedApiNames"
lower_camelcased_pluralized_api_name="lowerCamelCasedApiName"
underscored_api_name="underscored_api_name"
underscored_pluralized_api_name="underscored_pluralized_api_names"
human_readable_capitalized_api_name="Api Readable Name"
human_readable_capitalized_pluralized_api_name="Api Readable Names"
human_readable_non_capitalized_api_name="human readable non capitalized api name"
human_readable_non_capitalized_pluralized_api_name="human readable non capitalized pluralized api names"

echo "CamelCased (singular) api name: $camelcased_api_name"
echo "CamelCased pluralized api name: $camelcased_pluralized_api_name"
echo "Lower CamelCased pluralized api name: $lower_camelcased_pluralized_api_name"
echo "underscored (singular) api name: $underscored_api_name"
echo "underscored pluralized api name: $underscored_pluralized_api_name"
echo "human readable capitalized (singular) api name: $human_readable_capitalized_api_name"
echo "human readable capitalized pluralized api name: $human_readable_capitalized_pluralized_api_name"
echo "human readable non capitalized (singular) api name: $human_readable_non_capitalized_api_name"
echo "human readable non capitalized pluralized api name: $human_readable_non_capitalized_pluralized_api_name"

api_python_module_path="apis/$underscored_api_name.py"
api_javascript_object_path="javascript/src/apis/$underscored_api_name.js"
api_admin_frontend_section_path="javascript/src/frontends/admin/${underscored_pluralized_api_name}_section.js"
api_admin_frontend_editor_path="javascript/src/frontends/admin/${underscored_pluralized_api_name}_editor.js"
tasks_txt_path="tasks.txt"

template_populator ()
{
    local template="$1"

    template="$(echo "$template" | sed "s/|camelcased_pluralized_api_name|/$camelcased_pluralized_api_name/g")"
    template="$(echo "$template" | sed "s/|lower_camelcased_pluralized_api_name|/$lower_camelcased_pluralized_api_name/g")"
    template="$(echo "$template" | sed "s/|underscored_api_name|/$underscored_api_name/g")"
    template="$(echo "$template" | sed "s/|underscored_pluralized_api_name|/$underscored_pluralized_api_name/g")"
    template="$(echo "$template" | sed "s/|camelcased_api_name|/$camelcased_api_name/g")"
    template="$(echo "$template" | sed "s/|human_readable_capitalized_api_name|/$human_readable_capitalized_api_name/g")"
    template="$(echo "$template" | sed "s/|human_readable_capitalized_pluralized_api_name|/$human_readable_capitalized_pluralized_api_name/g")"
    template="$(echo "$template" | sed "s/|human_readable_non_capitalized_api_name|/$human_readable_non_capitalized_api_name/g")"
    template="$(echo "$template" | sed "s/|human_readable_non_capitalized_pluralized_api_name|/$human_readable_non_capitalized_pluralized_api_name/g")"
    template="$(echo "$template" | sed "s/^\t//g")" # the tabs are there for readability
    template="$(echo "$template" | sed "s/^    //g")" # the tabs are there for readability
    
    echo "$template"
}

# Templates template: 
## Generate tasks.txt {{{
#tasks_txt_template="$(cat <<EOF
#EOF
#)"
#
#echo "$(template_populator "$tasks_txt_template")" > "$tasks_txt_path"
## }}}

# Generate api_admin_frontend_editor_template {{{
api_admin_frontend_editor_template="$(cat <<EOF
    /*
    \$.|camelcased_pluralized_api_name|Editor

    AUTHOR: Daniel Chcouri <333222@gmail.com>

    RERUIRES: Node.js's EventEmitter
              Daniel Chcouri's theosp_common_js (theosp.js)
    */
    (function (\$) {
        // constructor {{{
        \$.|camelcased_pluralized_api_name|Editor = function (parent, key, options) {
            var self = this;

            self.elements = {
                parent: \$(parent)
            };

            if (typeof key === 'undefined') {
                key = null;
            }
            self.key = key;

            if (typeof options === 'undefined') {
                options = {};
            }

            self.options = theosp.object.clone(self.options); // clone the prototypical options
            \$.extend(self.options, options);

            self.model = theosp.object.clone(self.model); // clone the prototypical model

            self.init();
        };

        \$.|camelcased_pluralized_api_name|Editor.prototype = new EventEmitter();
        \$.|camelcased_pluralized_api_name|Editor.prototype.constructor = \$.|camelcased_pluralized_api_name|Editor;

        \$.fn.extend({
            |lower_camelcased_pluralized_api_name|Editor: function (key, options) {
                var |lower_camelcased_pluralized_api_name|Objects = [];

                this.each(function () {
                    |lower_camelcased_pluralized_api_name|Objects.push(new \$.|camelcased_pluralized_api_name|Editor(this, key, options));
                });

                return |lower_camelcased_pluralized_api_name|Objects;
            }
        });
        // }}}

        // properties {{{
        \$.|camelcased_pluralized_api_name|Editor.prototype.options = {
            // margins {{{
            css_prefix: 'Admin|camelcased_pluralized_api_name|Editor-'
            // }}}
        };

        \$.|camelcased_pluralized_api_name|Editor.prototype.model = {
            name: ''
        };
        // }}}

        // methods {{{

        // $ {{{
        \$.|camelcased_pluralized_api_name|Editor.prototype.\$ = function (selector, context) {
            var self = this;

            selector = theosp.string.supplant(selector, {
                prefix: self.options.css_prefix,
                id: self.id
            });

            return \$(selector, context);
        };
        // }}}

        // init {{{
        \$.|camelcased_pluralized_api_name|Editor.prototype.init = function () {
            var self = this;

            // Set events that were passed via the options object
            for (var event in self.options.events) {
                if (self.options.events.hasOwnProperty(event)) {
                    self.on(event, self.options.events[event]);
                }
            }

            if (self.key !== null) {
                \$.|underscored_api_name|_api.get(self.key, function (|underscored_api_name|) {
                    self.model.name = |underscored_api_name|.name;

                    self.initDom();
                });
            } else {
                self.initDom();
            }
        };
        // }}}

        // initDom {{{
        \$.|camelcased_pluralized_api_name|Editor.prototype.initDom = function () {
            var self = this;

            self.elements.parent.append(
                theosp.string.supplant(
                    (
                     '<div class="|prefix||underscored_pluralized_api_name|_editor_container">' +
                         '<div class="|prefix||underscored_pluralized_api_name|_editor">' +
                            '<form action="javascript:void(0);" id="|prefix||underscored_pluralized_api_name|_editor_form">' +
                                '<table>' +
                                    '<tbody>' +
                                        '<tr>' +
                                            '<td><label for="|prefix||underscored_api_name|_key">Key</label></td>' +
                                            '<td>' +
                                                '<input readonly="readonly" id="|prefix||underscored_api_name|_key" class="key" type="text" value="' + 
                                                    function () {
                                                        return self.key || "New";
                                                    }() + 
                                                '" />' +
                                            '</td>' +
                                        '</tr>' +
                                        '<tr>' +
                                            '<td><label for="|prefix||underscored_api_name|_name">Name</label></td>' +
                                            '<td>' +
                                                '<input id="|prefix||underscored_api_name|_name" class="name" type="text" value="|name|" maxlength="500" />' +
                                            '</td>' +
                                        '</tr>' +
                                    '</tbody>' +
                                '</table>' +
                                '<input type="submit" value="|submit_value|" id="|prefix|submit_button" /> ' +
                                '<input type="button" value="Cancel" id="|prefix|cancel_edits" />' +
                            '</form>' +
                         '</div>' +
                     '</div>'
                    ), {prefix: self.options.css_prefix,
                        name: self.model.name,
                        submit_value: self.key ? "Save" : "Add new |human_readable_non_capitalized_api_name|"
                    }
                )
            );

            self.\$('#|prefix||underscored_pluralized_api_name|_editor_form').submit(function () {
                self.save(function () {
                    self.emit('done');
                });
            });

            self.\$('#|prefix|cancel_edits').click(function () {
                self.cancel();
            });
        };
        // }}}

        // save {{{
        \$.|camelcased_pluralized_api_name|Editor.prototype.save = function (callback) {
            var self = this;

            self.model.name = self.\$('#|prefix||underscored_api_name|_name').val();

            var action_url;

            if (self.key === null) {
                action_url = '/|underscored_api_name|/create/';
            } else {
                action_url = '/|underscored_api_name|/' + self.key + '/save/';
            }

            \$.ajax({
                type: 'POST',
                cache: false,
                url: action_url,
                data: {
                    query: JSON.stringify({
                        name: self.model.name
                    })
                },
                success: function (response) { 
                    self.emit('saved');

                    if (typeof callback !== 'undefined') {
                        callback();
                    }

                    self.done();
                },
                dataType: 'json'
            });
        };
        // }}}

        // cancel {{{
        \$.|camelcased_pluralized_api_name|Editor.prototype.cancel = function () {
            var self = this;

            self.emit('cancelled');
            self.done();
        };
        // }}}

        // done {{{
        \$.|camelcased_pluralized_api_name|Editor.prototype.done = function () {
            var self = this;

            self.\$('.|prefix||underscored_pluralized_api_name|_editor_container').remove();

            self.emit('done');
        };
        // }}}

        // }}}
    })(jQuery);

    // vim:fdm=marker:fmr={{{,}}}:
EOF
)"

echo "$(template_populator "$api_admin_frontend_editor_template")" > "$api_admin_frontend_editor_path"
# }}}

# Generate api_admin_frontend_section_path {{{
api_admin_frontend_section_template="$(cat <<EOF
    /*
    \$.Admin|camelcased_pluralized_api_name|Section

    AUTHOR: Daniel Chcouri <333222@gmail.com>

    RERUIRES: Daniel Chcouri's theosp_common_js (theosp.js)
              Daniel Chcouri's $.AdminSection
                  Node.js's EventEmitter
              Steven Levithan date.format.js
    */
    (function (\$) {
        // constructor {{{
        \$.Admin|camelcased_pluralized_api_name|Section = function (parent, options) {
            var self = this;

            self.elements = {
                parent: \$(parent)
            };

            if (typeof options === 'undefined') {
                options = {};
            }
            self.options = theosp.object.clone(self.options); // clone the prototypical options
            \$.extend(self.options, options);

            self.|underscored_pluralized_api_name|_editor = null;

            self.init();
        };

        \$.Admin|camelcased_pluralized_api_name|Section.prototype = new $.AdminSection();
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.constructor = \$.Admin|camelcased_pluralized_api_name|Section;

        \$.fn.extend({
            admin|camelcased_pluralized_api_name|Section: function (options) {
                var admin|camelcased_pluralized_api_name|SectionObjects = [];

                this.each(function () {
                    admin|camelcased_pluralized_api_name|SectionObjects.push(new \$.Admin|camelcased_pluralized_api_name|Section(this, options));
                });

                return admin|camelcased_pluralized_api_name|SectionObjects;
            }
        });
        // }}}

        // properties {{{
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.|underscored_pluralized_api_name| = {
            // dom options {{{
            css_prefix: 'Admin|camelcased_pluralized_api_name|Section-'
            // }}}
        };
        // }}}

        // methods {{{

        // initDom {{{
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.initDom = function () {
            var self = this;

            self.elements.parent.html(
                theosp.string.supplant(
                    (
                     '<div class="|prefix|admin_|underscored_pluralized_api_name|_section_container">' +
                         '<div class="|prefix|admin_|underscored_pluralized_api_name|_section">' +
                            '<h3 style="display: none;"></h3>' +
                            '<table class="|prefix||underscored_pluralized_api_name|_table">' +
                                '<thead>' +
                                    '<tr>' +
                                        '<th class="|prefix|order_bys" id="|prefix|order_by_name">Name</th>' +
                                        '<th class="|prefix|order_bys" id="|prefix|order_by_created_by">Created By</th>' +
                                        '<th class="|prefix|order_bys" id="|prefix|order_by_modified_by">Modified By</th>' +
                                        '<th class="|prefix|order_bys" id="|prefix|order_by_date_created">Created</th>' +
                                        '<th class="|prefix|order_bys" id="|prefix|order_by_date_modified">Modified</th>' +
                                    '</tr>' +
                                '</thead>' +
                                '<tbody>' +
                                '</tbody>' +
                                '<tfoot>' +
                                    '<tr><td id="|prefix|status_bar" colspan="5">Click on a row to get its key</td></tr>' +
                                    '<tr><td colspan="6">' +
                                        '<div id="|prefix|pager"></div>' +
                                        '<a id="|prefix|add_|underscored_api_name|" href="javascript:void(0);">Add New |human_readable_capitalized_api_name|</a>' +
                                    '</td></tr>' +
                                '</tfoot>' +
                            '</table>' +
                            '<div class="|prefix||underscored_pluralized_api_name|_editor_container |prefix|invisible">' +
                                '<div class="|prefix||underscored_pluralized_api_name|_editor"></div>' +
                            '</div>' +
                         '</div>' +
                     '</div>'
                    ), {prefix: self.options.css_prefix
                    }
                )
            );

            self.elements.|underscored_pluralized_api_name|_section_title = self.\$('.|prefix|admin_|underscored_pluralized_api_name|_section_container h3');
            self.elements.|underscored_pluralized_api_name|_table = self.\$('.|prefix||underscored_pluralized_api_name|_table');
            self.elements.|underscored_pluralized_api_name|_table_tbody = self.\$('.|prefix||underscored_pluralized_api_name|_table > tbody');

            self.\$('.|prefix|order_bys').click(function () {
                var order_by = \$(this)[0].id.replace(self.options.css_prefix + 'order_by_', '');
                
                if (self.options.order_by === order_by) {
                    self.options.order_by = '-' + order_by;
                } else {
                    self.options.order_by = order_by;
                }

                self.options.page = 1;

                self.load_entities_table();
            });

            self.\$('#|prefix|add_|underscored_api_name|').click(function () {
                self.init_|underscored_api_name|_editor();
            });

            self.load_entities_table();
        };
        // }}}

        // load_entities_table {{{
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.load_entities_table = function () {
            var self = this;

            \$.|underscored_api_name|_api.list(self.options.order_by, self.options.page, function (response) {
                var |underscored_pluralized_api_name|_table_tbody = self.elements.|underscored_pluralized_api_name|_table_tbody;
                |underscored_pluralized_api_name|_table_tbody.html('');

                var |underscored_pluralized_api_name|_list = response.|underscored_pluralized_api_name|;
                self.options.pages_count = response.pager.pages_count;
                self.update_pager();

                for (var |underscored_api_name|_id in |underscored_pluralized_api_name|_list) {
                    if (|underscored_pluralized_api_name|_list.hasOwnProperty(|underscored_api_name|_id)) {
                        var |underscored_api_name| = |underscored_pluralized_api_name|_list[|underscored_api_name|_id];

                        |underscored_api_name|.date_created = self.parseDjangoJsonDate(|underscored_api_name|.date_created);
                        |underscored_api_name|.date_modified = self.parseDjangoJsonDate(|underscored_api_name|.date_modified);

                        |underscored_pluralized_api_name|_table_tbody.append(
                            theosp.string.supplant(
                                (
                                    '<tr class="|prefix||underscored_pluralized_api_name|_row" id="|prefix|entity_row_||underscored_api_name|_id|">' +
                                        '<td class="|prefix||underscored_pluralized_api_name|_row_name">||underscored_api_name|_name|</td>' + 
                                        '<td class="|prefix||underscored_pluralized_api_name|_row_created_by">|created_by|</td>' + 
                                        '<td class="|prefix||underscored_pluralized_api_name|_row_modified_by">|modified_by|</td>' + 
                                        '<td class="|prefix||underscored_pluralized_api_name|_row_created">|created|</td>' + 
                                        '<td class="|prefix||underscored_pluralized_api_name|_row_modified">|modified|</td>' + 
                                    '</tr>'
                                ), {prefix: self.options.css_prefix,
                                    created_by: |underscored_api_name|.created_by._User__email,
                                    modified_by: |underscored_api_name|.modified_by._User__email,
                                    created: |underscored_api_name|.date_created.format('isoDate') + ' ' + |underscored_api_name|.date_created.format('isoTime'),
                                    modified: |underscored_api_name|.date_modified.format('isoDate') + ' ' + |underscored_api_name|.date_modified.format('isoTime'),
                                    |underscored_api_name|_id: |underscored_api_name|_id,
                                    |underscored_api_name|_name: |underscored_api_name|.name
                                }
                            )
                        );
                    }
                }
            });

            self.\$('.|prefix||underscored_pluralized_api_name|_row')
                .die('click')
                .live('click', function () {
                    var |underscored_api_name|_key = self.get_entity_key_for_entities_table_row(this),
                        |underscored_api_name|_name = self.\$('#|prefix|entity_row_' + |underscored_api_name|_key + ' > .|prefix||underscored_pluralized_api_name|_row_name').html();

                    self.\$('#|prefix|status_bar').html(|underscored_api_name|_name + ' |underscored_api_name| key :: ' + |underscored_api_name|_key);
                });

            self.\$('.|prefix||underscored_pluralized_api_name|_row')
                .die('dblclick')
                .live('dblclick', function () {
                    self.init_|underscored_api_name|_editor(self.get_entity_key_for_entities_table_row(this));
                });
        };
        // }}}

        // remove_|underscored_api_name|_manager {{{
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.remove_|underscored_api_name|_manager = function () {
            var self = this;

            self.\$('.|prefix||underscored_pluralized_api_name|_editor').html('');
            self.|underscored_pluralized_api_name|_editor = null;
        };
        // }}}

        // init_|underscored_api_name|_editor {{{
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.init_|underscored_api_name|_editor = function (|underscored_api_name|_key) {
            var self = this;

            if (typeof |underscored_api_name|_key === 'undefined') {
                |underscored_api_name|_key = null;
            }

            var |underscored_api_name|_name = self.\$('#|prefix|entity_row_' + |underscored_api_name|_key + ' .|prefix||underscored_pluralized_api_name|_row_name').html();

            self.|underscored_pluralized_api_name|_editor = 
                self.\$('.|prefix||underscored_pluralized_api_name|_editor').|lower_camelcased_pluralized_api_name|Editor(|underscored_api_name|_key)[0];

            self.elements.|underscored_pluralized_api_name|_table.hide();
            
            // set subtitle
            var section_title = |underscored_api_name|_key ? "Edit " + |underscored_api_name|_name : "Add new |underscored_api_name|";
            self.set_section_title(section_title);

            var reload_table = false;
            self.|underscored_pluralized_api_name|_editor.on('saved', function () {
                reload_table = true;
            });

            self.|underscored_pluralized_api_name|_editor.on('done', function () {
                if (reload_table) {
                    self.load_entities_table();
                }

                self.clear_section_title();
                self.remove_|underscored_api_name|_manager();
                self.elements.|underscored_pluralized_api_name|_table.show();
            });
        };
        // }}}

        // set_section_title {{{
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.set_section_title = function (title) {
            var self = this;

            self.elements.|underscored_pluralized_api_name|_section_title.html(title).show();
        };
        // }}}

        // clear_section_title {{{
        \$.Admin|camelcased_pluralized_api_name|Section.prototype.clear_section_title = function () {
            var self = this;

            self.elements.|underscored_pluralized_api_name|_section_title.hide();
        };
        // }}}

        // closeSection {{{
        $.Admin|camelcased_pluralized_api_name|Section.prototype.closeSection = function () {
            var self = this;

            if (self.|underscored_pluralized_api_name|_editor !== null) {
                self.|underscored_pluralized_api_name|_editor.cancel();
            }
        };
        // }}}

        // }}}
    })(jQuery);

    // vim:fdm=marker:fmr={{{,}}}:
EOF
)"

echo "$(template_populator "$api_admin_frontend_section_template")" > "$api_admin_frontend_section_path"
# }}}

# Generate api_javascript_object_path {{{
api_javascript_object_template="$(cat <<EOF
    (function (\$) {
        \$.|underscored_api_name|_api = {
            // list {{{
            list: function (order, page, callback) {
                \$.ajax({
                    type: 'GET',
                    cache: false,
                    url: '/|underscored_api_name|/all/',
                    data: {order_by: order, page: page},
                    success: function (result) {
                        callback(result);
                    },
                    dataType: 'json'
                });
            },
            // }}}

            // get {{{
            get: function (key, callback) {
                \$.ajax({
                    type: 'GET',
                    cache: false,
                    url: '/|underscored_api_name|/' + key + '/',
                    success: function (result) {
                        callback(result);
                    },
                    dataType: 'json'
                });
            }
            // }}}
        };
    })(jQuery);

    // vim:fdm=marker:fmr={{{,}}}:
EOF
)"

echo "$(template_populator "$api_javascript_object_template")" > "$api_javascript_object_path"
# }}}

# Templates template: Generate tasks.txt {{{
tasks_txt_template="$(cat <<EOF
    1. Check |TODO| on $api_python_module_path

    2. Drop the following lines to app.yaml:

        # |underscored_api_name| API {{{
        # admin parts {{{
        - url: /|underscored_api_name|/create(/.*)?
          script: apis/|underscored_api_name|.py
          login: admin

        - url: /|underscored_api_name|/([^/]*)/(save|remove)(/.*)?
          script: apis/|underscored_api_name|.py
          login: admin
        # }}}

        - url: /|underscored_api_name|(/.*)?
          script: apis/|underscored_api_name|.py
        # }}}

    3. Add to the Makefile ADMIN_FRONTEND_JS_FILES var:
        \${JS_SRC_DIR}/apis/|underscored_api_name|.js\\ 
        \${ADMIN_FRONTEND_JS_SRC_DIR}/|underscored_pluralized_api_name|_editor.js\\ 
        \${ADMIN_FRONTEND_JS_SRC_DIR}/|underscored_pluralized_api_name|_section.js\\ 

    4. Add to /frontends/admin.html: 
            <h2>Edit</h2>
            <ul>
                <li><a id="open-|underscored_pluralized_api_name|-editor" href="javascript:void(0);">|human_readable_capitalized_pluralized_api_name|</a></li>
            </ul>

        <script type="text/javascript">
            \$('#open-|underscored_pluralized_api_name|-editor').click(function () {
                switchSection('|human_readable_capitalized_pluralized_api_name| Editor',
                    'admin|camelcased_pluralized_api_name|Section');
            });
        </script>

EOF
)"

echo "$(template_populator "$tasks_txt_template")" > "$tasks_txt_path"
# }}}

# Generate the element editor constructor style {{{
api_python_module_template="$(cat <<EOF
    #!/usr/bin/env python

    ###########################################################
    # Solve bug: http://groups.google.com/group/google-appengine-python/browse_thread/thread/e3a9d8b8be36870d/5dc96ab56b889dc6?pli=1
    # Remove the standard version of Django and put version 1.1
    import os

    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from appengine_django import InstallAppengineHelperForDjango
    InstallAppengineHelperForDjango(version='1.1')
    ###########################################################

    from google.appengine.ext import webapp, db
    from google.appengine.ext.webapp import template
    from google.appengine.ext.webapp.util import run_wsgi_app

    from lib import simplejson as json
    from django.utils.datastructures import SortedDict

    from google.appengine.api import users

    from urlparse import urlparse

    import os

    from apis.helpers.paging import PagedQuery

    from datetime import datetime, date
    class JsonEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime):
                return '**new Date(%i,%i,%i,%i,%i,%i)' % (obj.year,
                                                          obj.month-1,
                                                          obj.day,
                                                          obj.hour,
                                                          obj.minute,
                                                          obj.second)

            if isinstance(obj, date):
                return '**new Date(%i,%i,%i)' % (obj.year,
                                                 obj.month-1,
                                                 obj.day)

            if isinstance(obj, db.Model):
                dict_representation = {}
                for field in obj.fields():
                    dict_representation[field] = getattr(obj, field)

                return dict_representation

            return obj.__dict__


    class |camelcased_api_name|(db.Expando):
        # Attributes
        name = db.StringProperty(default="New |human_readable_capitalized_api_name|")

        # |TODO| Put your module attributes here
        # elements = db.TextProperty(default="{}")
        # options = db.TextProperty(default="{}")

        # modifications date tracking
        date_created = db.DateTimeProperty(auto_now_add=True)
        date_modified = db.DateTimeProperty(auto_now=True)

        # created by
        created_by = db.UserProperty()
        # modified by
        modified_by = db.UserProperty()


    def _get_path_|underscored_api_name|(path):
        "Get the |human_readable_non_capitalized_api_name| object of the url path's |human_readable_non_capitalized_api_name| key"

        |underscored_api_name|_key = urlparse(path).path.split('/')[2]

        try:
            |underscored_api_name| = db.get(db.Key(|underscored_api_name|_key))
        except db.BadKeyError:
            return (400, {'error': 'InvalidKey'})

        return (200, |underscored_api_name|)


    class All(webapp.RequestHandler):
        """Return an object with all the |human_readable_non_capitalized_pluralized_api_name| objects
        """
        def get(self):
            page_size = self.request.GET.get('page_size') or 30
            page = self.request.GET.get('page') or 1
            order_by = self.request.GET.get('order_by') or '-date_modified'

            page = int(page)

            |underscored_pluralized_api_name|_query = |camelcased_api_name|.all().order(order_by)
            paged_query = PagedQuery(|underscored_pluralized_api_name|_query, page_size)

            results = paged_query.fetch_page(page)
            pages_count = paged_query.page_count()

            response = {'|underscored_pluralized_api_name|': SortedDict(), 'pager': {'pages_count': pages_count}}
            for |underscored_api_name| in results:
                key = str(|underscored_api_name|.key())
                response['|underscored_pluralized_api_name|'][key] = |underscored_api_name|

            return self.response.out.write(json.dumps(response, cls=JsonEncoder))


    class Get(webapp.RequestHandler):
        """Retrun a |human_readable_non_capitalized_api_name| object 
        """
        def get(self):
            status, object = _get_path_|underscored_api_name|(self.request.path)

            if status != 200:
                self.response.set_status(status)
                return self.response.out.write(json.dumps(object, cls=JsonEncoder))
            else:
                |underscored_api_name| = object # just to improve readability

            return self.response.out.write(json.dumps(|underscored_api_name|, cls=JsonEncoder))


    class Create(webapp.RequestHandler):
        """Create a new |human_readable_non_capitalized_api_name|
        """

        def post(self):
            |underscored_api_name| = |camelcased_api_name|()

            query = json.loads(self.request.POST['query'])

            fields = |underscored_api_name|.fields()
            for key in query:
                if key in fields:
                    setattr(|underscored_api_name|, key, query[key])

            |underscored_api_name|.created_by = users.User()
            |underscored_api_name|.modified_by = users.User()

            |underscored_api_name|.put()

            return self.response.out.write(json.dumps({'|underscored_api_name|_key': str(|underscored_api_name|.key())}, cls=JsonEncoder))

    class Save(webapp.RequestHandler):
        """Edit existing one
        """
        def post(self):
            status, object = _get_path_|underscored_api_name|(self.request.path)

            if status != 200:
                self.response.set_status(status)
                return self.response.out.write(json.dumps(object, cls=JsonEncoder))
            else:
                |underscored_api_name| = object # just to improve readability

            query = json.loads(self.request.POST['query'])

            fields = |underscored_api_name|.fields()
            for key in query:
                if key in fields:
                    setattr(|underscored_api_name|, key, query[key])

            |underscored_api_name|.modified_by = users.User()

            |underscored_api_name|.put()

            return self.response.out.write(json.dumps({}, cls=JsonEncoder))


    class Default(webapp.RequestHandler):
        """Default serves the paths we don't have particular mapping for
        """
        def get(self):
            if self.request.path[-1] != '/':
                return self.redirect(self.request.path + '/', permanent=True)

            self.error(404)


    application = webapp.WSGIApplication([
        ('/|underscored_api_name|/all/', All),
        ('/|underscored_api_name|/create/', Create),
        ('/|underscored_api_name|/[^/]*/save/', Save),
        ('/|underscored_api_name|/[^/]*/', Get),
        ('.*', Default),
    ], debug=True)

    def main():
        run_wsgi_app(application)

    if __name__ == '__main__':
        main()
EOF
)"

echo "$(template_populator "$api_python_module_template")" > "$api_python_module_path"
# }}}

# vim:ft=bash:fdm=marker:fmr={{{,}}}:

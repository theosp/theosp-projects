/*
$.Admin{{ camelcased_pluralized_entity_name }}Section

AUTHOR: Daniel Chcouri <333222@gmail.com>

RERUIRES: Daniel Chcouri's theosp_common_js (theosp.js)
          Daniel Chcouri's $.AdminSection
              Node.js's EventEmitter
          Steven Levithan date.format.js
*/
(function ($) {
    // constructor {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section = function (parent, options) {
        var self = this;

        self.elements = {
            parent: $(parent)
        };

        if (typeof options === 'undefined') {
            options = {};
        }
        self.options = theosp.object.clone(self.options); // clone the prototypical options
        $.extend(self.options, options);

        self.{{ underscored_pluralized_entity_name }}_editor = null;

        self.init();
    };

    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype = new $.AdminSection();
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.constructor = $.Admin{{ camelcased_pluralized_entity_name }}Section;

    $.fn.extend({
        admin{{ camelcased_pluralized_entity_name }}Section: function (options) {
            var admin{{ camelcased_pluralized_entity_name }}SectionObjects = [];

            this.each(function () {
                admin{{ camelcased_pluralized_entity_name }}SectionObjects.push(new $.Admin{{ camelcased_pluralized_entity_name }}Section(this, options));
            });

            return admin{{ camelcased_pluralized_entity_name }}SectionObjects;
        }
    });
    // }}}

    // properties {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.options = {
        // dom options {{{
        css_prefix: 'Admin{{ camelcased_pluralized_entity_name }}Section-'
        // }}}
    };
    // }}}

    // methods {{{

    // initDom {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.initDom = function () {
        var self = this;

        self.elements.parent.html(
            theosp.string.supplant(
                (
                 '<div class="|prefix|admin_{{ underscored_pluralized_entity_name }}_section_container">' +
                     '<div class="|prefix|admin_{{ underscored_pluralized_entity_name }}_section">' +
                        '<h3 style="display: none;"></h3>' +
                        '<table class="|prefix|{{ underscored_pluralized_entity_name }}_table">' +
                            '<thead>' +
                                '<tr>' +
                                    {% @admin_frontend_section_table_properties %}
                                    '<th class="|prefix|order_bys" id="|prefix|order_by_{{ item.name }}">{{ item.capitalized_name }}</th>' +
                                    {% /@admin_frontend_section_table_properties %}
                                    '<th class="|prefix|order_bys" id="|prefix|order_by_created_by">Created By</th>' +
                                    '<th class="|prefix|order_bys" id="|prefix|order_by_modified_by">Modified By</th>' +
                                    '<th class="|prefix|order_bys" id="|prefix|order_by_date_created">Created</th>' +
                                    '<th class="|prefix|order_bys" id="|prefix|order_by_date_modified">Modified</th>' +
                                '</tr>' +
                            '</thead>' +
                            '<tbody>' +
                            '</tbody>' +
                            '<tfoot>' +
                                '<tr><td id="|prefix|status_bar" colspan="{{ admin_section_table_cols_count }}">Click on a row to get its key</td></tr>' +
                                '<tr><td colspan="{{ admin_section_table_cols_count }}">' +
                                    '<div id="|prefix|pager"></div>' +
                                    '<a id="|prefix|add_{{ underscored_entity_name }}" href="javascript:void(0);">Add New {{ readable_capitalized_entity_name }}</a>' +
                                '</td></tr>' +
                            '</tfoot>' +
                        '</table>' +
                        '<div class="|prefix|{{ underscored_pluralized_entity_name }}_editor_container |prefix|invisible">' +
                            '<div class="|prefix|{{ underscored_pluralized_entity_name }}_editor"></div>' +
                        '</div>' +
                     '</div>' +
                 '</div>'
                ), {prefix: self.options.css_prefix
                }
            )
        );

        self.elements.{{ underscored_pluralized_entity_name }}_section_title = self.$('.|prefix|admin_{{ underscored_pluralized_entity_name }}_section_container h3');
        self.elements.{{ underscored_pluralized_entity_name }}_table = self.$('.|prefix|{{ underscored_pluralized_entity_name }}_table');
        self.elements.{{ underscored_pluralized_entity_name }}_table_tbody = self.$('.|prefix|{{ underscored_pluralized_entity_name }}_table > tbody');

        self.$('.|prefix|order_bys').click(function () {
            var order_by = $(this)[0].id.replace(self.options.css_prefix + 'order_by_', '');
            
            if (self.options.order_by === order_by) {
                self.options.order_by = '-' + order_by;
            } else {
                self.options.order_by = order_by;
            }

            self.options.page = 1;

            self.load_entities_table();
        });

        self.$('#|prefix|add_{{ underscored_entity_name }}').click(function () {
            self.init_{{ underscored_entity_name }}_editor();
        });

        self.load_entities_table();
    };
    // }}}

    // load_entities_table {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.load_entities_table = function () {
        var self = this;

        $.{{ underscored_entity_name }}_api.list(self.options.order_by, self.options.page, function (response) {
            var {{ underscored_pluralized_entity_name }}_table_tbody = self.elements.{{ underscored_pluralized_entity_name }}_table_tbody;
            {{ underscored_pluralized_entity_name }}_table_tbody.html('');

            var {{ underscored_pluralized_entity_name }}_list = response.{{ underscored_pluralized_entity_name }};
            self.options.pages_count = response.pager.pages_count;
            self.update_pager();

            for (var {{ underscored_entity_name }}_id in {{ underscored_pluralized_entity_name }}_list) {
                if ({{ underscored_pluralized_entity_name }}_list.hasOwnProperty({{ underscored_entity_name }}_id)) {
                    var {{ underscored_entity_name }} = {{ underscored_pluralized_entity_name }}_list[{{ underscored_entity_name }}_id];

                    {{ underscored_entity_name }}.date_created = self.parseDjangoJsonDate({{ underscored_entity_name }}.date_created);
                    {{ underscored_entity_name }}.date_modified = self.parseDjangoJsonDate({{ underscored_entity_name }}.date_modified);

                    {{ underscored_pluralized_entity_name }}_table_tbody.append(
                        theosp.string.supplant(
                            (
                                '<tr class="|prefix|{{ underscored_pluralized_entity_name }}_row" id="|prefix|entity_row_|{{ underscored_entity_name }}_id|">' +
                                    {% @admin_frontend_section_table_properties %}
                                    '<td class="|prefix|{{ underscored_pluralized_entity_name }}_row_{{ item.name }}">|{{ item.name }}|</td>' + 
                                    {% /@admin_frontend_section_table_properties %}
                                    '<td class="|prefix|{{ underscored_pluralized_entity_name }}_row_created_by">|created_by|</td>' + 
                                    '<td class="|prefix|{{ underscored_pluralized_entity_name }}_row_modified_by">|modified_by|</td>' + 
                                    '<td class="|prefix|{{ underscored_pluralized_entity_name }}_row_created">|created|</td>' + 
                                    '<td class="|prefix|{{ underscored_pluralized_entity_name }}_row_modified">|modified|</td>' + 
                                '</tr>'
                            ), {prefix: self.options.css_prefix,

                                {{ underscored_entity_name }}_id: {{ underscored_entity_name }}_id,

                                {% @admin_frontend_section_table_properties %}
                                {{ item.name }}: {{ underscored_entity_name }}.{{ item.name }},
                                {% /@admin_frontend_section_table_properties %}

                                created_by: {{ underscored_entity_name }}.created_by._User__email,
                                modified_by: {{ underscored_entity_name }}.modified_by._User__email,
                                created: {{ underscored_entity_name }}.date_created.format('isoDate') + ' ' + {{ underscored_entity_name }}.date_created.format('isoTime'),
                                modified: {{ underscored_entity_name }}.date_modified.format('isoDate') + ' ' + {{ underscored_entity_name }}.date_modified.format('isoTime')
                            }
                        )
                    );
                }
            }
        });

        self.$('.|prefix|{{ underscored_pluralized_entity_name }}_row')
            .die('click')
            .live('click', function () {
                var {{ underscored_entity_name }}_key = self.get_entity_key_for_entities_table_row(this);

                self.$('#|prefix|status_bar').html('Item Key :: ' + {{ underscored_entity_name }}_key);
            });

        self.$('.|prefix|{{ underscored_pluralized_entity_name }}_row')
            .die('dblclick')
            .live('dblclick', function () {
                self.init_{{ underscored_entity_name }}_editor(self.get_entity_key_for_entities_table_row(this));
            });
    };
    // }}}

    // remove_{{ underscored_entity_name }}_manager {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.remove_{{ underscored_entity_name }}_manager = function () {
        var self = this;

        self.$('.|prefix|{{ underscored_pluralized_entity_name }}_editor').html('');
        self.{{ underscored_pluralized_entity_name }}_editor = null;
    };
    // }}}

    // init_{{ underscored_entity_name }}_editor {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.init_{{ underscored_entity_name }}_editor = function ({{ underscored_entity_name }}_key) {
        var self = this;

        if (typeof {{ underscored_entity_name }}_key === 'undefined') {
            {{ underscored_entity_name }}_key = null;
        }

        var {{ underscored_entity_name }}_name = self.$('#|prefix|entity_row_' + {{ underscored_entity_name }}_key + ' .|prefix|{{ underscored_pluralized_entity_name }}_row_name').html();

        self.{{ underscored_pluralized_entity_name }}_editor = 
            self.$('.|prefix|{{ underscored_pluralized_entity_name }}_editor').{{ lower_camelcased_pluralized_entity_name }}Editor({{ underscored_entity_name }}_key)[0];

        self.elements.{{ underscored_pluralized_entity_name }}_table.hide();
        
        // set subtitle
        var section_title = {{ underscored_entity_name }}_key ? "Edit" : "Add new {{ underscored_entity_name }}";
        self.set_section_title(section_title);

        var reload_table = false;
        self.{{ underscored_pluralized_entity_name }}_editor.on('saved', function () {
            reload_table = true;
        });

        self.{{ underscored_pluralized_entity_name }}_editor.on('done', function () {
            if (reload_table) {
                self.load_entities_table();
            }

            self.clear_section_title();
            self.remove_{{ underscored_entity_name }}_manager();
            self.elements.{{ underscored_pluralized_entity_name }}_table.show();
        });
    };
    // }}}

    // set_section_title {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.set_section_title = function (title) {
        var self = this;

        self.elements.{{ underscored_pluralized_entity_name }}_section_title.html(title).show();
    };
    // }}}

    // clear_section_title {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.clear_section_title = function () {
        var self = this;

        self.elements.{{ underscored_pluralized_entity_name }}_section_title.hide();
    };
    // }}}

    // closeSection {{{
    $.Admin{{ camelcased_pluralized_entity_name }}Section.prototype.closeSection = function () {
        var self = this;

        if (self.{{ underscored_pluralized_entity_name }}_editor !== null) {
            self.{{ underscored_pluralized_entity_name }}_editor.cancel();
        }
    };
    // }}}

    // }}}
})(jQuery);

// vim:fdm=marker:fmr={{{,}}}:

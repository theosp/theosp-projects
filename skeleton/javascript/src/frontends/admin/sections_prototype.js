/*
$.AdminSection

AUTHOR: Daniel Chcouri <333222@gmail.com>

RERUIRES: Node.js's EventEmitter
          Daniel Chcouri's theosp_common_js (theosp.js)
          Steven Levithan date.format.js
*/
(function ($) {
    // constructor {{{
    $.AdminSection = function (options) {
        var self = this;

        self.parent = null;

        if (typeof options === 'undefined') {
            options = {};
        }
        self.options = theosp.object.clone(self.options); // clone the prototypical options
        $.extend(self.options, options);
    };

    $.AdminSection.prototype = new EventEmitter();
    $.AdminSection.prototype.constructor = $.AdminSection;
    // }}}

    // properties {{{
    $.AdminSection.prototype.options = {
        // meta_options
        css_prefix: 'AdminSection-',

        // pager options
        order_by: '-date_modified',
        page: 1,
        pages_count: 1
    };
    // }}}

    // methods {{{

    // $ {{{
    $.AdminSection.prototype.$ = function (selector, context) {
        var self = this;

        selector = theosp.string.supplant(selector, {
            prefix: self.options.css_prefix
        });

        return $(selector, context);
    };
    // }}}

    // init {{{
    $.AdminSection.prototype.init = function () {
        var self = this;

        // Set events that were passed via the options object
        for (var event in self.options.events) {
            if (self.options.events.hasOwnProperty(event)) {
                self.on(event, self.options.events[event]);
            }
        }

        self.initDom();
    };
    // }}}

    // initDom {{{
    $.AdminSection.prototype.initDom = function () {
        var self = this;
    };
    // }}}

    // parseDjangoJsonDate {{{
    $.AdminSection.prototype.parseDjangoJsonDate = function (date_string) {
        var self = this;

        args = date_string.replace('**new Date(', '').replace(')', '').split(',');

        return new Date(args[0], args[1], args[2], args[3] || 0, args[4] || 0, args[5] || 0);
    };
    // }}}

    // update_pager {{{
    $.AdminSection.prototype.update_pager = function () {
        var self = this;

        self.$('#|prefix|pager').html('');

        if (self.options.pages_count !== 1) {
            for (var i = 1; i <= self.options.pages_count; i++) {
                self.$('#|prefix|pager').append('<a href="javascript:void(0);" class="' + self.options.css_prefix + 'pager_links">' + i + '</a> ');
            }
        }

        self.$('.|prefix|pager_links').click(function () {
            self.options.page = parseInt($(this).html(), 10);
            self.load_entities_table();
        });

        self.$('.|prefix|pager_links:eq(' + (self.options.page - 1) + ')').css('text-decoration', 'underline');
    };
    // }}}

    // load_entities_table {{{
    $.AdminSection.prototype.load_entities_table = function () {
        var self = this;
    };
    // }}}

    // get_entity_key_for_entities_table_row {{{
    $.AdminSection.prototype.get_entity_key_for_entities_table_row = function (entity_row) {
        var self = this;

        return $(entity_row)[0].id.replace(self.options.css_prefix + 'entity_row_', '');
    };
    // }}}

    // get_entity_key_for_entities_table_field {{{
    $.AdminSection.prototype.get_entity_key_for_entities_table_field = function (entity_field) {
        var self = this;

        return self.get_entity_key_for_entities_table_row($(entity_field).parent()[0]);
    };
    // }}}

    // }}}
})(jQuery);

// vim:fdm=marker:fmr={{{,}}}:

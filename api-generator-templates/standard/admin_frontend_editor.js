/*
$.{{ camelcased_pluralized_entity_name }}Editor

AUTHOR: Daniel Chcouri <333222@gmail.com>

RERUIRES: Node.js's EventEmitter
          Daniel Chcouri's theosp_common_js (theosp.js)
*/
(function ($) {
    // constructor {{{
    $.{{ camelcased_pluralized_entity_name }}Editor = function (parent, key, options) {
        var self = this;

        self.elements = {
            parent: $(parent)
        };

        if (typeof key === 'undefined') {
            key = null;
        }
        self.key = key;

        if (typeof options === 'undefined') {
            options = {};
        }

        self.options = theosp.object.clone(self.options); // clone the prototypical options
        $.extend(self.options, options);

        self.model = theosp.object.clone(self.model); // clone the prototypical model

        self.init();
    };

    $.{{ camelcased_pluralized_entity_name }}Editor.prototype = new EventEmitter();
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.constructor = $.{{ camelcased_pluralized_entity_name }}Editor;

    $.fn.extend({
        {{ lower_camelcased_pluralized_entity_name }}Editor: function (key, options) {
            var {{ lower_camelcased_pluralized_entity_name }}Objects = [];

            this.each(function () {
                {{ lower_camelcased_pluralized_entity_name }}Objects.push(new $.{{ camelcased_pluralized_entity_name }}Editor(this, key, options));
            });

            return {{ lower_camelcased_pluralized_entity_name }}Objects;
        }
    });
    // }}}

    // properties {{{
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.options = {
        // margins {{{
        css_prefix: 'Admin{{ camelcased_pluralized_entity_name }}Editor-'
        // }}}
    };

    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.model = {
        name: ''
    };
    // }}}

    // methods {{{

    // $ {{{
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.$ = function (selector, context) {
        var self = this;

        selector = theosp.string.supplant(selector, {
            prefix: self.options.css_prefix,
            id: self.id
        });

        return $(selector, context);
    };
    // }}}

    // init {{{
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.init = function () {
        var self = this;

        // Set events that were passed via the options object
        for (var event in self.options.events) {
            if (self.options.events.hasOwnProperty(event)) {
                self.on(event, self.options.events[event]);
            }
        }

        if (self.key !== null) {
            $.{{ underscored_entity_name }}_api.get(self.key, function ({{ underscored_entity_name }}) {
                self.model.name = {{ underscored_entity_name }}.name;

                self.initDom();
            });
        } else {
            self.initDom();
        }
    };
    // }}}

    // initDom {{{
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.initDom = function () {
        var self = this;

        self.elements.parent.append(
            theosp.string.supplant(
                (
                 '<div class="|prefix|{{ underscored_pluralized_entity_name }}_editor_container">' +
                     '<div class="|prefix|{{ underscored_pluralized_entity_name }}_editor">' +
                        '<form action="javascript:void(0);" id="|prefix|{{ underscored_pluralized_entity_name }}_editor_form">' +
                            '<table>' +
                                '<tbody>' +
                                    '<tr>' +
                                        '<td><label for="|prefix|{{ underscored_entity_name }}_key">Key</label></td>' +
                                        '<td>' +
                                            '<input readonly="readonly" id="|prefix|{{ underscored_entity_name }}_key" class="key" type="text" value="' + 
                                                function () {
                                                    return self.key || "New";
                                                }() + 
                                            '" />' +
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td><label for="|prefix|{{ underscored_entity_name }}_name">Name</label></td>' +
                                        '<td>' +
                                            '<input id="|prefix|{{ underscored_entity_name }}_name" class="name" type="text" value="|name|" maxlength="500" />' +
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
                    submit_value: self.key ? "Save" : "Add new {{ readable_noncapitalized_entity_name }}"
                }
            )
        );

        self.$('#|prefix|{{ underscored_pluralized_entity_name }}_editor_form').submit(function () {
            self.save(function () {
                self.emit('done');
            });
        });

        self.$('#|prefix|cancel_edits').click(function () {
            self.cancel();
        });
    };
    // }}}

    // save {{{
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.save = function (callback) {
        var self = this;

        self.model.name = self.$('#|prefix|{{ underscored_entity_name }}_name').val();

        var action_url;

        if (self.key === null) {
            action_url = '/{{ underscored_entity_name }}/create/';
        } else {
            action_url = '/{{ underscored_entity_name }}/' + self.key + '/save/';
        }

        $.ajax({
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
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.cancel = function () {
        var self = this;

        self.emit('cancelled');
        self.done();
    };
    // }}}

    // done {{{
    $.{{ camelcased_pluralized_entity_name }}Editor.prototype.done = function () {
        var self = this;

        self.$('.|prefix|{{ underscored_pluralized_entity_name }}_editor_container').remove();

        self.emit('done');
    };
    // }}}

    // }}}
})(jQuery);

// vim:fdm=marker:fmr={{{,}}}:

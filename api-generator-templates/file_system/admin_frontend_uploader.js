/*
$.{{ camelcased_pluralized_entity_name }}Uploader

AUTHOR: Daniel Chcouri <333222@gmail.com>

RERUIRES: Node.js's EventEmitter
          Daniel Chcouri's theosp_common_js (theosp.js)
*/
(function ($) {
    // constructor {{{
    $.{{ camelcased_pluralized_entity_name }}Uploader = function (parent, options) {
        var self = this;

        self.elements = {
            parent: $(parent)
        };

        if (typeof options === 'undefined') {
            options = {};
        }

        self.options = theosp.object.clone(self.options); // clone the prototypical options
        $.extend(self.options, options);

        self.model = theosp.object.clone(self.model); // clone the prototypical model
        self.upload_url = null;

        self.init();
    };

    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype = new EventEmitter();
    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.constructor = $.{{ camelcased_pluralized_entity_name }}Uploader;

    $.fn.extend({
        {{ lower_camelcased_pluralized_entity_name }}Uploader: function (key, options) {
            var {{ lower_camelcased_pluralized_entity_name }}Objects = [];

            this.each(function () {
                {{ lower_camelcased_pluralized_entity_name }}Objects.push(new $.{{ camelcased_pluralized_entity_name }}Uploader(this, key, options));
            });

            return {{ lower_camelcased_pluralized_entity_name }}Objects;
        }
    });
    // }}}

    // properties {{{
    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.options = {
        // margins {{{
        css_prefix: 'Admin{{ camelcased_pluralized_entity_name }}Uploader-'
        // }}}
    };

    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.model = {
        name: ''
    };
    // }}}

    // methods {{{

    // $ {{{
    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.$ = function (selector, context) {
        var self = this;

        selector = theosp.string.supplant(selector, {
            prefix: self.options.css_prefix,
            id: self.id
        });

        return $(selector, context);
    };
    // }}}

    // init {{{
    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.init = function () {
        var self = this;

        // Set events that were passed via the options object
        for (var event in self.options.events) {
            if (self.options.events.hasOwnProperty(event)) {
                self.on(event, self.options.events[event]);
            }
        }

        $.{{ underscored_entity_name }}_api.get_upload_url(function (upload_url) {
            self.upload_url = upload_url;

            self.initDom();
        });
    };
    // }}}

    // initDom {{{
    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.initDom = function () {
        var self = this;

        self.elements.parent.append(
            theosp.string.supplant(
                (
                 '<div class="|prefix|{{ underscored_pluralized_entity_name }}_uploader_container">' +
                     '<div class="|prefix|{{ underscored_pluralized_entity_name }}_uploader">' +

                        // form {{{
                        '<form action="|action|" method="POST" id="|prefix|{{ underscored_pluralized_entity_name }}_uploader_form" enctype="multipart/form-data" target="response_iframe">' +
                            '<table>' +
                                '<tbody>' +
                                    '<tr>' +
                                        '<td><label for="|prefix|{{ underscored_entity_name }}_permalink">Permanent Link</label></td>' +
                                        '<td>' +
                                            'http://{{ project_domain }}/{{ underscored_entity_name }}/<input id="|prefix|{{ underscored_entity_name }}_permalink" class="name" type="text" value="|name|" maxlength="500" name="permalink" />' +
                                        '</td>' +
                                    '</tr>' +
                                    '<tr>' +
                                        '<td><label for="|prefix|{{ underscored_entity_name }}_file">File</label></td>' +
                                        '<td>' +
                                            '<input id="|prefix|{{ underscored_entity_name }}_file" class="file" type="file" name="file" />' +
                                        '</td>' +
                                    '</tr>' +
                                '</tbody>' +
                            '</table>' +
                            '<input type="submit" value="|submit_value|" id="|prefix|submit_button" /> ' +
                            '<input type="button" value="Cancel" id="|prefix|cancel_edits" />' +
                        '</form>' +
                        // }}}

                        // iframe {{{
                        '<iframe name="response_iframe" id="|prefix|response_iframe" width="200" height="200" style="display: none;"></iframe>' +
                        // }}}
                        
                     '</div>' +
                 '</div>'
                ), {prefix: self.options.css_prefix,
                    name: self.model.name,
                    submit_value: "Upload {{ readable_noncapitalized_entity_name }}",
                    action: self.upload_url
                }
            )
        );

        self.$('#|prefix|response_iframe').load(function () {
            var current_iframe_location = $(this).contents().get(0).location.href;

            if (/success\/$/.test(current_iframe_location)) {
                self.emit('saved');
                self.emit('done');
            } else if (/failure\/.*?$/.test(current_iframe_location)) {
                $.{{ underscored_entity_name }}_api.get_upload_url(function (upload_url) {
                    self.upload_url = upload_url;
                    self.$("#|prefix|{{ underscored_pluralized_entity_name }}_uploader_form").attr("action", upload_url);

                    alert('Failed: ' + decodeURIComponent(current_iframe_location.replace(/.*failure\//, '')));
                })
            }
        });

        self.$('#|prefix|cancel_edits').click(function () {
            self.cancel();
        });
    };
    // }}}

    // cancel {{{
    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.cancel = function () {
        var self = this;

        self.emit('cancelled');
        self.done();
    };
    // }}}

    // done {{{
    $.{{ camelcased_pluralized_entity_name }}Uploader.prototype.done = function () {
        var self = this;

        self.$('.|prefix|{{ underscored_pluralized_entity_name }}_uploader_container').remove();

        self.emit('done');
    };
    // }}}

    // }}}
})(jQuery);

// vim:fdm=marker:fmr={{{,}}}:

/*
$.User

AUTHOR: Daniel Chcouri <333222@gmail.com>

RERUIRES: Node.js's EventEmitter
          Daniel Chcouri's ModesManager
          Daniel Chcouri's theosp_common_js (theosp.js)
*/
(function ($) {
    $.User = function (options) {
        var self = this;

        if (typeof options === 'undefined') {
            options = {};
        }
        self.options = theosp.object.clone(self.options); // clone the prototypical options
        $.extend(self.options, options);

        self.user_info = theosp.object.clone(self.user_info ); // clone the prototypical user_info 

        self.init();
    };

    $.User.prototype = new EventEmitter();
    $.User.prototype.constructor = $.User;

    $.User.prototype.options = { };

    $.User.prototype.user_info = { };

    $.User.prototype.init = function () {
        var self = this;

        $.ajax({
            type: 'GET',
            cache: false,
            url: '/user/me/',
            success: function (user_info) {
                self.user_info = user_info;

                self.emit('ready', self.user_info);
            },
            dataType: 'json',
            contentType: 'application/json; charset=utf-8'
        });
    };

    $.User.prototype.simpleUserConnectionStatusBar = function (jquery_object) {
        var self = this;

        if (typeof jquery_object === 'undefined') {
            return;
        }

        jquery_object.html('<a href="' + self.user_info.logout_url + '">Logout ' + self.user_info.email + '</a>');
    };
})(jQuery);

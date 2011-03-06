(function ($) {
    $.{{ underscored_entity_name }}_api = {
        // list {{{
        list: function (order, page, callback) {
            $.ajax({
                type: 'GET',
                cache: false,
                url: '/{{ underscored_entity_name }}/all/',
                data: {order_by: order, page: page},
                success: function (result) {
                    callback(result);
                },
                dataType: 'json'
            });
        },
        // }}}

        // get_upload_url {{{
        get_upload_url: function (success, failure) {
            if (typeof success === 'undefined') {
                if (typeof console !== 'undefined') {
                    console.log("$.{{ underscored_entity_name }}_api.get_upload_url(): Error success callback required.");
                }
                return;
            }

            if (typeof failure === 'undefined') {
                failure = function (result) {
                    if (typeof console !== 'undefined') {
                        console.log(result);
                    }
                }
            }

            $.ajax({
                type: 'GET',
                cache: false,
                url: '/{{ underscored_entity_name }}/get_upload_url/',
                success: function (result) {
                    success(result.upload_url);
                },
                failure: function (result) {
                    failure(result);
                },
                dataType: 'json'
            });
        },
        // }}}

        // get {{{
        get: function (key, callback) {
            $.ajax({
                type: 'GET',
                cache: false,
                url: '/{{ underscored_entity_name }}/' + key + '/',
                success: function (result) {
                    callback(result);
                },
                dataType: 'json'
            });
        },
        // }}}

        // remove {{{
        remove: function (key, callback) {
            $.ajax({
                type: 'GET',
                cache: false,
                url: '/{{ underscored_entity_name }}/' + key + '/remove/',
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

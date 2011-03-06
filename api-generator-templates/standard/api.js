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
        }
        // }}}
    };
})(jQuery);

// vim:fdm=marker:fmr={{{,}}}:

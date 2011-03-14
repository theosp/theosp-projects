(function ($) {
    $.{{ underscored_entity_name }}_api = {
        // list {{{
        list: function (order, page, success, error) {
            $.ajax({
                type: 'GET',
                cache: false,
                url: '/{{ underscored_entity_name }}/all/',
                data: {order_by: order, page: page},
                success: function (data, textStatus, jqXHR) {
                    if (typeof success !== 'undefined') {
                        success(data, textStatus, jqXHR);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    if (typeof error !== 'undefined') {
                        error(jqXHR, textStatus, errorThrown);
                    }

                    if (typeof console !== 'undefined') {
                        console.log(jqXHR, textStatus, errorThrown);
                    }
                },
                dataType: 'json'
            });
        },
        // }}}

        // get {{{
        get: function (key, success, error) {
            $.ajax({
                type: 'GET',
                cache: false,
                url: '/{{ underscored_entity_name }}/' + key + '/',
                success: function (data, textStatus, jqXHR) {
                    if (typeof success !== 'undefined') {
                        success(data, textStatus, jqXHR);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    if (typeof error !== 'undefined') {
                        error(jqXHR, textStatus, errorThrown);
                    }

                    if (typeof console !== 'undefined') {
                        console.log(jqXHR, textStatus, errorThrown);
                    }
                },
                dataType: 'json'
            });
        }
        // }}}
    };
})(jQuery);

// vim:fdm=marker:fmr={{{,}}}:

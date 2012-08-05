$(function () {
    $('.organization').each(function(index, value) {
        $(value).qtip({
            content: {
                url: "/organizations/" + $(value).attr("data-orgid") + "/popup"
            },

            position: {
                corner: {
                    target: 'center',
                    tootip: 'topLeft'
                }
            },

            style: {
                border: {
                    radius: 4
                }
            }
        });
    });
});

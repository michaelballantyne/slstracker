$(function () {
    $('#date').datepicker();

    var linkElement = $('#selectorg');

    var dialog = $('#orgsdialog').orgsdialog({
        onSelection: function (orgName, orgId) {
            linkElement.html(orgName);
            $('input[name=organization]').val(orgId);

        }
    });

    linkElement.click(function () {
        dialog.dialog('open');
        return false; 
    });

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

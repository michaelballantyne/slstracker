$(function () {
    $('#date').datepicker();

    var linkElement = $('#selectorg');

    var dialog = $('#dialog').orgsdialog({
        onSelection: function (orgName, orgId) {
            linkElement.html(orgName);
            $('input[name=organization]').val(orgId);

        }
    });

    linkElement.click(function () {
        dialog.dialog('open');
        return false; 
    });
});

$(function () {
    $('#date').datepicker();

    var linkElement = $('#selectorg');

    $('#reflection').tinymce({
        script_url : '/static/tiny_mce/tiny_mce.js',
        theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect,bullist,numlist,outdent,indent",
        theme_advanced_statusbar_location: "none",
        handle_event_callback: function () {
            if ($('#reflection').tinymce().isDirty()) {
                $('#unsaved').show();
            }
        }
    });

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

});

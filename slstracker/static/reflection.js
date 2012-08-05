$(function () {
    var reflection = $('#reflection');

    if ($('#reflectionsubmit').length != 0) {
        reflection.tinymce({
            script_url: '/static/tiny_mce/tiny_mce.js',
            theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontselect,fontsizeselect, bullist,numlist,|,outdent,indent",
            theme_advanced_statusbar_location : "none",
            mode: 'textareas',
            handle_event_callback: function () {
                if (reflection.tinymce().isDirty()) {
                    $('#unsaved').html('You have unsaved changes');
                } else {
                    $('#unsaved').html('');
                }
            }
        });
    } else {
        reflection.tinymce({
            script_url: '/static/tiny_mce/tiny_mce.js',
            readonly: true
        });
    }
});

$(function () {
    var saving = false;
    $('#reflection').tinymce({
        script_url : '/static/tiny_mce/tiny_mce.js',
        theme_advanced_buttons1 : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect,bullist,numlist,outdent,indent",
        theme_advanced_statusbar_location: "none",
        handle_event_callback: function () {
            if ($('#reflection').tinymce().isDirty()) {
                $('#unsaved').show();
                $(window).bind('beforeunload', function() { 
                    if (saving) {
                        return None;
                    } else {
                        return "You have modified your reflection, but not saved. You will lose these changes if you navigate away from this page."
                    }
                });
            }
        }
    });

    $('#reflectionsubmit').click(function () {
        saving = true;
    });
});

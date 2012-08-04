$(function () {
    $('#date').datepicker();

    $('#tabs').tabs();

    $('#selectorg').click(function () {
        dialog.dialog('open');
        return false; 
    });

    var reloadOrganizationsList = function () {
        $.ajax({
            url: "/organizations/",
            dataType: 'json',
            success: function (data) {
                $('#orgs .selectable').remove();
                data = data['organizations'];
                var rowNum, colNum, tr;
                for (rowNum = 0; rowNum < data.length; rowNum++) {
                    tr = $('<tr>');

                    if (rowNum % 2 === 0) {
                        tr.addClass('alt');
                    }

                    tr.addClass('selectable');

                    tr.attr('orgid', data[rowNum][ data[rowNum].length - 1 ]);
                    tr.attr('orgname', data[rowNum][0]);

                    for (colNum = 0; colNum < data[rowNum].length - 1; colNum++) {
                        tr.append( $('<td>').html(data[rowNum][colNum]) );
                    }

                    $('#orgs').append(tr);
                }
            }
        });
    };

    reloadOrganizationsList();

    var dialog = $('#dialog').dialog(
    {
        autoOpen: false,
        title: 'Select an Organization',
        height: 'auto',
        width: '40em',
        modal: true,
        open: function (event, ui) { 
            $('.ui-widget-overlay').bind('click', function (){
                $("#dialog").dialog('close'); 
            }); 
        }
    });

    $('.selectable').live('click', function () {
        dialog.dialog('close');
        $('#selectorg').html($(this).attr('orgname'));
        $('input[name=organization]').val($(this).attr('orgid'));
    });


    $('#orgsform').submit(function () {
        $.post("/organizations/", $(this).serialize(), function (result) {
            $('#selectorg').html($('input[name=name]').val());
            $('input[name=organization]').val(result.id);
            dialog.dialog('close');
            reloadOrganizationsList();
            $('#tabs').tabs('select',0);
        }); 

        return false;
    });

});

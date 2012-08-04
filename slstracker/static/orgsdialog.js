(function ($) {
    $.widget("sls.orgsdialog", {
        options: {
            dataUrl: "/organizations/",
            onSelection: function () {}
        },

        _create: function () {
            var widget = this;

            this.element.dialog(
            {
                autoOpen: false,
                title: 'Select an Organization',
                height: 'auto',
                width: '40em',
                modal: true,
                open: function (event, ui) { 
                    $('.ui-widget-overlay').bind('click', function (){
                        widget.element.dialog('close'); 
                    }); 
                }
            });

            this._tabs = this.element.find('#orgs-dialog-tabs').tabs();

            this.element.find('.orgsform').submit(function () {
                $.post(widget.options.dataUrl, $(this).serialize(), function (result) {
                    var orgName = widget.element.find('input[name=name]').val();
                    var orgId = result.id;

                    widget.element.dialog('close');
                    widget.loadFromServer()
                    widget._tabs.tabs('select', 0);

                    widget.options.onSelection(orgName, orgId);
                }); 

                return false;
            });

            this.loadFromServer();
        },

        _setOption: function () {
            switch(key) {
                case "dataUrl":
                    this.loadFromServer();
                break;
            }
        },
        
        destroy: function () {

        },

        loadFromServer: function () {
            var widget = this;

            $.ajax({
                url: widget.options.dataUrl,
                dataType: 'json',
                success: function (data) {
                    var table = widget.element.find('.orgs')
                    table.find('.selectable').remove();

                    orgs = data['organizations'];
                    var rowNum, colNum, tr;
                    for (rowNum = 0; rowNum < orgs.length; rowNum++) {
                        tr = $('<tr>');

                        if (rowNum % 2 === 0) {
                            tr.addClass('alt');
                        }

                        tr.addClass('selectable');

                        tr.attr('orgid', orgs[rowNum][ orgs[rowNum].length - 1 ]);
                        tr.attr('orgname', orgs[rowNum][0]);

                        for (colNum = 0; colNum < orgs[rowNum].length - 1; colNum++) {
                            tr.append( $('<td>').html(orgs[rowNum][colNum]) );
                        }

                        table.append(tr);
                    }
                    
                    table.find('.selectable').bind('click', function () {
                        widget.element.dialog('close');

                        widget.options.onSelection($(this).attr('orgname'), $(this).attr('orgid'));
                    });
                }
            });
        }
    });
}) (jQuery);

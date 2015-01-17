<%namespace file="../common/search.mak" import="searchbar"/>
<%
    _id = h.common.gen_id()
    _tb_id = "tb-%s" % _id
%>
<div class="easyui-layout" data-options="fit:true">
    <div data-options="region:'north',border:false" style="height:365px">
        <div class="easyui-calendar tasks" id="_calendar" 
            data-url="${request.resource_url(_context, 'calendar')}"
            data-options="
                border:false,
                formatter: function(date){
                    return format_tasks_data(
                        date, '${_(u'open tasks')}', '${_(u'closed tasks')}'
                    );
                },
                onChange: function(newDate, oldDate){
                    $('#${_id}').datagrid('load');
                },
                onNavigate: function(year, month){
                    get_calendar_tasks_data(year, month);
                }
            " 
            style="width:100%;height:360px;">
        </div>
    </div>
    <div data-options="region:'center',border:false">
        <table class="easyui-datagrid"
            id="${_id}"
            data-options="
                url:'${request.resource_url(_context, 'list')}',border:false,
                pagination:true,fit:true,pageSize:50,singleSelect:true,
                sortName:'time',sortOrder:'asc',
                pageList:[50,100,500],idField:'_id',checkOnSelect:false,
                selectOnCheck:false,toolbar:'#${_tb_id}',
                view: detailview,
                onExpandRow: function(index, row){
                    var row_id = 'row-${_id}-' + row.id;
                    $('#' + row_id).load(
                        '/tasks/details?id=' + row.id, 
                        function(){
                            $('#${_id}').datagrid('fixDetailRowHeight', index);
                            $('#${_id}').datagrid('fixRowHeight', index);
                        }
                    );
                },
                detailFormatter: function(index, row){
                    var row_id = 'row-${_id}-' + row.id;
                    return '<div id=' + row_id + '></div>';
                },          
                onBeforeLoad: function(param){
                    var date = $('#_calendar').calendar('options').current;
                    param.y = date.getFullYear();
                    param.m = date.getMonth() + 1;
                    param.d = date.getDate();
                    $.each($('#${_tb_id} .searchbar').find('input'), function(i, el){
                    if(!is_undefined($(el).attr('name')))
                        param[$(el).attr('name')] = $(el).val();
                    });
                }
            " width="100%">
            <thead>
                % if _context.has_permision('delete'):
                <th data-options="field:'_id',checkbox:true">${_(u"id")}</th>
                % endif
                <th data-options="field:'title',sortable:true,width:280">${_(u"title")}</th>
                <th data-options="field:'time',sortable:true,width:70,formatter: function(value,row,index){
                    var span = $('<span/>').addClass('fa fa-clock-o mr05');
                    return $('<div/>').append(span).html() + value;
                },
		        styler: function(value,row,index){if(row.closed) return 'opacity:0.6;background-color:#eee;';}" class="tc">${_(u'time')}</th>
            </thead>
        </table>

        <div class="datagrid-toolbar" id="${_tb_id}">
            <div class="actions button-container dl25">
                <div class="button-group minor-group">
                    % if _context.has_permision('add'):
                    <a href="#" class="button primary _action" 
                        data-options="container:'#${_id}',action:'dialog_open',url:'${request.resource_url(_context, 'add')}'">
                        <span class="fa fa-plus"></span>${_(u'Add')}
                    </a>
                    % endif
                    % if _context.has_permision('view'):
                    <a href="#" class="button _action"
                        data-options="container:'#${_id}',action:'dialog_open',property:'with_row',url:'${request.resource_url(_context, 'view')}'">
                        <span class="fa fa-circle-o"></span>${_(u'View')}
                    </a>
                    % endif
                    % if _context.has_permision('edit'):
                    <a href="#" class="button _action"
                        data-options="container:'#${_id}',action:'dialog_open',property:'with_row',url:'${request.resource_url(_context, 'edit')}'">
                        <span class="fa fa-pencil"></span>${_(u'Edit')}
                    </a>
                    % endif
                    % if _context.has_permision('delete'):
                    <a href="#" class="button danger _action" 
                        data-options="container:'#${_id}',action:'dialog_open',property:'with_rows',url:'${request.resource_url(_context, 'delete')}'">
                        <span class="fa fa-times"></span>${_(u'Delete')}
                    </a>
                    % endif
                </div>
            </div>
            <div class="ml25 tr">
                <div class="searchbar" style="margin-top: 2px;">
                    ${h.tags.select(
                        'closed', None, 
                        [('', _(u'--all--')), (1, _(u'closed')), (0, _(u'open'))], 
                        class_='easyui-combobox w5',
                        data_options="panelHeight:'auto',editable:false,onChange:function(o_v, n_v){$('#%s').datagrid('load');}" % _id
                    )}
                </div>
            </div>
        </div>
    </div>
</div>

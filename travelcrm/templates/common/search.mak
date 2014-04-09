<%def name="searchbar(container, advanced_id=None, func=None)">
    <div class="searchbar" style="padding-top: 2px;">
        ${h.tags.text("q", None, class_="text w30 searchbox", onkeyup="onkeyup_%s(event);" % container)}
        <span class="field-actions">
		    <span class="fa fa-search easyui-tooltip field-action _action" 
				  title="${_(u'search')}"
				  data-options="container: '#${container}', action: 'refresh'">
			</span>
			% if advanced_id and func:
            <script type="text/javascript">
                function show_advanced_${container}(e){
                	if($('#${advanced_id}').is(':visible'))
                		$('#${advanced_id}').css('z-index', 1);
                	else{
                		var zindex = get_higher_zindex();
                		console.log(zindex);
                	    $('#${advanced_id}').css('z-index', zindex + 1);
                    }
                	$('#${advanced_id}').toggle();
                }
                $('#${advanced_id} a._advanced_search_submit').on(
                	'click',
                	function(event){
                		event.preventDefault();
                		$('#${advanced_id}').toggle();
                		refresh_container('#${container}');                		
                	}
                );
                $('#${advanced_id} a._advanced_search_clear').on(
                    'click',
                    function(event){
                        event.preventDefault();
                        clear_inputs('#${advanced_id}');
                    }
                );

            </script>
            <span class="fa fa-search-plus easyui-tooltip field-action _action" 
                  title="${_(u'advanced search')}"
                  onclick="show_advanced_${container}();">
            </span>
            % endif
		</span>
		<script type="text/javascript">
			function onkeyup_${container}(e){
			    if(e.keyCode == 13) refresh_container('#${container}');  
			}
	    </script>
	    % if advanced_id and func:
	       ${func(advanced_id)}
	    % endif
	</div>
</%def>

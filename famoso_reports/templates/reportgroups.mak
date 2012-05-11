<form class="readonly">
<fieldset>
<legend>Your Report Groups</legend>
<ul>
% for group in reportgroups:
	<li><a href="${request.route_path('reportgroup', name=group.name)}">${group.displayname}</a></li>
% endfor
</ul>
</fieldset>
</form>

<%inherit file="layout.mak" />

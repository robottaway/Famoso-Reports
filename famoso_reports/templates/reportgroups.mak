<h2>This is a listing of report groups</h2>
% for group in reportgroups:
	<div><a href="${request.route_path('reportgroup', name=group.name)}">${group.displayname}</a></div>
% endfor

<%inherit file="layout.mak" />

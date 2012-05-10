<h2>This is a listing of reports for the report group '${reportgroup.name}'</h2>
<ul>
% for group in reportgroup.reports:
	<li>${group.name}</li>
% endfor
</ul>

<%inherit file="layout.mak" />

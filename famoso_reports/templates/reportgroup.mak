% if len(request.user.findReportGroups()) > 1:
	<div><a href="${request.route_path('reportgroups')}">All Report Groups</a> &#187; ${reportgroup.displayname}</div>
% endif

<h2>This is a listing of reports for <strong>${reportgroup.displayname}</strong></h2>
<ul>
% for report in reportgroup.reports:
	<li><a href="${request.route_path('report', name=reportgroup.name, reportname=report.name)}">${report.name}</a></li>
% endfor
</ul>

<%inherit file="layout.mak" />

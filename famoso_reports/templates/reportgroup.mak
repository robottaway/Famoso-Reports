% if len(request.user.findReportGroups()) > 1:
<div class="breadcrumb">
	<a href="${request.route_path('reportgroups')}">Back to Report Groups</a>
</div>
% endif

<form class="readonly">
<fieldset>
<legend>${reportgroup.displayname}</legend>
<ul>
% for report in reportgroup.reports:
	<li><a href="${request.route_path('report', name=reportgroup.name, reportname=report.name)}">${report.name}</a></li>
% endfor
</ul>
</fieldset>
</form>

<%inherit file="layout.mak" />

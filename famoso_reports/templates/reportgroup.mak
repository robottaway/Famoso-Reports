% if len(request.user.findReportGroups()) > 1:
<div class="breadcrumb">
	<a href="${request.route_path('reportgroups')}">Back to Report Groups</a>
</div>
% endif

${self.flash()}

% if request.user.admin:
<form action="${request.route_path('rename_reportgroup', name=reportgroup.name)}" method="POST">
<fieldset>
<legend>Rename this report group</legend>
<ul>
    <lu><input type="text" name="newname" value="${reportgroup.displayname}" /></li>
    <li><button type="submit">Rename Report Group</button></li>
</ul>
</fieldset>
</form>
% endif

<form class="readonly">
<fieldset>
<legend>${reportgroup.displayname}</legend>
<ul>
% for report in reportgroup.reports:
	<li><a href="${request.route_path('report', name=reportgroup.name, reportname=report.name)}">${report.displayname}</a></li>
% endfor
</ul>
</fieldset>
</form>

<%inherit file="layout.mak" />

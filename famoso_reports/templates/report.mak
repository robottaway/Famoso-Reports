${self.flash()}

<div>
	<a href="${request.route_path('reportgroup', name=reportgroup.name)}">Back to reports for <strong>${reportgroup.displayname}</strong></a>
</div>

<fieldset>
<legend>Files for report ${report.displayname}</legend>
<ul>
% for file in report.file_names:
<li><a href="${request.route_url('report_download', name=reportgroup.name, file=file)}">${file}</a></li>
% endfor
</ul>
</fieldset>

% if request.user.admin:
% if reportgroup.users:
<form action="${request.route_path('email_report', name=reportgroup.name, reportname=report.name)}" method="POST">
<fieldset>
<legend>Email report to users</legend>
<ul>
% for user in reportgroup.users:
<li><label>${user.displayName()}</label><input type="checkbox" name="mailto" value="${user.username}" />
% endfor
<li><button>Send Report</button></li>
</ul>
</fieldset>
</form>
% endif
% endif

<%inherit file="layout.mak" />

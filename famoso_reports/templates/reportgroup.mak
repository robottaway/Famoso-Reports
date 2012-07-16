<%
from pyramid.url import urlencode

def querymake(request, name, value):
	part = urlencode(request.params)
	if len(part) > 0:
		new = "%s=%s" % (name, value)
		part = "?%s&%s" % (part, new)
	else:
		part = "?%s=%s" % (name, value)
	return part
%>
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

% if len(fatts.keys()) > 0:
<form class="readonly">
<fieldset>
<legend>Filter reports by attributes</legend>
% if len(request.params.keys()) > 0:
<p><a href="${request.route_path('reportgroup', name=reportgroup.name)}">Clear Filter</a></p>
% endif
% for name, values in fatts.items():
<p><strong>${name}</strong><br/>
% for value in values:
<span><a href="${request.route_path('reportgroup', name=reportgroup.name)}${querymake(request, name, value)}">${value}</a>&nbsp;&nbsp;</span>
% endfor
</p>
% endfor
</fieldset>
</form>
% endif

<form class="readonly">
<fieldset>
<legend>${reportgroup.displayname}</legend>
<ul>
% for report in reports:
	<li><a href="${request.route_path('report', name=reportgroup.name, reportname=report.name)}">${report.displayname}</a></li>
% endfor
</ul>
</fieldset>
</form>

<%inherit file="layout.mak" />

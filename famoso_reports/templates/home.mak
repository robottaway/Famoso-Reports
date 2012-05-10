% if request.user:
<div>
	<div>You are logged in as user '${request.user.displayName()}'</div>
	<a href="${request.route_path('reportgroups')}">View Reports</a>
</div>
% endif

<%inherit file="layout.mak" />

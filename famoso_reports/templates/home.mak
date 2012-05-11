% if request.user:
<div class="good_links">
	<h2>You are logged in as user '${request.user.displayName()}'</h2>
	<a href="${request.route_path('reportgroups')}">View Reports</a>
</div>
% endif

<%inherit file="layout.mak" />

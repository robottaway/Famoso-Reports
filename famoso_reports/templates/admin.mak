<div>
	<a href="${request.route_path('create_user')}">Create User</a>
</div>

<form class="readonly">
<fieldset>
<legend>You can view and update user info</legend>
<ul> 
% for user in users:
	<li><a href="${request.route_path('user', username=user.username)}">${user.displayName()}</a></li>
% endfor
</ul>
</fieldset>
</form>

<%inherit file="layout.mak" />

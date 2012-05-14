${self.flash()}

<div>
	<a href="${request.route_path('new_user')}">Add New User</a>
</div>

<form class="readonly">
<fieldset>
<legend>You can view and update user info</legend>
<ul> 
% for user in users:
% if user.id != request.user.id:
	<li><a href="${request.route_path('user', username=user.username)}">${user.displayName()}</a></li>
% endif
% endfor
</ul>
</fieldset>
</form>

<%inherit file="layout.mak" />

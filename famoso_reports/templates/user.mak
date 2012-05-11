
% if not request.user.admin:
<form class="readonly">
<fieldset>
<legend>Your are viewing user '${user.displayName()}'</legend>
<ul>
	<li><label>Username</label><div>${user.username}</div></li>
	<li><label>First Name</label><input type="text" value="${user.first_name}" /></li>
	<li><label>Last Name</label><input type="text" value="${user.last_name}" /></li>
	<li><label>Email</label><input type="text" value="${user.email}" /></li>
	<li><button type="submit">Update User Details</button></li>
</ul>
</fieldset>
</form>
<form id="passwordreset" action='auth' method='POST'>
	<fieldset>
		<legend>Please enter your username and password</legend>
		<ul>
			<li><label for="old">Old Password</label><input type="password" name="old" /></li>
			<li><label for="password">New Password</label><input type="password" name="password" /></li>
			<li><label for="password">Confirm New Password</label><input type="password" name="password" /></li>
			<li><button type="submit">Update Password</button></li>
		</ul>
	</fieldset>
</form>
% else:
<form class="readonly">
<fieldset>
<legend>Your are viewing user '${user.displayName()}'</legend>
<ul>
	<li><label>Username</label><input type="text" value="${user.username}" /></li>
	<li><label>First Name</label><input type="text" value="${user.first_name}" /></li>
	<li><label>Last Name</label><input type="text" value="${user.last_name}" /></li>
	<li><label>Email</label><input type="text" value="${user.email}" /></li>
	<li><button type="submit">Update User Details</button></li>
</ul>
</fieldset>
</form>
<form id="passwordreset" action='auth' method='POST'>
	<fieldset>
		<legend>You can update this user '${user.displayName()}' password</legend>
		<ul>
			<li><label for="password">New Password</label><input type="password" name="password" /></li>
			<li><label for="password">Confirm New Password</label><input type="password" name="password" /></li>
			<li><button type="submit">Update Password</button></li>
		</ul>
	</fieldset>
</form>
% if request.user.id != user.id:
<form id="passwordreset" action='${request.route_path('update_user_groups')}' method='POST'>
	<fieldset>
		<legend>You can update this user '${user.displayName()}' password</legend>
		<input type="hidden" name="username" value="${user.username}" />
		<ul>
% for group in groups:
			<li><input type="checkbox" name="group" value="${group.name}" /><label>${group.displayname}</label></li>
% endfor
			<li><button type="submit">Update Report Groups</button></li>
		</ul>
	</fieldset>
</form>
% endif
% endif

<%inherit file="layout.mak" />

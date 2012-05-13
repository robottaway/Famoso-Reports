${self.flash()}
% if not request.user.admin:
${self.userdetails()}
${self.passwordreset()}
% else:
${self.userdetails()}
${self.passwordreset()}
% if request.user.id != user.id:
<form action="${request.route_path('update_user_groups', username=user.username)}" method="POST">
	<fieldset>
		<legend>You can update report groups for user '${user.displayName()}'</legend>
		<input type="hidden" name="username" value="${user.username}" />
		<ul>
% for group in groups:
<%
checked = 'checked' if user.hasReportGroup(group) else ''
%>
			<li><input type="checkbox" name="groups" value="${group.name}" ${checked}/><label>${group.displayname}</label></li>
% endfor
			<li><button type="submit">Update Report Groups</button></li>
		</ul>
	</fieldset>
</form>
% endif
% endif

<%def name="passwordreset()">
<form action="${request.route_path('update_password', username=user.username)}" method="POST">
	<fieldset>
		<legend>Update Password</legend>
		<ul>
			<li><label for="password">New Password</label><input type="password" name="password" /></li>
			<li><label for="confirmpassword">Confirm New Password</label><input type="password" name="confirmpassword" /></li>
			<li><button type="submit">Update Password</button></li>
		</ul>
	</fieldset>
</form>
</%def>

<%def name="userdetails()">
<form action="${request.route_path('update_user_details', username=user.username)}" method="POST">
<fieldset>
% if user.id != request.user.id:
<legend>Your are viewing user '${user.displayName()}'</legend>
% else:
<legend>Your Account Details</legend>
% endif
<ul>
	<li><label>Username</label><div>${user.username}</div></li>
	<li><label>First Name</label><input type="text" value="${user.first_name}" name="first_name" length="64"/></li>
	<li><label>Last Name</label><input type="text" value="${user.last_name}" name="last_name" length="64"/></li>
	<li><label>Email</label><input type="text" value="${user.email}" name="email" length="256"/></li>
	<li><button type="submit">Update User Details</button></li>
</ul>
</fieldset>
</form>
</%def>

<%inherit file="layout.mak" />

${self.flash()}

<form action="${request.route_path('create_user')}" method="POST">
<fieldset>
<legend>Create a new user</legend>
<ul>
	<li><label>Username</label><input type="text" value="" name="username" length="20" /></li>
	<li><label>Password</label><input type="password" value="" name="password" length="20" /></li>
	<li><label>Confirm Password</label><input type="password" value="" name="confirmpassword" length="20" /></li>
	<li><label>First Name</label><input type="text" value="" name="first_name" length="64"/></li>
	<li><label>Last Name</label><input type="text" value="" name="last_name" length="64"/></li>
	<li><label>Email</label><input type="text" value="" name="email" length="256"/></li>
	<li><label>Admin</label><input type="checkbox" value="admin" name="admin" /></li>
	<li><button type="submit">Create User</button></li>
</ul>
</fieldset>
</form>

<%inherit file="layout.mak" />

% if request.session.peek_flash():
% for msg in request.session.pop_flash():
<div class="flash">${msg}</div>
% endfor
% endif
<form id="signin" action='auth' method='POST'>
	<fieldset>
		<legend>Please enter your username and password</legend>
		<ul>
			<li><label for="username">Username</label><input type="text" name="username" /></li>
			<li><label for="password">Password</label><input type="password" name="password" /></li>
			<li><button type="submit">Sign In</button></li>
		</ul>
	</fieldset>
</form>

<%inherit file="layout.mak" />

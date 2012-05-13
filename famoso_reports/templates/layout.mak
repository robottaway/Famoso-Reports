<!doctype html>
<html>
<head>
	<title>${self.title()}</title>
	${self.styles()}
<head>
<body class="bp">

<div id="header">
<div>
% if request.user:
	<a href="${request.route_path('reportgroups')}">View Reports</a> |
	<a href="${request.route_path('user', username=request.user.username)}">Account</a> |
% if request.user.admin:
	<a href="${request.route_path('admin')}">Admin</a> |
% endif
	<a href="/deauth">Logout</a>
% endif
</div>
</div>

${next.body()}

${self.scripts()}
</body>
</html>

<%def name="title()">Famoso Reports</%def>

<%def name="styles()">
  <link href="/static/css/screen.css" media="screen, projection" rel="stylesheet" type="text/css" />
  <link href="/static/css/print.css" media="print" rel="stylesheet" type="text/css" />
  <!--[if lt IE 8]>
      <link href="/static/css/ie.css" media="screen, projection" rel="stylesheet" type="text/css" />
  <![endif]-->
</%def>

<%def name="flash()">
% if request.session.peek_flash():
% for msg in request.session.pop_flash():
<div class="error">${msg}</div>
% endfor
% endif
</%def>

<%def name="scripts()">
</%def>

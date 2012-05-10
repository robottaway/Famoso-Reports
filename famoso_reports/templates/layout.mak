<!doctype html>
<html>
<head>
	<title>${self.title()}</title>
	${self.styles()}
<head>
</body class="bp">
<div id="header">
<a href="${request.route_path('home')}">Home</a>
% if request.user:
	<a href="${request.route_path('reportgroups')}">View Reports</a>
	<a href="/deauth">Logout</a>
% else:
	<a href="/signin">Sign In</a>
% endif
</div>

<div><img id="logo" src="/static/images/logo.jpg" alt="logo" /></div>
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

<%def name="scripts()">
</%def>

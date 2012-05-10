<!doctype html>
<html>
<head>
	<title>${self.title()}</title>
	${self.styles()}
<head>
</body class="bp">
% if request.user:
	<div><a href="/deauth">Logout</a></div>
% else:
	<div><a href="/signin">Sign In</a></div>
% endif
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

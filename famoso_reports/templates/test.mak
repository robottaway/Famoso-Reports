<html>
<head>
  <title>Famoso Reports</title>
  <link href="/static/css/screen.css" media="screen, projection" rel="stylesheet" type="text/css" />
  <link href="/static/css/print.css" media="print" rel="stylesheet" type="text/css" />
  <!--[if IE]>
      <link href="/static/css/ie.css" media="screen, projection" rel="stylesheet" type="text/css" />
  <![endif]-->
</head>
<body class="two-col">
<div id="container">

<div id="header">
% if request.user:
	<div><a href="/deauth">Logout</a></div>
% else:
	<div><a href="/signin">Sign In</a></div>
% endif
	<div><img id="logo" src="/static/images/logo.jpg" alt="logo" /></div>
</div>

<div id="content">
	<h1>up and online!</h1>
</div>

<div id="sidebar">
	<div>hi</div>
</div>

</div>
<body>
</html>

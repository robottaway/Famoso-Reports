<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Famoso Nut Company</title>
    ${self.styles()}
    <link rel="SHORTCUT ICON" href="/static/images/favicon.ico">
    <meta http-equiv="cache-control" content="no-cache">
    <meta http-equiv="pragma" content="no-cache"> 
</head>
<body class="styles">
<div id="container">
    <div id="header">
        <img src="/static/images/logo.jpg" alt="Famoso" />
        <div id="slideshow">
            <img src="/static/images/slideshow1.jpg" />
            <img src="/static/images/slideshow2.jpg" />
            <img src="/static/images/slideshow3.jpg" />
            <img src="/static/images/slideshow4.jpg" />
        </div>
    </div>
% if request.user:
    <div id="nav">
	<a href="${request.route_path('reportgroups')}"><div>View Reports</div></a>
	<a href="${request.route_path('user', username=request.user.username)}"><div>Account</div></a>
% if request.user.admin:
	<a href="${request.route_path('admin')}"><div>Admin</div></a>
% else:
	<a href="#"><div></div></a>
% endif
	<a href="/deauth"><div>Logout</div></a>
	<a href="#"><div></div></a>
	<a href="#"><div></div></a>
    </div>
% endif
    <div id="mainContent">
        ${next.body()}
    </div>
</div>
<p class="Footer">Famoso Nut Company, LLC &#8226; 32331 Famoso Road McFarland, CA 93250 &#8226; (661)399-9697 </p>
${self.javascript()}
</body>
</html>

<%def name="styles()">
    <link href="/static/css/screen.css" media="screen, projection" rel="stylesheet" type="text/css" />
    <link href="/static/css/print.css" media="print" rel="stylesheet" type="text/css" />
    <!--[if IE]>
    <link href="/static/css/ie.css" media="screen, projection" rel="stylesheet" type="text/css" />
    <![endif]-->
</%def>

<%def name="javascript()">
<script type="text/javascript" src="/static/js/jquery-1.6.2.min.js"></script>
<script>
    $(document).ready(function() {
        var slides = [];
        $('#slideshow > img').each(function() { slides.push($(this)); });
        function next(i) {
            if (i == 0) {
                slides[0].delay(1000).fadeIn('slow').delay(3000).fadeOut('slow', function(){next(i+1)});
            }
            else if (i == 3) {
                slides[3].fadeIn('slow');
                return;
            }
            else slides[i].fadeIn('slow').delay(3000).fadeOut('slow', function(){next(i+1)});
        }
        next(0);
    });
</script>
</%def>

<%def name="flash()">
% if request.session.peek_flash():
% for msg in request.session.pop_flash():
<div class="error">${msg}</div>
% endfor
% endif
</%def>

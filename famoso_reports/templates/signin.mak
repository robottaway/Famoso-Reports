<!DOCTYPE html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>Famoso Nut Company</title>
    <meta name="description" content="Famoso Nut Company is a locally-owned Almond huller, sheller, handler, and sales organization dedicated to the sale of quality Almond products.">
    <meta name="viewport" content="width=device-width">

		<link rel="stylesheet" href="http://famosonut.com/css/style.css">

    <script type="text/javascript" src="//use.typekit.net/yed7aoq.js"></script>
    <script type="text/javascript">try{Typekit.load();}catch(e){}</script>
		<style>
		body .error, body .alert {
			background: #fbe3e4;
			color: #8a1f11;
			border: 1px solid #fbc2c4;
			padding: 5px;
		}
		</style>
  </head>
  <body class="login">
    <!--[if lt IE 7]>
        <p class="chromeframe">
          You are using an <strong>outdated</strong> browser. Please
          <a href="http://browsehappy.com/">upgrade your browser</a> or
          <a href="http://www.google.com/chromeframe/?redirect=true">activate Google Chrome Frame</a>
          to improve your experience.
        </p>
    <![endif]-->

    <div class="container header">
      <header class="wrapper clearfix">
      <h1 id="logo" class="hide-text">
        <a href="http://famosonut.com">
          Famoso Nut
        </a>
      </h1>
      <nav>
        <ul>
          <li class="home"><a href="http://famosonut.com">Home</a></li>
          <li class="about"><a href="http://famosonut.com/about">About</a></li>
          <li class="services"><a href="http://famosonut.com/services">Services</a></li>
          <li class="products"><a href="http://famosonut.com/products">Products</a></li>
          <li class="contact"><a href="http://famosonut.com/contact">Contact</a></li>
          <li class="grower-login"><a href="http://reports.famosonut.com" target="_blank">Grower Login</a></li>
        </ul>
      </nav>
      </header>
    </div>

    <div class="container top">
      <!-- #photo -->
      <img src="http://famosonut.com/images/layout/photo-header.jpg" class="desktop-hidden">
    </div>

    <div class="container main">

      <div class="wrapper">
        <h2>Grower Login</h2>
        <hr />
        <div class="login-form">
					${self.flash()}
          <p class="login-desc">
            Please enter your username and password.
          </p>
          <form id="signin" action="auth" method="post">
            <input class="username" type="text" name="username" value="" placeholder="username">
            <input class="password" type="password" name="password" value="" placeholder="password">

            <input type="submit" class="form-submit" type="button" value="Sign In">
          </form>
        </div>
      </div>

    </div><!-- main -->


    <div class="container footer">

      <footer class="wrapper">
        <div class="pull-left">
          <ul>
            <li class="home"><a href="http://famosonut.com">Home</a></li>
            <li class="about"><a href="http://famosonut.com/about">About</a></li>
            <li class="services"><a href="http://famosonut.com/services">Services</a></li>
            <li class="products"><a href="http://famosonut.com/products">Products</a></li>
            <li class="contact"><a href="http://famosonut.com/contact">Contact</a></li>
            <li class="grower-login"><a href="http://reports.famosonut.com" target="_blank">Grower Login</a></li>
          </ul>
          <p class="copyright">
            Copyright &copy; 2013 Famoso Nut Company, LLC. All rights reserved.
          </p>
        </div>
        <div class="pull-right">
          <div class="address">
            Famoso Nut Company, LLC<br />
            32331 Famoso Road, McFarland, CA 93250<br />
            (661) 399-9697
          </div>
        </div>
      </footer>

    </div>

    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="http://famosonut.com/new/js/vendor/jquery-1.10.1.min.js"><\/script>')</script>

    <script src="js/global.js"></script>
  </body>
</html>
<%def name="flash()">
% if request.session.peek_flash():
% for msg in request.session.pop_flash():
<div class="error">${msg}</div>
% endfor
% endif
</%def>

#!/usr/bin/python -u

import cgi

print "Content-type: text/html"
print # Do not remove
print """
<!DOCTYPE html>
<html lang="en">
<!-- Code taken from Bootstrap website -->
<html>
  <head>
    <title>Mekong Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="css/bootstrap.min.css" rel="stylesheet" media="screen">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <nav class="collapse navbar-collapse navbar-collapse" role="navigation">
          <ul class="nav navbar-nav">
            <li><a href="#">Home</a></li>
            <li><a href="#">Recommendations</a></li>
            <li><a href="#">Trolley</a></li>
            <li><a href="#">Checkout</a></li>
          </ul>
          <form class="navbar-form navbar-left" role="search">
            <div class="form-group">
                <input type="text" class="form-control" style="width: 300px;" placeholder="Quick title search"></input>
            </div>
            <button type="submit" class="btn btn-default">Search</button>
          </form>
          <ul class="nav navbar-nav">
            <li><a href="#">Advanced search</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
          <!-- TODO: FIX SO THAT IT SAYS YOUR USERNAME AND TAKES YOU TO A PAGE IF YOU CLICK ON IT! -->
            <li id="fat-menu" class="dropdown">
              <a id="drop3" class="dropdown-toggle" data-toggle="dropdown" role="button" href="#">
                Login
                <b class="caret"></b>
              </a>
              <div class="dropdown-menu" style="padding: 15px; padding-bottom: 0px; width: 250px;" aria-labelledby="drop3" role="menu">
                <form>
                  <label for="login">Login</label>
                  <input type="text" id="username" class="form-control" placeholder="Enter username" style="margin-bottom: 5px;"></input>
                  <input type="password" id="password" class="form-control" placeholder="Enter password" style="margin-bottom: 10px;"></input>
                  <div class="checkbox">
                    <label>
                      <input id="remember-me" type="checkbox"> Remember me
                    </label>
                  </div>
                  <input type="submit" id="login" class="btn btn-primary" style="margin-bottom: 10px; width: 215px" value="Login"></input>
                  <button type="submit" id="forgot" class="btn btn-danger" style="margin-bottom: 10px; width: 215px">Forgot Password</button>
                  <button type="submit" id="create" class="btn btn-warning" style="margin-bottom: 10px; width: 215px">Create account</button>
                </form>
              </div>
            </li> 
          </ul>
        </nav>
      </div>
    </div>
    
    <div id="content" class="container">
      <div class="jumbotron">
        <h1>mekong.com.au</h1>
        <p>Welcome to mekong.com.au</p>
      </div>
      
      <div class="progress progress-striped active">
        <div class="progress-bar progress-bar-success"  role="progressbar" aria-valuenow="45" aria-valuemin="0" aria-valuemax="100" style="width: 78%">
            <span class="sr-only">45% Complete</span>
        </div>
      </div>
      
      <div class="alert alert-success fade in">
        <button class="close" aria-hidden="true" data-dismiss="alert" type="button">
          ×
        </button>
        <strong>Item successfully added to cart.</strong>
      </div>
    </div>
  </body>
</html>
"""
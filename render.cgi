#!/usr/bin/python -u

def login_details(login):
    print """
                <ul class="nav navbar-nav navbar-right">
                    <li id="fat-menu" class="dropdown">
                        <a id="drop3" class="dropdown-toggle" data-toggle="dropdown" role="button" href="#">
"""
    if not login:
        print "Login"
    else:
        print login["username"]

    print """
                            <b class="caret"></b>
                        </a>
"""

    if not login:
        print """
                        <div class="dropdown-menu" style="padding: 15px; padding-bottom: 0px; width: 250px;" aria-labelledby="drop3" role="menu">
                            <form>
                                <label for="login">Login</label>
                                <input type="text" id="username" class="form-control" placeholder="Enter username" style="margin-bottom: 5px;"></input>
                                <input type="password" id="password" class="form-control" placeholder="Enter password" style="margin-bottom: 10px;"></input>
                                <button type="submit" id="login" class="btn btn-primary" style="margin-bottom: 10px; width: 215px">Login</button>
                                <button type="submit" id="login" class="btn btn-danger" style="margin-bottom: 10px; width: 215px">Forgot Password</button>
                                <button type="submit" id="create" class="btn btn-warning" style="margin-bottom: 10px; width: 215px">Create account</button>
                            </form>
                        </div>
"""
    else:
        print """
                        <ul class="dropdown-menu" aria-labelledby="drop3" role="menu">
                            <li role="presentation">
                                <a href="#">Account</a>
                            </li>
                            <li role="presentation">
                                History
                            </li>
                            <li role="presentation">
                                Settings
                            </li>
                        </ul>
"""
    print """
                    </li> 
                </ul>
"""

def html_header(title, login):
    print "Content-Type: text-html"
    print
    print """
<!DOCTYPE html>
<html lang="en">
<!-- Code taken from Bootstrap website -->
<html>
  <head>
    <title>
"""
    print title
    print """
    </title>
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
"""
    login_details(login)
    print """
            </nav>
        </div>
    </div>
    
    <div id="content" class="container">
        <div class="jumbotron">
            <h1>mekong.com.au</h1>
            <p>Welcome to mekong.com.au</p>
        </div>
        
        
        
        
        
        
</div>
    
    <div class="bs-old-docs">
        <p><br></p>
    </div>
    
    <div class="container bs-docs-container">
        <div class="row">
            <div class="col-md-3">
                <div class="panel panel-info" style="min-height: 300px;">
                    <div class="panel-heading">
                        <h3 class="panel-title">
                            <strong>Quick trolley</strong><br>
                            <div class="row">
                                <div class="col-md-6">
                                    0 items
                                </div>
                                <div class="col-md-6" align="right">
                                    $0.00
                                </div>
                            </div> 
                        </h3>
                    </div>
                    <div class="panel-body">
                        Your trolley is empty...
                    </div>
                </div>
            </div>
            <div class="col-md-9" role="main">
                <div class="panel panel-info fixed-left" style="min-height: 300px;">
                    <div class="panel-heading">
                        <h3 class="panel-title">Search results</h3>
                    </div>
                    <div class="panel-body">
                        No results to display.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://code.jquery.com/jquery.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="js/bootstrap.min.js"></script>
  </body>
</html>

"""

html_header("Mekong", {"username": "cjdb"})
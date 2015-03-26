<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - SabreGrid</title>

	<link rel="icon" type="image/x-icon" href="/static/img/favicon.ico" />

    <!-- Bootstrap core CSS -->
    <link href="/static/css/bootstrap.css" rel="stylesheet">
            
    <!-- Custom styles for this template -->
    <link href="/static/css/main.css" rel="stylesheet">
    <link href="/static/css/normalize.css" rel="stylesheet">

    <!-- Font-Awesome icons link-->
    <link rel="stylesheet" href="/static/fonts/font-awesome/css/font-awesome.min.css">
      
    <!-- Hover.css include -->
    <link href="/static/css/hover-min.css" rel="stylesheet" media="all">
      
</head>

<body>
    <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a href="/" class="navbar-brand">SabreGrid</a>
            </div>
            <div class="navbar-collapse collapse">
                <ul class="nav navbar-nav">
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </div>

    <div class="container body-content">
        {{!base}}
        <hr />
        <footer class="text-center">
            <p>&copy; {{ year }} - SabreGrid</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>

</body>
</html>

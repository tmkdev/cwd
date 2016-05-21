<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.11/c3.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.6/css/materialize.min.css">
  <script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.6/js/materialize.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.11/c3.min.js"></script>
  <!--Let browser know website is optimized for mobile-->
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{{title or 'CWD - Cron Watch Dog'}}</title>
  % if refreshinterval > 0:
  <meta http-equiv="refresh" content="{{ refreshinterval }}">
  % end
</head>
<body>
  <nav>
    <div class="nav-wrapper red darken-1">
      <a href="{{get_url("/")}}" id="brand" class="brand-logo center">CronWatchDog</a>
      <a href="{{get_url("/")}}" data-activates="mobile-demo" class="button-collapse"><i class="material-icons">menu</i></a>
      <ul class="right hide-on-med-and-down">
        <li><a href="{{get_url("/jobs")}}">Jobs</a></li>
        <li><a href="{{get_url("/email")}}">Email</a></li>
        <li><a href="{{get_url("/about")}}">About</a></li>
      </ul>
      <ul class="side-nav" id="mobile-demo">
        <li><a href="{{get_url("/jobs")}}">Jobs</a></li>
        <li><a href="{{get_url("/email")}}">Email</a></li>
        <li><a href="{{get_url("/about")}}">About</a></li>
      </ul>
    </div>
  </nav>
  {{!base}}
  <script>
    $( document ).ready(function(){
         $(".button-collapse").sideNav();

         Materialize.updateTextFields();
    })
  </script>
</body>
</html>

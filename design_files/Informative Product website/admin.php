<?php
  $_SESSION['programName'] = "myEmail";     // Change our program name in a single location (used in display and email)

  $runatUQ = true;                          // Set false if not run on your UQ zone

  header('Access-Control-Allow-Origin: https://deco3801-sunshine.uqcloud.net/');

  header('Access-Control-Allow-Methods: GET, POST');

  header("Access-Control-Allow-Headers: X-Requested-With");

  if ($runatUQ) {
    require_once "uq/auth.php";             // Include UQ routines that handle UQ single-signon authentication
    auth_require();                         // User must authenticate once per session to continue running script
// Populate associative array containing UQ user details:
//  "user" — the user's UQ username (eg uqxxx or s4xxxxxx)
//  "email" — the user's primary email address
//  "name" — the preferred name for addressing the user, eg "John Smith"
//  "groups" — a list of AD and LDAP groups the user is a member of
    $UQ = auth_get_payload();
  } else {
   $UQ['user']   = "4511443";
   $UQ['email']  = "s4511443@student.uq.edu.au";
   $UQ['name']   = "Louis Christopher";
   $UQ['groups'] = "[No group, run from localhost]";
  }

//IMPORTANT: You must not write anything to the browser before the html header, i.e be careful not to include a single space outside the php tags!
?>
<?php
  $servername = "127.0.0.1";
  $username = "informative_admin";
  $password = "shareshed";
  $db = "informative_website";

  // create connection
  $con = new mysqli($servername, $username, $password, $db);
  if ($con->connect_error) {
    die("Connection failed: ".$con->connect_error);
  }
  $query = "SELECT * FROM contact_form ORDER BY signed_on DESC";
  $data = mysqli_query($con, $query);
  $query_graph = "SELECT DATE(signed_on) AS date,
                        COUNT(*) AS total
                  FROM contact_form
                  WHERE signed_on BETWEEN (NOW() - INTERVAL 5 Day) AND NOW()
                  GROUP BY DATE(signed_on)
                  ORDER BY DATE(signed_on)";

  $query_cumulative = "SELECT DATE(signed_on) AS date,
                        COUNT(*) AS total
                  FROM contact_form
                  GROUP BY DATE(signed_on)
                  ORDER BY DATE(signed_on)";
  $graph_data = mysqli_query($con, $query_graph);
  $graph_cumulative = mysqli_query($con, $query_cumulative);
 ?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/css?family=Roboto+Condensed" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
    <link href='https://fonts.googleapis.com/css?family=Kaushan+Script' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700' rel='stylesheet' type='text/css'>

    <link rel="stylesheet" href="landingpage.css">
    <title>Share Shed | by Team Sunshine</title>

    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
      google.charts.setOnLoadCallback(drawChart2);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Date', 'Total User'],
         <?php
         $cumulative = 0;
         while($row = mysqli_fetch_array($graph_cumulative)){
           $cumulative += $row['total'];
           echo "['".$row['date']."',".$cumulative."],";
         }
         ?>
        ]);

        var options = {
          title: 'Cumulative User Chart',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('cumulative_chart'));

        chart.draw(data, options);
      }

      function drawChart2() {
        var data2 = google.visualization.arrayToDataTable([
          ['Date', 'User'],
         <?php
         while($row = mysqli_fetch_array($graph_data)){
         echo "['".$row['date']."',".$row['total']."],";
         }
         ?>
        ]);

        var options2 = {
          title: 'Daily User Chart',
          legend: { position: 'bottom' }
        };

        var chart2 = new google.visualization.LineChart(document.getElementById('day_chart'));

        chart2.draw(data2, options2);
      }
    </script>

  </head>
  <body id="page-top">
    <nav class="navbar navbar-expand-lg fixed-top" id="mainNav">
      <div class="container">
        <a class="navbar-brand js-scroll-trigger" href="index.html">Team Sunshine</a>
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav text-uppercase ml-auto">
            <li class="nav-item">
              <a class="nav-link js-scroll-trigger" href="#graphs">Graphs</a>
            </li>
            <li class="nav-item">
              <a class="nav-link js-scroll-trigger" href="#info">Customer Info</a>
            </li>
            <li class="nav-item">
              <a class="nav-link js-scroll-trigger" href="index.html">Back to Home</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>


    <header class="masthead bg-dark" id="masthead">
      <div class="container">
        <div class="intro-text2">
          <div class="intro-lead-in mt-2 text-left"><b>Welcome,</b> <?php echo $UQ['name'];?></div>
          <div class="topheading pb-2 text-left"><h4>View the summary statistics of <b>Share Shed</b> below.</h4></div>
        </div>
      </div>
    </header>

    <section id="graphs" class="section">
      <div class="container">
      <br><br>
        <?php
          if (mysqli_num_rows($graph_data)==0) {
            echo "No Data yet";
          } else {
            echo "<div class='row'>
                    <div class='col-md-6'>
                      <div id='cumulative_chart'></div>
                    </div>
                    <div class='col-md-6'>
                      <div id='day_chart'></div>
                    </div>
                  </div>";
          }
         ?>

      </div>
    </section>


    <section id="info" class="section">
      <div class="container">
        <h3 class="caption mb-3">Customers' Information </h3>
        <div class="table-responsive">
          <table class="table table-hover">
            <caption>Showing 1 to 4 of 4 entries</caption>
            <thead>
              <tr>
                <th style="width: 5%">#</th>
                <th style="width: 15%">Date & Time</th>
                <th style="width: 18%">Name</th>
                <th style="width: 18%">Email Address</th>
                <th style="width: 44%">Message</th>
              </tr>
            </thead>
            <tbody>
              <?php
                while($row = mysqli_fetch_array($data)){
                  echo "<tr>";
                  echo "<th scope='row'>". $row['id'] . "</td>";
                  echo "<td>". $row['signed_on'] . "</td>";
                  echo "<td>". $row['name'] . "</td>";
                  echo "<td>". $row['email'] . "</td>";
                  echo "<td>". $row['message'] . "</td>";
                  echo "</tr>";
                }
              ?>
            </tbody>
          </table>

          </div>
      </div>
    </section>

    <footer class="footer-bs">
      <div class="container white">
        <div class="row">
          <div class="col-md-4 col-sm-12 mb-3 footersection">
            <span class="copyright">&copy; Share Shed Inc</span><br>
            <span class="copyright mb-0">Icons made by <a class="white" href="http://www.freepik.com" title="Freepik">Freepik</a> from <a class="white"style="color=:white"href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a class="white"href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></span>
            <br><br>
          </div>
          <div class="col-md-4 footer-social col-sm-6 mb-3 footersection">
            <h4>Follow Us —</h4>
            <ul class="list-inline social-buttons">
              <li class="list-inline-item">
                <a href="https://twitter.com/teamsunshine4">
                  <i class="fab fa-twitter"></i>
                </a>
              </li>
              <li class="list-inline-item">
                <a href="https://www.facebook.com/Team-Sunshine-927693290753400/" target="_blank">
                  <i class="fab fa-facebook-f"></i>
                </a>
              </li>
              <li class="list-inline-item">
                <a href="https://www.instagram.com/teamsunshine.3801/" target="_blank">
                  <i class="fab fa-instagram"></i>
                </a>
              </li>
            </ul>
            <br>
          </div>
          <div class="col-md-4 col-sm-6 footer-nav footersection">
              <h4>Menu —</h4>
              <p><a href="#about"><a href="#graphs">Graphs</a> - <a href="#info">Customer Info</a> - <a href="index.html">Back to Home</a></p>
              <p><a href="#page-top"> Back to top &nbsp;<i class="fas fa-arrow-up"></i></p>
          </div>

        </div>
      </div>
    </footer>



    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <!-- Bootstrap core JavaScript -->
    <script src="additional/vendor/jquery/jquery.min.js"></script>
    <script src="additional/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Plugin JavaScript -->
    <script src="additional/vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Contact form JavaScript -->
    <script src="additional/js/jqBootstrapValidation.js"></script>
    <script src="additional/js/contact_me.js"></script>

    <!-- Custom scripts for this template -->
    <script src="additional/js/agency.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

  </body>
</html>

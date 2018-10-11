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
  $query = "SELECT * FROM contact_form";
  $data = mysqli_query($con, $query);
  $query_graph = "SELECT DATE(signed_on) AS date,
                        COUNT(*) AS total
                  FROM contact_form
                  GROUP BY DATE(signed_on)
                  ORDER BY DATE(signed_on)";
  $graph_data = mysqli_query($con, $query_graph);
 ?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="author" content="Louis Christopher" />
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=0;" />
    <meta name="apple-mobile-web-app-capable" content="yes" />

    <title><?php echo $_SESSION["programName"];?></title>

<?php
// CDN hosted (local fallback for css and js)
// The // at the beginning of each URL cause the files to be fetched over the same protocol as the current page (http: or https:)
?>
    <link rel="stylesheet" href="css/themes/myApp.min.css" />
    <link rel="stylesheet" href="css/themes/jquery.mobile.icons.min.css" />
    <link rel="stylesheet" href="//code.jquery.com/mobile/1.4.5/jquery.mobile.structure-1.4.5.min.css" />

    <script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
    <script src="//code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
    <script type="text/javascript">
      if (typeof jQuery == 'undefined') {
        document.write(unescape("%3Clink rel='stylesheet' href='css/jquery.mobile.structure-1.4.5.min.css' /%3E"));
        document.write(unescape("%3Cscript src='js/jquery-1.11.1.min.js' type='text/javascript'%3E%3C/script%3E"));
        document.write(unescape("%3Cscript src='js/jquery.mobile-1.4.5.min.js' type='text/javascript'%3E%3C/script%3E"));
      }
    </script>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Date', 'User'],
         <?php
         while($row = mysqli_fetch_array($graph_data)){
         echo "['".$row['date']."',".$row['total']."],";
         }
         ?>
        ]);

        var options = {
          title: 'User Join Chart',
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      }
    </script>

  </head>
  <body>
    <div data-role="page" data-theme="c">

      <div data-role="header" data-position="fixed" data-theme="c">
        <h1><?php echo $_SESSION["programName"];?></h1>
      </div>

      <div>
        <h1>Your Name: <?php echo $UQ['name'];?></h1>
      </div>

      <div data-role="content" data-theme="c">
        <div id="curve_chart" style="width: 900px; height: 500px"></div>
        <div>
          <h1>Table</h1>
          <table>
            <tr>
              <td>Name</td>
              <td>E-mail</td>
              <td>Message</td>
              <td>Joined at</td>
            </tr>
            <?php
              while($row = mysqli_fetch_array($data)){
                echo "<tr>";
                echo "<td>". $row['name'] . "</td>";
                echo "<td>". $row['email'] . "</td>";
                echo "<td>". $row['message'] . "</td>";
                echo "<td>". date('d-m-Y', strtotime($row['signed_on'])) . "</td>";
                echo "</tr>";
              }
            ?>
          </table>
          <?php
            while($row_graph = mysqli_fetch_array($graph_data)){
              echo "<p>" . $row['date'] . "</p>";
              echo "<p>" . $row['total'] . "</p>";
            }
           ?>
        </div>
      </div>

      <div data-role="footer" data-position="fixed" data-theme="c">
        <h1>Sending emails</h1>
      </div>

    </div>
  </body>
</html>

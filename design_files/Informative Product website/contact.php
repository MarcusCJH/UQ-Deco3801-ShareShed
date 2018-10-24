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

  if(!empty($_POST["send"])) {
    $name = $_POST["name"];
    $email = $_POST["email"];
    $message = $_POST["message"];
  }
  $query = "INSERT INTO contact_form (name, email, message) VALUES ('". $name."','". $email. "','". $message. "')";
  if (mysqli_query($con, $query)){
    header("Location: https://deco3801-sunshine.uqcloud.net/");
    die();
  } else {
    $msg = "ERROR: Could not able to execute $sql. " . mysqli_error($link);
}
 ?>

 <!DOCTYPE html>
 <html>
 <head>

 </head>
<body>
  <?php echo $msg ?>
</body>
</html>

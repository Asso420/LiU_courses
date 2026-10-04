<!DOCTYPE html>
<html>
<body>
   <h1>Barebone Bank</h1>

   <?php
   require 'check_response.php';
   $db_json = file_get_contents('db.json');
   $db = json_decode($db_json, true);
   
   if (!isset($_GET['uid']) || !array_key_exists($_GET['uid'], $db)): ?>
      <?php if (isset($_GET['uid'])): ?>
         <p>Unknown user ID!</p>
      <?php else: ?>
         <h3><i>Welcome to Barebone Bank, the authentic Web 1.0 banking experience!</i></h3>
      <?php endif ?>
      
      <p>Enter your unique user ID below to check your balance.</p>
      <form action="index.php">
         <label for="uid">User ID:</label><br/>
         <input type="text" id="uid" name="uid">
         <input type="submit" value="Log in">
      </form>
   
   <?php else: 
      $uid = $_GET['uid'];
      $user = $db[$uid];

      if (isset($_GET['response'])):
         $challenge = $_GET['challenge'];
         $response = $_GET['response'];
         $shared_secret = $user['shared_secret'];
         if (check_response($challenge, $response, $shared_secret)): ?>
            <p>Welcome <?=$user['name']?>!</p>
            <p>Your balance is <b>$<?=number_format($user['balance'])?></b></p>
         <?php else: ?>
            <p>Invalid response!</p>
         <?php endif ?>
         <p>Return to <a href="index.php">login</a>.</p>
      <?php else:
         $challenge = sprintf("%08d", rand(0, 99999999)); ?>

         <p>User ID: <?=$uid?> </p>
         <p>Enter the following into your bank token: <b><?=$challenge?></b></p>
         <form action="index.php">
            <input type="hidden" id="uid" name="uid" value="<?=$uid?>">
            <input type="hidden" id="challenge" name="challenge" value="<?=$challenge?>">
            <label for="response">Response:</label><br/>
            <input type="text" id="response" name="response">
            <input type="submit" value="Submit">
         </form>
         
      <?php endif ?>
   <?php endif ?>

</body>
</html>
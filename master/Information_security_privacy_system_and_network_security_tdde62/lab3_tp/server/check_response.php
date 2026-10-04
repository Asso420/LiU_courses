<?php

function check_response($challenge, $response, $shared_secret) {
   // Convert hex-encoded shared secret to raw binary
   $binary_secret = hex2bin($shared_secret);
   if (!$binary_secret) {
      throw new UnexpectedValueException("shared_secret is not a valid hex string");
   }

   //Compute response
   $hex_response = hash_hmac('sha256', $challenge, $binary_secret);

   // Format response as 8-digit decimal number
   $first_4 = substr($hex_response, 0, 8); // First 4 bytes of hex-encoded response
   $computed_response = substr(sprintf('%08d', hexdec($first_4)), -8);

   return $response == $computed_response;
 }

?>

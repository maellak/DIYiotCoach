#!/usr/bin/php-cli                                                             
<?php

    include "PhpSerial.php";

function setupSerial($device) {
   $serial = new phpSerial();

    $serial->deviceSet($device);

    $serial->confBaudRate(9600); //Baud rate: 9600
    $serial->confParity("none");  //Parity (this is the "N" in "8-N-1")
    $serial->confCharacterLength(8); //Character length     (this is the "8" in "8-N-1")
    $serial->confStopBits(1);  //Stop bits (this is the "1" in "8-N-1")
    $serial->confFlowControl("none");

    $serial->deviceOpen();
    return $serial;
}

$lhserial = setupSerial('/dev/ttyLH');
$rhserial = setupSerial('/dev/ttyRH');

while(true) {
    while(($lh = trim($lhserial->readPort())) == "") { /* Do nothing - Loop until != '' */  }
    while(($rh = trim($rhserial->readPort())) == "") { /* Do nothing - Loop until != '' */  }
    if(trim(substr($rh, 1, -1)) == '' || trim(substr($lh, 1, -1)) == '' || strlen($rh) > 70 || strlen($lh) > 70) { /*echo 'Invalid Data\n'; var_dump($rh); var_dump($lh);*/ continue; }
    echo '@'.substr($rh, 1, -1).':'.substr($lh, 1, -1)."#\n";
}

    $serial->deviceClose();
?>

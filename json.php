<?php

$action_default = "incident_count";
$actions = array($action_default);

$action = isset($_GET['a']) ? $_GET['a'] : $action_default;
if (!in_array($action, $actions)) { die("Bad action: $action"); }

error_reporting(-1); // report all errors

$ushahidi_config_db = "/var/www/vhosts/mainfo.cartong.org/httpdocs/application/config/database.php";

define('SYSPATH', "dummy");
unset($config);
require($ushahidi_config_db);

$user = $config['default']['connection']['user'];
$pass = $config['default']['connection']['pass'];
$host = $config['default']['connection']['host'];
$database = $config['default']['connection']['database'];

$mysqli = new mysqli($host, $user, $pass, $database);
if ($mysqli->connect_errno) {
    die("Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error);
}

$result = $mysqli->query("SELECT t1.incident_dateadd, t2.latitude , t2.longitude FROM incident AS t1 INNER JOIN location AS t2 ON t1.location_id = t2.id WHERE t1.incident_active = 1");
printf('{ "type": "FeatureCollection","features":[');

$array = array();
while ($row = $result->fetch_assoc()) {
  $onefeature = '{"type": "Feature", "properties":{"incident_dateadd":"'.$row["incident_dateadd"].'"}, "geometry": { "type": "Point", "coordinates": ['.round($row["longitude"],2).','.round($row["latitude"],2).']}},';
  $array[]= $onefeature;
}
$allfeat = "";
foreach ($array as $arr) {
$allfeat .= $arr;
    //echo $arr;

};
$trimed =rtrim($allfeat,",");
print($trimed);
echo "]}";

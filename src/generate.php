<?php
if (isset($_SERVER['HTTP_ORIGIN'])) {
    header("Access-Control-Allow-Origin: {$_SERVER['HTTP_ORIGIN']}");
    header('Access-Control-Allow-Credentials: true');
    header('Access-Control-Max-Age: 86400');    // cache for 1 day
}

// Access-Control headers are received during OPTIONS requests
if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {

    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_METHOD']))
        header("Access-Control-Allow-Methods: GET, POST, OPTIONS");         

    if (isset($_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']))
        header("Access-Control-Allow-Headers:        {$_SERVER['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']}");
}

function choices($setting, $settings_info)
{
    return array_map(function($choice) use($setting, $settings_info) {
        return [
            "name" => $choice,
            "weight" => $settings_info[$setting["name"]][$choice],
        ];
    }, $setting["choices"]);
}

$body = json_decode(file_get_contents('php://input'), true)["settings"];
$settings = json_decode(file_get_contents('../data/weight.json'), true);

$exchange = [];
foreach($body as $setting) 
{
    $element = [
        "name" => $setting["name"],
        "choices" => choices($setting, $settings)
    ];
    array_push($exchange, $element);
}

$filename = uniqid() . ".json";
$file = fopen("../exchange/" . $filename, "w");

fwrite($file, json_encode($exchange));

$output = [];
exec('cd ..; python3 script/generator.py exchange/'. $filename .' 4 2>&1', $output);

$result = json_decode(implode("\n",$output), true);
// var_dump(implode("<br>",$output));
$out = [];
foreach($result as $setting)
{
    $out[$setting["name"]] = $setting["choice"]["name"];
}

echo json_encode(["settings" => $out]);

fclose($file);

if(file_exists("../exchange/". $filename))
	unlink("../exchange/" . $filename);
<?php
$confs = [
    ['u' => 'root', 'p' => ''],
    ['u' => 'root', 'p' => 'root'],
    ['u' => 'root', 'p' => 'password'],
    ['u' => 'admin', 'p' => 'admin'],
];

foreach ($confs as $c) {
    try {
        $db = new PDO("mysql:host=localhost", $c['u'], $c['p']);
        echo "SUCCESS: " . $c['u'] . ":" . $c['p'] . "\n";
        exit;
    } catch (Exception $e) {
        echo "FAIL: " . $c['u'] . ":" . $c['p'] . " - " . $e->getMessage() . "\n";
    }
}

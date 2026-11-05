<?php
try {
    $db = new PDO("mysql:host=127.0.0.1", "root", "");
    echo "SUCCESS: 127.0.0.1:root:''\n";
} catch (Exception $e) {
    echo "FAIL: 127.0.0.1:root:'' - " . $e->getMessage() . "\n";
}

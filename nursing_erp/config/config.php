<?php
/**
 * Professional Nursing ERP - Configuration
 */

// Database Configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'nursing_erp_new'); // New DB name to avoid conflict

// Application Constants
define('APP_NAME', 'Holy Faith Nursing ERP');
define('APP_URL', 'http://localhost/clg_project/driver%20drowsiness/driver_drowsiness_system/nursing_erp');
define('CURRENCY', '₹');

// Timezone
date_default_timezone_set('Asia/Kolkata');

// Error Reporting (Development)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Database Connection
function getDB() {
    static $db;
    if ($db === null) {
        try {
            $db = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4", DB_USER, DB_PASS);
            $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            die("Database Connection Failed: " . $e->getMessage());
        }
    }
    return $db;
}

// Session Start
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

/**
 * Authentication Guard
 */
function authGuard() {
    if (!isset($_SESSION['user_id'])) {
        header("Location: " . APP_URL . "/modules/auth/login.php");
        exit;
    }
}

/**
 * Input Sanitization
 */
function sanitize($data) {
    return htmlspecialchars(strip_tags(trim($data)));
}

/**
 * Activity Logger
 */
function logActivity($action) {
    $db = getDB();
    $stmt = $db->prepare("INSERT INTO activity_logs (user_id, action, ip_address) VALUES (?, ?, ?)");
    $stmt->execute([
        $_SESSION['user_id'] ?? null,
        $action,
        $_SERVER['REMOTE_ADDR']
    ]);
}

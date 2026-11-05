<?php
require_once __DIR__ . '/../config/config.php';
$db = getDB();

// 0. Execute Setup SQL
$sql = file_get_contents(__DIR__ . '/../database/setup.sql');
$db->exec($sql);

// 1. Clear Existing Data
$db->exec("SET FOREIGN_KEY_CHECKS = 0");
$db->exec("TRUNCATE students");
$db->exec("TRUNCATE fee_payments");
$db->exec("TRUNCATE expenses");
$db->exec("SET FOREIGN_KEY_CHECKS = 1");

$first_names = ['Kiran', 'Anjali', 'Rahul', 'Sneha', 'Vikram', 'Priya', 'Amit', 'Sunita', 'Rajesh', 'Kavita', 'Suresh', 'Meena', 'Rohan', 'Swati', 'Vijay', 'Divya', 'Sandeep', 'Pooja', 'Manoj', 'Jyoti'];
$last_names = ['Kumar', 'Reddy', 'Sharma', 'Patil', 'Singh', 'Verma', 'Gupta', 'Yadav', 'Nair', 'Joshi', 'Chaudhary', 'Deshmukh', 'Malhotra', 'Iyer', 'Menon'];
$courses = $db->query("SELECT id FROM courses")->fetchAll(PDO::FETCH_COLUMN);
$categories = ['SC', 'ST', 'OBC', 'GEN'];
$cities = ['Hyderabad', 'Vijayawada', 'Vizag', 'Warangal', 'Guntur', 'Nellore', 'Kurnool'];
$agents = ['Global Edu', 'Nursing Career Hub', 'Direct', 'Institutional Referral', 'City Consultants'];

echo "Starting data population...\n";

for ($i = 1; $i <= 120; $i++) {
    $fname = $first_names[array_rand($first_names)];
    $lname = $last_names[array_rand($last_names)];
    $adm_no = "HF/2024/" . str_pad($i, 3, '0', STR_PAD_LEFT);
    $roll_no = "24" . ($i < 100 ? ($i < 10 ? 'BN0'.$i : 'BN'.$i) : 'BN'.$i);
    $course_id = $courses[array_rand($courses)];
    $gender = rand(0, 1) ? 'Male' : 'Female';
    $cat = $categories[array_rand($categories)];
    $city = $cities[array_rand($cities)];
    $agent = $agents[array_rand($agents)];
    $hostel = rand(0, 1);
    $bus = rand(0, 1);
    
    $stmt = $db->prepare("INSERT INTO students (admission_no, roll_no, first_name, last_name, father_name, gender, category, city, phone, course_id, admission_date, admission_agent, hostel_required, bus_required, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')");
    $stmt->execute([
        $adm_no,
        $roll_no,
        $fname,
        $lname,
        $lname . " Senior",
        $gender,
        $cat,
        $city,
        "9" . rand(100000000, 999999999),
        $course_id,
        date('Y-m-d', strtotime("-" . rand(1, 60) . " days")),
        $agent,
        $hostel,
        $bus
    ]);
    
    $student_id = $db->lastInsertId();
    $num_payments = rand(1, 3);
    for ($j = 1; $j <= $num_payments; $j++) {
        $db->prepare("INSERT INTO fee_payments (student_id, receipt_no, amount_paid, payment_date, payment_method, category_id) VALUES (?, ?, ?, ?, ?, ?)")
           ->execute([
               $student_id,
               "RCPT-" . bin2hex(random_bytes(4)),
               rand(5000, 25000),
               date('Y-m-d', strtotime("-" . rand(0, 30) . " days")),
               ['Cash', 'Online', 'Bank Transfer'][rand(0, 2)],
               rand(1, 3)
           ]);
    }
}

for ($k = 1; $k <= 20; $k++) {
    $db->prepare("INSERT INTO expenses (title, amount, expense_date, category) VALUES (?, ?, ?, ?)")
       ->execute([
           "Operational Expense " . $k,
           rand(1000, 15000),
           date('Y-m-d', strtotime("-" . rand(0, 30) . " days")),
           ['Maintenance', 'Salary', 'Utility', 'Inventory'][rand(0, 3)]
       ]);
}

echo "Successfully populated 120 students and related financial records.\n";

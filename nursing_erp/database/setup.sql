-- Professional Nursing ERP Database Schema
CREATE DATABASE IF NOT EXISTS nursing_erp_new;
USE nursing_erp_new;

-- 1. Users & Auth
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'staff', 'accountant', 'registrar') DEFAULT 'staff',
    status ENUM('active', 'inactive') DEFAULT 'active',
    last_login DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Branches & Academic Years
CREATE TABLE IF NOT EXISTS academic_years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year_name VARCHAR(20) NOT NULL,
    is_active TINYINT(1) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    duration_years INT NOT NULL
);

-- 3. Students
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admission_no VARCHAR(50) UNIQUE NOT NULL,
    roll_no VARCHAR(50),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    father_name VARCHAR(100),
    mother_name VARCHAR(100),
    dob DATE,
    gender ENUM('Male', 'Female', 'Other'),
    caste VARCHAR(50),
    category ENUM('SC', 'ST', 'OBC', 'GEN', 'Others'),
    address TEXT,
    city VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    course_id INT,
    admission_date DATE,
    admission_agent VARCHAR(100),
    hostel_required TINYINT(1) DEFAULT 0,
    bus_required TINYINT(1) DEFAULT 0,
    photo VARCHAR(255),
    status ENUM('active', 'inactive', 'outgoing', 'trash') DEFAULT 'active',
    is_deleted TINYINT(1) DEFAULT 0,
    deleted_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- 4. Finance
CREATE TABLE IF NOT EXISTS fee_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS fee_structures (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    academic_year_id INT,
    fee_category_id INT,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id),
    FOREIGN KEY (fee_category_id) REFERENCES fee_categories(id)
);

CREATE TABLE IF NOT EXISTS fee_payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    receipt_no VARCHAR(50) UNIQUE NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('Cash', 'Online', 'Cheque', 'Bank Transfer'),
    category_id INT,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (category_id) REFERENCES fee_categories(id)
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    expense_date DATE NOT NULL,
    category VARCHAR(100),
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Staff
CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    designation VARCHAR(100),
    department VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    salary DECIMAL(10,2),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Transport
CREATE TABLE IF NOT EXISTS transport_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name VARCHAR(100) NOT NULL,
    vehicle_no VARCHAR(50),
    driver_name VARCHAR(100),
    fee DECIMAL(10,2)
);

-- 7. Activity Logs
CREATE TABLE IF NOT EXISTS activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action TEXT NOT NULL,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Seed Initial Data
INSERT INTO users (username, password, full_name, role) VALUES ('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'System Admin', 'admin');
INSERT INTO academic_years (year_name, is_active) VALUES ('2024-25', 1);
INSERT INTO courses (course_name, duration_years) VALUES ('B.Sc Nursing', 4), ('GNM', 3), ('M.Sc Nursing', 2), ('P.B.B.Sc Nursing', 2);
INSERT INTO fee_categories (category_name) VALUES ('Tuition Fee'), ('Hostel Fee'), ('Transport Fee'), ('Library Fee'), ('Admission Fee');

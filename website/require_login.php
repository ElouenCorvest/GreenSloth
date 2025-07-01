<?php
session_start();

// Define valid credentials
$valid_user = 'admin';
$valid_pass = 'greensloth123';

// Handle login
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($_POST['username'] === $valid_user && $_POST['password'] === $valid_pass) {
        $_SESSION['logged_in'] = true;
    } else {
        $error = "Invalid username or password.";
    }
}
?>
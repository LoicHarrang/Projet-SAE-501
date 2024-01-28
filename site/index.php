<?php
require_once 'includes/header.php';
require_once 'Models/UserModel.php';
require_once 'Controllers/LoginController.php';

$controller = new LoginController();
$controller->login();

require_once 'includes/footer.php';
?>

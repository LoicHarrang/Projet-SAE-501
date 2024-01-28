<?php
class HomeController {
    public function index() {
        $productModel = new ProductModel();
        $produits = $productModel->listeMateriel();

        // Passer les produits à la vue
        require 'Views/home.php';
    }
}

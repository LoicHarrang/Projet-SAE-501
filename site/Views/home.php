<!-- Views/home.php -->
<?php include 'Components/tableau.php'; ?>
<section id="infos" class="infos">
    <div class="container my-4 content">
        <div class="section-title">
            <h1>Menu principal</h1>
        </div>

        <div class="row mx-1 text-center">
        <?php if ($produits): ?>
            <!-- Affichage des produits -->
            <?php afficheTableau($produits); ?>
        <?php else: ?>
            <p>Aucun matériel trouvé.</p>
        <?php endif; ?>
        </div>
    </div>
</section>

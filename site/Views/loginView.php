<!-- Views/loginView.php -->
<div class="wrapper">
    <div id="formContent" data-aos="zoom-in-down">
        <div class="first">
            <img src="img/mamazon.png" id="icon" alt="Mamazon" />
            <h1>Connexion</h1>
        </div>

        <form method="POST" action="">
            <input type="text" id="login" class="second" name="login" required placeholder="username" value="<?php echo htmlspecialchars($login ?? '', ENT_QUOTES); ?>">
            <input type="password" id="password" class="third" required name="password" placeholder="password">
            <input type="submit" class="fourth" value="Connexion" name="connexion">
        </form>

        <?php if (isset($message)): ?>
            <p id="<?php echo $message['id']; ?>">
                <?php echo $message['text']; ?>
            </p>
        <?php endif; ?>
    </div>
</div>

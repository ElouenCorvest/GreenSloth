<?php if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true): ?>
<div class="lockscreen">
    <img src="/src/img/shh_sloth.svg"/>
    <h1>Shhh....</h1>
    <h3>GreenSloth isn't finished yet</h3>
    <?php if (!empty($error)): ?>
        <div class="error"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required />
        <input type="password" name="password" placeholder="Password" required />
        <input type="submit" value="Unlock" class="clickable"/>
    </form>
</div>
<?php endif; ?>
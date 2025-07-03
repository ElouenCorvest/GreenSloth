<?php require __DIR__.'/../../require_login.php'; ?>

<!doctype html>
<html class="no-js" lang="en">

<head>
  <?php include "head_pages.php" ?>
</head>

<body>
  <?php require __DIR__.'/../../login_modal.php'; ?>

  <div id="layoutWrapper">
    <nav id="topnav"></nav>

    <div id="wrapper">
      <div id="content">
        
        <div id="citeModal" class="modal hidden"></div>

        <h1>To Dos of GreenSloth</h1>

        <p>In this section, we will list all the todos still to be done for GreenSloth to keep Elouen from slacking off! They will be seperated in sections for clarity.</p>

        <div class="progress-bar">
          <progress id="all-progress" max="100" value="10"></progress>
          <label for="all-progress" id="all-progress-label">hello</label>
        </div>

        <div class="todo-section">
          <h2>Admin</h2>
          <div class="todo">
            Come up with a title for Master Thesis
          </div>
          <div class="todo">
            Write Abstract for registration
          </div>
          <div class="todo">
            Register Master Thesis
          </div>
        </div>

        <div class="todo-section">
          <h2>Website Admin</h2>
          <div class="todo">
            Create "Impressum"
          </div>
          <div class="todo">
            Create Test Case
          </div>
        </div>

        <div class="todo-section">
          <h2>Models</h2>
          <div class="todo">
            Finish summary of Li2021
          </div>
          <div class="todo">
            Finish figure recreation of Li2021
          </div>
          <div class="todo">
            Finish summary of Saadat2021
          </div>
          <div class="todo">
            Finish figure recreation of Saadat2021
          </div>
          <div class="todo">
            Rewrite models in mxlbricks
          </div>
          <div class="todo">
            Develop Template for Schemes
          </div>
        </div>
  
      </div>
    </div>
  </div>

  <script type="module" src="../js/topnav.js"></script>
  <script type="module" src="../js/cite.js"></script>
  <script type="module" src="../js/todo.js"></script>
  <script src="//code.iconify.design/1/1.0.6/iconify.min.js"></script>

</body>

</html>

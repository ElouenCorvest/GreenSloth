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
  
        <div id="model-selector">
          <div id="bars">
            <input type="text" class="typeInBar clickable" onkeyup="modelSearch()" placeholder="Search for names.." title="Type in a name" id="searchBar"/>
            
            <button type="button" onclick="toggleTags()" class="tagsButton clickable" id="tagsButton">Tags</button>
          </div>
  
          <div class="tagsBox hidden" id="tagsBox"></div>
  
  
        <script>
          function modelSearch() {
            input = document.getElementById("searchBar");
            filter = input.value.toUpperCase();
            list = document.getElementById("model-selector");
            rows = list.getElementsByClassName("model-row")
  
            for (i = 0; i < rows.length; i++) {
              title = rows[i].getElementsByTagName("h1")[0];
              txtValue = title.textContent || title.innerText;
              if (txtValue.toUpperCase().indexOf(filter) > -1) {
                rows[i].style.display = "";
              } else {
                rows[i].style.display = "none"
              }
            }
          }
          </script>
      </div>
    </div>
  </div>

  <script type="module" src="../js/model_select.js"></script>
  <script type="module" src="../js/topnav.js"></script>
  <script type="module" src="../js/cite.js"></script>
  <script src="//code.iconify.design/1/1.0.6/iconify.min.js"></script>

</body>

</html>

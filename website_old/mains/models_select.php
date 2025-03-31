<!doctype html>
<html class="no-js" lang="en">

<head>
  <?php include('head.html'); ?>
</head>

<body>

  <!-- Topnav -->
  <div class="topnav-wrapper">
    <header class="topnav">
      <div class="topnav-left">
        <img src="../img/icon.svg"/>
        <div class="onlyText">PhotoModelBase</div>
      </div>

      <div class="topnav-center">
        <a class="tablinks" href="index.php">Home</a>
        <a class="tablinks active" href="models_select.php">Models</a>
      </div>

      <div class="topnav-right">

      </div>

    </header>
  </div>

  <div id="wrapper">
    <div id="content">
      

      <div id="model-selector">
        <div id="bars">
          <input type="text" class="typeInBar clickable" onkeyup="modelSearch()" placeholder="Search for names.." title="Type in a name"/>
          
          <button type="button" onclick="toggleTags()" class="tagsButton clickable">Tags</button>
        </div>

        <div class="tagsBox">
          <div class="tagsCategory">
            <h3 class="tagsHeading">Apparatus</h3>
            <div class="tagsRow">
              <button type="button" class="tag clickable">PSII</button>
              <button type="button" class="tag clickable">Cytochrome b<sub>6</sub>f</button>
              <button type="button" class="tag clickable">PSI</button>
              <button type="button" class="tag clickable">ATP Synthase</button>
            </div>
          </div>
        </div>

        <?php
          // Directory containing your model HTML files
          $models_dir = "../model_pages";

          // Open the directory
          if (is_dir($models_dir)) {
              if ($dh = opendir($models_dir)) {
                  echo '<div class="model-selector">';
                  
                  // Loop through the directory contents
                  while (($file = readdir($dh)) !== false) {
                      // Only process .php files
                      if (pathinfo($file, PATHINFO_EXTENSION) === 'php') {
                          // Get the model name (file name without extension)
                          $model_name = pathinfo($file, PATHINFO_FILENAME);

                          // Get the model file path
                          $file_path = $models_dir . '/' . $file;

                          // Simulate Contents of model Page
                          $contents_modelpage = file_get_contents($file_path);

                          // Find matching text inside simulate dmodle page
                          if (preg_match("/id='modelTitle'>(.*)<\/h1>/i", $contents_modelpage, $matches)) {
                            $model_title = $matches[1];
                          }
                          
                          // Generate the badge HTML
                          echo '
                          <div class="model-row">
                            <img src="../icon.png" class="model-img"/>
                            <h1 class="model-title">' . htmlspecialchars($model_title) . '</h1>
                            <div class="model-attributes">Test 1</div>
                            <a class="model-link" href="' . $models_dir . '/' . $file . '"></a>
                          </div>';
                      }
                  }
                  
                  echo '</div>';
                  
                  // Close the directory handle
                  closedir($dh);
              }
          }
        ?>
      </div>

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

  <script type="text/javascript" src="../js/model_select.js"></script>

</body>

</html>

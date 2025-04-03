<!doctype html>
<html class="no-js" lang="en">

<head>
  <?php include('head.html'); ?>
</head>

<script>
  const models = ['Matuszynska2016', 'Li2021', 'Saadat2021'];
</script>

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

        <div class="tagsBox" style="display: none;">
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

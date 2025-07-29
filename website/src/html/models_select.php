<!doctype html>
<html class="no-js" lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <link rel="stylesheet" href="../css/style.css">
  <meta name="description" content="">

  <meta property="og:title" content="">
  <meta property="og:type" content="">
  <meta property="og:url" content="">
  <meta property="og:image" content="">
  <meta property="og:image:alt" content="">

  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="manifest" href="/site.webmanifest">

  <title>GreenSloth</title>
  <meta name="theme-color" content="#fafafa">
</head>

<body>
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
          <p class="discreetText">As GreenSloth is not finished yet, we can only show you some models as a proof of concept. However, there are others already planned: <a href="https://doi.org/10.1007/BF00392212">Yokota1985</a>, <a href="https://doi.org/10.1093/jexbot/51.suppl_1.319">Poolman2000</a>, <a href="https://doi.org/10.1111/ppl.12962">Matuszynska2019</a>, <a href="https://doi.org/10.1038/s41477-021-00947-5">Li2021</a>, many more! </p>
  
  
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

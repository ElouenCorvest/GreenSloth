<!doctype html>
<html lang="en">

<head>
  <?php include('../mains/head.html'); ?>
</head>

<script>
  const modelName = 'Saadat2021';
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
        <a class="tablinks" href="../mains/index.php">Home</a>
        <a class="tablinks active" href="../mains/models_select.php">Models</a>
      </div>

      <div class="topnav-right">

      </div>

    </header>
  </div>

  <div id="wrapper">
    <div id="content-model">

        <div class="modelpageImg">
            <img src="../img/Matuszynska2016.png" style="width: 100%"/>
        </div>

        <h1 class="modelText" id='modelTitle'></h1>

        <a class="linkButton modelText clickable" id="github-link" target="_blank"><img src="../img/icons/github-mark.svg" style="height: 1em; vertical-align: middle;"/> Github</a>

        <div class="modelText" id="modelSummary">
          <h3>Summary</h3>
        </div>

    </div>

    <div class="modelTabContainer">
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrODE')",>ODE System</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrDerivedComps')">Derived Quantities</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrParams')">Parameters</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrDerivedParams')">Derived Parameters</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrRates')">Rates</button>
    </div>

    <div id="modelAttrODE" class="modelTabContent">
      <h3>ODE System</h3>
      <table id="modelAttrODETable"></table>
      <div id="modelAttrODEMath"></div>
    </div>

    <div id="modelAttrDerivedComps" class="modelTabContent">
      <h3>Derived Quantities</h3>
      <table id="modelAttrDerivedCompsTable"></table>
      <div id="modelAttrDerivedCompsMath"></div>
    </div>

    <div id="modelAttrParams" class="modelTabContent">
      <h3>Parameters</h3>
      <table id="modelAttrParamsTable"></table>
      <div id="modelAttrParamsMath"></div>
    </div>

    <div id="modelAttrDerivedParams" class="modelTabContent">
      <h3>Derived Parameters</h3>
      <table id="modelAttrDerivedParamsTable"></table>
      <div id="modelAttrDerivedParamsMath"></div>
    </div>

    <div id="modelAttrRates" class="modelTabContent">
      <h3>Rates</h3>
      <table id="modelAttrRatesTable"></table>
      <div id="modelAttrRatesMath"></div>
    </div>
  </div>

  <script>
    MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        tags: 'ams',
        maxBuffer: 25000
      }
    };
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <script  src="../node_modules/papaparse/papaparse.js"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
  <script type="text/javascript" src="../js/model_pages.js"></script>
</body>

</html>

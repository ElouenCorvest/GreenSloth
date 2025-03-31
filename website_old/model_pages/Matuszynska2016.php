<!doctype html>
<html lang="en">

<head>
  <?php include('../mains/head.html'); ?>
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
        <a class="tablinks" href="../mains/index.php">Home</a>
        <a class="tablinks active" href="../mains/models_select.php">Models</a>
      </div>

      <div class="topnav-right">

      </div>

    </header>
  </div>

  <div id="tags" class="hidden">
    <div id="apparatus">PSI</div>
  </div>

  <div id="wrapper">
    <div id="content-model">

        <div class="modelpageImg">
            <img src="../img/Matuszynska2016.png" style="width: 100%"/>
        </div>

        <h1 class="modelText" id='modelTitle'>Matuszynska2016</h1>

        <!-- <div id='modelTagsBox' class='tagsRow'>
          <span class='tag active'>Test</span>
        </div> -->

        <div class="modelText" id="modelSummary">
          <h3>Summary</h3>
            <p>The <a href="https://doi.org/10.1016/j.bbabio.2016.09.003">Matuszynska2016</a> model, a small kinetic model, was developed to delve deeper into the effect of light memory caused by non-photochemical quenching. The systematic investigation of the Xanthophyll cycle, a combination of the pigments of violaxanthin, antheraxanthin, and zeaxanthin, sparked a series of experiments to determine whether plant light memory can be detected in a time-scale of minutes to hours through pulse amplitude modulated chlorophyll fluorescence. The model was then created based on these experimental results, providing a comprehensive description of NPQ dynamics and the short-term memory of the <i>Arabidopsis thaliana</i> plant.</p>

            <p>To keep the model as simple as possible, several processes not directly linked to NPQ have been simplified to create a dynamic ODE system consisting only of 6 different compounds. With these simplifications, the authors could fulfil an additional goal: to make a general framework that is not specific to one model organism.</p>

            <p>To demonstrate the adaptability of their model, the authors took their calibrated <i>Arabidopsis thaliana</i> model and successfully applied it to the non-model organism <i>Epipremnum aureum</i>. This adaptation allowed them to simulate realistic fluorescence measurements and replicate all the key features of chlorophyll induction, showcasing the model's versatility and potential for use in a variety of organisms.</p>
        </div>

    </div>

    <div class="modelTabContainer">
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrODE', 'https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/Matuszynska2016/model_info/comps.csv')">ODE System</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrDerivedComps', 'https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/Matuszynska2016/model_info/derived_comps.csv')">Derived Quantities</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrParams', 'https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/Matuszynska2016/model_info/params.csv')">Parameters</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrDerivedParams', 'https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/Matuszynska2016/model_info/derived_params.csv')">Derived Parameters</button>
      <button class="clickable modelTab" onclick="openModelAttr(event, 'modelAttrRates', 'https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/Matuszynska2016/model_info/rates.csv')">Rates</button>
    </div>

    <div id="modelAttrODE" class="modelTabContent">
      <h3>ODE System</h3>
      <table id="modelAttrODETable"></table>
    </div>

    <div id="modelAttrDerivedComps" class="modelTabContent">
      <h3>Derived Quantities</h3>
      <table id="modelAttrDerivedCompsTable"></table>
    </div>

    <div id="modelAttrParams" class="modelTabContent">
      <h3>Parameters</h3>
      <table id="modelAttrParamsTable"></table>
    </div>

    <div id="modelAttrDerivedParams" class="modelTabContent">
      <h3>Derived Parameters</h3>
      <table id="modelAttrDerivedParamsTable"></table>
    </div>

    <div id="modelAttrRates" class="modelTabContent">
      <h3>Rates</h3>
      <table id="modelAttrRatesTable"></table>
    </div>
  </div>

  <script>
    MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']]
      }
    };
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <script  src="../node_modules/papaparse/papaparse.js"></script>
  <script type="text/javascript" src="../js/model_pages.js"></script>
</body>

</html>

<?php require 'require_login.php'; ?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link
    rel="stylesheet"
    href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"
  />
  <link rel="stylesheet" href="src/css/style.css">
  <meta name="description" content="">

  <meta property="og:title" content="">
  <meta property="og:type" content="">
  <meta property="og:url" content="">
  <meta property="og:image" content="">
  <meta property="og:image:alt" content="">

  <!-- <link rel="manifest" href="../site.webmanifest"> -->
  <meta name="theme-color" content="#fafafa">
  <title>GreenSloth Titlepage</title>
</head>

<body>
  <?php require 'login_modal.php'; ?>

  <div id="citeModal" class="modal hidden"></div>
  <div id="layoutWrapper" class="">
    <nav id="topnav"></nav>
    
    <div class="swiper-container">
      <div class="swiper-wrapper">
        <div class="swiper-slide" data-hash="Home">
          <div class="swiper-prev-button swiper-button">
            <span class="arrowUp"></span>
          </div>
          <div class="swiper-content">
            <img src="src/img/greensloth_color_complete.svg" style="min-height: 0; max-height: 50%; width: 30%; flex-grow: 1;"/>
            <p style="color: var(--mainAccentColor); font-weight: bold; font-size: 2.5em;">EASIER ACCESS TO PHOTOSYNTHETIC MODELS</p>
          </div>
          <div class="swiper-next-button swiper-button">
            <p>Find out more!</p>
            <span class="arrowDown"></span>
          </div>
          
        </div>
        <div class="swiper-slide"  data-history="Motivation">
          <div class="swiper-prev-button swiper-button">
            <span class="arrowUp"></span>
          </div>
          <div class="swiper-content">
            <h1>Motivation</h1>
            <p>
              In 2022, Elouen, the creator of GreenSloth, wrote his Bachelor's thesis about comparing the popular and simple steady-state Farquhar, von Caemmerer, and Berry Model (FvCB model) and a kinetic photosynthesis model. While searching for the other model, he searched various public sources for scientific literature and tried to recreate several models. During this time, he arrived at one conclusion: modeling, especially photosynthesis, aims to help others understand more of the essential process of life on Earth. However, the scientific community has not found a common way to share its models. This is where the idea of GreenSloth first came into play.
            </p>
            <p>
              During his further experience with photosynthetic models, he found that this issue was common for experts and amateurs in modelling, which inspired his mind even more to find a solution. He wanted to create a resource that collects popular photosynthesis models and enables an easier summary and accessibility, especially for amateurs in the modelling field. 
            </p>
            <p>
              With GreenSloth, Elouen hopes to facilitate researchers' access to the modeling world. He believes this is vital to understanding and coping with the complexity of photosynthesis. This website will enable even better scientific transparency.
            </p>
          </div>
          <div class="swiper-next-button swiper-button">
            <p>How to use!</p>
            <span class="arrowDown"></span>
          </div>
          
        </div>
        <div class="swiper-slide" data-hash="HowToUse">
          <div class="swiper-prev-button swiper-button">
            <span class="arrowUp"></span>
          </div>
          <div class="swiper-content" style="max-width: 1000px;">
            <h1>How To Use</h1>
            <p style="font-size: larger; text-align: center; font-weight: bold;">GreenSloth can be separated into three distinct aspects of model searching.</p>
            <div class="TabContainer">
              <button>Search</button>
              <button>Summary</button>
              <button>Comparision</button>
            </div>
            <div id="howtouse-search" class="howtouse-text hidden">
              <p>The first aspect of finding models is searching for them. Most commonly, new models are found by reading scientific literature, which has many positive aspects. However, it takes time and is tiring. Additionally, with the mass of new publications over time, some models will drown under the waves of new information. This is where GreenSloth comes into play, as it highlights already curated and popular models.</p>
              <p>GreenSloth shows its curated models in a <a href="src/html/models_select.php">list</a> with the model’s name and scheme. Furthermore, GreenSloth introduces manually curated categories to see where the chosen models overlap. These categories are separated into a tag system to facilitate selecting the right model.</p>
            </div>
            <div id="howtouse-summary" class="howtouse-text hidden">
              <p>Each of the models presented on GreenSloth comes with a curated summary from the publication and a completed version, which is available for download using the modelbase package. Additionally, some vital model information, like the ODE system, the parameters, etc., are tabularized for ease of access. Every model on GreenSloth will also include tests to give further insight into the completeness of each model.</p>
            </div>
            <div id="howtouse-comparision" class="howtouse-text hidden">
              <p>To help choose between models, GreenSloth lets you compare vital information between two models directly. This enables a quicker and more efficient way to choose which model is best tailored to your specific needs. While most comparisons are done using the information from each model summary, GreenSloth also uses more advanced, newly developed techniques.</p>
            </div>
          </div>
          <div class="swiper-next-button swiper-button">
            <p>Get Right into it!</p>
            <span class="arrowDown"></span>
          </div>
          
        </div>
        <div class="swiper-slide" data-history="PhotosynthesisScheme">
          <div class="swiper-prev-button swiper-button">
            <span class="arrowUp"></span>
          </div>
          <div class="swiper-content">
            <h3>Press the photosynthesis apparatus you wish to look into!</h3>
            <svg id="photosynthesis-scheme" style="flex-grow: 1;" width="216.05mm" height="125.18mm" version="1.1" viewBox="0 0 216.05 125.18" xmlns="http://www.w3.org/2000/svg">
              <g transform="translate(-3.2695 -25.238)">
                <rect x="3.2695" y="108.2" width="216.05" height="2" rx=".5" fill="#4d683d" style="paint-order:markers stroke fill"/>
                <rect x="3.2695" y="127.53" width="216.05" height="2" rx=".5" fill="#4d683d" style="paint-order:markers stroke fill"/>
                <g transform="translate(10.133 25.589)" fill="#000000" font-family="'Source Sans 3'" font-size="8.2931px" stroke-width=".20733">
                  <text x="-6.3343873" y="81.641235" style="line-height:1.05" xml:space="preserve"><tspan x="-6.3343873" y="81.641235" fill="#000000" font-weight="bold" stroke-width=".20733">Stroma</tspan></text>
                  <text x="-6.6826963" y="109.97566" style="line-height:1.05" xml:space="preserve"><tspan x="-6.6826963" y="109.97566" fill="#000000" font-weight="bold" stroke-width=".20733">Lumen</tspan></text>
                </g>
              </g>
              <a id="scheme-oec" transform="translate(6.8636 23.877)">
                <ellipse cx="34.445" cy="90.412" rx="11.573" ry="9.3954" fill="#bbdef0" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text x="28.570921" y="96.907669" font-family="'Source Sans 3'" font-size="6.3989px" stroke-width=".15997" style="line-height:1.05" xml:space="preserve"><tspan x="28.570921" y="96.907669" font-weight="bold" stroke-width=".15997">OEC</tspan></text>
              </a>
              <a id="scheme-psii" transform="translate(6.8637 .35047)">
                <ellipse cx="34.445" cy="93.275" rx="14.445" ry="19.33" fill="#5fad56" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text x="25.216417" y="96.725319" font-family="'Source Sans 3'" font-size="10.583px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan x="25.216417" y="96.725319" font-weight="bold" stroke-width=".26458">PSII</tspan></text>
              </a>
              <a id="scheme-cytb6f" transform="translate(6.8637 .35047)">
                <ellipse cx="83.335" cy="93.275" rx="14.445" ry="19.33" fill="#63c7b2" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text x="71.703972" y="95.296288" font-family="'Source Sans 3'" font-size="7.7885px" stroke="#000000" stroke-opacity="0" stroke-width=".19471" style="line-height:1.05" xml:space="preserve"><tspan x="71.703972" y="95.296288" font-weight="bold" stroke="#000000" stroke-opacity="0" stroke-width=".19471">Cytb6f</tspan></text>
              </a>
              <a id="scheme-psi" transform="translate(6.8637 .35047)">
                <ellipse cx="132.23" cy="93.275" rx="14.445" ry="19.33" fill="#4d9078" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text x="132.22528" y="96.725327" font-family="'Source Sans 3'" font-size="10.583px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan x="132.22528" y="96.725327" font-weight="bold" stroke-width=".26458" text-align="center" text-anchor="middle">PSI</tspan></text>
              </a>
              <a id="scheme-atpsynth" transform="translate(6.8637 .35047)">
                <rect x="168.08" y="73.945" width="19.692" height="38.661" rx="1.3495" fill="#f78154" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <g transform="matrix(1.4098 0 0 1.4098 -175.97 -39.243)">
                  <ellipse cx="256.94" cy="73.424" rx="2.7751" ry="7.8286" fill="#c86a8c" style="paint-order:markers stroke fill"/>
                  <ellipse cx="254.17" cy="73.424" rx="3.0834" ry="8.6985" fill="#f99b76" style="paint-order:markers stroke fill"/>
                  <ellipse transform="scale(-1,1)" cx="-244.88" cy="73.424" rx="2.7751" ry="7.8286" fill="#c86a8c" style="paint-order:markers stroke fill"/>
                  <ellipse transform="scale(-1,1)" cx="-247.66" cy="73.424" rx="3.0834" ry="8.6985" fill="#f99b76" style="paint-order:markers stroke fill"/>
                  <ellipse cx="251.08" cy="73.424" rx="3.426" ry="9.665" fill="#c86a8c" style="paint-order:markers stroke fill"/>
                </g>
                <g transform="translate(-4.4538 -22.039)" font-family="'Source Sans 3'">
                  <text x="182.6032" y="114.88722" font-size="10.583px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan x="182.6032" y="114.88722" font-weight="bold" stroke-width=".26458" text-align="center" text-anchor="middle">ATP</tspan></text>
                  <text x="182.46231" y="121.32639" font-size="6.7817px" stroke-width=".16954" style="line-height:1.05" xml:space="preserve"><tspan x="182.46231" y="121.32639" font-weight="bold" stroke-width=".16954" text-align="center" text-anchor="middle">Synth</tspan></text>
                </g>
              </a>
              <a id="scheme-cbb" transform="translate(6.8637 .35047)">
                <g stroke-linecap="round">
                  <path d="m129.18 26.72a21.82 21.82 0 0 1-21.82 21.82 21.82 21.82 0 0 1-21.82-21.82 21.82 21.82 0 0 1 21.82-21.82 21.82 21.82 0 0 1 21.82 21.82z" color="#000000" fill-opacity="0" stroke-linejoin="bevel" style="-inkscape-stroke:none"/>
                  <path d="m107.36 4.1504c-12.456 0-22.57 10.112-22.57 22.568s10.114 22.57 22.57 22.57c12.456 0 22.568-10.114 22.568-22.57s-10.112-22.568-22.568-22.568zm0 1.5c11.645 0 21.068 9.4231 21.068 21.068s-9.4231 21.07-21.068 21.07c-11.645 0-21.07-9.4251-21.07-21.07s9.4251-21.068 21.07-21.068z" color="#000000" fill="#d81159" stroke-linejoin="bevel" style="-inkscape-stroke:none"/>
                  <g fill="#d81159">
                    <path d="m124.68 21.844a0.75 0.75 0 0 0-0.5293 0.2207 0.75 0.75 0 0 0 0 1.0605l5.0293 5.0293 5.0312-5.0293a0.75 0.75 0 0 0 0-1.0605 0.75 0.75 0 0 0-1.0606 0l-3.9707 3.9707-3.9688-3.9707a0.75 0.75 0 0 0-0.53125-0.2207z" color="#000000" style="-inkscape-stroke:none"/>
                    <path d="m102.71-0.13086a0.75 0.75 0 0 0 0 1.0605l3.9707 3.9688-3.9707 3.9707a0.75 0.75 0 0 0 0 1.0605 0.75 0.75 0 0 0 1.0606 0l5.0312-5.0293-5.0312-5.0312a0.75 0.75 0 0 0-1.0606 0z" color="#000000" style="-inkscape-stroke:none"/>
                    <path d="m85.541 25.283-5.0293 5.0312a0.75 0.75 0 0 0 0 1.0605 0.75 0.75 0 0 0 1.0605 0l3.9707-3.9688 3.9688 3.9688a0.75 0.75 0 0 0 1.0605 0 0.75 0.75 0 0 0 0-1.0605z" color="#000000" style="-inkscape-stroke:none"/>
                    <path d="m111.49 43.289a0.75 0.75 0 0 0-0.53125 0.21875l-5.0293 5.0312 5.0293 5.0312a0.75 0.75 0 0 0 1.0606 0 0.75 0.75 0 0 0 0-1.0625l-3.9688-3.9688 3.9688-3.9688a0.75 0.75 0 0 0 0-1.0625 0.75 0.75 0 0 0-0.5293-0.21875z" color="#000000" style="-inkscape-stroke:none"/>
                  </g>
                </g>
                <text x="97.809265" y="30.169697" font-family="'Source Sans 3'" font-size="10.583px" stroke-width="1.5" style="line-height:1.05" xml:space="preserve"><tspan x="97.809265" y="30.169697" font-weight="bold" stroke-width="1.5">CBB</tspan></text>
              </a>
              <a id="scheme-fnr" transform="translate(6.8637 .35047)">
                <ellipse cx="146.73" cy="67.026" rx="8.4889" ry="5.2234" fill="#f2c14e" style="paint-order:markers stroke fill"/>
                <text x="146.53954" y="69.122124" font-family="'Source Sans 3'" font-size="6.4286px" stroke-width=".16071" style="line-height:1.05" xml:space="preserve"><tspan x="146.53954" y="69.122124" font-weight="bold" stroke-width=".16071" text-align="center" text-anchor="middle">FNR</tspan></text>
              </a>
            </svg>
          </div>
          <div class="swiper-next-button swiper-button">
            <span class="arrowDown"></span>
          </div>
          
        </div>
      </div>

      <div class="swiper-pagination"></div>
    </div>

  </div>

  <script type="module" src="src/js/index.js"></script>
  <script type="module" src="src/js/topnav.js"></script>
  <script type="module" src="src/js/cite.js"></script>
  <script src="//code.iconify.design/1/1.0.6/iconify.min.js"></script>
  

</body>

</html>

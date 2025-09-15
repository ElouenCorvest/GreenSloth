<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"
  />
  <link rel="stylesheet" href="/src/css/style.css">
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

  <meta name="theme-color" content="#fafafa">
  <title>GreenSloth</title>
</head>

<body>
  <div id="citeModal" class="modal hidden"></div>
  <div id="layoutWrapper" class="">
    <nav id="topnav"></nav>
    
    <div class="swiper-container">
      <div class="swiper-wrapper">
        <div class="swiper-slide index-slide" data-hash="Home">
          <div class="swiper-content swiper-content-flex">
            <img src="src/img/greensloth_color_complete.svg" id="index-swiper-slide1-logo"/>
            <p id="index-swiper-slide1-text">EASIER ACCESS TO PHOTOSYNTHETIC MODELS</p>
          </div>
          <div class="swiper-next-button swiper-button">
            <p>Find out more!</p>
            <span class="arrowDown"></span>
          </div>
          
        </div>
        <div class="swiper-slide index-slide"  data-history="Motivation">
          <div class="swiper-prev-button swiper-button">
            <span class="arrowUp"></span>
          </div>
          <div class="swiper-content swiper-content-flex">
            <h1>Motivation</h1>
            <div class="long-text swiper-no-swiping" id="motivation-text">
              <p>Photosynthesis is arguably the most crucial process of life on Earth. It feeds us, clothes us, heals us, and calms us. Therefore, it has long been a significant target for research, and while we now know a great deal about how, why, and who photosynthesis is, there are still aspects of it that we cannot quite grasp. However, with the rise of computational prowess, we have developed new ways to examine and understand photosynthesis. Through digital models of photosynthesis!</p>
              <p>While this field has existed for decades, it has recently gained significant importance. To such an extent that there are many different models of photosynthesis, each attempting to depict various aspects, some even the entirety, of the process. This boom enables a researcher interested in this field to have the power of choice of models. However, this power also comes with a curse.</p>
              <p>The different models all have their strengths and aim to cater to people who are not proficient in creating a model on their own. However, since the publication of models is not as heavily regulated as lab work and most model builders are experts in their field, a disconnect exists between the model and the target user. It can be challenging to find a model that fits your needs. This is where <b>GreenSloth</b> comes in.</p>
              <p><b>GreenSloth</b> will help you, the researcher interested in modelling photosynthesis, decide which model is best suited for your needs. While this project is still in its infancy, we, the <a href="https://www.cpbl.rwth-aachen.de/go/id/sazuq/?lidx=1" target="_blank">Computational Life Science</a> group of the Biology department at RWTH Aachen, led by Prof. Dr. rer. nat. Matuszyńska, stand behind it and its idea. If you understand our motivation and would like to be part of it, please email (<a href="mailto:elouen.corvest@rwth-aachen.de" target="_blank">elouen.corvest@rwth-aachen.de</a>) us with your ideas, models to include, or general feedback on how we can make <b>GreenSloth</b> better for you.</p>
            </div>
          </div>
          <div class="swiper-next-button swiper-button">
            <p>How to use!</p>
            <span class="arrowDown"></span>
          </div>
          
        </div>
        <div class="swiper-slide index-slide" data-hash="HowToUse">
          <div class="swiper-prev-button swiper-button">
            <span class="arrowUp"></span>
          </div>
          <div class="swiper-content swiper-content-grid">
            <h1>How To Use</h1>
            <p style="font-size: larger; text-align: center; font-weight: bold;">GreenSloth can be separated into three distinct aspects of model searching.</p>
            <div class="TabContainer index-tab-container">
              <button>Search</button>
              <button>Summary</button>
              <button>Comparision</button>
            </div>
            <div id="howtouse-search" class="hidden long-text">
              <p>The first aspect of finding models is searching for them. Most commonly, new models are found by reading scientific literature, which has many positive aspects. However, it takes time and is tiring. Additionally, with the mass of new publications over time, some models will drown under the waves of new information. This is where GreenSloth comes into play, as it highlights already curated and popular models.</p>
              <p>GreenSloth shows its curated models in a <a href="src/html/models_select.php">list</a> with the model's name and scheme. Furthermore, GreenSloth introduces manually curated categories to see where the chosen models overlap. These categories are separated into a tag system to facilitate selecting the right model.</p>
            </div>
            <div id="howtouse-summary" class="hidden long-text">
              <p>Each of the models presented on GreenSloth comes with a curated summary from the publication and a completed version, which is available for download using the modelbase package. Additionally, some vital model information, like the ODE system, the parameters, etc., are tabularized for ease of access. Every model on GreenSloth will also include tests to give further insight into the completeness of each model.</p>
            </div>
            <div id="howtouse-comparision" class="hidden long-text">
              <p>To help choose between models, GreenSloth lets you compare vital information between two models directly. This enables a quicker and more efficient way to choose which model is best tailored to your specific needs. While most comparisons are done using the information from each model summary, GreenSloth also uses more advanced, newly developed techniques.</p>
            </div>
          </div>
          <div class="swiper-next-button swiper-button">
            <p>Get Right into it!</p>
            <span class="arrowDown"></span>
          </div>
          
        </div>
        <div class="swiper-slide index-slide" data-history="PhotosynthesisScheme">
          <div class="swiper-prev-button swiper-button">
            <span class="arrowUp"></span>
          </div>
          <div class="swiper-content">
            <h3>Press the part of photosynthesis to see which models include it!</h3>
            <svg id="photosynthesis-scheme" width="216.05mm" height="125.18mm" version="1.1" viewBox="0 0 216.05 125.18" xmlns="http://www.w3.org/2000/svg">
              <g id="g26" transform="translate(-3.2695 -25.238)">
                <rect id="rect1" x="3.2695" y="108.2" width="216.05" height="2" rx=".5" fill="#4d683d" style="paint-order:markers stroke fill"/>
                <rect id="rect43" x="3.2695" y="127.53" width="216.05" height="2" rx=".5" fill="#4d683d" style="paint-order:markers stroke fill"/>
                <g id="g43" transform="translate(10.133 25.589)" fill="#000000" font-family="'Source Sans 3'" font-size="8.2931px" stroke-width=".20733">
                  <text id="text1-2" x="-6.3343873" y="81.641235" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-7" x="-6.3343873" y="81.641235" fill="#000000" font-weight="bold" stroke-width=".20733">Stroma</tspan></text>
                  <text id="text1-2-3" x="-6.6826963" y="109.97566" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-7-6" x="-6.6826963" y="109.97566" fill="#000000" font-weight="bold" stroke-width=".20733">Lumen</tspan></text>
                </g>
              </g>
              <a id="scheme-oec" transform="translate(6.8636 23.877)">
                <ellipse id="ellipse1-5" cx="34.445" cy="90.412" rx="11.573" ry="9.3954" fill="#bbdef0" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text id="text1-35" x="28.570921" y="96.907669" font-family="'Source Sans 3'" font-size="6.3989px" stroke-width=".15997" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-62" x="28.570921" y="96.907669" font-weight="bold" stroke-width=".15997">OEC</tspan></text>
              </a>
              <a id="scheme-psii" transform="translate(6.8637 .35047)">
                <ellipse id="ellipse1" cx="34.445" cy="93.275" rx="14.445" ry="19.33" fill="#5fad56" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text id="text1" x="25.216417" y="96.725319" font-family="'Source Sans 3'" font-size="10.583px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1" x="25.216417" y="96.725319" font-weight="bold" stroke-width=".26458">PSII</tspan></text>
              </a>
              <a id="scheme-cytb6f" transform="translate(6.8637 .35047)">
                <ellipse id="path1-2" cx="83.335" cy="93.275" rx="14.445" ry="19.33" fill="#63c7b2" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text id="text1-9" x="71.703972" y="95.296288" font-family="'Source Sans 3'" font-size="7.7885px" stroke="#000000" stroke-opacity="0" stroke-width=".19471" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-1" x="71.703972" y="95.296288" font-weight="bold" stroke="#000000" stroke-opacity="0" stroke-width=".19471">Cytb6f</tspan></text>
              </a>
              <a id="scheme-psi" transform="translate(6.8637 .35047)">
                <ellipse id="path1-9" cx="132.23" cy="93.275" rx="14.445" ry="19.33" fill="#4d9078" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <text id="text1-3" x="132.22528" y="96.725327" font-family="'Source Sans 3'" font-size="10.583px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-6" x="132.22528" y="96.725327" font-weight="bold" stroke-width=".26458" text-align="center" text-anchor="middle">PSI</tspan></text>
              </a>
              <a id="scheme-atpsynth" transform="translate(6.8637 .35047)">
                <rect id="rect2" x="168.08" y="73.945" width="19.692" height="38.661" rx="1.3495" fill="#f78154" stroke="#fff" stroke-dashoffset="3.2519" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" style="paint-order:markers stroke fill"/>
                <g id="g8" transform="matrix(1.4098 0 0 1.4098 -175.97 -39.243)">
                  <ellipse id="path4-9-3" cx="256.94" cy="73.424" rx="2.7751" ry="7.8286" fill="#c86a8c" style="paint-order:markers stroke fill"/>
                  <ellipse id="path4-9" cx="254.17" cy="73.424" rx="3.0834" ry="8.6985" fill="#f99b76" style="paint-order:markers stroke fill"/>
                  <ellipse id="path4-9-3-2" transform="scale(-1,1)" cx="-244.88" cy="73.424" rx="2.7751" ry="7.8286" fill="#c86a8c" style="paint-order:markers stroke fill"/>
                  <ellipse id="path4-9-2" transform="scale(-1,1)" cx="-247.66" cy="73.424" rx="3.0834" ry="8.6985" fill="#f99b76" style="paint-order:markers stroke fill"/>
                  <ellipse id="path4" cx="251.08" cy="73.424" rx="3.426" ry="9.665" fill="#c86a8c" style="paint-order:markers stroke fill"/>
                </g>
                <g id="g9" transform="translate(-4.4538 -22.039)" font-family="'Source Sans 3'">
                  <text id="text1-3-3" x="182.6032" y="114.88722" font-size="10.583px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-6-6" x="182.6032" y="114.88722" font-weight="bold" stroke-width=".26458" text-align="center" text-anchor="middle">ATP</tspan></text>
                  <text id="text1-3-31" x="182.46231" y="121.32639" font-size="6.7817px" stroke-width=".16954" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-6-9" x="182.46231" y="121.32639" font-weight="bold" stroke-width=".16954" text-align="center" text-anchor="middle">Synth</tspan></text>
                </g>
              </a>
              <a id="scheme-cbb" transform="translate(.66246 8.3033)">
                <g id="path26" stroke-linecap="round">
                  <path id="path37" d="m129.18 26.72a21.82 21.82 0 0 1-21.82 21.82 21.82 21.82 0 0 1-21.82-21.82 21.82 21.82 0 0 1 21.82-21.82 21.82 21.82 0 0 1 21.82 21.82z" color="#000000" fill-opacity="0" stroke-linejoin="bevel" style="-inkscape-stroke:none"/>
                  <path id="path38" d="m107.36 4.1504c-12.456 0-22.57 10.112-22.57 22.568s10.114 22.57 22.57 22.57c12.456 0 22.568-10.114 22.568-22.57s-10.112-22.568-22.568-22.568zm0 1.5c11.645 0 21.068 9.4231 21.068 21.068s-9.4231 21.07-21.068 21.07c-11.645 0-21.07-9.4251-21.07-21.07s9.4251-21.068 21.07-21.068z" color="#000000" fill="#d81159" stroke-linejoin="bevel" style="-inkscape-stroke:none"/>
                  <g id="g33" fill="#d81159">
                    <path id="path36" d="m124.68 21.844a0.75 0.75 0 0 0-0.5293 0.2207 0.75 0.75 0 0 0 0 1.0605l5.0293 5.0293 5.0312-5.0293a0.75 0.75 0 0 0 0-1.0605 0.75 0.75 0 0 0-1.0606 0l-3.9707 3.9707-3.9688-3.9707a0.75 0.75 0 0 0-0.53125-0.2207z" color="#000000" style="-inkscape-stroke:none"/>
                    <path id="path35" d="m102.71-0.13086a0.75 0.75 0 0 0 0 1.0605l3.9707 3.9688-3.9707 3.9707a0.75 0.75 0 0 0 0 1.0605 0.75 0.75 0 0 0 1.0606 0l5.0312-5.0293-5.0312-5.0312a0.75 0.75 0 0 0-1.0606 0z" color="#000000" style="-inkscape-stroke:none"/>
                    <path id="path34" d="m85.541 25.283-5.0293 5.0312a0.75 0.75 0 0 0 0 1.0605 0.75 0.75 0 0 0 1.0605 0l3.9707-3.9688 3.9688 3.9688a0.75 0.75 0 0 0 1.0605 0 0.75 0.75 0 0 0 0-1.0605z" color="#000000" style="-inkscape-stroke:none"/>
                    <path id="path33" d="m111.49 43.289a0.75 0.75 0 0 0-0.53125 0.21875l-5.0293 5.0312 5.0293 5.0312a0.75 0.75 0 0 0 1.0606 0 0.75 0.75 0 0 0 0-1.0625l-3.9688-3.9688 3.9688-3.9688a0.75 0.75 0 0 0 0-1.0625 0.75 0.75 0 0 0-0.5293-0.21875z" color="#000000" style="-inkscape-stroke:none"/>
                  </g>
                </g>
                <text id="text1-6" x="97.809265" y="30.169697" font-family="'Source Sans 3'" font-size="10.583px" stroke-width="1.5" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-10" x="97.809265" y="30.169697" font-weight="bold" stroke-width="1.5">CBB</tspan></text>
              </a>
              <a id="scheme-fnr" transform="translate(1.2198 8.8918)">
                <ellipse id="path27" cx="146.73" cy="67.026" rx="8.4889" ry="5.2234" fill="#f2c14e" style="paint-order:markers stroke fill"/>
                <text id="text1-3-0" x="146.53954" y="69.122124" font-family="'Source Sans 3'" font-size="6.4286px" stroke-width=".16071" style="line-height:1.05" xml:space="preserve"><tspan id="tspan1-6-61" x="146.53954" y="69.122124" font-weight="bold" stroke-width=".16071" text-align="center" text-anchor="middle">FNR</tspan></text>
              </a>
              <a id="scheme-pq" transform="translate(20.088 -54.22)">
                <rect id="rect3" x="37.12" y="140.06" width="17.091" height="15.576" rx="5.5295" fill="#bf93c0" stroke="#fff" stroke-linejoin="round" stroke-width="1.7544" style="paint-order:markers stroke fill"/>
                <text id="text2" x="45.390369" y="149.88583" font-family="'Source Sans 3'" font-size="8.4667px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan id="tspan3" x="45.390369" y="149.88583" font-size="8.4667px" font-weight="bold" stroke-width=".26458" text-align="center" text-anchor="middle">PQ</tspan></text>
              </a>
              <a id="scheme-pc" transform="matrix(1.0437 0 0 1 66.984 -34.89)">
                <rect id="rect4" x="33.235" y="140.26" width="24.861" height="16.281" rx="6.5393" fill="#8684cf" stroke="#fff" stroke-linejoin="round" stroke-width="2.1634" style="paint-order:markers stroke fill"/>
                <text id="text4" x="45.390369" y="149.88583" font-family="'Source Sans 3'" font-size="8.4667px" stroke-width=".26458" style="line-height:1.05" xml:space="preserve"><tspan id="tspan4" x="45.390369" y="149.88583" font-size="8.4667px" font-weight="bold" stroke-width=".26458" text-align="center" text-anchor="middle">PC</tspan></text>
              </a>
            </svg>
          </div>
        </div>
      </div>

      <div class="swiper-pagination"></div>
    </div>

  </div>

  <script type="module" src="./src/js/index.js"></script>
  <script type="module" src="./src/js/topnav.js"></script>
  <script type="module" src="./src/js/cite.js"></script>
  <script src="//code.iconify.design/1/1.0.6/iconify.min.js"></script>
  

</body>

</html>

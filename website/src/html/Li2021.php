<!DOCTYPE html>
<html>

<head>
  <?php include "head_pages.php" ?>
</head>

<body>
  <div id="layoutWrapper">
    <nav id="topnav"></nav>

    <div id="wrapper">
      <div id="content">
        
        <!-- The Cite Modal -->
        <div id="citeModal" class="modal hidden"></div>
        
      </div>
    </div>
  </div>

  <script>
    MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        tags: 'ams',
        maxBuffer: 10 * 1024,
      }
    };
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  <script type="module" src="../js/model_pages.js"></script>
  <script type="module" src="../js/topnav.js"></script>
  <script type="module" src="../js/cite.js"></script>
  <script src="//code.iconify.design/1/1.0.6/iconify.min.js"></script>
</body>

</html>

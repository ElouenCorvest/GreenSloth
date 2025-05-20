// core version + navigation, pagination modules:
import Swiper from 'swiper';
import { Navigation, Pagination } from 'swiper/modules';

// Register the Navigation module
Swiper.use([Navigation, Pagination]);

// import Swiper from 'swiper'

var swiper = new Swiper('.swiper-container', {

    direction: 'vertical',
    mousewheel: true,
    slidesPerView: 1,
    grabCursor: true,
    autoHeight: true,
    loop: true,

    // Navigation arrows
    navigation: {
        nextEl: '.swiper-next-button',
        prevEl: '.swiper-prev-button'
    },

    //Dots
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
        type: "bullets"
    },

    // URL Navigation
    hashNavigation: {
        watchstate: true,
        replaceState: true,
      },

  });

// Photosynthesis Scheme

// Photosynthesis Scheme - Set the links
var schemePsii = document.getElementById("scheme-psii")
schemePsii.setAttribute("href", "models_select.html?appar=PSII")

var schemeCytb6f = document.getElementById("scheme-cytb6f")
schemeCytb6f.setAttribute("href", "models_select.html?appar=Cytb6f")

var schemePsi = document.getElementById("scheme-psi")
schemePsi.setAttribute("href", "models_select.html?appar=PSI")

var schemeAtpsynth = document.getElementById("scheme-atpsynth")
schemeAtpsynth.setAttribute("href", "models_select.html?appar=ATPSynth")

var schemeCBB = document.getElementById("scheme-cbb")
schemeCBB.setAttribute("href", "models_select.html?appar=CBB")

var schemeFNR = document.getElementById("scheme-fnr")
schemeFNR.setAttribute("href", "models_select.html?appar=FNR")

var schemeOEC = document.getElementById("scheme-oec")
schemeOEC.setAttribute("href", "models_select.html?appar=OEC")
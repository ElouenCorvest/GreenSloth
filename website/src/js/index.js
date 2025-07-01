// core version + navigation, pagination modules:
import Swiper from 'swiper';
import { Navigation, Pagination, Mousewheel, History, HashNavigation } from 'swiper/modules';

// import Swiper from 'swiper'

var swiper = new Swiper('.swiper-container', {

    modules: [Navigation, Pagination, Mousewheel, HashNavigation],

    observer: true,
    observerParents: true,

    direction: 'vertical',
    mousewheel: {
        enabled: true
    },
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
        watchState: true,
    },

  });

// How To Use
var tabContainer = document.getElementsByClassName("TabContainer")[0]
console.log(tabContainer.children)
for (let i = 0; i < tabContainer.children.length; i++) {
    const button = tabContainer.children[i]
    button.addEventListener('click', function() {
        for (let j = 0; j < tabContainer.children.length; j++) {
            const otherButton = tabContainer.children[j]
            if (otherButton != button) {
                otherButton.classList.remove("active")
                const text = document.getElementById(`howtouse-${otherButton.innerHTML.toLowerCase()}`)
                text.classList.add("hidden")
            } else {
                otherButton.classList.add("active")
                const text = document.getElementById(`howtouse-${otherButton.innerHTML.toLowerCase()}`)
                text.classList.remove("hidden")
            }
        }
    })
}

// Photosynthesis Scheme

// Photosynthesis Scheme - Set the links
var schemePsii = document.getElementById("scheme-psii")
schemePsii.setAttribute("href", "../src/html/models_select.php?appar=PSII")

var schemeCytb6f = document.getElementById("scheme-cytb6f")
schemeCytb6f.setAttribute("href", "../src/html/models_select.php?appar=Cytb6f")

var schemePsi = document.getElementById("scheme-psi")
schemePsi.setAttribute("href", "../src/html/models_select.php?appar=PSI")

var schemeAtpsynth = document.getElementById("scheme-atpsynth")
schemeAtpsynth.setAttribute("href", "../src/html/models_select.php?appar=ATPSynth")

var schemeCBB = document.getElementById("scheme-cbb")
schemeCBB.setAttribute("href", "../src/html/models_select.php?appar=CBB")

var schemeFNR = document.getElementById("scheme-fnr")
schemeFNR.setAttribute("href", "../src/html/models_select.php?appar=FNR")

var schemeOEC = document.getElementById("scheme-oec")
schemeOEC.setAttribute("href", "../src/html/models_select.php?appar=OEC")
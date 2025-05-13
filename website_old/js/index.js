import Swiper from 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.mjs';
import Navigation from"https://cdn.jsdelivr.net/npm/swiper@11/modules/navigation.min.mjs"
import Pagination from"https://cdn.jsdelivr.net/npm/swiper@11/modules/pagination.min.mjs"

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
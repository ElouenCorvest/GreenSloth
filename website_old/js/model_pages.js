// Select all items in the container
const cards = document.querySelectorAll('.attributeCard');
var clickedFlag = false

cards.forEach(card => {
    // Add first click event
    card.addEventListener('click', () => {
        if (card.classList.contains('clicked')) {
            cards.forEach(sibling => {
                if (sibling == card) {
                    sibling.classList.remove('clicked')
                } else {
                    sibling.classList.remove('notClicked')
                };
            });
        } else
        cards.forEach(sibling => {
            if (sibling == card) {
                sibling.classList.add('clicked')
                sibling.classList.remove('notClicked')
            } else {
                sibling.classList.add('notClicked', 'inactiveCard')
                if (sibling.classList.contains('afterCard')) {
                    sibling.classList.add('inactiveCardAfter')
                };
                sibling.classList.remove('clicked', 'activeCard')
            };
        });
    });
    // Add mouseenter event
    card.addEventListener('mouseenter', () => {
        var activeCardFlag = false;
        cards.forEach(sibling => {
            if (sibling == card) {
                activeCardFlag = true
                card.classList.add('activeCard')
                card.classList.remove('inactiveCard', 'inactiveCardAfter')
            };
            if (sibling !== card && !sibling.classList.contains('clicked')) {
                sibling.classList.add('inactiveCard')
            };
            if (sibling !== card && activeCardFlag) {
                sibling.classList.add('inactiveCardAfter')
                sibling.classList.add('afterCard')
            };
        });
    });
    // Add mouseleave event
    card.addEventListener('mouseleave', () => {
        cards.forEach(sibling => {
            if (sibling.classList.contains('notClicked')) {
                sibling.classList.remove('activeCard')
                sibling.classList.add('inactiveCard')
                if (sibling.classList.contains('afterCard')) {
                    sibling.classList.add('inactiveCardAfter')
                };
            } else if (sibling.classList.contains('clicked')) {
                sibling.classList.remove('inactiveCard', 'inactiveCardAfter', 'afterCard')
            } else {
                sibling.classList.remove('inactiveCard', 'inactiveCardAfter', 'afterCard', 'activeCard')
            };
        });
    });
})

// cards.forEach(card => {
//     console.log(mouseLeaveFLag)
//     // Add click event listerner
//     card.addEventListener('click', () => {
//         if (card.classList.contains('activeCard')) {
//             cards.forEach(sibling => {
//                 sibling.classList.remove('activeCard', 'inactiveCard', 'inactiveCardAfter');
//             })
//         } else {
//             card.classList.add('activeCard');
//             var flag = false
//             cards.forEach(sibling => {
//                 sibling.classList.remove('inactiveCard', 'inactiveCardAfter');
//                 if (sibling == card) {
//                     flag = true
//                 };
//                 if (sibling !== card) {
//                     sibling.classList.add('inactiveCard');
//                     sibling.classList.remove('activeCard');
//                 };
//                 if (sibling !== card && flag == true ) {
//                     sibling.classList.add('inactiveCardAfter')
//                 };
//             });
//         };
//     });


//     // Add hover event listeners
//     card.addEventListener('mouseenter', () => {
//         // Change the background of all other siblings
//         var flag = false
//         cards.forEach(sibling => {
//             if (sibling == card) {
//                 flag = true
//                 sibling.classList.remove('inactiveCard', 'inactiveCardAfter')
//             };
//             if (sibling !== card) {
//                 sibling.classList.add("cardSibling")
//             };
//             if (sibling !== card && flag == true ) {
//                 sibling.classList.add("cardSiblingAfter")
//             };
//         });
//     });

//     if (mouseLeaveFLag) {
//         // Revert the background color when mouse leaves
//         card.addEventListener('mouseleave', () => {
//             // Reset the background of all items
//             cards.forEach(sibling => {
//                 sibling.classList.remove("cardSiblingAfter", "cardSibling")
//             });
//         });
//     };
// });



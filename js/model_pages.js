// Select all items in the container
const cards = document.querySelectorAll('.attributeCard');
let mouseLeaveFLag = true;

cards.forEach(card => {
    console.log(mouseLeaveFLag)
    // Add click event listerner
    card.addEventListener('click', () => {
        if (card.classList.contains('activeCard')) {
            cards.forEach(sibling => {
                sibling.classList.remove('activeCard', 'inactiveCard', 'inactiveCardAfter');
            })
        } else {
            card.classList.add('activeCard');
            var flag = false
            cards.forEach(sibling => {
                sibling.classList.remove('inactiveCard', 'inactiveCardAfter');
                if (sibling == card) {
                    flag = true
                };
                if (sibling !== card) {
                    sibling.classList.add('inactiveCard');
                    sibling.classList.remove('activeCard');
                };
                if (sibling !== card && flag == true ) {
                    sibling.classList.add('inactiveCardAfter')
                };
            });
        };
    });


    // Add hover event listeners
    card.addEventListener('mouseenter', () => {
        // Change the background of all other siblings
        var flag = false
        cards.forEach(sibling => {
            if (sibling == card) {
                flag = true
                sibling.classList.remove('inactiveCard', 'inactiveCardAfter')
            };
            if (sibling !== card) {
                sibling.classList.add("cardSibling")
            };
            if (sibling !== card && flag == true ) {
                sibling.classList.add("cardSiblingAfter")
            };
        });
    });

    if (mouseLeaveFLag) {
        // Revert the background color when mouse leaves
        card.addEventListener('mouseleave', () => {
            // Reset the background of all items
            cards.forEach(sibling => {
                sibling.classList.remove("cardSiblingAfter", "cardSibling")
            });
        });
    };
});

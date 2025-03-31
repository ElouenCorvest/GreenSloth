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

function fetchCSV() {
    const csvUrl = "https://example.com/data.csv"; // Replace with your CSV URL

    Papa.parse(csvUrl, {
        download: true,
        header: true,
        skipEmptyLines: true,
        chunk: function(results, parser) { // Process in chunks
            appendToTable(results.data);
        },
        complete: function() {
            MathJax.typeset(); // Render LaTeX after loading
        }
    });
}

function appendToTable(data) {
    let table = document.getElementById("csvTable");
    if (!table.innerHTML) {
        // Create headers
        let thead = "<thead><tr>";
        Object.keys(data[0]).forEach(header => {
            thead += `<th>${header}</th>`;
        });
        thead += "</tr></thead><tbody>";
        table.innerHTML = thead;
    }

    // Append rows dynamically
    let tbody = table.querySelector("tbody") || table;
    data.forEach(row => {
        let tr = "<tr>";
        Object.values(row).forEach(cell => {
            tr += `<td>\(${cell}\)</td>`; // Wrap LaTeX in \( ... \)
        });
        tr += "</tr>";
        tbody.innerHTML += tr;
    });
}

function openModelAttr(evt, AttrName, AttrUrl) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("modelTabContent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("modelTab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(AttrName).style.display = "block";
    evt.currentTarget.className += " active";

    Papa.parse(AttrUrl, {
        download: true,
        header: true,
        skipEmptyLines: true,
        complete: function(results) {
            const data = results.data;
            let tableHTML = "<thead><tr>";

            // Generate table headers
            Object.keys(data[0]).forEach(header => {
                tableHTML += `<th>${header}</th>`;
            });
            tableHTML += "</tr></thead><tbody>";

            // Generate table rows
            data.forEach(row => {
                tableHTML += "<tr>";
                Object.values(row).forEach(cell => {
                    if (cell.includes("https://")) {
                        var insert = `<a href="${cell}">here</a>`
                    } else {
                        var insert = cell
                    }
                    tableHTML += `<td>${insert}</td>`;
                });
                tableHTML += "</tr>";
            });
            tableHTML += "</tbody>";
            document.getElementById(`${AttrName}Table`).innerHTML = tableHTML;

            // Tell MathJax to re-render LaTeX
            MathJax.typeset();
        }
        });
}
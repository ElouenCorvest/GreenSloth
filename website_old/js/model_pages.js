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

document.getElementById('modelTitle').innerHTML = modelName
document.getElementById('github-link').setAttribute("href", `https://github.com/ElouenCorvest/GreenSloth/tree/main/models/${modelName}`)

function openModelAttr(evt, AttrName) {
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

    if (AttrName.includes("ODE")) {
        var infoVar = 'comps'
    } else if (AttrName.includes("Rates")) {
        var infoVar = 'rates'
    } else if (AttrName.includes("DerivedParams")) {
        var infoVar = 'derived_params'
    } else if (AttrName.includes("Params")) {
        var infoVar = 'params'
    } else if (AttrName.includes("DerivedComps")){
        var infoVar = 'derived_comps'
    }
    
    // Get CSV Tables
    Papa.parse(`https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${modelName}/model_info/${infoVar}.csv`, {
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

    // Get Equations

    (async() => {
        // Fetch README
        const md_file = await axios.get(`https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${modelName}/README.md`);

        // Get correct regex pattenr based on Attribute
        if (AttrName.includes("ODE")) {
            var regex_match = /#### Part of ODE system(.*)#### Conserved quantities/gms
        } else if (AttrName.includes("Rates")) {
            var regex_match = /### Reaction Rates(.*)<\/details>/gms
        } else if (AttrName.includes("DerivedParams")) {
            var regex_match = /#### Derived Parameters(.*)### Reaction Rates/gms
        } else if (AttrName.includes("Params")) {
            var regex_match = /### Parameters(.*)#### Derived Parameters/gms
        } else if (AttrName.includes("DerivedComps")){
            var regex_match = /#### Conserved quantities(.*)### Parameters/gms
        }
        var extraction = md_file.data.match(regex_match);
        console.log(extraction)
        var math_lines = extraction[0].match(/(?<=`math)[^`]*(?=\n```)/gms);
            if (math_lines !== null) {
                let mathHTML = "\\begin{align}";
                math_lines.forEach(row => {
                    var row_cleaned = row.match(/(?<=\n)[^`]*/gm)[0];
                    row_cleaned = row_cleaned.replace(/[^&]=/mg, " &=");
                    row_cleaned = row_cleaned.replace("\\begin{align}", "")
                    row_cleaned = row_cleaned.replace("\\end{align}", "")
                    mathHTML += row_cleaned
                    if (!row.endsWith('\\\\')) {
                        mathHTML += "\\\\"
                    }
                    // mathHTML += "[9pt]"
                });
                console.log(mathHTML)
                mathHTML += "\\end{align}";
                document.getElementById(`${AttrName}Math`).innerHTML = mathHTML;

                // Tell MathJax to re-render LaTeX
                MathJax.typeset();
            }
    })();
}

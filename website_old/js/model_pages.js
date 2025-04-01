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

function openModelAttr(evt, AttrName, AttrUrl, MdUrl) {
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

    // Get CSV Tables
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

    // Get Equations

    (async() => {
        console.log(MdUrl)
        const md_file = await axios.get(MdUrl);
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
        console.log(extraction[0].match(/(?<=\n)(.*)=(.*)(?=\n)/mg));
        var math_lines = extraction[0].match(/(?<=\n)(.*)=(.*)(?=\n)/mg);
            if (math_lines !== null) {
                let mathHTML = "\\begin{align}";
                math_lines.forEach(row => {
                    console.log(row.replace(/[^&]=/mg, " &="));
                    mathHTML += `${row.replace(/[^&]=/mg, " &=")}`;
                    if (!row.includes('\\\\')) {
                        mathHTML += "\\\\"
                    }
                    mathHTML += "[9pt]"
                });
                mathHTML += "\\end{align}";
                console.log(mathHTML)
                document.getElementById(`${AttrName}Math`).innerHTML = mathHTML;

                // Tell MathJax to re-render LaTeX
                MathJax.typeset();
            }
    })();
}

// (async() => {
//     const res = await axios.get("https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/Matuszynska2016/README.md")
//     console.log(res.data.match(/#### Part of ODE system(.*)#### Conserved quantities/gms))
//     })()
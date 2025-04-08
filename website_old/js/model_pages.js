// Get the Model Name
var modelName = location.href.split("/").slice(-1)[0].split(".")[0];

// Model Scheme
document.querySelectorAll(".thisScheme").forEach(item => {
    item.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${modelName}/${modelName}_scheme.svg`
});

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("compareModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// Create Compare Select
var modalSelect = document.getElementById("compareModel2")
fetch("/js/models.json")
    .then(response => response.json())
    .then(models => {
        models.forEach(model => {
            if (model.name == modelName) {
                return
            }
            const modelOption = document.createElement("option")
            modelOption.value = model.name
            modelOption.innerHTML = model.name
            modalSelect.appendChild(modelOption)
        });
    });

// Get model information
function parseModelInfo(modelName, InfoVar) {
    return new Promise((resolve, reject) => {
        Papa.parse(`https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${modelName}/model_info/${InfoVar}.csv`, {
            download: true,
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                resolve(results.data)
            },
            error: function(err) {
                reject(err);
            }
            
            });
    })
};

async function getModelInfo(modelName) {
    console.log(modelName)
    return {
        compsData: await parseModelInfo(modelName, 'comps'),
        paramsData: await parseModelInfo(modelName, 'params'),
        ratesData: await parseModelInfo(modelName, 'rates'),
        derivedCompsData: await parseModelInfo(modelName, 'derived_comps'),
        derivedParamsData: await parseModelInfo(modelName, 'derived_params'),
    }
};

// Put Info in Table
function createInfoTable(response) {
    const attrNames = ["ODE", "Params", "Rates", "DerivedComps", "DerivedParams"];
    var zip = attrNames.map(function(e, i) {return [e, Object.values(response)[i]]});

    for (let i = 0; i < zip.length; i++) {
        var attrName = zip[i][0]
        var data = zip[i][1]

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
        document.getElementById(`modelAttr${attrName}Table`).innerHTML = tableHTML;

        // Tell MathJax to re-render LaTeX
        MathJax.typeset();
    }
    
};

// Create Info List
function createInfoList(response, side) {
    const attrNames = ["ODE", "Params", "Rates", "DerivedComps", "DerivedParams"];
    var zip = attrNames.map(function(e, i) {return [e, Object.values(response)[i]]});

    for (let i = 0; i < zip.length; i++) {
        var attrName = zip[i][0]
        var data = zip[i][1]

        document.getElementById(`compareInformation${side}${attrName}`).innerText = data.length
    }
};

// Get this models Info and input into right places
getModelInfo(modelName)
    .then(response => {
        createInfoTable(response);
        createInfoList(response, "Left")
    });

// Modal Select change function
function modalChange() {
    var chosenModel = document.getElementById("compareModel2").value;
    
    if (chosenModel !== "") {
        const schemeRight = document.getElementById("compareSchemeRight")
        schemeRight.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${chosenModel}/${chosenModel}_scheme.svg`;

        getModelInfo(chosenModel)
            .then(response => {
                createInfoList(response, "Right")
            })

    }
};

// Modal compare Button Actions
function chooseCompareAttr(evt, AttrName) {
    const modalCompareLeft = document.getElementById("modalCompareLeft");
    const modalCompareRight = document.getElementById("modalCompareRight");
    
    // Hide all but selected compare Tab on left side
    const childrenLeft = modalCompareLeft.children;
    for (var i = 0; i < childrenLeft.length; i++) {
        var child = childrenLeft[i]
        child.classList.add("hidden")
        if (child.id.includes(AttrName)) {
            child.classList.remove("hidden")
        }
    };

    // Hide all but selected compare Tab on right side
    const childrenRight = modalCompareRight.children;
    for (var i = 0; i < childrenRight.length; i++) {
        var child = childrenRight[i]
        child.classList.add("hidden")
        if (child.id.includes(AttrName)) {
            child.classList.remove("hidden")
        }
    };
}

document.getElementById('modelTitle').innerHTML = modelName
document.getElementById('compareModel1').innerHTML = modelName
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
                mathHTML += "\\end{align}";
                document.getElementById(`${AttrName}Math`).innerHTML = mathHTML;

                // Tell MathJax to re-render LaTeX
                MathJax.typeset();
            }
    })();
}

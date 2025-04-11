// Important Variables
var modelName = location.href.split("/").slice(-1)[0].split(".")[0];
const InformationCats = {
    "ODEs": "ODE",
    "Derived Compounds": "DerivedComps",
    "Parameters": "Params",
    "Derived Parameters": "DerivedParams",
    "Rates": "Rates"
}

// Helper Functions

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
    const attrNames = Object.values(InformationCats);
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
    const attrNames = Object.values(InformationCats);
    var zip = attrNames.map(function(e, i) {return [e, Object.values(response)[i]]});

    for (let i = 0; i < zip.length; i++) {
        var attrName = zip[i][0]
        var data = zip[i][1]

        document.getElementById(`compareInformation${side}${attrName}`).innerText = data.length
    }
};

// Modal compare Button Actions
function chooseCompareAttr(AttrName) {
    
    // Hide all but selected compare Tab on left side
    const childrenLeft = compareModalBodyCompareLeft.children;
    for (var i = 0; i < childrenLeft.length; i++) {
        var child = childrenLeft[i]
        child.classList.add("hidden")
        if (child.id.includes(AttrName)) {
            child.classList.remove("hidden")
        }
    };

    // Hide all but selected compare Tab on right side
    const childrenRight = compareModalBodyCompareRight.children;
    for (var i = 0; i < childrenRight.length; i++) {
        var child = childrenRight[i]
        child.classList.add("hidden")
        if (child.id.includes(AttrName)) {
            child.classList.remove("hidden")
        }
    };
}

// Compare Modal Select Function
function modalChange() {
    const chosenModel = compareModalSelect.value;
    
    if (chosenModel !== "") {
        const schemeRight = document.getElementById("compareSchemesRight")
        schemeRight.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${chosenModel}/${chosenModel}_scheme.svg`;

        getModelInfo(chosenModel)
            .then(response => {
                createInfoList(response, "Right")
            })

    }
};

// Get Compare modal
var compareModal = document.getElementById("compareModal");

// Open Compare Modal
var openCompareModal = document.getElementById("compareModalButton")
openCompareModal.onclick = function() {
    compareModal.classList.toggle("hidden")
    this.classList.toggle("active")
}

// Create Compare Modal Content
var compareModalContent = document.createElement("div")
compareModalContent.classList.add("modalContent")
compareModalContent.id = "compareModalContent"
compareModal.appendChild(compareModalContent)

// Compare Modal Header
var compareModalHeader = document.createElement("div")
compareModalHeader.classList.add("modalHeader")
compareModalHeader.id = "compareModalHeader"
compareModalContent.appendChild(compareModalHeader)

// Compare Modal Heading
var compareModalHeading = document.createElement("h2")
compareModalHeading.innerText = "Compare"
compareModalHeader.appendChild(compareModalHeading)

// Compare Modal Heading This Model
var compareModalHeadingThisModel = document.createElement("h2")
compareModalHeadingThisModel.innerText = modelName
compareModalHeadingThisModel.id = "compareModalHeadingThisModel"
compareModalHeader.appendChild(compareModalHeadingThisModel)

// Compare Modal Heading Select Model
var compareModalSelect = document.createElement("select");
compareModalSelect.id = "compareModalSelect"
compareModalSelect.addEventListener('change', () => {
    modalChange();
});
compareModalHeader.appendChild(compareModalSelect);

// Compare Modal Heading Select Default Value
var compareModalSelectDefaultVal = document.createElement("option");
compareModalSelectDefaultVal.value = "";
compareModalSelectDefaultVal.innerHTML = "Select another model..."
compareModalSelect.appendChild(compareModalSelectDefaultVal)

// Compare Modal Heading Select Option Creator
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
            compareModalSelect.appendChild(modelOption)
        });
    });

// Modal Close Button
var compareClose = document.createElement("span")
compareClose.classList.add("close")
compareClose.innerHTML = "&times;"
compareClose.onclick = function(){
    compareModal.classList.toggle("hidden");
    openCompareModal.classList.toggle("active")
}
compareModalHeader.appendChild(compareClose)

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == compareModal) {
        compareModal.classList.toggle("hidden");
        openCompareModal.classList.toggle("active")
    }
  }

// Compare Modal Body
var compareModalBody = document.createElement("div")
compareModalBody.classList.add("modalBody")
compareModalBody.id = "compareModalBody"
compareModalContent.appendChild(compareModalBody)

// Compare Modal Body Tab Selection
var compareModalBodyTabs = document.createElement("div")
compareModalBodyTabs.classList.add("TabContainer")
compareModalBody.appendChild(compareModalBodyTabs)

// Compare Modal Body Tabs
const compareModalTabChoices = ["Information", "Schemes"]
compareModalTabChoices.forEach(choice => {
    var compareModalTab = document.createElement("button");
    compareModalTab.innerHTML = choice;
    compareModalTab.classList.add("clickable", "modelTab");
    compareModalTab.addEventListener('click', () => {
        chooseCompareAttr(choice);
    });
    compareModalBodyTabs.appendChild(compareModalTab)
})

// Compare Modal Body Compare
var compareModalBodyCompare = document.createElement("div")
compareModalBodyCompare.classList.add("compareModalBodyCompare")
compareModalBody.appendChild(compareModalBodyCompare)

// Compare Modal Body Compare Left
var compareModalBodyCompareLeft = document.createElement("div")
compareModalBodyCompareLeft.id = ("compareModalBodyCompareLeft")
compareModalBodyCompare.appendChild(compareModalBodyCompareLeft)

// Compare Modal Body Compare Right
var compareModalBodyCompareRight = document.createElement("div")
compareModalBodyCompareRight.id = ("compareModalBodyCompareRight")
compareModalBodyCompare.appendChild(compareModalBodyCompareRight)

// This Model Data
// Scheme
const sides = ["Left", "Right"]
sides.forEach(side => {
    var parentElement = document.getElementById(`compareModalBodyCompare${side}`)

    // Scheme
    var compareModalBodyCompareScheme = document.createElement("img")
    var tmpArray = ["modelScheme", "hidden"]
    if (side === "Left") {tmpArray.push("thisScheme")}
    compareModalBodyCompareScheme.classList.add(...tmpArray);compareModalBodyCompareScheme.id = `compareSchemes${side}`
    parentElement.appendChild(compareModalBodyCompareScheme)

    // Information
    var compareModalBodyCompareInformation = document.createElement("div")
    compareModalBodyCompareInformation.classList.add("hidden", "compareInformation")
    compareModalBodyCompareInformation.id = `compareInformation${side}`
    parentElement.appendChild(compareModalBodyCompareInformation)
    for (const [text, ids] of Object.entries(InformationCats)) {
        var catName = document.createElement("h4")
        catName.innerHTML = `Number of ${text}:`
        compareModalBodyCompareInformation.appendChild(catName)
        var catId = document.createElement("p")
        catId.id = `compareInformation${side}${ids}`
        compareModalBodyCompareInformation.appendChild(catId)
    }
})

function openModelAttr(evt, AttrName) {
    var i, tabcontent, tablinks;
    
    this.classList.toggle("active")

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

// Add at End
// Model Scheme
document.getElementById('modelTitle').innerHTML = modelName
document.getElementById('github-link').setAttribute("href", `https://github.com/ElouenCorvest/GreenSloth/tree/main/models/${modelName}`)
document.querySelectorAll(".thisScheme").forEach(item => {
    item.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${modelName}/${modelName}_scheme.svg`
});
// Get this models Info and input into right places
getModelInfo(modelName)
    .then(response => {
        createInfoTable(response);
        createInfoList(response, "Left")
    });

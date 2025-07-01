import Papa from "papaparse";
import { marked } from 'marked';
import modelData from "../js/models.json"

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

// Custom math block parser
const markedMathExtension = {
    extensions: [
      {
        name: 'math',
        level: 'inline',
        start(src) {
          return src.match(/\$/)?.index;
        },
        tokenizer(src) {
          const match = /^\$([^$]+)\$/.exec(src);
          if (match) {
            return {
              type: 'math',
              raw: match[0],
              text: match[1].trim(), // the inside of $$
              tokens: [],
            };
          }
        },
        renderer(token) {
          return `$${token.text}$`;
        }
      }
    ]
  };
  
marked.use(markedMathExtension);

// Insert Element into DOM with prior Comment
function insertCommentedElement(parent, ele, comm) {
    comm = document.createComment(comm)
    parent.appendChild(comm)
    parent.appendChild(ele)
}

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

// Get Github Last Update
async function updateLastModified(ele) {
    let res, lastUpdate;
    const url = `https://api.github.com/repos/ElouenCorvest/GreenSloth/commits?path=models/${modelName}`;
    
    try {
        const response = await fetch(url)
        const commits = await response.json();
        if (commits.length > 0) {
            const lastCommit = commits["0"]
            const date = new Date(lastCommit.commit.author.date)
            lastUpdate = new Intl.DateTimeFormat(
                undefined,
                {
                    "localeMatcher": "best fit",
                    "year": "numeric",
                    "month": "long",
                    "day": "numeric"
                }
            ).format(date)
            res = `Last Update: ${lastUpdate}`
        } else {
            res = "There exits no Updates"
        }
    } catch (error) {
        console.error('Error fetching commit info:', error);
        res = "Error loading Update Info"
    }

    ele.innerHTML = res
    }

// Get Github Last Update
async function updateDOI(ele) {
    const response = await fetch("../js/models.json");
    const modelsInfo = await response.json();
    for (let i=0; i < modelsInfo.length; i++) {
        if (modelsInfo[i].name === modelName) {
            ele.href = modelsInfo[i]["DOI"]
            ele.innerHTML = `DOI: ${modelsInfo[i]["DOI"]}`
        }
    }
}

// Clean Math String
function cleanMathStr(text) {
    var mathLines = text.match(/(?<=`math)[^`]*(?=\n```)/gms);
        if (mathLines !== null) {
            let mathHTML = "\\begin{align}";
            mathLines.forEach(row => {
                var row_cleaned = row.match(/(?<=\n)[^`]*/gm)[0];
                row_cleaned = row_cleaned.replace(/[^&]=/mg, " &=");
                row_cleaned = row_cleaned.replace("\\begin{align}", "")
                row_cleaned = row_cleaned.replace("\\end{align}", "")
                mathHTML += row_cleaned
                if (!row.endsWith('\\\\')) {
                    mathHTML += "\\\\"
                }
            });
            mathHTML += "\\end{align}";
            return mathHTML
        }
}

// Get Infromation from Model Markdown File
async function getMdFile() {
    const response = await fetch(`https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${modelName}/README.md`);
    const completeText = await response.text();
    
    const summaryRegex = new RegExp(`#\\s*${modelName}\\s*([\\s\\S]*?)\\s*##\\s*Installation`);
    var summarySection = completeText.match(summaryRegex)[1];
    summarySection = marked.parse(summarySection)

    const ODESection = completeText.match(/#### Part of ODE system(.*)#### Conserved quantities/gms)[0];
    const ODESectionMath = cleanMathStr(ODESection)

    const conservedQuantitySection = completeText.match(/#### Conserved quantities(.*)### Parameters/gms)[0];
    const conservedQuantitySectionMath = cleanMathStr(conservedQuantitySection)

    const parametersSection = completeText.match(/### Parameters(.*)#### Derived Parameters/gms)[0];

    const derivedParamsSection = completeText.match(/#### Derived Parameters(.*)### Reaction Rates/gms)[0];
    const derivedParamsSectionMath = cleanMathStr(derivedParamsSection)

    const ratesSection = completeText.match(/### Reaction Rates(.*)### Figures/gms)[0];
    const ratesSectionMath = cleanMathStr(ratesSection)

    const figuresSection = completeText.match(/### Figures(.*)/gms)[0];
    const figuresDetailsRegex = /<details>\s*<summary>(.*?)<\/summary>\s*([\s\S]*?)<\/details>/g;

    let matches;
    const figures = [];

    while ((matches = figuresDetailsRegex.exec(figuresSection)) !== null) {
        const title = matches[1].trim();  // Title inside <summary>...</summary>
        const content = matches[2];        // Inside the <details> block

        // Extract the <img> src
        const imgMatch = content.match(/<img[^>]+src=['"]([^'"]+)['"]/);
        const imgSrc = imgMatch ? imgMatch[1] : null;

        // Remove the <img> tag from the content to get the text only
        const text = marked.parse(content.replace(/<img[^>]*>/g, '').trim());

        figures.push({ title, imgSrc, text });
    }

    return {
        summarySection: summarySection,
        ODE: {
            text: ODESection,
            math: ODESectionMath
        },
        DerivedComps: {
            text: conservedQuantitySection,
            math: conservedQuantitySectionMath
        },
        Params: parametersSection,
        DerivedParams: {
            text: derivedParamsSection,
            math: derivedParamsSectionMath
        },
        Rates: {
            text: ratesSection,
            math: ratesSectionMath
        },
        figures: figures
    }

}

///////////////////////////////////////////////////////
// Content Pipeline
///////////////////////////////////////////////////////
var contentElement = document.getElementById("content")

///////////////////////////////////////////////////////
// Compare Modal
///////////////////////////////////////////////////////
// Insert Compare Modal
var compareModal = document.createElement("div")
compareModal.id = "compareModal"
compareModal.classList.add("modal", "hidden")
insertCommentedElement(contentElement, compareModal, "The Compare Modal")

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
fetch("../js/models.json")
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
    modelSummaryBlockBarCompare.classList.toggle("active")
}
compareModalHeader.appendChild(compareClose)

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == compareModal) {
        compareModal.classList.toggle("hidden");
        modelSummaryBlockBarCompare.classList.toggle("active")
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

///////////////////////////////////////////////////////
// Model Summary Block
///////////////////////////////////////////////////////
// Insert Model Summary Block
var modelSummaryBlock = document.createElement("div")
modelSummaryBlock.id = "modelSummaryBlock"
insertCommentedElement(contentElement, modelSummaryBlock, "The Model Summary")

// Insert Model Scheme
var modelSummaryBlockScheme = document.createElement("img")
modelSummaryBlockScheme.classList.add("modelScheme", "thisScheme")
modelSummaryBlock.appendChild(modelSummaryBlockScheme)

// Insert Model Head
var modelSummaryBlockHead = document.createElement("div")
modelSummaryBlockHead.id = "modelBlockHead"
modelSummaryBlock.appendChild(modelSummaryBlockHead)

// Insert Model Head Title
var modelSummaryBlockHeadTitle = document.createElement("h1")
modelSummaryBlockHeadTitle.classList.add("modelText")
modelSummaryBlockHeadTitle.innerHTML = modelName
modelSummaryBlockHead.appendChild(modelSummaryBlockHeadTitle)

// Insert Model Head DOI
var modelSummaryBlockHeadDOI = document.createElement("a")
modelSummaryBlockHeadDOI.classList.add("discreetText")
modelSummaryBlockHeadDOI.target = "_blank"
modelSummaryBlockHeadDOI.href = modelData[modelName]["DOI"]
modelSummaryBlockHeadDOI.innerHTML = `DOI: ${modelData[modelName]["DOI"]}`
modelSummaryBlockHead.appendChild(modelSummaryBlockHeadDOI)

// Insert Tab Container
var modelSummaryBlockBar = document.createElement("div")
modelSummaryBlockBar.classList.add("TabContainer")
modelSummaryBlockBar.id = "modelButtonBar"
insertCommentedElement(modelSummaryBlock, modelSummaryBlockBar, "The Model Summary Buttons")

// Insert Model Button Bar Github Button
var modelSummaryBlockBarGithub = document.createElement("a")
modelSummaryBlockBarGithub.target = "_blank"
modelSummaryBlockBarGithub.href = `https://github.com/ElouenCorvest/GreenSloth/tree/main/models/${modelName}`
modelSummaryBlockBarGithub.style = "display: flex; text-decoration: none; align-items: last baseline; justify-content: center;"
modelSummaryBlockBar.prepend(modelSummaryBlockBarGithub)

// Insert Model Button Bar Github Button Logo With Text
var modelSummaryBlockBarGithubLogoText = document.createElement("div")
modelSummaryBlockBarGithubLogoText.classList.add("logoWithText")
modelSummaryBlockBarGithubLogoText.innerHTML = "Github"
modelSummaryBlockBarGithubLogoText.style = "flex-grow: 1"
modelSummaryBlockBarGithub.appendChild(modelSummaryBlockBarGithubLogoText)

// Insert Model Button Bar Github Button Logo
var githubLogo = document.createElement("span")
githubLogo.classList.add("githubLogo")
modelSummaryBlockBarGithubLogoText.prepend(githubLogo)

// Insert Model Button Bar Compare Button
var modelSummaryBlockBarCompare = document.createElement("button")
modelSummaryBlockBarCompare.onclick = function() {
    compareModal.classList.toggle("hidden")
    this.classList.toggle("active")
}
modelSummaryBlockBarCompare.append("Compare")
modelSummaryBlockBar.appendChild(modelSummaryBlockBarCompare)

// Insert Model Button Bar Last Updated
var modelSummaryBlockBarLastUpdate = document.createElement("p")
modelSummaryBlockBarLastUpdate.classList.add("discreetText")
modelSummaryBlockBarLastUpdate.innerHTML = "Last Update: Loading..."
modelSummaryBlockBarLastUpdate.style = "flex-grow: 1; margin: 0; font-size: 0.7em; text-align: center;"
updateLastModified(modelSummaryBlockBarLastUpdate)
modelSummaryBlockBarGithub.appendChild(modelSummaryBlockBarLastUpdate)

// Insert Model Summary
var modelSummaryBlockText = document.createElement("div")
modelSummaryBlockText.classList.add("modelText")
modelSummaryBlock.appendChild(modelSummaryBlockText)

// Insert Model Summary Title
var modelSummaryBlockTextTitle = document.createElement("h3")
modelSummaryBlockTextTitle.innerHTML = "Summary"
modelSummaryBlockText.appendChild(modelSummaryBlockTextTitle)

// Insert Model Summary Text
var modelSummaryBlockTextText = document.createElement("p")
modelSummaryBlockText.appendChild(modelSummaryBlockTextText)

///////////////////////////////////////////////////////
// Tab Container for Model Information
///////////////////////////////////////////////////////
// Insert Tab Container
var tabContainer = document.createElement("div")
tabContainer.classList.add("TabContainer")
insertCommentedElement(contentElement, tabContainer, "The Information Tabs")

// Tab Container Buttons
const tabContainerButtons = {
    ODE: "ODE System",
    DerivedComps: "Derived Quantities",
    Params: "Parameters",
    DerivedParams: "Derived Parameters",
    Rates: "Rates",
    Figures: "Figures"
}

for (const [key, value] of Object.entries(tabContainerButtons)) {
    var tabContainerButton = document.createElement("button")
    tabContainerButton.addEventListener("click", function() {
        openModelAttr(this, `modelAttr${key}`);
    });
    tabContainerButton.innerHTML = value
    tabContainer.appendChild(tabContainerButton)
}

function openModelAttr(button, AttrName) {
    const allButtons = button.parentElement.children
    const allInfo = document.querySelectorAll(".modelTabContent")

    if (button.classList.contains("active")) {
        button.classList.toggle("active")
        const modelInfo = document.getElementById(AttrName)
        modelInfo.classList.toggle("hidden")
    } else {
        for (let i = 0; i < allButtons.length; i++) {
            if (allButtons[i] === button) {
                allButtons[i].classList.add("active")
            } else {
                allButtons[i].classList.remove("active")
            }
        }
    
        for (let i = 0; i < allInfo.length; i++) {
            if (allInfo[i].id === AttrName) {
                allInfo[i].classList.remove("hidden")
            } else {
                allInfo[i].classList.add("hidden")
            }
        }
    }

}

///////////////////////////////////////////////////////
// Model Information
///////////////////////////////////////////////////////
// All Model Info
for (const [key, value] of Object.entries(tabContainerButtons)) {
    var modelAttrContent = document.createElement("div")
    modelAttrContent.id = `modelAttr${key}`;
    modelAttrContent.classList.add("modelTabContent", "hidden")
    insertCommentedElement(contentElement, modelAttrContent, `Model Info ${value}`)

    if (key != "Figures") {
        var modelAttrContentTable = document.createElement("table")
        modelAttrContentTable.id = `modelAttr${key}Table`
        modelAttrContent.appendChild(modelAttrContentTable)
        var modelAttrContentMath = document.createElement("div")
        modelAttrContentMath.id = `modelAttr${key}Math`
        modelAttrContentMath.classList.add("modelAttrMath")
        modelAttrContent.appendChild(modelAttrContentMath)
    }

    
}

// Add at End
// Model Scheme
document.querySelectorAll(".thisScheme").forEach(item => {
    item.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${modelName}/${modelName}_scheme.svg`
});
// Get this models Info and input into right places
getModelInfo(modelName)
    .then(response => {
        createInfoTable(response);
        createInfoList(response, "Left")
    });

getMdFile().then(response => {
    // Insert Summary
    modelSummaryBlockTextText.innerHTML = response.summarySection

    // Insert Math
    const allMath = document.querySelectorAll(".modelAttrMath")
    for (let i = 0; i < allMath.length; i++) {
        var changeFlag = allMath[i].id.match(/(?<=modelAttr)(.*)(?=Math)/)[0];
        var mathHTML = response[changeFlag]["math"]
        if (mathHTML != null) {
            allMath[i].innerHTML = mathHTML
        }
    }

    // Insert Figures
    const modelAttrFigures = document.getElementById("modelAttrFigures")
    var arrowDown = document.createElement("span")
    arrowDown.classList.add("arrowDown")

    for (let i = 0; i < response.figures.length; i++) {
        var figureInfo = response.figures[i]
        var figureImgSrc = figureInfo.imgSrc
        var figureTitle = figureInfo.title
        var figureText = figureInfo.text

        var modelAttrFiguresContainer = document.createElement("div")
        modelAttrFiguresContainer.classList.add("modelAttrFiguresContainer")
        modelAttrFigures.appendChild(modelAttrFiguresContainer)

        var modelAttrFiguresContainerHead = document.createElement("button")
        modelAttrFiguresContainerHead.classList.add("modelAttrFiguresContainerHead", "clickable")
        modelAttrFiguresContainerHead.addEventListener("click", function() {
            var siblings = this.parentNode.childNodes
            for (let i = 0; i < siblings.length; i++) {
                if (siblings[i] == this) {
                    this.classList.toggle("active")
                } else {
                    siblings[i].classList.toggle("hidden")
                }
            }
        });
        modelAttrFiguresContainer.appendChild(modelAttrFiguresContainerHead)

        var arrowDown1 = document.createElement("span")
        arrowDown1.classList.add("arrowDown")
        modelAttrFiguresContainerHead.appendChild(arrowDown1)

        var modelAttrFiguresContainerHeadTitle = document.createElement("h3")
        modelAttrFiguresContainerHeadTitle.innerHTML = figureTitle
        modelAttrFiguresContainerHead.appendChild(modelAttrFiguresContainerHeadTitle)

        var arrowDown2 = document.createElement("span")
        arrowDown2.classList.add("arrowDown")
        modelAttrFiguresContainerHead.appendChild(arrowDown2)

        var modelAttrFiguresContainerContent = document.createElement("div")
        modelAttrFiguresContainerContent.classList.add("modelAttrFiguresContainerContent", "hidden")
        modelAttrFiguresContainer.appendChild(modelAttrFiguresContainerContent)

        var modelAttrFiguresContainerContentImg = document.createElement("img")
        modelAttrFiguresContainerContentImg.classList.add()
        modelAttrFiguresContainerContentImg.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${modelName}/${figureImgSrc}`
        modelAttrFiguresContainerContent.appendChild(modelAttrFiguresContainerContentImg)

        modelAttrFiguresContainerContent.innerHTML += figureText

    }

})
import { marked } from 'marked';
import modelData from "../js/models.json"
import { appendCommentedElement, prependCommentedElement, getModelInfo, createInfoTable, getMdFile, createFigures } from "./utils.js";

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
            res = "There exists no Updates"
        }
    } catch (error) {
        console.error('Error fetching commit info:', error);
        res = "Error loading Update Info"
    }

    ele.innerHTML = res
    }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Content Pipeline
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
const bodyElement = document.body



//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Image Modal
//////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Insert Image Modal
var imageModal = document.createElement("div")
imageModal.id = "image-modal"
imageModal.classList.add("modal", "hidden")
prependCommentedElement(bodyElement, imageModal, "The Image Modal")

// Insert Image Modal Close
var imageModalClose = document.createElement("span")
imageModalClose.classList.add("close")
imageModalClose.innerHTML = "&times;"
imageModalClose.onclick = function(){
    imageModal.classList.toggle("hidden");
}
imageModal.appendChild(imageModalClose)

// Insert Image Modal Image
var imageModalImg = document.createElement("img")
imageModal.appendChild(imageModalImg)

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == imageModal) {
        imageModal.classList.toggle("hidden");
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Insert Content
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
const layoutWrapper = document.createElement("div")
layoutWrapper.id = "layoutWrapper"
prependCommentedElement(bodyElement, layoutWrapper, "The Layout Wrapper")

const topnav = document.createElement("div")
topnav.id = "topnav"
appendCommentedElement(layoutWrapper, topnav, "The TopNav")

const wrapper = document.createElement("div")
wrapper.id = "wrapper-model"
appendCommentedElement(layoutWrapper, wrapper, "The Wrapper")

const sideBarElement = document.createElement("nav")
sideBarElement.id = "model-sidebar"
sideBarElement.classList.add("sidebar")
appendCommentedElement(wrapper, sideBarElement, "The Sidebar")

const contentElement = document.createElement("div")
contentElement.id = "model-content"
appendCommentedElement(wrapper, contentElement, "The Content")

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Sidebar
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
const sideBarName = document.createElement("h2")
// sideBarName.classList.add("modelText")
sideBarName.innerHTML = modelName
sideBarElement.appendChild(sideBarName)

const sideBarTitle = document.createElement("h3")
// sideBarTitle.classList.add("modelText")
sideBarTitle.innerHTML = "Contents"
sideBarElement.appendChild(sideBarTitle)

const sideBarList = document.createElement("ul")
sideBarElement.appendChild(sideBarList)

// Back to Top
var sideBarListItem = document.createElement("li")
var listItemLink = document.createElement("a")
listItemLink.innerHTML = "Back to Top"
listItemLink.href = "#model-header"
listItemLink.addEventListener("click", function() {
    const allSideBarLinks = document.querySelectorAll("#model-sidebar a")
    for (const item of allSideBarLinks) {
        if (item === this) {
            item.classList.add("active")
        } else {
            item.classList.remove("active")
        }
    }
})
sideBarListItem.appendChild(listItemLink)
sideBarList.appendChild(sideBarListItem)

// Compare
var sideBarListItem = document.createElement("li")
var listItemLink = document.createElement("a")
listItemLink.innerHTML = "Compare"
listItemLink.href = "../Compare.html?select=" + modelName
sideBarListItem.appendChild(listItemLink)
sideBarList.appendChild(sideBarListItem)

// Summary
var sideBarListItem = document.createElement("li")
var listItemLink = document.createElement("a")
listItemLink.innerHTML = "Summary"
listItemLink.href = `#modelAttrSummary`
listItemLink.addEventListener("click", function() {
    const allSideBarLinks = document.querySelectorAll("#model-sidebar a")
    for (const item of allSideBarLinks) {
        if (item === this) {
            item.classList.add("active")
        } else {
            item.classList.remove("active")
        }
    }
})
sideBarListItem.appendChild(listItemLink)
sideBarList.appendChild(sideBarListItem)

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Content
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // Header
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Create Model Header
var modelHeader = document.createElement("div")
modelHeader.id = "model-header"
appendCommentedElement(contentElement, modelHeader, "Model Header")

// Insert Model Title
var modelHeaderTitle = document.createElement("h1")
modelHeaderTitle.classList.add("modelText")
modelHeaderTitle.innerHTML = modelName
modelHeader.appendChild(modelHeaderTitle)

// Insert Model DOI
var modelHeaderDOI = document.createElement("a")
modelHeaderDOI.classList.add("discreetText", "grid-right")
modelHeaderDOI.target = "_blank"
modelHeaderDOI.href = modelData[modelName]["DOI"]
modelHeaderDOI.innerHTML = `DOI: ${modelData[modelName]["DOI"]}`
modelHeader.appendChild(modelHeaderDOI)

// Insert Model Button Bar
var modelHeaderButtonBar = document.createElement("div")
modelHeaderButtonBar.classList.add("TabContainer")
modelHeaderButtonBar.id = "model-button-bar"
appendCommentedElement(modelHeader, modelHeaderButtonBar, "The Model Summary Buttons")

// Insert Model Button Bar Github Button
var modelHeaderButtonBarGithub = document.createElement("a")
modelHeaderButtonBarGithub.target = "_blank"
modelHeaderButtonBarGithub.href = `https://github.com/ElouenCorvest/GreenSloth/tree/main/models/${modelName}`
modelHeaderButtonBar.prepend(modelHeaderButtonBarGithub)

// Insert Model Button Bar Github Button Logo With Text
var modelHeaderButtonBarGithubLogoText = document.createElement("div")
modelHeaderButtonBarGithubLogoText.classList.add("logoWithText")
modelHeaderButtonBarGithubLogoText.innerHTML = "Github"
modelHeaderButtonBarGithubLogoText.style = "flex-grow: 1"
modelHeaderButtonBarGithub.appendChild(modelHeaderButtonBarGithubLogoText)

// Insert Model Button Bar Github Button Logo
var githubLogo = document.createElement("span")
githubLogo.classList.add("githubLogo")
modelHeaderButtonBarGithubLogoText.prepend(githubLogo)

// Insert Model Button Bar Compare Button
var modelHeaderButtonBarCompare = document.createElement("a")
modelHeaderButtonBarCompare.href = "../Compare.html?select=" + modelName
modelHeaderButtonBarCompare.append("Compare")
modelHeaderButtonBar.appendChild(modelHeaderButtonBarCompare)

// Insert Model Button Bar Last Updated
var modelHeaderButtonBarLastUpdate = document.createElement("p")
modelHeaderButtonBarLastUpdate.innerHTML = "Last Update: Loading..."
modelHeaderButtonBarLastUpdate.style = "flex-grow: 1; margin: 0; font-size: 0.7em; text-align: center;"
updateLastModified(modelHeaderButtonBarLastUpdate)
modelHeaderButtonBarGithub.appendChild(modelHeaderButtonBarLastUpdate)

    ///////////////////////////////////////////////////////
    // Model Summary Block
    ///////////////////////////////////////////////////////

// Insert Model Summary Block
var modelSummaryBlock = document.createElement("section")
modelSummaryBlock.id = "modelAttrSummary"
modelSummaryBlock.classList.add("modelTabContent")
appendCommentedElement(contentElement, modelSummaryBlock, "The Model Summary")

// Insert Model Scheme Block
var modelSummaryBlockSchemeBlock = document.createElement("div")
modelSummaryBlockSchemeBlock.classList.add("model-scheme-container")
modelSummaryBlockSchemeBlock.addEventListener("click", function() {
    this.childNodes.forEach(element => {
        if (element.nodeName === "IMG") {
            imageModalImg.src = element.src
        }
    })
    imageModal.classList.toggle("hidden")
})
modelSummaryBlock.appendChild(modelSummaryBlockSchemeBlock)

// Insert Model Scheme
var modelSummaryBlockScheme = document.createElement("img")
modelSummaryBlockScheme.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${modelName}/${modelName}_scheme.svg`
modelSummaryBlockScheme.classList.add("model-scheme")
modelSummaryBlockSchemeBlock.appendChild(modelSummaryBlockScheme)

// Insert Model Summary
var modelSummaryBlockText = document.createElement("div")
modelSummaryBlockText.classList.add("model-text")
modelSummaryBlock.appendChild(modelSummaryBlockText)

// Insert Model Summary Title
var modelSummaryBlockTextTitle = document.createElement("h3")
modelSummaryBlockTextTitle.innerHTML = "Summary"
modelSummaryBlockText.appendChild(modelSummaryBlockTextTitle)

// Insert Model Summary Text
var modelSummaryBlockTextText = document.createElement("p")
modelSummaryBlockText.appendChild(modelSummaryBlockTextText)

// Insert model categories
const modelInfoCats = {
    ODE: "ODE System",
    DerivedComps: "Derived Quantities",
    Params: "Parameters",
    DerivedParams: "Derived Parameters",
    Rates: "Rates",
    Figures: "Figures",
    Demonstrations: "Demonstrations"
}

for (const [key, value] of Object.entries(modelInfoCats)) {
    var modelAttrSection = document.createElement("section")
    modelAttrSection.classList.add("modelTabContent")
    modelAttrSection.id = `modelAttr${key}`
    appendCommentedElement(contentElement, modelAttrSection, `Model ${key}`)

    var modelAttrTitle = document.createElement("h2")
    modelAttrTitle.innerHTML = value
    modelAttrSection.appendChild(modelAttrTitle)

    //  Sidebar
    var listItem = document.createElement("li")
    var listItemLink = document.createElement("a")
    listItemLink.innerHTML = value
    listItemLink.href = `#modelAttr${key}`
    listItemLink.addEventListener("click", function() {
        const allSideBarLinks = document.querySelectorAll("#model-sidebar a")
        for (const item of allSideBarLinks) {
            if (item === this) {
                item.classList.add("active")
            } else {
                item.classList.remove("active")
            }
        }
    })
    listItem.appendChild(listItemLink)
    sideBarList.appendChild(listItem)

    if (key != "Figures" && key != "Demonstrations") {
        var modelAttrTableDiv = document.createElement("div")
        modelAttrTableDiv.classList.add("model-attr-table-div")
        modelAttrSection.appendChild(modelAttrTableDiv)

        var modelAttrTable = document.createElement("table")
        modelAttrTable.id = `modelAttr${key}Table`
        modelAttrTableDiv.appendChild(modelAttrTable)

        var modelAttrMath = document.createElement("div")
        modelAttrMath.id = `modelAttr${key}Math`
        modelAttrMath.classList.add("modelAttrMath")
        modelAttrSection.appendChild(modelAttrMath)
    }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// End
//////////////////////////////////////////////////////////////////////////////////////////////////////////////

getModelInfo(modelName)
    .then(response => {
        createInfoTable(response);
        // createInfoList(response, "left", informationPointer);
    })

getMdFile(modelName).then(response => {
    // Insert Summary
    modelSummaryBlockTextText.innerHTML = response.summarySection

    // Insert Math
    const allMath = document.querySelectorAll(".modelAttrMath")
    for (let i = 0; i < allMath.length; i++) {
        var changeFlag = allMath[i].id.match(/(?<=modelAttr)(.*)(?=Math)/)[0];
        try {
            var mathHTML = response[changeFlag]["math"]
            if (mathHTML != null) {
                allMath[i].innerHTML = mathHTML
            }
        } catch {
            continue
        }
    }

    // Insert Figures
    const modelAttrFigures = document.getElementById("modelAttrFigures")
    modelAttrFigures.classList.add("model-attr-figures")
    createFigures(response.figures, modelName, modelAttrFigures)

    // Insert Demonstrations
    const modelAttrDemonstrations = document.getElementById("modelAttrDemonstrations")
    modelAttrDemonstrations.classList.add("model-attr-figures")
    createFigures(response.demonstrations, modelName, modelAttrDemonstrations)
    
})

// At the very End
import('./topnav.js');

// import('./cite.js');

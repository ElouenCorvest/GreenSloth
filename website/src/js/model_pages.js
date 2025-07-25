import Papa from "papaparse";
import { marked } from 'marked';
import modelData from "../js/models.json"
import vennDiagramm from "../img/venn_diagramm.svg?raw"
import Swiper from 'swiper';
import { Navigation, Thumbs } from 'swiper/modules';
import chroma from "chroma-js"
import Plotly from 'plotly.js-dist'

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

// Append Element into DOM with prior Comment
function appendCommentedElement(parent, ele, comm) {
    comm = document.createComment(comm)
    parent.appendChild(comm)
    parent.appendChild(ele)
}

// Append Element into DOM with prior Comment
function prependCommentedElement(parent, ele, comm) {
    comm = document.createComment(comm)
    parent.prepend(comm)
    parent.prepend(ele)
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
    const pointObject = {
        "compsData": "ODE",
        "paramsData": "Params",
        "ratesData": "Rates",
        "derivedCompsData": "DerivedComps",
        "derivedParamsData": "DerivedParams"
    }

    for (const [key, value] of Object.entries(response)) {
        var data = value

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
        document.getElementById(`modelAttr${pointObject[key]}Table`).innerHTML = tableHTML;

        // Tell MathJax to re-render LaTeX
        MathJax.typeset();
    }
};

// Create Info List
function createInfoList(response, side, informationPointer) {
    for (const [key, value] of Object.entries(informationPointer)) {
        var valueElement = document.getElementById(`compare-information-${side}-${value.toLowerCase()}`)
        if (response != "") {
            valueElement.innerText = response[value].length
        } else {
            valueElement.innerText = ""
        }
    }
};

function filterGlossIDAbbr(gloss) {
    var filteredGloss = {}
        gloss.forEach(row => {
            filteredGloss[row["Glossary ID"]] = row["Common Abbr."]
        })

    return filteredGloss
}

function filterGlossIDPythonVar(gloss) {
    var filteredGloss = {}
        gloss.forEach(row => {
            filteredGloss[row["Glossary ID"]] = row["Python Var"]
        })

    return filteredGloss
}

// Get Main Glossary
async function getMainGlossary() {
    return new Promise((resolve, reject) => {
        Papa.parse(`https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/comps_glossary.csv`, {
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
}

// Get Both Model Info
async function getBothModelInfo(modelName, otherModelName) {
    const res = await Promise.all([
        getModelInfo(modelName),
        getModelInfo(otherModelName),
        getMainGlossary()
    ])

    return res
}

// Get Sim
function getSim(path) {
    return new Promise((resolve, reject) => {
        fetch(path).then(response => {
            resolve(response.json())
        })
    }

    )
}


// Get Both Sims
async function getBothSims(thisModel, otherModel, pfd) {
    const res = await Promise.all([
        getSim(`/simulations/${thisModel}/${pfd}.json`),
        getSim(`/simulations/${otherModel}/${pfd}.json`)
    ])

    return res
}

// Get Simulation result
// async function getSimRes(modelName, pfd) {
//     const res = await Promise.all(
//         import modelData from "../js/models.json"
//     )
// }

// Compare Modal Select Function
function modalChange(informationPointer) {
    const chosenModel = compareModalSelect.value;

    // Get Left Variable Math
    const leftVariables = document.getElementById("compare-variables-left")
    leftVariables.innerHTML = ""

    // Get Right Variable Math
    const rightVariables = document.getElementById("compare-variables-right")
    rightVariables.innerHTML = ""

    // Get Common Variables
    const commonVariables = document.getElementById("compare-variables-common-math")
    commonVariables.innerHTML = ""

    const commonVariablesText = document.getElementById("compare-variables-common-text")

    // Get Simulation Select
    const simSelectBox = document.getElementById("compare-simulation-select")
    const simSelectTab = document.getElementById("compare-tab-simulation")

    // Get Compare Select
    const compareSelect = document.getElementById("compare-tab-select")

    const schemeRight = document.getElementById("compare-schemes-right")

    if (chosenModel !== "") {
        schemeRight.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${chosenModel}/${chosenModel}_scheme.svg`;

        const bothInfo = getBothModelInfo(modelName, chosenModel)
        bothInfo.then(res => {
            const thisModelInfo = res[0]
            const otherModelInfo = res[1]
            const mainGloss = res[2]

            createInfoList(otherModelInfo, "right", informationPointer)

            var combinedVars = []
            for (let info of [thisModelInfo, otherModelInfo]){
                var filteredGlossComps = filterGlossIDAbbr(info["compsData"])
                var filteredGlossDerivedComps = filterGlossIDAbbr(info["derivedCompsData"])
                combinedVars.push({...filteredGlossComps, ...filteredGlossDerivedComps})
            }

            const thisModelVars = combinedVars[0]
            const thisModelVarsKeys = Object.keys(thisModelVars)
            const otherModelVars = combinedVars[1]
            const otherModelVarsKeys = Object.keys(otherModelVars)

            const mainGlossPointerAbbr = filterGlossIDAbbr(mainGloss)
            const mainGlossPointerPythonVar = filterGlossIDPythonVar(mainGloss)
            
            const commonVars = thisModelVarsKeys.filter(value => otherModelVarsKeys.includes(value))

            const thisModelVarsUnique = thisModelVarsKeys.filter(value => !commonVars.includes(value))
            const otherModelVarsUnique = otherModelVarsKeys.filter(value => !commonVars.includes(value))

            thisModelVarsUnique.forEach(ele => {
                var newP = document.createElement("p")
                newP.innerText = mainGlossPointerAbbr[ele]
                leftVariables.appendChild(newP)
            })
            
            otherModelVarsUnique.forEach(ele => {
                var newP = document.createElement("p")
                newP.innerText = mainGlossPointerAbbr[ele]
                rightVariables.appendChild(newP)
            })

            simSelectBox.innerHTML = ""
            var defaultVal = document.createElement("option");
            defaultVal.value = "";
            defaultVal.innerHTML = "Select Variable"
            simSelectBox.appendChild(defaultVal)
            varCompare()

            commonVars.forEach(ele => {

                var varOption = document.createElement("option")
                varOption.value = mainGlossPointerPythonVar[ele]
                varOption.innerHTML = mainGlossPointerPythonVar[ele]
                simSelectBox.appendChild(varOption)

                var newP = document.createElement("p")
                newP.innerText = mainGlossPointerAbbr[ele]
                newP.addEventListener("click", function() {
                    simSelectBox.value = mainGlossPointerPythonVar[ele]
                    compareSelect.value = "Simulation"
                    changeCompareTabs(simSelectTab)
                })
                commonVariables.appendChild(newP)
            })

            MathJax.typeset()

            if (commonVars.length > 0) {
                commonVariablesText.innerText = "Click the Variable to see the simulation!"
            }
        })

    } else {
        schemeRight.src = ""

        const thisModelInfo = getModelInfo(modelName)
        thisModelInfo.then(res => {

            createInfoList("", "right", informationPointer)

            const filteredGlossCompsAbbr = filterGlossIDAbbr(res["compsData"])
            const filteredGlossDerivedCompsAbbr = filterGlossIDAbbr(res["derivedCompsData"])
            const filteredGlossCombinedAbbr = {...filteredGlossCompsAbbr, ...filteredGlossDerivedCompsAbbr}
            var leftVariables = document.getElementById("compare-variables-left")
            for (const [key, value] of Object.entries(filteredGlossCombinedAbbr)) {
                var newP = document.createElement("p")
                newP.innerText = value
                leftVariables.appendChild(newP)
            }

            const filteredGlossCompsPythonVar = filterGlossIDPythonVar(res["compsData"])
            const filteredGlossDerivedCompsPythonVar = filterGlossIDPythonVar(res["derivedCompsData"])
            const filteredGlossCombined = {...filteredGlossCompsPythonVar, ...filteredGlossDerivedCompsPythonVar}
            // Compare Modal Heading Select Option Creator
            const availableVars = Object.values(filteredGlossCombined)
            availableVars.forEach(element => {
                var varOption = document.createElement("option")
                varOption.value = element
                varOption.innerHTML = element
                simSelectBox.appendChild(varOption)
            })

            MathJax.typeset()
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
            res = "There exists no Updates"
        }
    } catch (error) {
        console.error('Error fetching commit info:', error);
        res = "Error loading Update Info"
    }

    ele.innerHTML = res
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

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Content Pipeline
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
const bodyElement = document.body

const citeModal = document.createElement("div")
citeModal.id = "citeModal"
citeModal.classList.add("modal", "hidden")
prependCommentedElement(bodyElement, citeModal, "The Cite Modal")

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Compare Modal
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Insert Compare Modal
var compareModal = document.createElement("div")
compareModal.id = "compareModal"
compareModal.classList.add("modal", "hidden")
prependCommentedElement(bodyElement, compareModal, "The Compare Modal")

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
    modalChange(informationPointer);
});
compareModalHeader.appendChild(compareModalSelect);

// Compare Modal Heading Select Default Value
var compareModalSelectDefaultVal = document.createElement("option");
compareModalSelectDefaultVal.value = "";
compareModalSelectDefaultVal.innerHTML = "Select another model..."
compareModalSelect.appendChild(compareModalSelectDefaultVal)

// Compare Modal Heading Select Option Creator
const availableModels = Object.keys(modelData)
availableModels.forEach(element => {
    if (element != modelName) {
        const modelOption = document.createElement("option")
        modelOption.value = element
        modelOption.innerHTML = element
        compareModalSelect.appendChild(modelOption)
    }
})

// Modal Close Button
var compareClose = document.createElement("span")
compareClose.classList.add("close")
compareClose.innerHTML = "&times;"
compareClose.onclick = function(){
    compareModal.classList.toggle("hidden");
    modelHeaderButtonBarCompare.classList.toggle("active")
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
compareModalBodyTabs.id = "compare-tab-container"
compareModalBodyTabs.classList.add("TabContainer")
compareModalBody.appendChild(compareModalBodyTabs)

// Change Active Body
function changeCompareBody(changeTo) {
    const allCompareBlocks = document.querySelectorAll(".compare-body")
    allCompareBlocks.forEach(block => {
        block.classList.add("hidden")
        if (block.id.includes(changeTo.toLowerCase())) {
            block.classList.remove("hidden")
        }
    })
    if (changeTo.toLowerCase() == "simulation") {
        varCompare()
    }
}

// Change Compare Func
function changeCompareTabs(tabClicked) {
    var siblings = tabClicked.parentNode.childNodes
    siblings.forEach(element => {
        element.classList.remove("active")
    })
    tabClicked.classList.add("active")

    changeCompareBody(tabClicked.innerHTML)
}

// Compare Modal Select Box
const compareModalTabSelect = document.createElement("select")
compareModalTabSelect.id = "compare-tab-select"
compareModalTabSelect.addEventListener("change", function() {
    changeCompareBody(this.value)
})
compareModalBody.appendChild(compareModalTabSelect)

var compareModalTabSelectDefaultOption = document.createElement("option")
compareModalTabSelectDefaultOption.value = "Which Compare Category?.."
compareModalTabSelectDefaultOption.innerText = "Which Compare Category?.."
compareModalTabSelect.appendChild(compareModalTabSelectDefaultOption)

// Compare Modal Body Tabs
const compareModalTabChoices = ["Variables", "Simulation", "Information", "Schemes"]
compareModalTabChoices.forEach(choice => {
    var compareModalTab = document.createElement("button");
    compareModalTab.id = `compare-tab-${choice.toLowerCase()}`
    compareModalTab.innerHTML = choice;
    compareModalTab.addEventListener('click', function() {
        changeCompareTabs(this)
    });
    compareModalBodyTabs.appendChild(compareModalTab)

    var compareModalTabSelectOption = document.createElement("option")
    compareModalTabSelectOption.value = choice
    compareModalTabSelectOption.innerText = choice
    compareModalTabSelect.appendChild(compareModalTabSelectOption)

    var compareModalTabBody = document.createElement("div")
    compareModalTabBody.classList.add("compare-body", "hidden")
    compareModalTabBody.id = `compare-body-${choice.toLowerCase()}`
    compareModalBody.appendChild(compareModalTabBody)
})

// Compare Modal Select Options


//////////////// VARIABLES ////////////////
// Get Variable Comparision
const compareModalBodyVariables = document.getElementById("compare-body-variables")

// Create colors
const gradient = chroma.scale(["#F19A3E", "#3DA480"])

// Create Left Model Variables
var compareModalBodyVariablesLeft = document.createElement("div")
compareModalBodyVariablesLeft.classList.add("compare-variables-math")
compareModalBodyVariablesLeft.id = "compare-variables-left"
compareModalBodyVariablesLeft.style.color = gradient(0).css()
compareModalBodyVariables.appendChild(compareModalBodyVariablesLeft)

const compareModalBodyVariablesDiagramm = document.createElement("div")
compareModalBodyVariablesDiagramm.id = "venndiagramm"
compareModalBodyVariablesDiagramm.innerHTML = vennDiagramm
compareModalBodyVariables.appendChild(compareModalBodyVariablesDiagramm)

// Get Venn Diagram Left Side
const vennLeft = document.getElementById("venndiagramm-left")
vennLeft.style.fill = gradient(0).css()

// Get Venn Diagram Left Side
const vennMiddle = document.getElementById("venndiagramm-middle")
vennMiddle.style.fill = gradient(0.5).css()

// Get Venn Diagram Right Side
const vennRight = document.getElementById("venndiagramm-right")
vennRight.style.fill = gradient(1).css()

// Create Right Model Variables
var compareModalBodyVariablesRight = document.createElement("div")
compareModalBodyVariablesRight.classList.add("compare-variables-math")
compareModalBodyVariablesRight.id = "compare-variables-right"
compareModalBodyVariablesRight.style.color = gradient(1).css()
compareModalBodyVariables.appendChild(compareModalBodyVariablesRight)

// Create Common Model Variables Container
var compareModalBodyVariablesCommonContainer = document.createElement("div")
compareModalBodyVariablesCommonContainer.id = "compare-variables-common"
compareModalBodyVariables.appendChild(compareModalBodyVariablesCommonContainer)

var compareModalBodyVariablesCommon = document.createElement("div")
compareModalBodyVariablesCommon.classList.add("compare-variables-math")
compareModalBodyVariablesCommon.id = "compare-variables-common-math"
compareModalBodyVariablesCommon.style.color = gradient(0.5).css()
compareModalBodyVariablesCommonContainer.appendChild(compareModalBodyVariablesCommon)

// Create Common Variables Explanation
var compareModalBodyVariablesCommonText = document.createElement("p")
compareModalBodyVariablesCommonText.classList.add("discreetText")
compareModalBodyVariablesCommonText.id = "compare-variables-common-text"
compareModalBodyVariablesCommonContainer.appendChild(compareModalBodyVariablesCommonText)

//////////////// SIMULATIONS ////////////////
// Get Simulation Body
const compareModalBodySimulation = document.getElementById("compare-body-simulation")

// Create Explanation Text Container
var compareModalBodySimulationTextContainer = document.createElement("div")
compareModalBodySimulationTextContainer.id = "compare-simulation-text-container"
compareModalBodySimulation.appendChild(compareModalBodySimulationTextContainer)

// Create Explanation Text Heading
var compareModalBodySimulationTextHead = document.createElement("h3")
compareModalBodySimulationTextHead.classList.add()
compareModalBodySimulationTextHead.innerText = "Choose which variable to Plot!"
compareModalBodySimulationTextContainer.appendChild(compareModalBodySimulationTextHead)

// Create Explanation Text Heading
var compareModalBodySimulationText = document.createElement("p")
compareModalBodySimulationText.classList.add("discreetText")
compareModalBodySimulationText.innerText = "All simulations follow the initial conditions of the authors. The only aspect that varies is the PPFD, which you can choose on the right. The plots show the change of concentration over time and have a dark adapted state (PPFD = 50) at the start. (Please keep the scale of the y-axis in mind)"
compareModalBodySimulationTextContainer.appendChild(compareModalBodySimulationText)

function plotVariables(plot, data) {
    Plotly.newPlot( plot, data, {
        annotations: [
            {
                x: 5, y: 0.1,
                text: "PPFD = 50",
                xref: "x", yref: "paper",
                showarrow: false,
                font: {
                    size: 16
                }
            }
        ],
        title: "",
        margin: {
            t: 15,
            b: 40,
            r: 0,
        },
        yaxis: {
            title: {
                text: "Concentration"
            },
            exponentformat: "e",
            showgrid: false,
            ticks: "outside",
            ticklen: 5,
        },
        xaxis: {
            title: {
                text: "Time [s]"
            },
            showgrid: false,
            ticks: "outside",
            ticklen: 5
        },
        legend : {
            orientation: "h",
            x: 0.5,
            xanchor: "center",
            y: 1.1,
            yanchor: "bottom"
        },
        shapes: [
            {
            type: "rect",
            xref: "x",
            yref: "paper", // y-reference is assigned to the plot paper [0,1]
            x0: "0",
            x1: "10",
            y0: 0,
            y1: 1,
            fillcolor: "#d3d3d3",
            opacity: 0.2,
            line: {
                width: 0,
            },
            },
            {
                type: "line",
                x0: 0,
                y0: 0,
                x1: 1,
                y1: 0,
                xref: "paper",
                yref: "paper",
                line: {
                    color: "black",
                    width: 2
                }
            },
            {
                type: "line",
                x0: 0,
                y0: 0,
                x1: 0,
                y1: 1,
                xref: "paper",
                yref: "paper",
                line: {
                    color: "black",
                    width: 2
                }
            }
        ],
    });
}

// Select Change Func
function varCompare() {
    const varSelectBox = document.getElementById("compare-simulation-select")
    const modelSelectBox = document.getElementById("compareModalSelect")
    const otherModel = modelSelectBox.value
    const pfdSlider = document.getElementById("compare-simulation-pfdslider")
    const pfd = pfdSlider.value
    const leftVenn = document.getElementById("venndiagramm-left")
    const leftColor = leftVenn.style.fill
    const rightVenn = document.getElementById("venndiagramm-right")
    const rightColor = rightVenn.style.fill

    console.log(leftColor)

    const chosenVar = varSelectBox.value;

    console.log(pfd)
    var plot = document.getElementById('compare-simulation-chart');

    if (varSelectBox.value == "") {
        plotVariables(plot, [{"x": 0, "y": 0}])
    }

    if (otherModel !== "") {
        const bothSims = getBothSims(modelName, otherModel, pfd)
        bothSims.then(res =>{
            const simThisModel = res[0]
            const simOtherModel = res[1]

            simThisModel[chosenVar]["type"] = "line"
            simThisModel[chosenVar]["name"] = modelName
            simThisModel[chosenVar]["line"] = {color: leftColor}
            simOtherModel[chosenVar]["type"] = "line"
            simOtherModel[chosenVar]["name"] = otherModel
            simOtherModel[chosenVar]["line"] = {color: rightColor}

            const data = [simThisModel[chosenVar], simOtherModel[chosenVar]]

            plotVariables(plot, data)
        })
    } else {
        const thisSim = getSim(`/simulations/${modelName}/${pfd}.json`)
        thisSim.then(res => {
            const data = res[chosenVar]

            data["type"] = "line"
            data["name"] = modelName
            data["line"] = {color: leftColor}

            plotVariables(plot, [data])

        })
    }
}

// Compare Modal Simulation Select
var compareModalBodySimulationSelect = document.createElement("select");
compareModalBodySimulationSelect.id = "compare-simulation-select"
compareModalBodySimulationSelect.addEventListener('change', () => {
    varCompare()
});
compareModalBodySimulation.appendChild(compareModalBodySimulationSelect);

// Compare Modal Simulation Select Value
var compareModalBodySimulationSelectDefaultVal = document.createElement("option");
compareModalBodySimulationSelectDefaultVal.value = "";
compareModalBodySimulationSelectDefaultVal.innerHTML = "Select Variable"
compareModalBodySimulationSelect.appendChild(compareModalBodySimulationSelectDefaultVal)

// Create Slider Container
var sliderContainer = document.createElement("div")
sliderContainer.id = "compare-simulation-sliders"
compareModalBodySimulation.appendChild(sliderContainer);

// Create Slider Text
var sliderText = document.createElement("p")
sliderContainer.appendChild(sliderText)

// Create Slider
var pfdSlider = document.createElement("input")
pfdSlider.id = "compare-simulation-pfdslider"
pfdSlider.classList.add("slider")
pfdSlider.type = "range"
pfdSlider.min = 100
pfdSlider.max = 1400
pfdSlider.step = 100
pfdSlider.addEventListener("input", (event) => {
    sliderText.innerText = `PPFD: ${event.target.value}`
    varCompare()
})
sliderContainer.appendChild(pfdSlider);
sliderText.innerText = `PPFD: ${pfdSlider.value}`

// Create Simulation Chart
var compareModalBodySimulationChart = document.createElement("div")
compareModalBodySimulationChart.id = "compare-simulation-chart"
compareModalBodySimulation.appendChild(compareModalBodySimulationChart)

//////////////// SCHEMES ////////////////
// Insert Scheme
const compareModalBodySchemes = document.getElementById("compare-body-schemes")

// Left Scheme
var compareModalBodySchemesLeftContainer = document.createElement("div")
compareModalBodySchemesLeftContainer.id = "compare-schemes-left-container"
compareModalBodySchemesLeftContainer.classList.add("compare-schemes", "model-scheme-container")
compareModalBodySchemesLeftContainer.addEventListener("click", function() {
    console.log("hello")
    this.childNodes.forEach(element => {
        if (element.nodeName === "IMG") {
            imageModalImg.src = element.src
        }
    })
    imageModal.classList.toggle("hidden")
})
compareModalBodySchemes.appendChild(compareModalBodySchemesLeftContainer)

var compareModalBodySchemesLeftImg = document.createElement("img")
compareModalBodySchemesLeftImg.id = "compare-schemes-left"
compareModalBodySchemesLeftImg.classList.add("compare-schemes", "model-scheme")
compareModalBodySchemesLeftImg.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${modelName}/${modelName}_scheme.svg`
compareModalBodySchemesLeftContainer.appendChild(compareModalBodySchemesLeftImg)

// Right Scheme
var compareModalBodySchemesRightContainer = document.createElement("div")
compareModalBodySchemesRightContainer.id = "compare-schemes-right-container"
compareModalBodySchemesRightContainer.classList.add("compare-schemes", "model-scheme-container")
compareModalBodySchemesRightContainer.addEventListener("click", function() {
    console.log("hello")
    this.childNodes.forEach(element => {
        if (element.nodeName === "IMG") {
            imageModalImg.src = element.src
        }
    })
    imageModal.classList.toggle("hidden")
})
compareModalBodySchemes.appendChild(compareModalBodySchemesRightContainer)

var compareModalBodySchemesRightImg = document.createElement("img")
compareModalBodySchemesRightImg.id = "compare-schemes-right"
compareModalBodySchemesRightImg.classList.add("compare-schemes", "model-scheme")
compareModalBodySchemesRightContainer.appendChild(compareModalBodySchemesRightImg)

//////////////// INFORMATION ////////////////
// Parent container
const compareModalBodyInformation = document.getElementById("compare-body-information")

// Left Side
var compareModalBodyInformationLeft = document.createElement("div")
compareModalBodyInformationLeft.id = "compare-information-left"
compareModalBodyInformationLeft.classList.add("compare-information")
compareModalBodyInformationLeft.addEventListener("mouseleave", function() {
    const allInfoBox = document.getElementsByClassName("compare-information-box")
    for (let element of allInfoBox) {
        element.classList.remove("active", "inactive")
    }
})
compareModalBodyInformation.appendChild(compareModalBodyInformationLeft)

// Right Side
var compareModalBodyInformationRight = document.createElement("div")
compareModalBodyInformationRight.id = "compare-information-right"
compareModalBodyInformationRight.classList.add("compare-information")
compareModalBodyInformationRight.addEventListener("mouseleave", function() {
    const allInfoBox = document.getElementsByClassName("compare-information-box")
    for (let element of allInfoBox) {
        element.classList.remove("active", "inactive")
    }
})
compareModalBodyInformation.appendChild(compareModalBodyInformationRight)

const informationPointer = {
    "ODEs": "compsData",
    "Derived Compounds": "derivedCompsData",
    "Parameters": "paramsData",
    "Derived Parameters": "derivedParamsData",
    "Rates": "ratesData"
}

// Make rows for both sides
const sides = ["left", "right"]
sides.forEach(side => {
    var parentElement = document.getElementById(`compare-information-${side}`)

    for (const [key, value] of Object.entries(informationPointer)) {
        var infoBox = document.createElement("div")
        infoBox.id = `compare-information-box-${side}-${value.toLowerCase()}`
        infoBox.classList.add("compare-information-box")
        infoBox.addEventListener("mouseover", function() {
            const allInfoBox = document.getElementsByClassName("compare-information-box")
            const thisAttr = (this.id).split("-").at(-1)
            for (let element of allInfoBox) {
                element.classList.remove("active")
                element.classList.add("inactive")
                var elementAttr = (element.id).split("-").at(-1)
                if (elementAttr === thisAttr) {
                    element.classList.add("active")
                    element.classList.remove("inactive")
                }
            }
        })
        
        parentElement.appendChild(infoBox)

        var infoBoxTitle = document.createElement("h3")
        infoBoxTitle.innerText = key
        infoBox.appendChild(infoBoxTitle)

        var infoBoxValue = document.createElement("p")
        infoBoxValue.id = `compare-information-${side}-${value.toLowerCase()}`
        infoBox.appendChild(infoBoxValue)
    }
})

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
wrapper.id = "wrapper"
appendCommentedElement(layoutWrapper, wrapper, "The Wrapper")

const contentElement = document.createElement("div")
contentElement.id = "content"
appendCommentedElement(wrapper, contentElement, "The Content")

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
var modelHeaderButtonBarCompare = document.createElement("button")
modelHeaderButtonBarCompare.onclick = function() {
    compareModal.classList.toggle("hidden")
    this.classList.toggle("active")
}
modelHeaderButtonBarCompare.append("Compare")
modelHeaderButtonBar.appendChild(modelHeaderButtonBarCompare)

// Insert Model Button Bar Last Updated
var modelHeaderButtonBarLastUpdate = document.createElement("p")
modelHeaderButtonBarLastUpdate.innerHTML = "Last Update: Loading..."
modelHeaderButtonBarLastUpdate.style = "flex-grow: 1; margin: 0; font-size: 0.7em; text-align: center;"
updateLastModified(modelHeaderButtonBarLastUpdate)
modelHeaderButtonBarGithub.appendChild(modelHeaderButtonBarLastUpdate)

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Create Model Info Selector
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Insert Model Info Selector
var modelInfoSelector = document.createElement("div")
modelInfoSelector.id = "model-info-selector"
appendCommentedElement(contentElement, modelInfoSelector, "The Model Info Selector")

// Insert Model Info Dropdown
var modelInfoSelectorDropdown = document.createElement("select")
modelInfoSelectorDropdown.classList.add("clickable")
modelInfoSelectorDropdown.id = "model-info-selector-dropdown"
modelInfoSelectorDropdown.addEventListener("change", function() {
    const chosenSection = modelInfoSelectorDropdown.value
    if (chosenSection != "") {
        galleryTop.slideTo(chosenSection)
    }
})
appendCommentedElement(modelInfoSelector, modelInfoSelectorDropdown, "The Model Info Dropdown")

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Create Swiper Thumbs Div
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Insert Swiper Thumbs Div
var swiperThumbDiv = document.createElement("div")
swiperThumbDiv.classList.add("swiper-container", "gallery-thumbs")
appendCommentedElement(modelInfoSelector, swiperThumbDiv, "The Swiper Thumb Div")

// Insert Swiper Thumbs Wrapper
var swiperThumbWrapper = document.createElement("div")
swiperThumbWrapper.classList.add("swiper-wrapper")
appendCommentedElement(swiperThumbDiv, swiperThumbWrapper, "The Swiper Thumb Wrapper")

// Insert Swiper Thumbs Summary
var swiperThumbSummary = document.createElement("div")
swiperThumbSummary.classList.add("swiper-slide", "clickable")
swiperThumbSummary.innerHTML = "Summary"
appendCommentedElement(swiperThumbWrapper, swiperThumbSummary, "The Swiper Thumb Summary")

// Insert Model Info Select Summary
var modelInfoSelectorDropdownOptionSummary = document.createElement("option")
modelInfoSelectorDropdownOptionSummary.innerHTML = "Summary"
modelInfoSelectorDropdownOptionSummary.value = modelInfoSelectorDropdown.childNodes.length
modelInfoSelectorDropdown.appendChild(modelInfoSelectorDropdownOptionSummary)

// Tab Container Buttons
const modelInfoCats = {
    ODE: "ODE System",
    DerivedComps: "Derived Quantities",
    Params: "Parameters",
    DerivedParams: "Derived Parameters",
    Rates: "Rates",
    Figures: "Figures"
}

// Insert Swiper Thumbs
for (const [key, value] of Object.entries(modelInfoCats)) {
    var swiperThumb = document.createElement("div")
    swiperThumb.classList.add("clickable", "swiper-slide")
    swiperThumb.innerHTML = value
    appendCommentedElement(swiperThumbWrapper, swiperThumb, `The Swiper Thumb ${key}`)

    var modelInfoSelectorDropdownOption = document.createElement("option")
    modelInfoSelectorDropdownOption.innerHTML = value
    modelInfoSelectorDropdownOption.value = modelInfoSelectorDropdown.childNodes.length
    modelInfoSelectorDropdown.appendChild(modelInfoSelectorDropdownOption)
}

///////////////////////////////////////////////////////
// Create Swiper Div
///////////////////////////////////////////////////////
// Insert Swiper Div
var swiperDiv = document.createElement("div")
swiperDiv.classList.add("swiper", "gallery-top")
appendCommentedElement(contentElement, swiperDiv, "The Swiper Div")

// Insert Swiper Buttons Row
var swiperButtons = document.createElement("div")
swiperButtons.id = "swiper-model-buttons"
appendCommentedElement(swiperDiv, swiperButtons, "The Swiper Buttons")

// Insert Swiper Prev Arrow
var swiperPrev = document.createElement("span")
swiperPrev.classList.add("swiper-button")
swiperPrev.addEventListener("click", function() {
    var numSlides = galleryTop.slides.length
    var thisSlideIndex = galleryTop.activeIndex
    if (thisSlideIndex == 0) {
        var newSlideIndex = numSlides - 1
    } else {
        var newSlideIndex = thisSlideIndex - 1
    }
    galleryTop.slideTo(newSlideIndex)
})
appendCommentedElement(swiperButtons, swiperPrev, "The Swiper Prev Arrow")

var swiperPrevArrow = document.createElement("span")
swiperPrevArrow.classList.add("arrowUp")
swiperPrevArrow.id = "swiper-model-button-prev"
swiperPrev.appendChild(swiperPrevArrow)

// Insert Swiper Next Arrow
var swiperNext = document.createElement("div")
swiperNext.classList.add("swiper-button")
swiperNext.addEventListener("click", function() {
    var numSlides = galleryTop.slides.length
    var thisSlideIndex = galleryTop.activeIndex
    if (thisSlideIndex == numSlides - 1) {
        var newSlideIndex = 0
    } else {
        var newSlideIndex = thisSlideIndex + 1
    }
    galleryTop.slideTo(newSlideIndex)
})
appendCommentedElement(swiperButtons, swiperNext, "The Swiper Next Arrow")

var swiperNextArrow = document.createElement("span")
swiperNextArrow.classList.add("arrowUp")
swiperNextArrow.id = "swiper-model-button-next"
swiperNext.appendChild(swiperNextArrow)

// Insert Swiper Wrapper
var swiperWrapper = document.createElement("div")
swiperWrapper.classList.add("swiper-wrapper", "swiper-wrapper-models")
appendCommentedElement(swiperDiv, swiperWrapper, "The Swiper Wrapper")

// Insert Swiper Slide Summary
var swiperSummary = document.createElement("div")
swiperSummary.classList.add("swiper-slide", "swiper-slide-models")
appendCommentedElement(swiperWrapper, swiperSummary, "The Swiper Slide Summary")

// Insert Swiper Slides
for (const [key, value] of Object.entries(modelInfoCats)) {
    var swiperSlide = document.createElement("div")
    swiperSlide.classList.add("swiper-slide", "swiper-slide-models", "modelTabContent")
    swiperSlide.id = `modelAttr${key}`
    appendCommentedElement(swiperWrapper, swiperSlide, `The Swiper Slide ${key}`)

    if (key != "Figures") {
        var modelAttrTableDiv = document.createElement("div")
        modelAttrTableDiv.classList.add("model-attr-table-div")
        swiperSlide.appendChild(modelAttrTableDiv)

        var modelAttrTable = document.createElement("table")
        modelAttrTable.id = `modelAttr${key}Table`
        modelAttrTableDiv.appendChild(modelAttrTable)

        var modelAttrMath = document.createElement("div")
        modelAttrMath.id = `modelAttr${key}Math`
        modelAttrMath.classList.add("modelAttrMath")
        swiperSlide.appendChild(modelAttrMath)
    }
}

///////////////////////////////////////////////////////
// Init Swiper
///////////////////////////////////////////////////////
Swiper.use([Navigation, Thumbs]);
var galleryThumbs = new Swiper('.gallery-thumbs', {
    spaceBetween: 10,
    slidesPerView: 'auto', // <- makes slide width match content
    freeMode: true,
    watchSlidesVisibility: true,
    watchSlidesProgress: true,
    // no loop here
  });  

var galleryTop = new Swiper('.gallery-top', {
    spaceBetween: 10,
    loop: true,
    loopedSlides: 5,
    autoHeight: true,
    allowTouchMove: false,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    thumbs: {
        swiper: galleryThumbs,
    },
});

///////////////////////////////////////////////////////
// Model Summary Block
///////////////////////////////////////////////////////
// Insert Model Summary Block
var modelSummaryBlock = document.createElement("div")
modelSummaryBlock.id = "model-summary-block"
appendCommentedElement(swiperSummary, modelSummaryBlock, "The Model Summary")

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
modelSummaryBlockScheme.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${modelName}/${modelName}_scheme.svg`
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

// Add at End
// Get this models Info and input into right places
getModelInfo(modelName)
    .then(response => {
        createInfoTable(response);
        createInfoList(response, "left", informationPointer)

        const filteredGlossCompsAbbr = filterGlossIDAbbr(response["compsData"])
        const filteredGlossDerivedCompsAbbr = filterGlossIDAbbr(response["derivedCompsData"])
        const filteredGlossCombinedAbbr = {...filteredGlossCompsAbbr, ...filteredGlossDerivedCompsAbbr}
        var leftVariables = document.getElementById("compare-variables-left")
        for (const [key, value] of Object.entries(filteredGlossCombinedAbbr)) {
            var newP = document.createElement("p")
            newP.innerText = value
            leftVariables.appendChild(newP)
        }

        const filteredGlossCompsPythonVar = filterGlossIDPythonVar(response["compsData"])
        const filteredGlossDerivedCompsPythonVar = filterGlossIDPythonVar(response["derivedCompsData"])
        const filteredGlossCombined = {...filteredGlossCompsPythonVar, ...filteredGlossDerivedCompsPythonVar}
        // Compare Modal Heading Select Option Creator
        const compareModalBodySimulationSelect = document.getElementById("compare-simulation-select")
        const availableVars = Object.values(filteredGlossCombined)
        availableVars.forEach(element => {
            var varOption = document.createElement("option")
            varOption.value = element
            varOption.innerHTML = element
            compareModalBodySimulationSelect.appendChild(varOption)
        })

        MathJax.typeset()

        galleryTop.update()
    });

getMdFile().then(response => {
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
            galleryTop.update()
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

    galleryTop.update()

})

// At the very End
import('./topnav.js');

import('./cite.js');

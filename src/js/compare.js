import modelData from "../js/models.json"
import { getModelInfo, getSiblings, filterGlossIDAbbr, filterGlossIDPythonVar, getTwoModelInfo, createInfoList, informationPointer, getFullModelInfo, getSim, getBothSims, getMdFile } from "../js/utils.js"
import chroma from "chroma-js"
import vennDiagramm from "../img/venn_diagramm.svg?raw"
import Plotly from 'plotly.js-dist'

// Helper Functions
function selectChange(selectElement) {
    const leftModelSelect = document.getElementById("compare-model-left-select")
    const rightModelSelect = document.getElementById("compare-model-right-select")
    
    if (selectElement == leftModelSelect) {
        var side = "left"
        var oppSide = "right"
        var oppModelSelect = rightModelSelect
    } else {
        var side = "right"
        var oppSide = "left"
        var oppModelSelect = leftModelSelect
    }
    const thisVariables = document.getElementById("compare-variables-" + side)
    thisVariables.innerHTML = ""

    const otherVariables = document.getElementById("compare-variables-" + oppSide)
    otherVariables.innerHTML = ""

    const commonVariables = document.getElementById("compare-variables-common-math")
    commonVariables.innerHTML = ""

    const schemeThis = document.getElementById("compare-schemes-" + side)
    schemeThis.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${selectElement.value}/${selectElement.value}_scheme.svg`

    const selectBoxDemon = document.getElementById(`compare-demonstrations-select-${side}`)
    selectBoxDemon.innerHTML = ""

    var defaultVal = document.createElement("option");
    defaultVal.value = "";
    defaultVal.innerHTML = "Select Demonstration"
    selectBoxDemon.appendChild(defaultVal)

    const demonContainer = document.getElementById(`compare-demonstrations-container-${side}`)
    demonContainer.innerHTML = ""
    
    getModelInfo(selectElement.value)
        .then(response => {
            createInfoList(response, side, informationPointer)
        })

    getMdFile(selectElement.value)
        .then(response => {
            const demonstrations = response.demonstrations
            
            for (let i = 0; i < demonstrations.length; i++) {
                var demonInfo = demonstrations[i]
                var demonImgSrc = demonInfo.imgSrc
                var demonTitle = demonInfo.title
                var demonText = demonInfo.text

                var demoOption = document.createElement("option")
                demoOption.value = demonTitle
                demoOption.innerHTML = demonTitle
                selectBoxDemon.appendChild(demoOption)

                var demonBox = document.createElement("div")
                demonBox.id = `compare-demonstrations-${side}-box-${demonTitle.toLowerCase().replace(/\s/g, '')}`
                demonBox.classList.add("compare-demonstrations-box", "hidden")

                var demonstrationImg = document.createElement("img")
                demonstrationImg.id = `compare-demonstrations-${side}-img-${demonTitle.toLowerCase().replace(/\s/g, '')}`
                demonstrationImg.classList.add("compare-demonstrations-img")
                demonstrationImg.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${selectElement.value}/${demonImgSrc}`
                demonBox.appendChild(demonstrationImg)
                demonContainer.appendChild(demonBox)

                demonBox.innerHTML += demonText
            }
        })

    var simSelectBox = document.getElementById("compare-simulation-select")
    simSelectBox.innerHTML = ""
    var defaultVal = document.createElement("option");
    defaultVal.value = "";
    defaultVal.innerHTML = "Select Variable"
    simSelectBox.appendChild(defaultVal)
    const simSelectTab = document.getElementById("compare-tab-simulation")

    if (oppModelSelect.value !== "") {
        const bothInfo = getTwoModelInfo(selectElement.value, oppModelSelect.value)
        bothInfo.then(res => {
            const thisModelInfo = res[0]
            const otherModelInfo = res[1]
            const mainGloss = res[2]

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
                thisVariables.appendChild(newP)
            })
            
            otherModelVarsUnique.forEach(ele => {
                var newP = document.createElement("p")
                newP.innerText = mainGlossPointerAbbr[ele]
                otherVariables.appendChild(newP)
            })
            
            commonVars.forEach(ele => {
                var varOption = document.createElement("option")
                varOption.value = mainGlossPointerPythonVar[ele]
                varOption.innerHTML = mainGlossPointerPythonVar[ele]
                simSelectBox.appendChild(varOption)

                var newP = document.createElement("p")
                newP.innerText = mainGlossPointerAbbr[ele]
                newP.addEventListener("click", function() {
                    simSelectBox.value = mainGlossPointerPythonVar[ele]
                    changeCompareTabs(simSelectTab)
                })
                commonVariables.appendChild(newP)
            })

            MathJax.typeset()

        })
    } else {
        getFullModelInfo(selectElement.value)
            .then(response => {
                const thisModelInfo = response[0]
                const mainGloss = response[1]

                const filteredGlossCompsAbbr = filterGlossIDAbbr(thisModelInfo["compsData"])
                const filteredGlossDerivedCompsAbbr = filterGlossIDAbbr(thisModelInfo["derivedCompsData"])
                const filteredGlossCombinedAbbr = {...filteredGlossCompsAbbr, ...filteredGlossDerivedCompsAbbr}

                const mainGlossPointerAbbr = filterGlossIDAbbr(mainGloss)
                const mainGlossPointerPythonVar = filterGlossIDPythonVar(mainGloss)

                var leftVariables = document.getElementById("compare-variables-" + side)
                for (const [key, value] of Object.entries(filteredGlossCombinedAbbr)) {
                    var varOption = document.createElement("option")
                    varOption.value = mainGlossPointerPythonVar[key]
                    varOption.innerHTML = mainGlossPointerPythonVar[key]
                    simSelectBox.appendChild(varOption)

                    var newP = document.createElement("p")
                    newP.innerText = value
                    leftVariables.appendChild(newP)
                }
                MathJax.typeset()
            })
    }
}

//////////////////////////////////////////////////

const contentElement = document.getElementById("compare-content")

// Compare Model Selects
const leftModelSelect = document.getElementById("compare-model-left-select")
leftModelSelect.addEventListener("change", function() {
    // 1. Get the current URL path (e.g., /page-b.html)
    const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;

    // 2. Replace the current history entry with the clean URL
    window.history.replaceState({}, document.title, cleanUrl);

    selectChange(this)
})
const rightModelSelect = document.getElementById("compare-model-right-select")
rightModelSelect.addEventListener("change", function() {
    selectChange(this)
})

// Compare Modal Heading Select Option Creator
const availableModels = Object.keys(modelData)
availableModels.forEach(element => {
    const modelOption = document.createElement("option")
    modelOption.value = element
    modelOption.innerHTML = element
    leftModelSelect.appendChild(modelOption)
    rightModelSelect.appendChild(modelOption.cloneNode(true))
})

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
    var siblings = getSiblings(tabClicked)
    siblings.forEach(element => {
        element.classList.remove("active")
    })
    tabClicked.classList.add("active")

    changeCompareBody(tabClicked.innerHTML)
}

// Create Compare Tabs
const compareTabs = document.getElementById("compare-tabs")
const compareTabChoices = ["Variables", "Simulation", "Information", "Demonstrations", "Schemes"]
compareTabChoices.forEach(choice => {
    var compareTab = document.createElement("button");
    compareTab.id = `compare-tab-${choice.toLowerCase()}`
    compareTab.innerHTML = choice;
    compareTab.addEventListener('click', function() {
        changeCompareTabs(this)
    });
    compareTabs.appendChild(compareTab)

    // var compareTabSelectOption = document.createElement("option")
    // compareTabSelectOption.value = choice
    // compareTabSelectOption.innerText = choice
    // compareTabSelect.appendChild(compareTabSelectOption)
    
    var compareTabBody = document.createElement("div")
    compareTabBody.classList.add("compare-body", "hidden")
    compareTabBody.id = `compare-body-${choice.toLowerCase()}`
    contentElement.appendChild(compareTabBody)
})

//////////////// VARIABLES ////////////////
// Get Variable Comparision
const compareBodyVariables = document.getElementById("compare-body-variables")

// Create colors
const gradient = chroma.scale(["#F19A3E", "#3DA480"])

// Create Left Model Variables
var compareBodyVariablesLeft = document.createElement("div")
compareBodyVariablesLeft.classList.add("compare-variables-math")
compareBodyVariablesLeft.id = "compare-variables-left"
compareBodyVariablesLeft.style.color = gradient(0).css()
compareBodyVariables.appendChild(compareBodyVariablesLeft)

const compareBodyVariablesDiagramm = document.createElement("div")
compareBodyVariablesDiagramm.id = "venndiagramm"
compareBodyVariablesDiagramm.innerHTML = vennDiagramm
compareBodyVariables.appendChild(compareBodyVariablesDiagramm)

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
var compareBodyVariablesRight = document.createElement("div")
compareBodyVariablesRight.classList.add("compare-variables-math")
compareBodyVariablesRight.id = "compare-variables-right"
compareBodyVariablesRight.style.color = gradient(1).css()
compareBodyVariables.appendChild(compareBodyVariablesRight)

// Create Common Model Variables Container
var compareBodyVariablesCommonContainer = document.createElement("div")
compareBodyVariablesCommonContainer.id = "compare-variables-common"
compareBodyVariables.appendChild(compareBodyVariablesCommonContainer)

var compareBodyVariablesCommon = document.createElement("div")
compareBodyVariablesCommon.classList.add("compare-variables-math")
compareBodyVariablesCommon.id = "compare-variables-common-math"
compareBodyVariablesCommon.style.color = gradient(0.5).css()
compareBodyVariablesCommonContainer.appendChild(compareBodyVariablesCommon)

// Create Common Variables Explanation
var compareBodyVariablesCommonText = document.createElement("p")
compareBodyVariablesCommonText.classList.add("discreetText")
compareBodyVariablesCommonText.id = "compare-variables-common-text"
compareBodyVariablesCommonContainer.appendChild(compareBodyVariablesCommonText)

//////////////// SIMULATIONS ////////////////
// Get Simulation Body
const compareBodySimulation = document.getElementById("compare-body-simulation")

// Create Explanation Text Container
var compareBodySimulationTextContainer = document.createElement("div")
compareBodySimulationTextContainer.id = "compare-simulation-text-container"
compareBodySimulation.appendChild(compareBodySimulationTextContainer)

// Create Explanation Text Heading
var compareBodySimulationTextHead = document.createElement("h3")
compareBodySimulationTextHead.classList.add()
compareBodySimulationTextHead.innerText = "Choose which variable to Plot!"
compareBodySimulationTextContainer.appendChild(compareBodySimulationTextHead)

// Create Explanation Text Heading
var compareBodySimulationText = document.createElement("p")
compareBodySimulationText.classList.add("discreetText")
compareBodySimulationText.innerText = "All simulations follow the initial conditions of the authors. The only aspect that varies is the PPFD, which you can choose on the right. The plots show the change of concentration over time and have a dark adapted state (PPFD = 50) at the start. (Please keep the scale of the y-axis in mind)"
compareBodySimulationTextContainer.appendChild(compareBodySimulationText)

function plotVariables(plot, data) {
    Plotly.react( plot, data, {
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

    const pfdSlider = document.getElementById("compare-simulation-pfdslider")
    const pfd = pfdSlider.value
    const leftVenn = document.getElementById("venndiagramm-left")
    const leftColor = leftVenn.style.fill
    const rightVenn = document.getElementById("venndiagramm-right")
    const rightColor = rightVenn.style.fill

    const chosenVar = varSelectBox.value;

    var plot = document.getElementById('compare-simulation-chart');

    const leftModelSelect = document.getElementById("compare-model-left-select")
    const rightModelSelect = document.getElementById("compare-model-right-select")

    if (varSelectBox.value == "") {
        plotVariables(plot, [{"x": 0, "y": 0}])
        return
    }

    if (leftModelSelect.value == "" && rightModelSelect.value == "") {
        return
    } else if (leftModelSelect.value != "" && rightModelSelect.value != "") {
        const bothSims = getBothSims(leftModelSelect.value, rightModelSelect.value, pfd)
        bothSims.then(res =>{
            
            const simLeftModel = res[0]
            const simRightModel = res[1]

            const simLeftData = {
                "x": Object.keys(simLeftModel[chosenVar]),
                "y": Object.values(simLeftModel[chosenVar]),
                "type": "line",
                "name": leftModelSelect.value,
                "line": {color: leftColor}
            }

            const simRightData = {
                "x": Object.keys(simRightModel[chosenVar]),
                "y": Object.values(simRightModel[chosenVar]),
                "type": "line",
                "name": rightModelSelect.value,
                "line": {color: rightColor}
            }

            const data = [simLeftData, simRightData]

            plotVariables(plot, data)
        })
    } else if (leftModelSelect.value != "" && rightModelSelect.value == "") {
        const thisSim = getSim(`/simulations/${leftModelSelect.value}/${pfd}.json`)
        thisSim.then(res => {
            const data = {
                "x": Object.keys(res[chosenVar]),
                "y": Object.values(res[chosenVar]),
                "type": "line",
                "name": leftModelSelect.value,
                "line": {color: leftColor}
            }

            plotVariables(plot, [data])
        })
    } else {
        const thisSim = getSim(`/simulations/${rightModelSelect.value}/${pfd}.json`)
        thisSim.then(res => {
            const data = res[chosenVar]

            data["type"] = "line"
            data["name"] = rightModelSelect.value
            data["line"] = {color: rightColor}

            plotVariables(plot, [data])
        })
    }
}

// Compare Modal Simulation Select
var compareBodySimulationSelect = document.createElement("select");
compareBodySimulationSelect.id = "compare-simulation-select"
compareBodySimulationSelect.addEventListener('change', () => {
    varCompare()
});
compareBodySimulation.appendChild(compareBodySimulationSelect);

// Compare Modal Simulation Select Value
var compareBodySimulationSelectDefaultVal = document.createElement("option");
compareBodySimulationSelectDefaultVal.value = "";
compareBodySimulationSelectDefaultVal.innerHTML = "Select Variable"
compareBodySimulationSelect.appendChild(compareBodySimulationSelectDefaultVal)

// Create Slider Container
var sliderContainer = document.createElement("div")
sliderContainer.id = "compare-simulation-sliders"
compareBodySimulation.appendChild(sliderContainer);

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
var compareBodySimulationChart = document.createElement("div")
compareBodySimulationChart.id = "compare-simulation-chart"
compareBodySimulation.appendChild(compareBodySimulationChart)

//////////////// SCHEMES ////////////////
// Insert Scheme
const compareBodySchemes = document.getElementById("compare-body-schemes")

// Left Scheme
var compareBodySchemesLeftContainer = document.createElement("div")
compareBodySchemesLeftContainer.id = "compare-schemes-left-container"
compareBodySchemesLeftContainer.classList.add("compare-schemes", "model-scheme-container")
compareBodySchemesLeftContainer.addEventListener("click", function() {
    this.childNodes.forEach(element => {
        if (element.nodeName === "IMG") {
            imageModalImg.src = element.src
        }
    })
    imageModal.classList.toggle("hidden")
})
compareBodySchemes.appendChild(compareBodySchemesLeftContainer)

var compareBodySchemesLeftImg = document.createElement("img")
compareBodySchemesLeftImg.id = "compare-schemes-left"
compareBodySchemesLeftImg.classList.add("compare-schemes", "model-scheme")
compareBodySchemesLeftContainer.appendChild(compareBodySchemesLeftImg)

// Right Scheme
var compareBodySchemesRightContainer = document.createElement("div")
compareBodySchemesRightContainer.id = "compare-schemes-right-container"
compareBodySchemesRightContainer.classList.add("compare-schemes", "model-scheme-container")
compareBodySchemesRightContainer.addEventListener("click", function() {
    this.childNodes.forEach(element => {
        if (element.nodeName === "IMG") {
            imageModalImg.src = element.src
        }
    })
    imageModal.classList.toggle("hidden")
})
compareBodySchemes.appendChild(compareBodySchemesRightContainer)

var compareBodySchemesRightImg = document.createElement("img")
compareBodySchemesRightImg.id = "compare-schemes-right"
compareBodySchemesRightImg.classList.add("compare-schemes", "model-scheme")
compareBodySchemesRightContainer.appendChild(compareBodySchemesRightImg)

//////////////// INFORMATION ////////////////
// Parent container
const compareBodyInformation = document.getElementById("compare-body-information")

// Left Side
var compareBodyInformationLeft = document.createElement("div")
compareBodyInformationLeft.id = "compare-information-left"
compareBodyInformationLeft.classList.add("compare-information")
compareBodyInformationLeft.addEventListener("mouseleave", function() {
    const allInfoBox = document.getElementsByClassName("compare-information-box")
    for (let element of allInfoBox) {
        element.classList.remove("active", "inactive")
    }
})
compareBodyInformation.appendChild(compareBodyInformationLeft)

// Right Side
var compareBodyInformationRight = document.createElement("div")
compareBodyInformationRight.id = "compare-information-right"
compareBodyInformationRight.classList.add("compare-information")
compareBodyInformationRight.addEventListener("mouseleave", function() {
    const allInfoBox = document.getElementsByClassName("compare-information-box")
    for (let element of allInfoBox) {
        element.classList.remove("active", "inactive")
    }
})
compareBodyInformation.appendChild(compareBodyInformationRight)

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

//////////////// Demonstrations ////////////////

function selectChangeDemonstrations(selectElement) {
    const leftDemonSelect = document.getElementById("compare-demonstrations-select-left")
    const rightDemonSelect = document.getElementById("compare-demonstrations-select-right")
    
    
    if (selectElement == leftDemonSelect) {
        var side = "left"
    } else {
        var side = "right"
    }
    const demonContainer = document.getElementById(`compare-demonstrations-container-${side}`)

    const allCompareBlocks = demonContainer.children
    console.log(typeof allCompareBlocks)
    const selectedValue = selectElement.value.toLowerCase().replace(/\s/g, '')
    for (let block of allCompareBlocks) {
         block.classList.add("hidden")
        if (block.id.includes(selectedValue)) {
            block.classList.remove("hidden")
        }
    }
}

// Parent container
const compareBodyDemonstrations = document.getElementById("compare-body-demonstrations")

for (const side of ["left", "right"]) {
    var parentElement = document.createElement("div")
    parentElement.id = `compare-demonstrations-${side}`
    parentElement.classList.add("compare-demonstrations")
    compareBodyDemonstrations.appendChild(parentElement)

    var selectBox = document.createElement("select")
    selectBox.id = `compare-demonstrations-select-${side}`
    selectBox.classList.add("compare-demonstrations-selectbox")
    selectBox.addEventListener("change", function() {
        selectChangeDemonstrations(this)
    })
    parentElement.appendChild(selectBox)

    var defaultVal = document.createElement("option");
    defaultVal.value = "";
    defaultVal.innerHTML = "Select Demonstration"
    selectBox.appendChild(defaultVal)

    var demonstrationContainer = document.createElement("div")
    demonstrationContainer.id = `compare-demonstrations-container-${side}`
    demonstrationContainer.classList.add("compare-demonstrations-container")
    parentElement.appendChild(demonstrationContainer)

}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// End
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// See if already selected
window.addEventListener('DOMContentLoaded', () => {
    // 1. Get the query string from the URL (e.g., "?select=blue")
    const params = new URLSearchParams(window.location.search);
    
    // 2. Pull out the specific value for "select"
    const choice = params.get("select");

    // 3. If a choice exists, set the select menu value
    if (choice) {
        const selectElement = document.getElementById("compare-model-left-select");
        selectElement.value = choice;
        selectChange(selectElement)
    }
});
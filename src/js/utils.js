import Papa from "papaparse";
import { marked } from 'marked';

export const getSiblings = (el) => {
  return Array.from(el.parentNode.children).filter(sibling => sibling !== el);
};

// Get model information
export function parseModelInfo(modelName, InfoVar) {
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

export async function getModelInfo(modelName) {
    return {
        compsData: await parseModelInfo(modelName, 'comps'),
        paramsData: await parseModelInfo(modelName, 'params'),
        ratesData: await parseModelInfo(modelName, 'rates'),
        derivedCompsData: await parseModelInfo(modelName, 'derived_comps'),
        derivedParamsData: await parseModelInfo(modelName, 'derived_params'),
    }
};

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

export async function getFullModelInfo(modelName) {
    const res = await Promise.all([
            getModelInfo(modelName),
            getMainGlossary()
        ])
    return res
}

export async function getTwoModelInfo(modelName, otherModelName) {
    const res = await Promise.all([
            getModelInfo(modelName),
            getModelInfo(otherModelName),
            getMainGlossary()
        ])
    return res
}

// Create Info List
export function createInfoList(response, side, informationPointer) {
    for (const [key, value] of Object.entries(informationPointer)) {
        var valueElement = document.getElementById(`compare-information-${side}-${value.toLowerCase()}`)
        if (response != "") {
            valueElement.innerText = response[value].length
        } else {
            valueElement.innerText = ""
        }
    }
};

export function filterGlossIDAbbr(gloss) {
    var filteredGloss = {}
        gloss.forEach(row => {
            filteredGloss[row["Glossary ID"]] = row["Common Abbr."]
        })

    return filteredGloss
}

export function filterGlossIDPythonVar(gloss) {
    var filteredGloss = {}
        gloss.forEach(row => {
            filteredGloss[row["Glossary ID"]] = row["Python Var"]
        })

    return filteredGloss
}

export const informationPointer = {
    "ODEs": "compsData",
    "Derived Compounds": "derivedCompsData",
    "Parameters": "paramsData",
    "Derived Parameters": "derivedParamsData",
    "Rates": "ratesData"
}

// Get Sim
export function getSim(path) {
    return new Promise((resolve, reject) => {
        fetch(path).then(response => {
            resolve(response.json())
        })
    })
}

// Get Both Sims
export async function getBothSims(thisModel, otherModel, pfd) {
    const res = await Promise.all([
        getSim(`/simulations/${thisModel}/${pfd}.json`),
        getSim(`/simulations/${otherModel}/${pfd}.json`)
    ])

    return res
}

// Append Element into DOM with prior Comment
export function appendCommentedElement(parent, ele, comm) {
    comm = document.createComment(comm)
    parent.appendChild(comm)
    parent.appendChild(ele)
}

// Append Element into DOM with prior Comment
export function prependCommentedElement(parent, ele, comm) {
    comm = document.createComment(comm)
    parent.prepend(comm)
    parent.prepend(ele)
}

// Put Info in Table
export function createInfoTable(response) {
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
export async function getMdFile(modelName) {
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

    const figuresSection = completeText.match(/### Figures(.*)### Demonstrations/gms)[0];
    const figuresDetailsRegex = /<details>\s*<summary>(.*?)<\/summary>\s*([\s\S]*?)<\/details>/g;

    const demonstrationsSection = completeText.match(/### Demonstrations(.*)/gms)[0];
    // const figuresDetailsRegex = /<details>\s*<summary>(.*?)<\/summary>\s*([\s\S]*?)<\/details>/g;

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

    const demonstrations = [];

    while ((matches = figuresDetailsRegex.exec(demonstrationsSection)) !== null) {
        const title = matches[1].trim();  // Title inside <summary>...</summary>
        const content = matches[2];        // Inside the <details> block

        // Extract the <img> src
        const imgMatch = content.match(/<img[^>]+src=['"]([^'"]+)['"]/);
        const imgSrc = imgMatch ? imgMatch[1] : null;

        // Remove the <img> tag from the content to get the text only
        const text = marked.parse(content.replace(/<img[^>]*>/g, '').trim());

        demonstrations.push({ title, imgSrc, text });
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
        figures: figures,
        demonstrations: demonstrations
    }

}

export function createFigures(figureObject, modelName, parentElement) {
    for (let i = 0; i < figureObject.length; i++) {
        var figureInfo = figureObject[i]
        var figureImgSrc = figureInfo.imgSrc
        var figureTitle = figureInfo.title
        var figureText = figureInfo.text

        var modelAttrFiguresContainer = document.createElement("div")
        modelAttrFiguresContainer.classList.add("modelAttrFiguresContainer")
        parentElement.appendChild(modelAttrFiguresContainer)

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
        modelAttrFiguresContainerContentImg.src = `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${modelName}/${figureImgSrc}`
        modelAttrFiguresContainerContent.appendChild(modelAttrFiguresContainerContentImg)

        modelAttrFiguresContainerContent.innerHTML += figureText

    }
}
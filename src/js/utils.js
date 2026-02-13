import Papa from "papaparse";

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
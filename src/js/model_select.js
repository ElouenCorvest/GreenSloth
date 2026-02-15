import modelInfo from "../js/models.json"

var tagsButton = document.getElementById("tagsButton")
tagsButton.addEventListener("click", () => {
    document.querySelector('.tagsButton').classList.toggle('active');
    document.querySelector('.tagsBox').classList.toggle('hidden')
});

var modelSelector = document.getElementById("model-selector")
const tagsBox = document.getElementById("tagsBox");

var simpleTags = {}
modelSelector = document.getElementById("model-selector");

for (const [name, info] of Object.entries(modelInfo)) {
    const modelRow = document.createElement("div");
    // modelRow.setAttribute("class", "model-row");
    modelRow.classList.add("model-row")
    modelRow.id = name
    modelSelector.appendChild(modelRow);

    const modelImg = document.createElement("img");
    modelImg.setAttribute("src", `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/refs/heads/main/models/${name}/${name}_scheme.svg`);
    modelRow.appendChild(modelImg);

    const modelTitle = document.createElement("h1");
    modelTitle.innerHTML = name;
    modelRow.appendChild(modelTitle);

    const modelLink = document.createElement("a");
    modelLink.href = `/model/${name}.html`
    modelRow.appendChild(modelLink);
    
    const linkSpanner = document.createElement("span");
    linkSpanner.setAttribute("class", "linkSpanner");
    modelLink.appendChild(linkSpanner);

    // Create Tags
    const tags = info.tags 

    const tagsCategory = Object.keys(tags)
    tagsCategory.forEach(cat => {
        var cleanCat = cat.replaceAll(" ", "-")
        cleanCat = cleanCat.toLowerCase()

        simpleTags[cleanCat] = (simpleTags[cleanCat] || {});
        // Create Tag Category if not existant already
        var catExists = document.getElementById(`tags-category-${cleanCat}`);
        var catTagsExists = document.getElementById(`tags-category-${cleanCat}-row`);
        if (catExists == null) {
            const catDiv = document.createElement("div");
            catDiv.id = (`tags-category-${cleanCat}`)
            catDiv.classList.add("tags-category")
            const catHead = document.createElement("h3");
            catHead.innerHTML = cat;
            catDiv.appendChild(catHead);
            const catTags = document.createElement("div");
            catTags.id = `tags-category-${cleanCat}-row`
            catTags.classList.add("tags-row");
            catDiv.appendChild(catTags);
            
            tagsBox.appendChild(catDiv);
            var catExists = document.getElementById(`tags-category-${cleanCat}`);
            var catTagsExists = document.getElementById(`tags-category-${cleanCat}-row`);
        }
        
        tags[cat].forEach(tag => {
            var cleanTag = tag.replaceAll(" ", "-")
            cleanTag = cleanTag.toLowerCase()
            simpleTags[cleanCat][cleanTag] = (simpleTags[cleanCat][cleanTag] || []).concat([name])

            var tagExists = document.getElementById(`tag-button-${cleanCat}-${cleanTag}`);
            if (tagExists == null) {
                const tagButton = document.createElement("button");
                tagButton.innerHTML = tag;
                tagButton.id = (`tag-button-${cleanCat}-${cleanTag}`);
                tagButton.classList.add("clickable", "tag");
                tagButton.onclick = function() {
                    this.classList.toggle("active")
                    tagSelection()
                };
                catTagsExists.appendChild(tagButton);
                var tagExists = document.getElementById(`tag-button-${cleanCat}-${cleanTag}`        );
            }
        }); 
    });
};

const searchParams = new URLSearchParams(window.location.search);

const paramPointer = {
    PSII: "psii",
    PSI: "psi",
    Cytb6f: "cytochrome-b6f",
    AtpSynth: "atp-synthase",
    PQ: "pq-cycle",
    PC: "pc",
    CBB: "cbb-cycle"
} 

if (searchParams.has("appar")) {
    const urlAppar = searchParams.get("appar")
    document.getElementById(`tag-button-part-of-photosynthesis-${paramPointer[urlAppar]}`).classList.toggle("active")
}

function tagSelection() {
    var activeTags = document.querySelectorAll('.tag.active')
    var activeModels = []

    for (let i = 0; i < activeTags.length; i++) {
        var activeTag = activeTags[i]
        var catId = activeTag.parentElement.id.replace("tags-category-", "")
        catId = catId.replace("-row", "")
        var tagId = activeTag.id.replace(`tag-button-${catId}-`, "")
        if (i == 0) {
            activeModels = activeModels.concat(simpleTags[catId][tagId])
        } else {
            var newActiveModels = []
            console.log(activeModels)
            console.log(simpleTags[catId][tagId])
            activeModels.forEach(modelName => {
                if (simpleTags[catId][tagId].includes(modelName)) {
                    console.log("hello")
                    newActiveModels.push(modelName)
                }
            })
            console.log(newActiveModels)
            activeModels = [...newActiveModels]
        }
    }

    
    console.log(activeModels)
    if (activeTags.length !== 0) {
        document.querySelectorAll('.model-row').forEach(row => {
            row.classList.add("hidden")
        })
    } else {
        document.querySelectorAll('.model-row').forEach(row => {
            row.classList.remove("hidden")
        })
    }
    
    activeModels.forEach(model => {
        document.getElementById(model).classList.remove("hidden")
    })

}

tagSelection()
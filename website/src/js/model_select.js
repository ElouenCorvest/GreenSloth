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
    modelImg.setAttribute("src", `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${name}/${name}_scheme.svg`);
    modelRow.appendChild(modelImg);

    const modelTitle = document.createElement("h1");
    modelTitle.innerHTML = name;
    modelRow.appendChild(modelTitle);

    const modelLink = document.createElement("a");
    modelLink.href = `${name}.php`
    modelRow.appendChild(modelLink);
    
    const linkSpanner = document.createElement("span");
    linkSpanner.setAttribute("class", "linkSpanner");
    modelLink.appendChild(linkSpanner);

    // Create Tags
    const tags = info.tags 

    const tagsCategory = Object.keys(tags)
    tagsCategory.forEach(cat => {
        simpleTags[cat] = (simpleTags[cat] || {});
        // Create Tag Category if not existant already
        var catExists = document.getElementById(`tagsCategory${cat}`);
        var catTagsExists = document.getElementById(`tagsCategory${cat}Row`);
        if (catExists == null) {
            const catDiv = document.createElement("div");
            catDiv.id = (`tagsCategory${cat}`)
            catDiv.classList.add("tagsCategory")
            const catHead = document.createElement("h3");
            catHead.innerHTML = cat;
            catDiv.appendChild(catHead);
            const catTags = document.createElement("div");
            catTags.id = `tagsCategory${cat}Row`
            catTags.classList.add("tagsRow");
            catDiv.appendChild(catTags);
            
            tagsBox.appendChild(catDiv);
            var catExists = document.getElementById(`tagsCategory${cat}`);
            var catTagsExists = document.getElementById(`tagsCategory${cat}Row`);
        }
        
        tags[cat].forEach(tag => {
            simpleTags[cat][tag] = (simpleTags[cat][tag] || []).concat([name])

            var tagExists = document.getElementById(`tagButton${cat}${tag}`);
            if (tagExists == null) {
                const tagButton = document.createElement("button");
                tagButton.innerHTML = tag;
                tagButton.id = (`tagButton${cat}${tag}`);
                tagButton.classList.add("clickable", "tag");
                tagButton.onclick = function() {
                    this.classList.toggle("active")
                    tagSelection()
                };
                catTagsExists.appendChild(tagButton);
                var tagExists = document.getElementById(`tagButton${cat}${tag}`);
            }
        }); 
    });
};

const searchParams = new URLSearchParams(window.location.search);

if (searchParams.has("appar")) {
    const urlAppar = searchParams.get("appar")
    document.getElementById(`tagButtonApparatus${urlAppar}`).classList.toggle("active")
}

tagSelection()

function tagSelection() {
    var activeTags = document.querySelectorAll('.tag.active')
    var activeModels = []
    activeTags.forEach(activeTag => {
        var catId = activeTag.parentElement.id.replace("tagsCategory", "")
        catId = catId.replace("Row", "")
        var tagId = activeTag.id.replace(`tagButton${catId}`, "")
        if (activeTags.length <= 1) {
            activeModels = activeModels.concat(simpleTags[catId][tagId])
        } else {
            var newActiveModels = []
            activeModels.forEach(modelName => {
                if (!(modelName in simpleTags[catId][tagId])) {
                    newActiveModels.push(modelName)
                }
            })
            activeModels = [...newActiveModels]
        }
    })

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
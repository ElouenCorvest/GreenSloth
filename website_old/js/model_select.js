function toggleTags() {
    document.querySelector('.tagsButton').classList.toggle('active');
    document.querySelector('.tagsBox').classList.toggle('open')
};

const tags = document.querySelectorAll('.tag');
const url = new URL(window.location)

tags.forEach(tag => {
    if (url.searchParams.has(tag.innerHTML)) {
        toggleTags()
        tag.classList.add('active')
    };

    tag.addEventListener('click', () => {
        if (tag.classList.contains('active')) {
            tag.classList.remove('active')
            url.searchParams.delete(tag.innerHTML)
            history.pushState(null, '', url)
        } else {
            tag.classList.add('active');
            url.searchParams.append(tag.innerHTML, true);
            history.pushState(null, '', url)
        };
    });
})

var modelSelector = document.getElementById("model-selector")

fetch("../js/models.json")
    .then(response => response.json())
    .then (models => {
        const modelSelector = document.getElementById("model-selector");
        models.forEach(model => {
            const modelRow = document.createElement("div");
            modelRow.setAttribute("class", "model-row");
            modelSelector.appendChild(modelRow);

            const modelImg = document.createElement("img");
            modelImg.setAttribute("src", `https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${model.name}/${model.name}_scheme.svg`);
            modelRow.appendChild(modelImg);

            const modelTitle = document.createElement("h1");
            modelTitle.innerHTML = model.name;
            modelRow.appendChild(modelTitle);

            const modelLink = document.createElement("a");
            modelLink.href = `../model_pages/${model.name}.html`
            modelRow.appendChild(modelLink);
            
            const linkSpanner = document.createElement("span");
            linkSpanner.setAttribute("class", "linkSpanner");
            modelLink.appendChild(linkSpanner);
        });
    });
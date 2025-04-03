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

models.forEach(name => {
    rowHTML = `
    <div class="model-row">
        <img src="https://raw.githubusercontent.com/ElouenCorvest/GreenSloth/e626f80fcd4f34c6ec468c17fb9e2b192d3a4ed2/models/${name}/${name}_scheme.svg"/>
        <h1>${name}</h1>
        <a href="../model_pages/${name}.php"><span class="linkSpanner"></span></a>
    </div>
    `
    modelSelector.innerHTML += rowHTML
})
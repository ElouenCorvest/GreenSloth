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
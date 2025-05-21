// Cite Modal
var citeModal = document.getElementById("citeModal")

// Open Cite Modal
var openCiteModal = document.getElementById("openCiteModal")
openCiteModal.onclick = function() {
    citeModal.classList.toggle("hidden")
    this.classList.toggle("active")
}

var citeModalContent = document.createElement("div")
citeModalContent.classList.add("modalContent")
citeModal.appendChild(citeModalContent)

// Modal Header
var citeModalHeader = document.createElement("div")
citeModalHeader.classList.add("modalHeader")
citeModalContent.appendChild(citeModalHeader)

// Modal Heading
var citeModalHeading = document.createElement("h2")
citeModalHeading.innerText = "How to Cite"
citeModalHeader.appendChild(citeModalHeading)

// Modal Close Button
var citeClose = document.createElement("span")
citeClose.classList.add("close")
citeClose.innerHTML = "&times;"
citeClose.onclick = function(){
    citeModal.classList.toggle("hidden");
    openCiteModal.classList.toggle("active")
}
citeModalHeader.appendChild(citeClose)

// Modal Body
var citeModalBody = document.createElement("div")
citeModalBody.classList.add("modalBody")
citeModalContent.appendChild(citeModalBody)

// Modal Body Text
var citeModalBodyText = document.createElement("p")
citeModalBodyText.innerText = "If you found this website helpful and used it for any publication, we kindly as you to cite us. Additonally, do not forget to cite all the models you use. For that you can find the appropriate DOIs on each page"
citeModalBody.appendChild(citeModalBodyText)

// Modal Body Copy Block
var citeModalBodyCopy = document.createElement("div")
citeModalBodyCopy.classList.add("copyBlock")
citeModalBody.appendChild(citeModalBodyCopy)

// Modal Body Copy Text
var citeModalBodyCopyText = document.createElement("p")
citeModalBodyCopyText.innerText = "INSERT CITATION HERE"

// Modal Body Copy Button
var citeModalBodyCopyButton = document.createElement("button")
citeModalBodyCopyButton.classList.add("copyButton")
citeModalBodyCopyButton.setAttribute("allow", "clipboard-read; clipboard-write")

// Modal Body Copy Button Text
var citeModalBodyCopyButtonText = document.createElement("span")
const orginalText = "<span class='iconify' data-icon='mdi:content-copy'></span> Copy"
citeModalBodyCopyButtonText.innerHTML = orginalText
citeModalBodyCopyButton.appendChild(citeModalBodyCopyButtonText)
citeModalBodyCopyButton.onclick = function() {
    navigator.clipboard.writeText(citeModalBodyCopyText.innerText)

    if (citeModalBodyCopyButton.classList.contains("active")) {
    } else {
        citeModalBodyCopyButton.classList.add("active")
    }
    citeModalBodyCopyButtonText.style.opacity = 0;

    setTimeout(function() {
        citeModalBodyCopyButtonText.innerHTML = "Copied!"
        citeModalBodyCopyButtonText.style.opacity = 1;
    }, 300)

    setTimeout(function() {
        citeModalBodyCopyButtonText.style.opacity = 0;
        citeModalBodyCopyButton.classList.remove("active")
        setTimeout(function() {
            citeModalBodyCopyButtonText.innerHTML = orginalText
            citeModalBodyCopyButtonText.style.opacity = 1;
        }, 300)

    }, 1000)
}





// Add elements to Copy Block
citeModalBodyCopy.appendChild(citeModalBodyCopyButton)
citeModalBodyCopy.appendChild(citeModalBodyCopyText)


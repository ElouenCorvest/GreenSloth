// Cite Modal
var citeModal = document.getElementById("citeModal")
// Open Cite Modal
var openCiteModal = document.getElementById("openCiteModal")
openCiteModal.onclick = function() {
    citeModal.classList.toggle("hidden")
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
citeClose.onclick = function(){citeModal.classList.toggle("hidden")}
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
const orginalText = "<span class='iconify' data-icon='mdi:content-copy'></span> Copy"
citeModalBodyCopyButton.innerHTML = orginalText
citeModalBodyCopyButton.setAttribute("allow", "clipboard-read; clipboard-write")
citeModalBodyCopyButton.onclick = function() {
    navigator.clipboard.writeText(citeModalBodyCopyText.innerText)

    citeModalBodyCopyButton.innerHTML = "Copied!"
    if (citeModalBodyCopyButton.classList.contains("active")) {
    } else {
        citeModalBodyCopyButton.classList.add("active")
    }

    const changeCopyButton = setTimeout(function() {
        citeModalBodyCopyButton.classList.remove("active")
        citeModalBodyCopyButton.innerHTML = orginalText;
        
    }, 2000)

    // setTimeout(citeModalBodyCopyButton.innerHTML = orginalText, 10000)
}

// Add elements to Copy Block
citeModalBodyCopy.appendChild(citeModalBodyCopyButton)
citeModalBodyCopy.appendChild(citeModalBodyCopyText)


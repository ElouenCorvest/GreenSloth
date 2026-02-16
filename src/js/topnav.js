// URL of page
const siteUrl = window.location.origin
import iconSrc from "../img/icon.svg"

// Top Nav Bar
var topnavBar = document.getElementById("topnav")

// Top Nav Bar Top
var topnavBarTop = document.createElement("div")
topnavBarTop.id = "topnav-top"
topnavBar.appendChild(topnavBarTop)

// Left Side
var topnavBarLeft = document.createElement("div")
topnavBarLeft.classList.add("topnav-left")
topnavBarTop.appendChild(topnavBarLeft)

var topnavBarLeftImage = document.createElement("img")
topnavBarLeftImage.src = iconSrc
topnavBarLeft.appendChild(topnavBarLeftImage)

// Center
var topnavBarCenter = document.createElement("div")
topnavBarCenter.classList.add("topnav-center")
topnavBarTop.appendChild(topnavBarCenter)

// Center Text when small media query
var topnavBarCenterMQSmallText = document.createElement("h3")
topnavBarCenterMQSmallText.classList.add("topnav-text")
topnavBarCenterMQSmallText.innerHTML = "Under Construction"
topnavBarCenter.appendChild(topnavBarCenterMQSmallText)

// Center Home
var topnavBarCenterHome = document.createElement("a")
topnavBarCenterHome.classList.add("tablinks", "topnav-link")
topnavBarCenterHome.href = window.origin
topnavBarCenterHome.innerHTML = "Home"
topnavBarCenter.appendChild(topnavBarCenterHome)

// Center Model Select
var topnavBarCenterModelSelect = document.createElement("a")
topnavBarCenterModelSelect.classList.add("tablinks", "topnav-link")
topnavBarCenterModelSelect.href = siteUrl + "/models_select.html"
topnavBarCenterModelSelect.innerHTML = "Models"
topnavBarCenter.appendChild(topnavBarCenterModelSelect)

// Center Cite
// var topnavBarCenterCite = document.createElement("button")
// topnavBarCenterCite.classList.add("tablinks", "topnav-link", "open-cite-modal")
// topnavBarCenterCite.innerHTML = "Cite"
// topnavBarCenter.appendChild(topnavBarCenterCite)

// Center Github
var topnavBarCenterGithub = document.createElement("a")
topnavBarCenterGithub.classList.add("tablinks", "logoWithText", "topnav-link")
topnavBarCenterGithub.href = "https://github.com/ElouenCorvest/GreenSloth/tree/main"
topnavBarCenterGithub.target = "_blank"
topnavBarCenterGithub.innerHTML = "GreenSloth"
topnavBarCenter.appendChild(topnavBarCenterGithub)

// Center Github Logo
var githubLogo = document.createElement("span")
githubLogo.classList.add("githubLogo")
topnavBarCenterGithub.prepend(githubLogo)

// Center Compare
var topnavBarCenterCompare = document.createElement("a")
topnavBarCenterCompare.classList.add("tablinks", "topnav-link")
topnavBarCenterCompare.href = "/Compare.html"
topnavBarCenterCompare.innerHTML = "Compare"
topnavBarCenter.appendChild(topnavBarCenterCompare)

// Center HowToUse
var topnavBarCenterHowToUse = document.createElement("a")
topnavBarCenterHowToUse.classList.add("tablinks", "topnav-link")
topnavBarCenterHowToUse.href = siteUrl + "/#HowToUse"
topnavBarCenterHowToUse.innerHTML = "How To Use"
topnavBarCenter.appendChild(topnavBarCenterHowToUse)

// Center AboutUs
var topnavBarCenterContribution = document.createElement("a")
topnavBarCenterContribution.classList.add("tablinks", "topnav-link")
topnavBarCenterContribution.href = siteUrl + "/AboutUs.html"
topnavBarCenterContribution.innerHTML = "About Us"
topnavBarCenter.appendChild(topnavBarCenterContribution)

// Center Impressum
var topnavBarCenterImpressum = document.createElement("a")
topnavBarCenterImpressum.classList.add("tablinks", "topnav-link")
topnavBarCenterImpressum.href = siteUrl + "/Impressum.html"
topnavBarCenterImpressum.innerHTML = "Impressum"
topnavBarCenter.appendChild(topnavBarCenterImpressum)

// Center Contribution
// var topnavBarCenterTodos = document.createElement("a")
// topnavBarCenterTodos.classList.add("tablinks", "topnav-link")
// topnavBarCenterTodos.href = siteUrl + "/src/html/todos.php"
// topnavBarCenterTodos.innerHTML = "To Dos"
// topnavBarCenter.appendChild(topnavBarCenterTodos)

// Right Side
var topnavBarRight = document.createElement("div")
topnavBarRight.classList.add("topnav-right")
topnavBarTop.appendChild(topnavBarRight)

// Center Text when small media query
var topnavBarRightText = document.createElement("h3")
topnavBarRightText.innerHTML = ""
topnavBarRight.appendChild(topnavBarRightText)

// Small Media Query Nav Links
var smNavLinkBox = document.createElement("div")
smNavLinkBox.id = "topnav-link-box"
smNavLinkBox.classList.add("hidden")
topnavBar.appendChild(smNavLinkBox)

// Right Burger
var topnavBarRightBurger = document.createElement("button")
topnavBarRightBurger.classList.add("stash--burger-classic", "clickable", "topnav-burger")
topnavBarRightBurger.addEventListener("click", function() {
    this.classList.toggle("active")
    smNavLinkBox.classList.toggle("hidden")
});
topnavBarRight.appendChild(topnavBarRightBurger)

// Nav Link Box Home
const allTabLinks = document.getElementsByClassName("topnav-link")

for (let element of allTabLinks) {
    var newElement = element.cloneNode(true)
    newElement.classList.replace("topnav-link", "topnav-link-box-link")
    smNavLinkBox.appendChild(newElement)
}

// Get out of Link Box when clicking anywhere else
var allSiblings = topnavBar.parentElement.children

for (let element of allSiblings) {
    if (element != topnavBar) {
        element.addEventListener("click", function() {
            smNavLinkBox.classList.add("hidden")
        });
    }
}
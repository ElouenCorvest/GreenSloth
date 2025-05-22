// URL of page
const url = window.location.href
const urlHere = window.location.pathname

// Top Nav Bar
var topnavBar = document.getElementById("topnav")

// Left Side
var topnavBarLeft = document.createElement("div")
topnavBarLeft.classList.add("topnav-left")
topnavBar.appendChild(topnavBarLeft)

var topnavBarLeftImage = document.createElement("img")
topnavBarLeftImage.src = "../icon.svg"
topnavBarLeft.appendChild(topnavBarLeftImage)

// Center
var topnavBarCenter = document.createElement("div")
topnavBarCenter.classList.add("topnav-center")
topnavBar.appendChild(topnavBarCenter)

// Center Home
var topnavBarCenterHome = document.createElement("a")
topnavBarCenterHome.classList.add("tablinks")
topnavBarCenterHome.href = "../../index.html"
topnavBarCenterHome.innerHTML = "Home"
topnavBarCenter.appendChild(topnavBarCenterHome)

// Center Model Select
var topnavBarCenterModelSelect = document.createElement("a")
topnavBarCenterModelSelect.classList.add("tablinks")
topnavBarCenterModelSelect.href = "/src/html/models_select.html"
topnavBarCenterModelSelect.innerHTML = "Models"
topnavBarCenter.appendChild(topnavBarCenterModelSelect)

// Center Cite
var topnavBarCenterCite = document.createElement("button")
topnavBarCenterCite.classList.add("tablinks")
topnavBarCenterCite.id = "openCiteModal"
topnavBarCenterCite.innerHTML = "Cite"
topnavBarCenter.appendChild(topnavBarCenterCite)

// Center Github
var topnavBarCenterGithub = document.createElement("a")
topnavBarCenterGithub.classList.add("tablinks", "logoWithText")
topnavBarCenterGithub.href = "https://github.com/ElouenCorvest/GreenSloth/tree/main"
topnavBarCenterGithub.target = "_blank"
topnavBarCenterGithub.innerHTML = "GreenSloth"
topnavBarCenter.appendChild(topnavBarCenterGithub)

// Center Github Logo
var githubLogo = document.createElement("span")
githubLogo.classList.add("githubLogo")
topnavBarCenterGithub.prepend(githubLogo)

// Center HowToUse
var topnavBarCenterHowToUse = document.createElement("a")
topnavBarCenterHowToUse.classList.add("tablinks")
topnavBarCenterHowToUse.href = "../../slides/HowToUse"
topnavBarCenterHowToUse.innerHTML = "How To Use"
topnavBarCenter.appendChild(topnavBarCenterHowToUse)

// Center Contribution
var topnavBarCenterContribution = document.createElement("a")
topnavBarCenterContribution.classList.add("tablinks")
topnavBarCenterContribution.href = "/src/html/contribution.html"
topnavBarCenterContribution.innerHTML = "Contribution"
topnavBarCenter.appendChild(topnavBarCenterContribution)

// Right Side
var topnavBarRight = document.createElement("div")
topnavBarRight.classList.add("topnav-right")
topnavBar.appendChild(topnavBarRight)
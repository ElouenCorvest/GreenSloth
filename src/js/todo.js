import chroma from 'chroma-js';

// Style sheet
var cssSheet = window.document.styleSheets[0]

// Unchecked Box
const uncheckedBox = document.createElement("span")
uncheckedBox.classList.add("ri--checkbox-blank-circle-line")

// Checked Box
const checkedBox = document.createElement("span")
checkedBox.classList.add("ri--checkbox-circle-line")

// Get Complete progress bar
var allProgress = document.getElementById("all-progress")
var allProgressLabel = document.getElementById("all-progress-label")

// Get all todos
var todos = document.getElementsByClassName("todo")
console.log(todos)
Array.from(todos).forEach(todo => {
    console.log(todo)
    if (todo.classList.contains("todo-done")) {
        todo.prepend(checkedBox.cloneNode(true))
    } else {
        todo.prepend(uncheckedBox.cloneNode(true))
    }
});

// Get all done todos
var doneTodos = document.getElementsByClassName("todo-done")

// Color gradient
var progressGradient = chroma.scale(["CC2936", "FFC100", "57A773"]).domain([0, 100])

// Change all progress value
var allProgressNum = (doneTodos.length / todos.length) * 100
allProgress.value = allProgressNum
cssSheet.insertRule(`.progress-bar > ::-webkit-progress-value {background-color: ${progressGradient(allProgressNum).css()};}`, 0)
allProgressLabel.innerHTML = `${allProgressNum}%`


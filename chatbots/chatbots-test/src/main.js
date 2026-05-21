import { ChatOllama } from "@langchain/ollama"
import { marked } from "marked"

const chatModel = new ChatOllama({
    model: "qwen3.5",
    temperature: 0,
    maxRetries: 2,
})

const page = document.querySelector("#app")

// 1. Create a main container for the chat interface
const chatContainer = document.createElement("div")
chatContainer.style.display = "flex"
chatContainer.style.flexDirection = "column"
chatContainer.style.maxWidth = "600px"
chatContainer.style.margin = "20px auto"
chatContainer.style.fontFamily = "system-ui, -apple-system, sans-serif"
page.appendChild(chatContainer)

// 2. Create the scrolling chat area
const chatHistory = document.createElement("div")
chatHistory.style.flex = "1"
chatHistory.style.minHeight = "400px"
chatHistory.style.maxHeight = "600px"
chatHistory.style.overflowY = "auto"
chatHistory.style.border = "1px solid #e0e0e0"
chatHistory.style.borderRadius = "8px"
chatHistory.style.padding = "15px"
chatHistory.style.backgroundColor = "#f9f9f9"
chatHistory.style.marginBottom = "15px"
chatContainer.appendChild(chatHistory)

// 3. Create the input area
const messageBox = document.createElement("input")
messageBox.type = "text"
messageBox.style.width = "100%"
messageBox.style.padding = "12px"
messageBox.style.border = "1px solid #ccc"
messageBox.style.borderRadius = "6px"
messageBox.style.boxSizing = "border-box"
messageBox.style.fontSize = "16px"
messageBox.placeholder = "Type your message here..."
chatContainer.appendChild(messageBox)

// Helper function to append styled bubbles to the chat
function appendMessageBubble(text, isUser = false) {
    // Wrapper to handle left/right alignment
    const row = document.createElement("div")
    row.style.display = "flex"
    row.style.justifyContent = isUser ? "flex-end" : "flex-start"
    row.style.marginBottom = "12px"

    // The actual bubble
    const bubble = document.createElement("div")
    bubble.style.maxWidth = "75%"
    bubble.style.padding = "10px 14px"
    bubble.style.borderRadius = "14px"
    bubble.style.fontSize = "15px"
    bubble.style.lineHeight = "1.4"

    if (isUser) {
        bubble.style.backgroundColor = "#007aff" // Classic chat blue
        bubble.style.color = "#ffffff"
        bubble.style.borderBottomRightRadius = "2px" // Subtle chat tail
        bubble.textContent = text 
    } else {
        bubble.style.backgroundColor = "#e9e9eb" // Classic gray
        bubble.style.color = "#000000"
        bubble.style.borderBottomLeftRadius = "2px"
        bubble.innerHTML = marked.parse(text) // Render formatted markdown
    }

    row.appendChild(bubble)
    chatHistory.appendChild(row)
    
    // Auto-scroll to the bottom of the chat
    chatHistory.scrollTop = chatHistory.scrollHeight
    
    return bubble // Return reference if we need to modify it later (like for loading states)
}

async function getAiResponse(message) {
    // Create a temporary bubble for the typing indicator
    const loadingBubble = appendMessageBubble("Thinking...", false)
    
    try {
        const msg = await chatModel.invoke(message)
        // Replace typing text with the final markdown-parsed response
        loadingBubble.innerHTML = marked.parse(msg.content)
    } catch (error) {
        loadingBubble.textContent = "Error fetching response. Please try again."
        loadingBubble.style.backgroundColor = "#ffdddd"
        loadingBubble.style.color = "#d00000"
    }
    
    // Adjust scroll again after content height changes
    chatHistory.scrollTop = chatHistory.scrollHeight
}

// Event Listener
messageBox.addEventListener("keypress", function(event) {
    if (event.key === "Enter" && messageBox.value.trim() !== "") {
        const userMessage = messageBox.value.trim()
        
        // 1. Post user message instantly
        appendMessageBubble(userMessage, true)
        
        // 2. Clear input field immediately
        messageBox.value = ""
        
        // 3. Trigger AI response
        getAiResponse(userMessage)
    }
})
const textarea = document.querySelector("textarea");
const sendButton = document.querySelector(".send-button");

// Send on Enter key (Shift+Enter for new line)
textarea.addEventListener("keydown", function(e) {
    if (e.key == "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
})
// Send on button click
sendButton.addEventListener("click", sendMessage);

async function sendMessage() {
const message = textarea.value.trim()
if (!message) return 
textarea.value = ""
addMessage("user", message)
showTyping(true)

}
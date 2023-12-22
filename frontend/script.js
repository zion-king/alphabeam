function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === '') {
        return;
    }

    // Display user message
    displayMessage('user', userInput);

    // Simulate a bot response
    const botResponse = "Hi! How can I assist you today?";
    displayMessage('bot', botResponse);

    // Clear user input
    document.getElementById('user-input').value = '';
}

function displayMessage(sender, message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageContainer = document.createElement('div');
    const messageContent = document.createElement('div');

    messageContainer.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    messageContent.classList.add('message-content');
    messageContent.innerText = message;

    messageContainer.appendChild(messageContent);
    chatMessages.appendChild(messageContainer);

    // Scroll to the bottom to show the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleKeyDown(event) {
    // Prevent form submission on Enter key press
    if (event.key === 'Enter') {
        event.preventDefault();
    }
}

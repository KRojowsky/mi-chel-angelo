document.querySelector('.chat-icon').addEventListener('click', function() {
    document.getElementById('chatPopup').style.display = 'block';
});

function closeChatPopup() {
    document.getElementById('chatPopup').style.display = 'none';
}

function sendMessage(event) {
    if (event && event.key !== 'Enter') return;

    let messageInput = document.getElementById('chatInput');
    let messageText = messageInput.value.trim();

    if (messageText !== '') {
        appendUserMessage(messageText);
        messageInput.value = '';

        checkUserMessage(messageText);
    }
}

function appendUserMessage(message) {
    let chatMessages = document.getElementById('chatMessages');
    let messageDiv = document.createElement('div');
    messageDiv.className = 'message-user';
    messageDiv.innerHTML = `
        <div class="message-text">
            <p>${message}</p>
        </div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addUserMessage(messageText) {
    appendUserMessage(messageText);
    checkUserMessage(messageText);
}

function checkUserMessage(messageText) {
    const lowerCaseMessage = messageText.toLowerCase();
    if (lowerCaseMessage.includes('sprawdź status zamówienia') || lowerCaseMessage.includes('status zamówienia')) {
        setTimeout(function() {
            sendMessageFromBot('Podaj numer zamówienia:');
        }, 1000);
    }
}

function sendMessageFromBot(messageText) {
    let chatMessages = document.getElementById('chatMessages');
    let messageDiv = document.createElement('div');
    messageDiv.className = 'message-bot';
    messageDiv.innerHTML = `
        <div class="chatbot-img-container">
            <img src="${staticImagePath}" alt="ikona chatbota" class="chatbot-img">
        </div>
        <div class="message-text">
            <p>${messageText}</p>
        </div>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

let staticImagePath = document.getElementById('static-image-path').value;s
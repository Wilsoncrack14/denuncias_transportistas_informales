document.addEventListener('DOMContentLoaded', () => {
    const chatFab = document.getElementById('chatFab');
    const chatWidget = document.getElementById('chatWidget');
    const closeChatBtn = document.getElementById('closeChatBtn');
    const chatContainer = document.getElementById('chatContainer');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');

    // Toggle Chat
    function toggleChat() {
        chatWidget.classList.toggle('active');
        if (chatWidget.classList.contains('active')) {
            messageInput.focus();
            chatContainer.scrollTop = chatContainer.scrollHeight;
        } else {
            // Reset chat state when closed
            chatContainer.innerHTML = `
                <div class="message other-message">
                    <strong>Sistema:</strong> ¡Hola! ¿En qué puedo ayudarte hoy?
                </div>
            `;
            messageInput.value = '';
        }
    }

    chatFab.addEventListener('click', toggleChat);
    closeChatBtn.addEventListener('click', toggleChat);

    // WebSocket Logic
    const userId = 'user_' + Math.floor(Math.random() * 1000);
    console.log('Connecting as:', userId);

    let ws;

    function connectWebSocket() {
        ws = new WebSocket(`ws://localhost:8002/ws/${userId}`);

        ws.onopen = () => {
            console.log('Connected to Chat Service');
        };

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const isMe = data.sender === userId;
            addMessage(data.sender, data.content, isMe ? 'my-message' : 'other-message');
        };

        ws.onclose = () => {
            console.log('Disconnected. Reconnecting in 3s...');
            setTimeout(connectWebSocket, 3000);
        };
    }

    connectWebSocket();

    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message && ws.readyState === WebSocket.OPEN) {
            ws.send(message);
            messageInput.value = '';
        }
    }

    function addMessage(sender, text, className) {
        const div = document.createElement('div');
        div.classList.add('message', className);
        div.innerHTML = `<strong>${sender === userId ? 'Yo' : sender}:</strong> ${text}`;
        chatContainer.appendChild(div);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});

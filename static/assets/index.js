async function sendMessage() {
  const input = document.getElementById('messageInput');
  const message = input.value.trim();
  if (!message) return;

  appendMessage('user', message);
  input.value = '';

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  const data = await response.json();
  appendMessage('bot', data.response);
}

function appendMessage(role, text) {
  const msgDiv = document.createElement('div');
  msgDiv.className = role;
  msgDiv.innerText = text;

  const messages = document.getElementById('messages');
  messages.appendChild(msgDiv);
  messages.scrollTop = messages.scrollHeight;
}

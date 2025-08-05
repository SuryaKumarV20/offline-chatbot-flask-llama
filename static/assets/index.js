document.getElementById("chatForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  await sendMessage();
});

async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  input.value = "";
  input.disabled = true;

  appendMessage("bot", "Typing...", true);

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();

    removeTyping();
    appendMessage("bot", data.response);
  } catch (error) {
    removeTyping();
    appendMessage("bot", "❌ Error: Failed to connect to the chatbot.");
  } finally {
    input.disabled = false;
    input.focus();
  }
}

function appendMessage(role, text, isTyping = false) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${role}`;
  msgDiv.innerText = text;

  const time = document.createElement("div");
  time.className = "timestamp";
  time.innerText = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  msgDiv.appendChild(time);

  const container = document.getElementById("messages");
  container.appendChild(msgDiv);
  container.scrollTop = container.scrollHeight;

  if (isTyping) msgDiv.classList.add("typing");
}

function removeTyping() {
  const container = document.getElementById("messages");
  const typing = container.querySelector(".typing");
  if (typing) container.removeChild(typing);
}

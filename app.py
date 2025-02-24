import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# HTML шаблон с Puter.js на клиентской стороне
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Claude 3.5 Sonnet Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
        .message {
            margin: 5px 0;
            padding: 5px;
        }
        .user {
            background-color: #e6f3ff;
            margin-left: 20%;
        }
        .assistant {
            background-color: #f0f0f0;
            margin-right: 20%;
        }
        #input {
            width: 100%;
            padding: 5px;
        }
    </style>
</head>
<body>
    <script src="https://js.puter.com/v2/"></script>
    <h1>Чат с Claude 3.5 Sonnet</h1>
    <div id="chat" class="chat-container"></div>
    <input id="input" type="text" placeholder="Введите сообщение..." onkeypress="handleKeyPress(event)">
    <button onclick="sendMessage()">Отправить</button>
    <button onclick="clearHistory()" style="margin-left: 10px;">Очистить историю</button>

    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');
        const MAX_HISTORY_LENGTH = 10;  // Ограничение длины истории

        // Загружаем историю из localStorage при загрузке страницы
        let conversationHistory = JSON.parse(localStorage.getItem('conversationHistory')) || [];

        // Функция для сохранения истории в localStorage
        function saveHistory() {
            localStorage.setItem('conversationHistory', JSON.stringify(conversationHistory));
        }

        // Функция для очистки истории
        function clearHistory() {
            conversationHistory = [];
            saveHistory();
            chat.innerHTML = '';  // Очищаем чат на странице
        }

        // Функция для добавления сообщения в чат
        function addMessage(content, isUser) {
            const message = document.createElement('div');
            message.className = `message ${isUser ? 'user' : 'assistant'}`;
            message.textContent = content;
            chat.appendChild(message);
            chat.scrollTop = chat.scrollHeight;
        }

        // Отображаем сохраненную историю при загрузке страницы
        conversationHistory.forEach(msg => {
            addMessage(msg.content, msg.role === 'user');
        });

        async function sendMessage() {
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, true);
            input.value = '';

            try {
                // Добавляем сообщение пользователя в историю
                conversationHistory.push({ role: 'user', content: message });
                conversationHistory = conversationHistory.slice(-MAX_HISTORY_LENGTH);  // Ограничиваем длину истории
                saveHistory();  // Сохраняем историю

                // Вызываем Puter.js AI на клиентской стороне с потоковой передачей
                const response = await puter.ai.chat(conversationHistory, {
                    model: 'claude-3-5-sonnet',
                    stream: true
                });

                let fullResponse = '';
                for await (const part of response) {
                    fullResponse += part?.text || '';
                    // Обновляем сообщение по мере получения частей ответа
                    const lastMessage = chat.querySelector('.message.assistant:last-child');
                    if (lastMessage) {
                        lastMessage.textContent = fullResponse;
                    } else {
                        addMessage(fullResponse, false);
                    }
                }

                // Добавляем полный ответ ИИ в историю
                conversationHistory.push({ role: 'assistant', content: fullResponse });
                conversationHistory = conversationHistory.slice(-MAX_HISTORY_LENGTH);  // Ограничиваем длину истории
                saveHistory();  // Сохраняем историю

            } catch (error) {
                addMessage('Ошибка: ' + error.message, false);
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
"""

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def serve_chat():
    return HTML_TEMPLATE

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"message": "No favicon"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

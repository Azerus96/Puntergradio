import gradio as gr
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
import logging
from typing import List, Dict

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище для истории разговора (в памяти, для простоты)
conversation_history: List[Dict[str, str]] = []

# HTML шаблон с Puter.js (с изменениями для отображения только текущих сообщений)
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

    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');

        function addMessage(content, isUser) {
            const message = document.createElement('div');
            message.className = `message ${isUser ? 'user' : 'assistant'}`;
            message.textContent = content;
            chat.appendChild(message);
            chat.scrollTop = chat.scrollHeight;
        }

        async function sendMessage() {
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, true);
            input.value = '';

            try {
                // Отправляем сообщение на бэкенд через fetch
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                if (data.error) {
                    addMessage('Ошибка: ' + data.error, false);
                } else {
                    addMessage(data.response, false);
                }
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

# Создаем FastAPI приложение
app = FastAPI()

# Добавляем маршрут для корневого пути
@app.get("/", response_class=HTMLResponse)
async def serve_chat():
    return HTML_TEMPLATE

# Добавляем маршрут для favicon.ico (опционально)
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return {"message": "No favicon"}

# Добавляем маршрут для обработки сообщений
@app.post("/chat")
async def chat_endpoint(request: Dict[str, str]):
    global conversation_history
    user_message = request.get("message")

    if not user_message:
        return {"error": "Сообщение не может быть пустым"}

    try:
        # Добавляем сообщение пользователя в историю
        conversation_history.append({"role": "user", "content": user_message})

        # Формируем полный контекст для ИИ (включая всю историю)
        messages = conversation_history.copy()

        # Отправляем запрос к ИИ с полной историей
        response = await puter.ai.chat(messages, {
            model: 'claude-3-5-sonnet',
            stream: True
        })

        full_response = ""
        for await part in response:
            full_response += part?.text || ""

        # Добавляем ответ ИИ в историю
        conversation_history.append({"role": "assistant", "content": full_response})

        # Возвращаем только последний ответ ИИ
        return {"response": full_response}

    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {str(e)}")
        return {"error": str(e)}

# Создаем Gradio интерфейс (оставляем для совместимости, но он не используется)
with gr.Blocks() as demo:
    gr.HTML(lambda: HTML_TEMPLATE)

# Запускаем приложение
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

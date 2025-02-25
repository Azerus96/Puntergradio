Вы правы, я допустил ошибку в форматировании. Вот все коды, аккуратно оформленные в отдельных блоках:

### app.py
```python
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --bg-color: #ffffff;
            --text-color: #000000;
            --user-bg: #e6f3ff;
            --assistant-bg: #f0f0f0;
            --border-color: #ccc;
            --header-color: #333;
            --button-bg: #4a90e2;
            --button-text: white;
            --input-bg: white;
            --code-bg: #f5f5f5;
            --code-border: #ddd;
        }
        
        .dark-mode {
            --bg-color: #1e1e1e;
            --text-color: #e0e0e0;
            --user-bg: #2c4b6e;
            --assistant-bg: #2d2d2d;
            --border-color: #444;
            --header-color: #e0e0e0;
            --button-bg: #2a5a9e;
            --button-text: #e0e0e0;
            --input-bg: #333;
            --code-bg: #2d2d2d;
            --code-border: #444;
        }
        
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: var(--bg-color);
            color: var(--text-color);
            transition: background-color 0.3s, color 0.3s;
        }
        
        h1 {
            color: var(--header-color);
        }
        
        .chat-container {
            height: 400px;
            overflow-y: auto;
            border: 1px solid var(--border-color);
            padding: 10px;
            margin-bottom: 10px;
            background-color: var(--bg-color);
        }
        
        .message {
            margin: 5px 0;
            padding: 5px;
            border-radius: 5px;
            word-wrap: break-word;
        }
        
        .user {
            background-color: var(--user-bg);
            margin-left: 20%;
        }
        
        .assistant {
            background-color: var(--assistant-bg);
            margin-right: 20%;
        }
        
        #input {
            width: calc(100% - 12px);
            padding: 8px;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            background-color: var(--input-bg);
            color: var(--text-color);
        }
        
        button {
            padding: 8px 12px;
            background-color: var(--button-bg);
            color: var(--button-text);
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px 5px 5px 0;
        }
        
        button:hover {
            opacity: 0.9;
        }
        
        .toolbar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        
        .toolbar-left, .toolbar-right {
            display: flex;
            gap: 5px;
        }
        
        .code-block {
            background-color: var(--code-bg);
            border: 1px solid var(--code-border);
            border-radius: 4px;
            padding: 10px;
            margin: 10px 0;
            position: relative;
            font-family: monospace;
            white-space: pre-wrap;
        }
        
        .copy-button {
            position: absolute;
            top: 5px;
            right: 5px;
            padding: 3px 6px;
            font-size: 12px;
            background-color: var(--button-bg);
            color: var(--button-text);
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        
        .file-input-container {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        
        #file-list {
            margin-top: 5px;
            font-size: 0.9em;
        }
        
        .file-item {
            display: flex;
            align-items: center;
            margin-bottom: 5px;
        }
        
        .remove-file {
            margin-left: 5px;
            cursor: pointer;
            color: red;
        }
        
        /* Адаптивный дизайн для мобильных устройств */
        @media (max-width: 600px) {
            body {
                padding: 10px;
            }
            
            .toolbar {
                flex-direction: column;
                gap: 10px;
            }
            
            .toolbar-left, .toolbar-right {
                justify-content: center;
            }
            
            .user {
                margin-left: 10%;
            }
            
            .assistant {
                margin-right: 10%;
            }
            
            button {
                padding: 10px;
            }
            
            h1 {
                font-size: 1.5em;
                text-align: center;
            }
        }
        
        /* Стили для полноэкранного режима */
        .fullscreen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            margin: 0;
            max-width: none;
            padding: 20px;
            box-sizing: border-box;
        }
        
        .fullscreen .chat-container {
            height: calc(100vh - 200px);
        }
    </style>
</head>
<body>
    <script src="https://js.puter.com/v2/"></script>
    <h1>Чат с Claude 3.5 Sonnet</h1>
    
    <div class="toolbar">
        <div class="toolbar-left">
            <button id="dark-mode-toggle" onclick="toggleDarkMode()">🌙 Тёмный режим</button>
            <button id="fullscreen-toggle" onclick="toggleFullscreen()">⛶ Полный экран</button>
        </div>
        <div class="toolbar-right">
            <button onclick="clearHistory()">🗑️ Очистить историю</button>
        </div>
    </div>
    
    <div id="chat" class="chat-container"></div>
    
    <div class="file-input-container">
        <input type="file" id="file-input" multiple>
        <div id="file-list"></div>
    </div>
    
    <input id="input" type="text" placeholder="Введите сообщение..." onkeypress="handleKeyPress(event)">
    <button onclick="sendMessage()">Отправить</button>

    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');
        const fileInput = document.getElementById('file-input');
        const fileList = document.getElementById('file-list');
        const MAX_HISTORY_LENGTH = 9999;  // Увеличенное ограничение длины истории
        let selectedFiles = [];
        
        // Загружаем настройки темы из localStorage
        const isDarkMode = localStorage.getItem('darkMode') === 'true';
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
            document.getElementById('dark-mode-toggle').textContent = '☀️ Светлый режим';
        }
        
        // Функция переключения темного режима
        function toggleDarkMode() {
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', isDark);
            document.getElementById('dark-mode-toggle').textContent = isDark ? '☀️ Светлый режим' : '🌙 Тёмный режим';
        }
        
        // Функция переключения полноэкранного режима
        function toggleFullscreen() {
            const isFullscreen = document.body.classList.toggle('fullscreen');
            document.getElementById('fullscreen-toggle').textContent = isFullscreen ? '⛶ Выйти из полного экрана' : '⛶ Полный экран';
        }

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
        
        // Обработка выбора файлов
        fileInput.addEventListener('change', function(e) {
            handleFileSelection(e.target.files);
        });
        
        // Функция для обработки выбранных файлов
        async function handleFileSelection(files) {
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                
                // Проверяем, не превышает ли размер файла 10 МБ
                if (file.size > 10 * 1024 * 1024) {
                    alert(`Файл ${file.name} слишком большой. Максимальный размер - 10 МБ.`);
                    continue;
                }
                
                // Добавляем файл в список выбранных
                selectedFiles.push(file);
                
                // Отображаем файл в списке
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <span>${file.name} (${formatFileSize(file.size)})</span>
                    <span class="remove-file" data-index="${selectedFiles.length - 1}">✖</span>
                `;
                fileList.appendChild(fileItem);
            }
            
            // Очищаем input, чтобы можно было выбрать те же файлы повторно
            fileInput.value = '';
            
            // Добавляем обработчики для кнопок удаления
            document.querySelectorAll('.remove-file').forEach(button => {
                button.addEventListener('click', function() {
                    const index = parseInt(this.getAttribute('data-index'));
                    removeFile(index);
                });
            });
        }
        
        // Функция для удаления файла из списка
        function removeFile(index) {
            selectedFiles.splice(index, 1);
            updateFileList();
        }
        
        // Обновление отображения списка файлов
        function updateFileList() {
            fileList.innerHTML = '';
            selectedFiles.forEach((file, index) => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <span>${file.name} (${formatFileSize(file.size)})</span>
                    <span class="remove-file" data-index="${index}">✖</span>
                `;
                fileList.appendChild(fileItem);
            });
            
            document.querySelectorAll('.remove-file').forEach(button => {
                button.addEventListener('click', function() {
                    const index = parseInt(this.getAttribute('data-index'));
                    removeFile(index);
                });
            });
        }
        
        // Форматирование размера файла
        function formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
            else return (bytes / 1048576).toFixed(1) + ' MB';
        }

        // Функция для обработки кода в сообщениях
        function processCodeBlocks(text) {
            // Регулярное выражение для поиска блоков кода (между ```)
            const codeBlockRegex = /```([\s\S]*?)```/g;
            
            // Заменяем блоки кода на специальные элементы
            return text.replace(codeBlockRegex, function(match, code) {
                const language = code.split('\\n')[0].trim();
                const codeContent = language && !language.includes(' ') ? 
                    code.substring(language.length).trim() : code;
                
                return `<div class="code-block">
                    ${language && !language.includes(' ') ? `<div class="language">${language}</div>` : ''}
                    <button class="copy-button" onclick="copyCode(this)">Копировать</button>
                    <pre>${codeContent}</pre>
                </div>`;
            });
        }
        
        // Функция для копирования кода
        function copyCode(button) {
            const codeBlock = button.nextElementSibling;
            const textToCopy = codeBlock.textContent;
            
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    button.textContent = 'Скопировано!';
                    setTimeout(() => {
                        button.textContent = 'Копировать';
                    }, 2000);
                })
                .catch(err => {
                    console.error('Ошибка при копировании: ', err);
                    button.textContent = 'Ошибка';
                    setTimeout(() => {
                        button.textContent = 'Копировать';
                    }, 2000);
                });
        }

        // Функция для добавления сообщения в чат
        function addMessage(content, isUser) {
            const message = document.createElement('div');
            message.className = `message ${isUser ? 'user' : 'assistant'}`;
            
            if (isUser) {
                message.textContent = content;
            } else {
                // Обрабатываем блоки кода в сообщениях ассистента
                message.innerHTML = processCodeBlocks(content);
            }
            
            chat.appendChild(message);
            chat.scrollTop = chat.scrollHeight;
        }

        // Отображаем сохраненную историю при загрузке страницы
        conversationHistory.forEach(msg => {
            addMessage(msg.content, msg.role === 'user');
        });

        async function sendMessage() {
            const message = input.value.trim();
            if (!message && selectedFiles.length === 0) return;

            // Добавляем сообщение пользователя в чат
            let userMessage = message;
            
            // Если есть прикрепленные файлы, добавляем информацию о них
            if (selectedFiles.length > 0) {
                userMessage += `\n\nПрикрепленные файлы: ${selectedFiles.map(f => f.name).join(', ')}`;
            }
            
            addMessage(userMessage, true);
            input.value = '';

            try {
                // Подготавливаем сообщения для отправки
                let messagesToSend = [];
                
                // Добавляем сообщение пользователя
                messagesToSend.push({ role: 'user', content: message });
                
                // Если есть файлы, обрабатываем их
                if (selectedFiles.length > 0) {
                    for (const file of selectedFiles) {
                        try {
                            // Читаем содержимое файла
                            const fileContent = await readFileAsText(file);
                            
                            // Добавляем содержимое файла как отдельное сообщение
                            messagesToSend.push({
                                role: 'user',
                                content: `Содержимое файла ${file.name}:\n\n${fileContent}`
                            });
                        } catch (error) {
                            console.error(`Ошибка при чтении файла ${file.name}:`, error);
                            addMessage(`Ошибка при чтении файла ${file.name}: ${error.message}`, false);
                        }
                    }
                    
                    // Очищаем список файлов после отправки
                    selectedFiles = [];
                    fileList.innerHTML = '';
                }
                
                // Объединяем с историей, но соблюдаем ограничение
                const fullHistory = [...conversationHistory, ...messagesToSend];
                const historyToSend = fullHistory.slice(-MAX_HISTORY_LENGTH);
                
                // Добавляем сообщения пользователя в историю
                conversationHistory = historyToSend;
                saveHistory();

                // Вызываем Puter.js AI на клиентской стороне с потоковой передачей
                const response = await puter.ai.chat(historyToSend, {
                    model: 'claude-3-5-sonnet',
                    stream: true
                });

                let fullResponse = '';
                for await (const part of response) {
                    fullResponse += part?.text || '';
                    // Обновляем сообщение по мере получения частей ответа
                    const lastMessage = chat.querySelector('.message.assistant:last-child');
                    if (lastMessage) {
                        lastMessage.innerHTML = processCodeBlocks(fullResponse);
                    } else {
                        addMessage(fullResponse, false);
                    }
                }

                // Добавляем полный ответ ИИ в историю
                conversationHistory.push({ role: 'assistant', content: fullResponse });
                saveHistory();  // Сохраняем историю

            } catch (error) {
                addMessage('Ошибка: ' + error.message, false);
            }
        }
        
        // Функция для чтения файла как текст
        function readFileAsText(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = event => resolve(event.target.result);
                reader.onerror = error => reject(error);
                reader.readAsText(file);
            });
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Глобальная функция для копирования кода
        window.copyCode = function(button) {
            const codeBlock = button.nextElementSibling;
            const textToCopy = codeBlock.textContent;
            
            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    button.textContent = 'Скопировано!';
                    setTimeout(() => {
                        button.textContent = 'Копировать';
                    }, 2000);
                })
                .catch(err => {
                    console.error('Ошибка при копировании: ', err);
                    button.textContent = 'Ошибка';
                    setTimeout(() => {
                        button.textContent = 'Копировать';
                    }, 2000);
                });
        };
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

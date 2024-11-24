function renderMarkdown(markdownText) {
    // Converte o texto Markdown para HTML
    const rawHtml = marked.parse(markdownText);
    
    // Sanitiza o HTML gerado para remover qualquer conteúdo malicioso
    return DOMPurify.sanitize(rawHtml);
}


// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatInput = document.querySelector('#helpModal input[type="text"]');
    const sendButton = document.querySelector('#helpModal button[class*="absolute"]');
    const modalContent = document.querySelector('#helpModal');
    
    // Create a messages container
    const messagesContainer = document.createElement('div');
    messagesContainer.className = 'messages-container mt-4 max-h-[300px] overflow-y-auto';
    // Insert messages container before the input div
    modalContent.insertBefore(messagesContainer, document.querySelector('#helpModal .mt-6'));

    // Quick action buttons
    const actionButtons = document.querySelectorAll('#helpModal .grid button');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const buttonText = this.textContent.trim();
            sendMessage(buttonText);
        });
    });

    async function sendMessage(text) {
        if (!text) return;
    
        // Log para verificar o texto enviado
        console.log('Sending message:', text);
    
        // Create and append user message
        appendMessage(text, 'user');
    
        try {
            // Usando as variáveis communityId e userId passadas do Django
            const response = await fetch(askQuestionUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    text: text
                })
            });
    
            const data = await response.json();
    
            if (data.data && data.data.text) {
                appendMessage(data.data.text, 'bot');
            } else if (data.error) {
                console.error('Error from backend:', data.error);
                appendMessage('Desculpe, ocorreu um erro ao processar sua solicitação.', 'bot');
            }
        } catch (error) {
            //console.error('Error:', error);
            appendMessage('Desculpe, ocorreu um erro ao processar sua solicitação.', 'bot');
        }
    
        chatInput.value = '';
    }
    
    
    // Append message to chat
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender} mb-4 p-3 rounded-lg ${
            sender === 'user' 
                ? 'bg-[#8ABF17] text-white ml-auto' 
                : 'bg-gray-100 text-black'
        }`;
        messageDiv.style.maxWidth = '80%';
        
        if (sender === 'bot') {
            // Renderiza o texto do bot como Markdown e sanitiza
            messageDiv.innerHTML = renderMarkdown(text);
        } else {
            // Para mensagens do usuário, mostra o texto diretamente
            messageDiv.textContent = text;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }      

    // Event listeners
    sendButton.addEventListener('click', () => {
        sendMessage(chatInput.value);
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage(chatInput.value);
        }
    });

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Add CSS styles
const style = document.createElement('style');
style.textContent = `
    .message.user {
        border-radius: 15px 15px 0 15px;
    }
    
    .message.bot {
        border-radius: 15px 15px 15px 0;
    }
    
    .messages-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
    }
    
    #helpModal.max-h-screen {
        transition: all 0.3s ease-in-out;
    }

    .message.bot p {
    margin-bottom: 10px;
    }

    .message.bot ul {
        padding-left: 20px;
    }

    .message.bot li {
        margin-bottom: 5px;
    }
`;
document.head.appendChild(style);

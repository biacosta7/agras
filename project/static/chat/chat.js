function renderMarkdown(markdownText) {
    // Converte o texto Markdown para HTML
    const rawHtml = marked.parse(markdownText);
    
    // Sanitiza o HTML gerado para remover qualquer conteúdo malicioso
    return DOMPurify.sanitize(rawHtml);
}

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        // Inicialize o VirtualSelect
        VirtualSelect.init({
            ele: '#cultivos',
            placeholder: 'Selecione os cultivos',
            search: true,
            multiple: true,
            noOptionsText: 'Nenhum cultivo encontrado',
            selectAllText: 'Selecionar todos',
            selectedTextFormat: 'count > 2'
        });

    }, 100);
});

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        // Inicialize o VirtualSelect
        VirtualSelect.init({
            ele: '#organisms',
            placeholder: 'Selecione os organismos',
            search: true,
            multiple: true,
            noOptionsText: 'Nenhum organismo encontrado',
            selectAllText: 'Selecionar todos',
            selectedTextFormat: 'count > 2'
        });

    }, 100);
});


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

    // Event listener for showing/hiding the utilities section
    document.getElementById("toggle-utilities").addEventListener("click", toggleUtilities);

    // Event listener for submitting selected cultivos
    document.getElementById("submit-cultivos").addEventListener("click", submitCultivos);

    // Event listener for showing/hiding the organisms section
    document.getElementById("toggle-organisms").addEventListener("click", toggleOrganisms);

    // Event listener for submitting selected organisms
    document.getElementById("submit-organisms").addEventListener("click", submitOrganisms);

    // Function to toggle utilities section visibility
function toggleUtilities() {
    const utilitiesSection = document.getElementById("utilities-section");
    const organismsSection = document.getElementById("organisms-section");

    // Fecha a seção de organismos, se estiver aberta
    if (!organismsSection.classList.contains("hidden")) {
        organismsSection.classList.add("hidden");
    }

    // Alterna a visibilidade da seção de utilidades
    if (utilitiesSection.classList.contains("hidden")) {
        utilitiesSection.classList.remove("hidden"); // Exibe a seção
    } else {
        utilitiesSection.classList.add("hidden"); // Esconde a seção
    }
    }

    // Function to toggle organisms section visibility
    function toggleOrganisms() {
        const organismsSection = document.getElementById("organisms-section");
        const utilitiesSection = document.getElementById("utilities-section");

        // Fecha a seção de utilidades, se estiver aberta
        if (!utilitiesSection.classList.contains("hidden")) {
            utilitiesSection.classList.add("hidden");
        }

        // Alterna a visibilidade da seção de organismos
        if (organismsSection.classList.contains("hidden")) {
            organismsSection.classList.remove("hidden"); // Exibe a seção
        } else {
            organismsSection.classList.add("hidden"); // Esconde a seção
        }
    }


    // Function to handle submission of selected cultivos and send the request to the chatbot
    async function submitCultivos(selectedCultivos) {
        try {
            const response = await fetch(askQuestionUrl, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    text: "Cultivos selecionados: " + selectedCultivos,
                    user_context: {
                        products: selectedCultivos, // Envia os cultivos selecionados
                    },
                }),
            });
    
            const data = await response.json();
    
            if (data.data && data.data.text) {
                appendMessage(data.data.text, 'bot');
            } else if (data.error) {
                console.error('Error from backend:', data.error);
                appendMessage('Desculpe, ocorreu um erro ao processar sua solicitação.', 'bot');
            }
        } catch (error) {
            console.error("Erro:", error);
            alert("Erro ao enviar os cultivos. Tente novamente.");
        }
    }

    // Função de submit dos cultivos selecionados
    document.getElementById("submit-cultivos").addEventListener("click", function () {
        // Use getSelectedOptions() para obter os valores selecionados
        const selectedOptions = document.querySelector('#cultivos').getSelectedOptions();
        console.log("Opções selecionadas:", selectedOptions); // Veja o retorno

        if (!selectedOptions || selectedOptions.length === 0) {
            alert("Por favor, selecione pelo menos um cultivo!");
            return;
        }

        // Extrai os valores das opções selecionadas
        const selectedCultivos = selectedOptions.map(option => option.value);
        
        const text = "Cultivos selecionados: " + selectedCultivos;
        console.log(text);

        // Envie os organismos selecionados para o backend
        submitCultivos(selectedCultivos);
    });


    // Function to handle submission of selected cultivos and send the request to the chatbot
    async function submitOrganisms(selectedOrganismos) {
        try {
            const response = await fetch(askQuestionUrl, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    text: "Organismos indesejádos selecionados: " + selectedOrganismos,
                    user_context: {
                        organisms: selectedOrganismos, // Envia os organismos selecionados
                    },
                }),
            });
    
            const data = await response.json();
    
            if (data.data && data.data.text) {
                appendMessage(data.data.text, 'bot');
            } else if (data.error) {
                console.error('Error from backend:', data.error);
                appendMessage('Desculpe, ocorreu um erro ao processar sua solicitação.', 'bot');
            }
        } catch (error) {
            console.error("Erro:", error);
            alert("Erro ao enviar os organismos. Tente novamente.");
        }
    }

    // Função de submit dos organismos selecionados
    document.getElementById("submit-organisms").addEventListener("click", function () {
        // Use getSelectedOptions() para obter os valores selecionados
        const selectedOptions = document.querySelector('#organisms').getSelectedOptions();
        console.log("Opções selecionadas:", selectedOptions); // Veja o retorno

        if (!selectedOptions || selectedOptions.length === 0) {
            alert("Por favor, selecione pelo menos um organismo!");
            return;
        }

        // Extrai os valores das opções selecionadas
        const selectedOrganismos = selectedOptions.map(option => option.value);
        
        const text = "Organismos selecionados: " + selectedOrganismos;
        console.log(text);

        // Envie os organismos selecionados para o backend
        submitCultivos(selectedOrganismos);
    });
    
    // Function to send a message in the chat
    async function sendMessage(text) {
        if (!text) return;
    
        console.log('Sending message:', text);
    
        // Cria e adiciona a mensagem do usuário no chat
        appendMessage(text, 'user');
    
        try {
            // Adiciona o contexto ao payload da mensagem
            const response = await fetch(askQuestionUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    text: text,
                    user_context: userContext // Adiciona o contexto ao corpo da requisição
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
            console.error('Error:', error);
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

    // Event listeners for sending messages
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
        list-style-type: disc; 
        padding-left: 20px;     
        margin-top: 5px;        
        margin-bottom: 5px;    
    }

    .message.bot li {
        margin-bottom: 5px;
    }

    #cultivos {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        background-color: #fff;
    }

    #cultivos:focus {
        outline-color: #4CAF50;
    }
`;
document.head.appendChild(style);

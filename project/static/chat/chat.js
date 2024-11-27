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
            placeholder: 'Selecione o organismo',
            search: true,
            multiple: false,
            noOptionsText: 'Nenhum organismo encontrado',
            selectedTextFormat: 'count > 2'
        });

    }, 100);
});

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        // Inicialize o VirtualSelect
        VirtualSelect.init({
            ele: '#cultivos2',
            placeholder: 'Selecione os cultivos',
            search: true,
            multiple: true,
            noOptionsText: 'Nenhum cultivo encontrado',
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

    // Criar o container de mensagens
    const messagesContainer = document.createElement('div');
    messagesContainer.className = 'messages-container mt-4 max-h-[300px] overflow-y-auto';
    // Certifique-se de que a variável chats contém dados válidos
    if (typeof chats !== 'falha' && Array.isArray(chats)) {
        // Adicionar histórico de mensagens ao container
        chats.forEach(chat => {
            appendMessage(chat.text_input, 'user');
            appendMessage(chat.gemini_output, 'bot');
        });
    } else {
        console.error('Chats data is undefined or not an array:', chats);
    }
    if (modalContent) {
        modalContent.insertBefore(messagesContainer, modalContent.querySelector('.mt-6'));
    }

    // Event listener for showing/hiding the utilities section
    document.getElementById("toggle-utilities").addEventListener("click", toggleUtilities);

    // Event listener for submitting selected cultivos
    document.getElementById("submit-cultivos").addEventListener("click", submitCultivos);

    // Event listener for showing/hiding the organisms section
    document.getElementById("toggle-organisms").addEventListener("click", toggleOrganisms);

    // Event listener for submitting selected organisms
    //document.getElementById("submit-organisms").addEventListener("click", submitOrganisms);

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

    function toggleOrganisms2() {
        const organismsSection2 = document.getElementById("organisms-section2");
        const organismsSection = document.getElementById("organisms-section");
        const utilitiesSection = document.getElementById("utilities-section");

        // Fecha a seção de utilidades, se estiver aberta
        if (!utilitiesSection.classList.contains("hidden")) {
            utilitiesSection.classList.add("hidden");
        }
        
        // Fecha a seção de organismos, se estiver aberta
        if (!organismsSection.classList.contains("hidden")) {
            organismsSection.classList.add("hidden");
        }

        // Alterna a visibilidade da seção de organismos 2 (cultivos dos organismos)
        if (organismsSection2.classList.contains("hidden")) {
            organismsSection2.classList.remove("hidden"); // Exibe a seção
        } else {
            organismsSection2.classList.add("hidden"); // Esconde a seção
        }
    }


    // Function to handle submission of selected cultivos and send the request to the chatbot
    async function submitCultivos(selectedCultivos) {
        try {
            // Verifica se há cultivos selecionados
            if (selectedCultivos.length === 0 || selectedCultivos instanceof MouseEvent) {
                console.log('Nenhum cultivo selecionado ou evento detectado. Impedindo o fetch.');
                return;  // Não faz o fetch se o valor for '[object MouseEvent]' ou se não houver cultivos
            }
        
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
        
            // Limpar a seleção de cultivos após o envio
            const cultivoSelect = document.querySelector('#cultivos');
            if (cultivoSelect) {
                cultivoSelect.reset();  // Limpa as opções selecionadas
                console.log("Cultivos selecionados foram limpos.");
            }
        } catch (error) {
            console.error("Erro:", error);
            alert("Erro ao enviar os cultivos. Tente novamente.");
        }
    
    }    
    

    // Função de submit dos cultivos selecionados
    document.getElementById("submit-cultivos").addEventListener("click", (event) => {
        event.preventDefault(); // Previne o comportamento padrão do botão
    
        const cultivosSelect = document.querySelector('#cultivos');
        if (!cultivosSelect) {
            console.error("Elemento #cultivos não encontrado!");
            return;
        }
    
        // Use o método apropriado do VirtualSelect para obter os valores selecionados
        const selectedOptions = cultivosSelect.virtualSelect.getSelectedOptions();
        
        if (!selectedOptions || selectedOptions.length === 0) {
            alert("Por favor, selecione pelo menos um cultivo!");
            return; // Não chama submitCultivos se não houver opções
        }
    
        // Extrai os valores das opções selecionadas
        const selectedCultivos = selectedOptions.map(option => option.value);
        console.log("Cultivos selecionados:", selectedCultivos);
    
        // Envia os cultivos selecionados
        submitCultivos(selectedCultivos);
        toggleUtilities();
    });
        
        
    // Variáveis globais para armazenar as seleções
    let selectedOrganismos = [];
    let selectedCultivosOrganismos = [];

    // Função para enviar os dados ao chatbot
    async function submitCombinedData() {
        try {
            if (selectedOrganismos.length === 0 && selectedCultivosOrganismos.length === 0) {
                alert("Nenhum dado selecionado para envio.");
                return;
            }

            // Texto consolidado para envio
            const combinedText = `
                Organismos indesejados selecionados: ${selectedOrganismos}.
                Cultivos que possuem esses organismos: ${selectedCultivosOrganismos}.
            `;

            const response = await fetch(askQuestionUrl, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    text: combinedText,
                    user_context: {
                        organisms: selectedOrganismos,
                        cultivos: selectedCultivosOrganismos,
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
            alert("Erro ao enviar os dados. Tente novamente.");
        }
    }

    // Função para lidar com o primeiro popup (organismos)
    document.getElementById("submit-organisms").addEventListener("click", function () {
        const organismsElement = document.querySelector('#organisms');
        const organismsOptions = organismsElement.value;
    
        if (!organismsOptions || organismsOptions.length === 0) {
            alert("Por favor, selecione pelo menos um organismo!");
            return;
        }
    
        // Atualize a variável com os valores selecionados
        selectedOrganismos = organismsOptions;
    
        console.log("Organismos selecionados:", selectedOrganismos);
    
        // Fecha o modal do primeiro popup
        toggleOrganisms();
    
        // Abre o segundo modal
        toggleOrganisms2();
    });    

    // Função para lidar com o segundo popup (cultivos dos organismos)
    document.getElementById("submit-organisms2").addEventListener("click", function () {
        const cultivosOptions = document.querySelector('#cultivos2').getSelectedOptions();

        if (!cultivosOptions || cultivosOptions.length === 0) {
            alert("Por favor, selecione pelo menos um cultivo!");
            return;
        }

        // Extrai os valores das opções selecionadas
        selectedCultivosOrganismos = cultivosOptions.map(option => option.value);

        console.log("Cultivos selecionados:", selectedCultivosOrganismos);

        // Fecha o modal do segundo popup
        toggleOrganisms2();

        // Envia os dados combinados após o segundo popup
        submitCombinedData();
    });
    
    // Função para enviar uma mensagem
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
        
        chatInput.value = ''; // Limpa o campo de entrada após o envio
    }

    // Array para armazenar as mensagens com a data
    let messageHistory = [];

    // Função para renderizar as mensagens em ordem decrescente de data
    function renderMessages() {
        messagesContainer.innerHTML = ''; // Limpa o container de mensagens

        // Ordena as mensagens pela data (do mais recente para o mais antigo)
        messageHistory.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

        // Adiciona as mensagens ordenadas ao container
        messageHistory.forEach(message => {
            appendMessage(message.text, message.sender);
        });
    }

    // Função para adicionar a mensagem ao histórico
    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender} mb-4 p-3 rounded-lg ${
            sender === 'user' 
                ? 'bg-[#8ABF17] text-white ml-auto' 
                : 'bg-gray-100 text-black'
        }`;
        messageDiv.style.maxWidth = '80%';

        if (sender === 'bot') {
            messageDiv.innerHTML = renderMarkdown(text); // Para mensagens do bot, renderiza o texto como Markdown
        } else {
            messageDiv.textContent = text; // Para mensagens do usuário, apenas o texto
        }

        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Event listener para enviar a mensagem ao pressionar Enter
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage(chatInput.value);
            chatInput.value = ''; // Limpa o campo de entrada após o envio
        }
    });

    // Event listener para enviar a mensagem ao clicar no botão de envio
    sendButton.addEventListener('click', () => {
        sendMessage(chatInput.value);
        chatInput.value = ''; // Limpa o campo de entrada após o envio
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

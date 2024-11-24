document.addEventListener("DOMContentLoaded", () => {
    const readButton = document.getElementById("readPageButton");
    let currentAudio = null;
    let isPlaying = false;

    if (readButton) {
        readButton.addEventListener("click", async () => {
            try {
                // Caso já tenha um áudio carregado
                if (currentAudio) {
                    if (isPlaying) {
                        console.log("Pausing audio...");
                        currentAudio.pause(); // Pausar o áudio
                        isPlaying = false;
                        readButton.textContent = 'Read Page';
                    } else {
                        console.log("Resuming audio...");
                        await currentAudio.play(); // Retomar o áudio
                        isPlaying = true;
                        readButton.textContent = 'Stop';
                    }
                    return; // Encerrar o processamento
                }

                // Desabilitar botão durante o processamento
                readButton.disabled = true;
                readButton.textContent = 'Processing...';

                // Obter o texto visível na página
                const visibleText = Array.from(document.body.querySelectorAll('*'))
                    .filter(element => {
                        const style = window.getComputedStyle(element);
                        return style.display !== 'none' && style.visibility !== 'hidden';
                    })
                    .map(element => element.innerText)
                    .join(' ')
                    .trim();

                console.log("Visible text fetched:", visibleText);

                // Fazer requisição para o servidor
                const response = await fetch("/comunidades/read-page/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ 
                        text: visibleText, 
                        url: window.location.href,
                    }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                console.log("Audio response received.");

                // Criar áudio a partir do Blob
                const blob = await response.blob();
                const audioUrl = URL.createObjectURL(blob);
                currentAudio = new Audio(audioUrl);

                // Configurar evento para quando o áudio terminar
                currentAudio.onended = () => {
                    console.log("Audio ended.");
                    isPlaying = false;
                    readButton.textContent = 'Read Page';
                    URL.revokeObjectURL(audioUrl); // Revogar URL
                    currentAudio = null; // Limpar referência
                };

                // Reproduzir áudio
                console.log("Starting audio playback...");
                await currentAudio.play();
                isPlaying = true;
                readButton.textContent = 'Stop';

            } catch (error) {
                console.error("Error processing audio:", error);
                alert("Failed to process audio. Please try again.");
            } finally {
                readButton.disabled = false;
            }
        });
    }
});

// Improved CSRF token function with error handling
function getCookie(name) {
    try {
        if (!document.cookie || document.cookie === "") {
            return null;
        }
        
        const token = document.cookie
            .split(';')
            .map(c => c.trim())
            .find(c => c.startsWith(name + '='));
            
        return token ? decodeURIComponent(token.substring(name.length + 1)) : null;
    } catch (error) {
        console.error('Error getting CSRF token:', error);
        return null;
    }
}

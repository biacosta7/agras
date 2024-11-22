document.addEventListener("DOMContentLoaded", () => {
    const readButton = document.getElementById("readPageButton");
    let isPlaying = false;
    let currentAudio = null;

    if (readButton) {
        readButton.addEventListener("click", async () => {
            try {
                // If audio is playing, stop it
                if (isPlaying && currentAudio) {
                    currentAudio.pause();
                    currentAudio = null;
                    isPlaying = false;
                    return;
                }

                // Disable button during processing
                readButton.disabled = true;
                readButton.textContent = 'Processing...';

                // Get only visible text content
                const visibleText = Array.from(document.body.querySelectorAll('*'))
                    .filter(element => {
                        const style = window.getComputedStyle(element);
                        return style.display !== 'none' && style.visibility !== 'hidden';
                    })
                    .map(element => element.innerText)
                    .join(' ')
                    .trim();

                const response = await fetch("/comunidades/read-page/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie('csrftoken')
                    },
                    body: JSON.stringify({ 
                        text: visibleText, 
                        url: window.location.href 
                    })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const blob = await response.blob();
                const audioUrl = URL.createObjectURL(blob);
                currentAudio = new Audio(audioUrl);

                // Clean up previous audio URL
                currentAudio.onended = () => {
                    URL.revokeObjectURL(audioUrl);
                    isPlaying = false;
                    readButton.textContent = 'Read Page';
                };

                await currentAudio.play();
                isPlaying = true;
                readButton.textContent = 'Stop';

            } catch (error) {
                console.error("Error processing audio:", error);
                alert("Failed to process audio. Please try again.");
            } finally {
                readButton.disabled = false;
                if (!isPlaying) {
                    readButton.textContent = 'Read Page';
                }
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

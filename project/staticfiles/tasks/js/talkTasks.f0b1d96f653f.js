const talkButton = document.querySelector('.talk-button');
const synth = window.speechSynthesis;
let isSpeaking = false; // Flag para alternância do botão

function getPreferredVoice(voices, lang = "pt-BR") {
    const preferredNames = ["Google português do Brasil", "Luciana", "Maria", "Fernanda"];
    for (let name of preferredNames) {
        const voice = voices.find(v => v.name.includes(name) && v.lang === lang);
        if (voice) return voice;
    }
    return voices.find(v => v.lang === lang) || voices[0];
}

function talk() {
    // Se já está falando, interrompe a fala e reinicia
    if (isSpeaking) {
        synth.cancel();
        isSpeaking = false;
        talkButton.classList.remove('talking');
        return;
    }

    const taskDescriptions = Array.from(document.querySelectorAll('.task-description'));
    const dayEventH3s = Array.from(document.querySelectorAll('.day-events > h3'));

    let text = "Tarefas. "; // Texto inicial fixo

    if (taskDescriptions.length > 0 && dayEventH3s.length > 0) {
        // Concatena textos de dayEventH3s e taskDescriptions, respeitando as posições
        const maxLength = Math.max(taskDescriptions.length, dayEventH3s.length);
        for (let i = 0; i < maxLength; i++) {
            const h3Text = dayEventH3s[i]?.textContent.trim() || ""; // Texto do <h3> ou vazio
            const descriptionText = taskDescriptions[i]?.textContent.trim() || ""; // Texto da descrição ou vazio
            text += `${h3Text} ${descriptionText}. `;
        }
    } else {
        // Texto padrão caso não haja tarefas
        text += "Selecione um ou mais dias para visualizar as tarefas previstas para cada.";
    }

    let voices = synth.getVoices();

    if (voices.length > 0) {
        let msg = new SpeechSynthesisUtterance();
        let preferredVoice = getPreferredVoice(voices, "pt-BR");

        msg.voice = preferredVoice || voices[0];
        msg.rate = 1.15;
        msg.pitch = 1.0;
        msg.text = text;
        msg.lang = "pt-BR";

        // Adiciona a classe de animação ao botão
        talkButton.classList.add('talking');
        isSpeaking = true; // Define flag como ativa

        // Remove a animação e redefine flag ao finalizar
        msg.onend = () => {
            talkButton.classList.remove('talking');
            isSpeaking = false;
        };

        // Cancela flag se houver erro
        msg.onerror = () => {
            talkButton.classList.remove('talking');
            isSpeaking = false;
            console.error("Erro durante a síntese de fala.");
        };

        synth.speak(msg);
    } else {
        console.error("Nenhuma voz disponível.");
    }
}

talkButton.addEventListener('click', talk);

if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = () => synth.getVoices();
}

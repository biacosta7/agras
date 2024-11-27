const talkButton = document.querySelector('.talk-button');
const synth = window.speechSynthesis;

function getPreferredVoice(voices, lang = "pt-BR") {
    const preferredNames = ["Google português do Brasil", "Luciana", "Maria", "Fernanda"];
    for (let name of preferredNames) {
        const voice = voices.find(v => v.name.includes(name) && v.lang === lang);
        if (voice) return voice;
    }
    return voices.find(v => v.lang === lang) || voices[0];
}

function talk() {
    let text = "Tarefas"; // Texto a ser falado
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

        // Remove a animação ao finalizar
        msg.onend = () => {
            talkButton.classList.remove('talking');
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
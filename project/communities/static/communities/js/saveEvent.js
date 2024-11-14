// Importa a função que garante que a data esteja no formato DD/MM/AAAA
import { formatDate } from './newDateFunctions.js'

// Importa o objeto que contém o estado atual do calendário
import { calendarState } from './showCalendar.js'

import { showCalendar } from './showCalendar.js';

// Objeto que faz a correspondência entre a cor do marcador e a cor de fundo do grupo
const colorMapping = {
    "var(--red-marker-bg-color)": "var(--red-form-group-bg-color)",
    "var(--orange-marker-bg-color)": "var(--orange-form-group-bg-color)",
    "var(--yellow-marker-bg-color)": "var(--yellow-form-group-bg-color)",
    "var(--green-marker-bg-color)": "var(--green-form-group-bg-color)",
    "var(--blue-marker-bg-color)": "var(--blue-form-group-bg-color)",
    "var(--pink-marker-bg-color)": "var(--pink-form-group-bg-color)",
    "var(--black-marker-bg-color)": "var(--black-form-group-bg-color)",
    "var(--gray-marker-bg-color)": "var(--gray-form-group-bg-color)",
    "var(--white-marker-bg-color)": "var(--white-form-group-bg-color)"
};

// Endpoint do envio do formulário
const url_do_seu_servidor = "https://eocqr43t4jsm544.m.pipedream.net";

// Seleciona o pop-up de salvar, o foumulário, o botão de selecionar a cor do evento, o pop-up de selecionar a cor do evento
const saveEventPopup = document.querySelector('.save-event-popup');
const saveEventFormGroup1 = document.querySelector('.save-event-form-group1');
const saveEventButton = document.querySelector('.save-event-button');
const saveEventForm = document.querySelector('.save-event-form');
const saveEventStatus = document.querySelector('.save-event-popup-status');
const dateTime = document.querySelectorAll('.event-date-time p');
const colorPickerButton = document.querySelector('#color-picker');
const colorPickerPopup = document.querySelector('.color-picker-popup');
const colorPickerPopupButtons = document.querySelectorAll('.color-picker-button');
//const overlay = document.createElement('div');

function closeSaveEventPopup() {
    // Esconde o pop-up
    saveEventPopup.classList.remove('active');
    // Remove
    colorPickerButton.removeEventListener('click', openColorPickerPopup);
    // Remove
    saveEventButton.removeEventListener('click', saveEvent);
}

function saveEvent() {
    // Adiciona o marcador de evento no dia
    //calendarState.selectedDayElement.classList.add('marked-day');
    // Coleta os dados do formulário
    const title = "adubar cenoura";
    const description = "usar enxada";
    const frequency = "";
    const color = document.querySelector('#color-picker').style.backgroundColor;
    
    // Cria a data de início do evento com base no dia selecionado
    const startDate = new Date(calendarState.year, calendarState.month, calendarState.day);
    
    // Cria o objeto do evento
    const dayEvent = {
        title,
        description,
        start_date: startDate,
        frequency,
        end_date: null,  // Pode ser definido se houver um campo de data final
        color
    };

    // Adiciona o evento ao array de eventos
    calendarState.dayEvents.push(dayEvent);
    
    
    // Atualiza o calendário
    showCalendar(calendarState.month, calendarState.year);
    // Fecha o pop-up
    closeSaveEventPopup();
}

function closeColorPickerPopup() {
    colorPickerPopupButtons.forEach(button => {
        // Remove o evento
        button.removeEventListener('click', selectColor);
    });

    colorPickerPopup.classList.remove('active');
    //overlay.classList.remove('active');
    colorPickerPopup.removeEventListener('click', closeSaveEventPopup)
}

function selectColor(event) {
    // Atualiza a cor de fundo do botão de edição de cor com a cor do botão clicado
    const markerColor = event.target.style.backgroundColor;
    colorPickerButton.style.backgroundColor = markerColor;
    // Atualiza a cor de fundo do grupo
    saveEventFormGroup1.style.backgroundColor = colorMapping[markerColor];

    // Fecha o pop-up
    closeColorPickerPopup();
}

function openColorPickerPopup() {
    // Cria uma sobreposição
    //overlay.classList.add('overlay');
    //saveEventForm.appendChild(overlay);

    // Mostra o pop-up e a sobreposição
    colorPickerPopup.classList.add('active');
    //overlay.classList.add('active');

    // Adiciona o evento de clique nos botões
    colorPickerPopupButtons.forEach(button => {
        button.addEventListener('click', selectColor);
    });

    // Adiciona o evento de clique na sobreposição para fechar o pop-up
    colorPickerPopup.addEventListener('click', closeSaveEventPopup)

    // Impede a propagação do clique no quadrado
    const colorPickerSquare = document.querySelector('.color-picker-popup-square');
    colorPickerSquare.addEventListener('click', (event) => {
        event.stopPropagation();
    });
}

// Função para abrir o pop-up de salvar
export function openSaveEventPopup() {
    // Mostra o pop-up
    saveEventPopup.classList.add('active');

    // Atualiza a data e hora do evento
    dateTime[0].textContent = formatDate(`${calendarState.day}/${calendarState.month}/${calendarState.year}`);
    dateTime[1].textContent = 'Manhã'   // Valor padrão

    // Adiciona o evento de clique no botão de selecionar cor para abrir o pop-up de selecionar a cor do evento
    colorPickerButton.addEventListener('click', openColorPickerPopup);  //REMOVERRRRRR DPSSS

    // Adiciona o evento de clique no botão de salvar para salvar o evento
    saveEventButton.addEventListener('click', saveEvent);

    // Evento de submit no formulário
    saveEventForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário
        console.log("Código adicional executado!");
    
        // Coleta os dados do formulário
        const formData = new FormData(this);
    
        // Envia os dados com AJAX
        fetch(url_do_seu_servidor, {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("Formulário enviado com sucesso!", data);
            // Aqui você pode executar código adicional após o envio, como atualizar a interface
        })
        .catch(error => {
            console.error("Erro ao enviar o formulário:", error);
        });
    });
}
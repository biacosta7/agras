// Importa as novas funções que criei para manipular datas
import { getDayOfWeek, getDayOfWeekName, getMonthName } from './newDateFunctions.js';
// Importa o objeto que contém o estado atual do calendário
import { calendarState } from './showCalendar.js'
// Importa a função de abrir o pop-up de salvar evento
import { openSaveEventPopup } from './saveEvent.js';

// Seleciona o calendário, o pop-up de criar um evento no calendário, o botão dele
const calendar = document.querySelector('.calendar');
const createEventPopup = document.querySelector('.add-event');
const createEventButton = document.querySelector('.create-event-button');
const overlay = document.createElement('div');

// Função para fechar o pop-up de criar
function closeCreateEventPopup() {
    createEventPopup.classList.remove('active');                               // Esconde o pop-up
    overlay.classList.remove('active');                                        // Esconde a sobreposição
    createEventButton.removeEventListener('click', handleCreateEventClick);    // Remove o escutador do botão
    overlay.removeEventListener('click', closeCreateEventPopup);               // Remove o escutador da sobreposição
}

// Função para lidar com o clique no botão "Criar"
function handleCreateEventClick() {
    closeCreateEventPopup();                                                          // Fecha o pop-up de criar
    openSaveEventPopup(calendarState.year, calendarState.month, calendarState.day);   // Abre o pop-up de salvar
}

// Função para abrir o pop-up de criar
export function openCreateEventPopup() {
    // Cria uma sobreposição
    overlay.classList.add('overlay');
    calendar.appendChild(overlay);

    // Exibe a data no pop-up
    let dayOfWeek = getDayOfWeek(calendarState.year, calendarState.month, calendarState.day);
    let dayOfWeekName = getDayOfWeekName(dayOfWeek);
    document.querySelector('.event-date').textContent = `${dayOfWeekName}, ${calendarState.day} de ${getMonthName(calendarState.month)}`;

    // Mostra o pop-up e a sobreposição
    createEventPopup.classList.add('active');
    overlay.classList.add('active');

    // Adiciona o evento de clique no botão "Criar" para abrir o pop-up de salvar um evento
    createEventButton.addEventListener('click', handleCreateEventClick);
    // Adiciona o evento de clique na sobreposição para fechar o pop-up
    overlay.addEventListener('click', closeCreateEventPopup);
}
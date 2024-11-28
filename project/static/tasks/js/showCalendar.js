// Importa as novas funções que criei para manipular datas
import { getDayOfWeek, getDayOfWeekName, getDaysInMonth, getMonthName } from './newDateFunctions.js';
// Importa a função de exibição do pop-up de adicionar evento no calendário
//import { listAllEvents } from './listEvents.js';
// Importa a função de pegar os eventos do dia e de adicionar marcadores nos dias com eventos
import { getEventsForDay, addMarker } from './markDays.js'

// Constantes globais para armazenar a data atual (hoje)
const currentDate = new Date();
const YEAR = currentDate.getFullYear();
const MONTH = currentDate.getMonth() + 1; // getMonth() retorna o mês de 0 a 11, então é adicionado 1
const DAY = currentDate.getDate();

function parseDateString(dateString) {
    if (!dateString) return null;
    const [year, month, day] = dateString.split('-').map(Number);
    return new Date(year, month, day);
}


// Função para mapear status para cor
function getTaskColor(status) {
    status = status.toLowerCase();
    if (status === 'pendente') {
        return 'var(--dar-red-color)';
    } 
    else if (status === 'progresso') {
        return 'var(--dark-brown-color)';
    } 
    else if (status === 'concluída') {
        return 'var(--dark-green-color)';
    } 
    else {
        return 'var(--dark-gray-color)';
    }
}

// Processa os dados das tarefas
const processedTasks = tasksData.map(task => ({
    title: task.title,
    description: task.description,
    start_date: parseDateString(task.start_date),
    end_date: task.end_date ? parseDateString(task.end_date) : parseDateString(task.start_date),
    recurrence: task.recurrence.toLowerCase(),
    priority: task.priority,
    status: task.status,  // Inclui o status
    color: getTaskColor(task.status),  // Obtém a cor com base no status
    area_name: task.area_name,
    seedbed_name: task.seedbed_name,
    responsible_users: task.responsible_users,
}));

// Objeto constante global para armazenar o estado do calendário
export const calendarState = {
    year: YEAR,
    month: MONTH,
    day: DAY,
    selectedDays: [],
    dayEvents: processedTasks
};

// Captura os botões de controle do calendário
const previousButton = document.querySelector('.previous-month');
const nextButton = document.querySelector('.next-month');

// Função para lidar com o toque em um dia do mês (para smartphones e tablets)
function handleDayTouch(event) {
    const dayElement = event.target;

    // Previne o comportamento padrão para evitar interferências
    event.preventDefault();

    // Alterna a seleção do dia
    toggleDaySelection(dayElement);

    // Lógica adicional (exemplo: listagem de eventos)
    listSelectedDaysEvents();
}

// Função para lidar com o clique em um dia do mês (para computadores)
function handleDayClick(event) {
    // Se o botão pressionado do mouse não foi o esquerdo
    if (event.button !== 0) return;

    const dayElement = event.target;

    // Alterna a seleção do dia
    toggleDaySelection(dayElement);

    // Lógica adicional (exemplo: listagem de eventos)
    listSelectedDaysEvents();
}

// Função para alternar a seleção de um dia
function toggleDaySelection(dayElement) {
    const dayNumber = parseInt(dayElement.textContent);

    // Verifica se o dia já está selecionado
    const isSelected = dayElement.classList.contains('selected-day');

    if (isSelected) {
        // Desmarca o dia
        dayElement.style.backgroundColor = 'var(--days-bg-color)';
        dayElement.classList.remove('selected-day');

        // Remove o dia do estado
        calendarState.selectedDays = calendarState.selectedDays.filter(
            (selectedDay) => selectedDay !== dayNumber
        );
    } else {
        // Marca o dia
        dayElement.style.backgroundColor = 'var(--green-agras-color)';
        dayElement.classList.add('selected-day');

        // Adiciona o dia ao estado
        calendarState.selectedDays.push(dayNumber);
    }
}

function listSelectedDaysEvents() {
    const asideSection = document.querySelector('.list-tasks-aside-section');
    const warningDiv = asideSection.querySelector('.warning-to-select-a-day');

    // Remove os divs de dias que não estão mais selecionados
    const existingDayDivs = asideSection.querySelectorAll('.day-events');
    existingDayDivs.forEach(dayDiv => {
        const day = parseInt(dayDiv.getAttribute('data-day'));
        if (!calendarState.selectedDays.includes(day)) {
            asideSection.removeChild(dayDiv);
        }
    });

    if (calendarState.selectedDays.length === 0) {
        // Mostra a mensagem de aviso se não houver dias selecionados
        warningDiv.style.display = 'block';
    } 
    else {
        // Esconde a mensagem de aviso
        warningDiv.style.display = 'none';

        // Para cada dia selecionado, verifica se já existe um div correspondente
        calendarState.selectedDays.forEach(day => {
            let dayDiv = asideSection.querySelector(`.day-events[data-day='${day}']`);
            if (!dayDiv) {
                // Cria um novo div para o dia
                dayDiv = document.createElement('div');
                dayDiv.classList.add('day-events');
                dayDiv.setAttribute('data-day', day);

                // Cria o header com o número do dia e o nome do dia da semana
                const date = new Date(calendarState.year, calendarState.month - 1, day);
                const dayOfWeekName = getDayOfWeekName(date.getDay());
                const header = document.createElement('h3');
                header.textContent = `Dia ${day}, ${dayOfWeekName}`;
                dayDiv.appendChild(header);

                // Obtém os eventos do dia
                const events = getEventsForDay(day, calendarState.month, calendarState.year);

                // Cria divs para cada evento (tarefa)
                events.forEach(event => {
                    // Cria o cartão da tarefa
                    const taskCard = document.createElement('div');
                    taskCard.classList.add('task-card');

                    // Metade do cartão: descrição
                    const descriptionDiv = document.createElement('div');
                    descriptionDiv.classList.add('task-description');
                    descriptionDiv.textContent = event.description;
                    taskCard.appendChild(descriptionDiv);

                    // Outra metade: informações adicionais
                    const infoDiv = document.createElement('div');
                    infoDiv.classList.add('task-info');

                    // Cor
                    const colorDiv = document.createElement('div');
                    colorDiv.classList.add('task-color');
                    colorDiv.style.backgroundColor = event.color;
                    colorDiv.textContent = `${event.status}`;
                    infoDiv.appendChild(colorDiv);

                    // Área e Canteiro
                    const areaSeedbedDiv = document.createElement('div');
                    areaSeedbedDiv.classList.add('task-area-seedbed');
                    areaSeedbedDiv.innerHTML = `<strong>${event.area_name || '-'}</strong><br>${event.seedbed_name || '-'}`;
                    infoDiv.appendChild(areaSeedbedDiv);


                    // Botão "Consultar"
                    const consultButton = document.createElement('button');
                    consultButton.classList.add('task-consult-button');
                    consultButton.textContent = 'Consultar';
                    // Adicione um event listener se necessário
                    infoDiv.appendChild(consultButton);

                    // Usuários Responsáveis
                    const usersDiv = document.createElement('div');
                    usersDiv.classList.add('task-users');
                    //usersDiv.textContent = `${event.responsible_users.join(', ')}`;
                    usersDiv.textContent = `${event.responsible_users[0][0]}`; // Só a 1ª letra do 1º responsável
                    infoDiv.appendChild(usersDiv);

                    // Adiciona o infoDiv ao taskCard
                    taskCard.appendChild(infoDiv);

                    // Adiciona o taskCard ao dayDiv
                    dayDiv.appendChild(taskCard);
                });

                // Adiciona o div do dia à seção
                asideSection.appendChild(dayDiv);
            }
        });
    }
}

// Função para limpar as seleções
function clearSelections() {
    // Limpa os dias selecionados no estado
    calendarState.selectedDays = [];

    // Remove a classe 'selected-day' e redefine os estilos de todos os dias
    const daysCells = document.querySelectorAll('.days');
    daysCells.forEach(cell => {
        cell.classList.remove('selected-day');
        cell.style.backgroundColor = ''; // Reseta a cor de fundo
    });

    // Reseta a seção de listagem de eventos
    const asideSection = document.querySelector('.list-tasks-aside-section');
    asideSection.innerHTML = '';
    const warningDiv = document.createElement('div');
    warningDiv.classList.add('warning-to-select-a-day');
    warningDiv.textContent = 'Selecione um ou mais dias para visualizar as tarefas previstas para cada.';
    asideSection.appendChild(warningDiv);
}

export function showCalendar(month, year) {
    const calendarTitle = document.querySelector('.calendar-title');
    const monthElement = document.querySelector('.month');
    const daysCells = monthElement.querySelectorAll('.days');

    const dayOfWeek = getDayOfWeek(year, month, 1);                 // Dia da semana do primeiro dia do mês
    const daysInMonth = getDaysInMonth(year, month);                // Total de dias no mês
    const daysInPreviousMonth = getDaysInMonth(year, month - 1);    // Total de dias no mês anterior

    // Atualiza o título do calendário com o mês e o ano
    calendarTitle.textContent = `${getMonthName(month)} ${year}`;

    let dayCounter = 1;

    // Limpa as células antes de preencher
    daysCells.forEach(cell => {
        // Remove o conteúdo anterior
        cell.textContent = '';
        // Remove os estilos anteriores
        cell.style.backgroundColor = '';
        //cell.style.color = '';
        cell.style.border = '';
        cell.style.boxShadow = '';
        cell.style.cursor = '';
        // Remove os escutadores de eventos antigos
        cell.removeEventListener('mousedown', handleDayClick);
        cell.removeEventListener('touchstart', handleDayTouch);

        // Remove as classes CSS anteriores
        cell.classList.remove('marked-day', 'selected-day');

        // Remove as divs de números e marcadores, se existirem
        const dayNumber = cell.querySelector('.day-number');
        if (dayNumber) {
            cell.removeChild(dayNumber);
        }

        const markersContainer = cell.querySelector('.markers-container');
        if (markersContainer) {
            cell.removeChild(markersContainer);
        }
    });

    // Preenche as células com os últimos dias do mês anterior
    for (let i = 0; i < dayOfWeek; i++) {
        daysCells[i].textContent = daysInPreviousMonth - dayOfWeek + i + 1;   // Últimos dias do mês anterior
        daysCells[i].style.backgroundColor = 'var(--other-days-bg-color)';    // Cor do mês anterior
    }

    // Preenche os dias do mês
    for (let i = dayOfWeek; i < dayOfWeek + daysInMonth; i++) {
        // Cria a div dos números
        const dayNumber = document.createElement("div");
        dayNumber.classList.add("day-number");
        daysCells[i].appendChild(dayNumber);
        dayNumber.textContent = dayCounter;

        // Cria a div dos marcadores
        const markersContainer = document.createElement("div");
        markersContainer.classList.add("markers-container");
        daysCells[i].appendChild(markersContainer);

        // Define a aparência inicial do dia
        daysCells[i].style.backgroundColor = 'var(--days-bg-color)';
        daysCells[i].style.cursor = 'pointer';

        // Obtém eventos para o dia
        const eventsForDay = getEventsForDay(dayCounter, month, year);
        if (eventsForDay.length > 0) {
            daysCells[i].classList.add('marked-day');

            // Adiciona marcadores até o máximo de 2
            for (let j = 0; j < Math.min(eventsForDay.length, 2); j++) {
                addMarker(markersContainer, eventsForDay[j].color);
            }

            // Adiciona texto "e mais x tarefas" se houver mais de 2 eventos
            if (eventsForDay.length > 2) {
                const extraTasksDiv = document.createElement("div");
                extraTasksDiv.classList.add("extra-tasks");
                extraTasksDiv.textContent = `e mais ${eventsForDay.length - 2} tarefas.`;
                daysCells[i].appendChild(extraTasksDiv);
            }
        }

        // Adiciona escutadores de eventos de clique e toque
        daysCells[i].addEventListener('mousedown', handleDayClick);
        daysCells[i].addEventListener('touchstart', handleDayTouch);

        dayCounter++;
    }

    // Preenche as células restantes com os primeiros dias próximo mês
    let nextDayCounter = 1;
    for (let i = dayOfWeek + daysInMonth; i < daysCells.length; i++) {
        daysCells[i].textContent = nextDayCounter;                            // Dias do mês seguinte
        daysCells[i].style.backgroundColor = 'var(--other-days-bg-color)';    // Cor do próximo mês
        nextDayCounter++;
    }

}

function updateCalendar(newMonth, newYear) {
    // Limpa as seleções ao atualizar o calendário
    clearSelections();
    showCalendar(newMonth, newYear);    // Atualiza o calendário com os novos valores de mês e ano
}

function main() {
    console.log(calendarState.dayEvents);

    // Evento de clique pro botão anterior
    previousButton.addEventListener('click', () => {
        if (calendarState.month === 1) {
            calendarState.month = 12;   // Se estiver em janeiro, vai para dezembro
            calendarState.year--;       // Diminui o ano
        } else {
            calendarState.month--;      // Apenas diminui o mês
        }
        updateCalendar(calendarState.month, calendarState.year); // Atualiza o calendário
    });

    // Evento de clique pro botão seguinte
    nextButton.addEventListener('click', () => {
        if (calendarState.month === 12) {
            calendarState.month = 1;    // Se estiver em dezembro, vai para janeiro
            calendarState.year++;       // Aumenta o ano
        } else {
            calendarState.month++;      // Apenas aumenta o mês
        }
        updateCalendar(calendarState.month, calendarState.year); // Atualiza o calendário
    });

    showCalendar(calendarState.month, calendarState.year);
}

// Chama a função main ao carregar o script
main();
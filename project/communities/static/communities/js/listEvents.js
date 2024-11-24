// Importa as novas funções que criei para manipular datas
import { getDayOfWeek, getDayOfWeekName, getMonthName } from './newDateFunctions.js';

import { getEventsForDay } from './markDays.js'

export function listAllEvents(day, month, year) {
    // Obter os eventos do dia
    const events = getEventsForDay(day, month, year);

    // Selecionar o popup de exibição dos eventos
    const createEventPopup = document.querySelector('.add-event');
    const savedEventsContainer = createEventPopup.querySelector('.saved-events');

    // Limpar eventos anteriores
    savedEventsContainer.innerHTML = '';

    // Atualizar a data no popup
    let dayOfWeek = getDayOfWeek(year, month, day);
    let dayOfWeekName = getDayOfWeekName(dayOfWeek);
    document.querySelector('.event-date').textContent = `${dayOfWeekName}, ${day} de ${getMonthName(month)}`;

    if (events.length === 0) {
        // Exibir mensagem de que não há eventos
        const noEventsMessage = document.createElement('span');
        noEventsMessage.classList.add('saved-event');
        noEventsMessage.textContent = 'Não há tarefas neste dia.';
        savedEventsContainer.appendChild(noEventsMessage);
    } else {
        // Listar os eventos
        events.forEach(event => {
            const eventElement = document.createElement('span');
            eventElement.classList.add('saved-event');

            const titleElement = document.createElement('h3');
            titleElement.classList.add('event-title');
            titleElement.textContent = event.title;

            const descriptionElement = document.createElement('p');
            descriptionElement.classList.add('event-description');
            descriptionElement.textContent = event.description;

            // Botões de ação (se necessário)
            // const deleteButton = document.createElement('button');
            // deleteButton.classList.add('material-icons', 'delete-event');
            // deleteButton.textContent = 'close';

            // const concludeButton = document.createElement('button');
            // concludeButton.classList.add('material-icons', 'conclude-event');
            // concludeButton.textContent = 'check';

            eventElement.appendChild(titleElement);
            eventElement.appendChild(descriptionElement);
            // eventElement.appendChild(deleteButton);
            // eventElement.appendChild(concludeButton);

            savedEventsContainer.appendChild(eventElement);
        });
    }

    // Exibir o popup
    //openCreateEventPopup();
}

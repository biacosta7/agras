// Importa as novas funções que criei para manipular datas
import { getDayOfWeek } from './newDateFunctions.js';

// Importa o objeto que contém o estado atual do calendário
import { calendarState } from './showCalendar.js'

export function getEventsForDay(day, month, year) {
    // Filtra os eventos armazenados no calendário
    return calendarState.dayEvents.filter(event => {
        const eventStartDate = new Date(event.start_date);
        const eventEndDate = event.end_date ? new Date(event.end_date) : null;
        const currentDate = new Date(year, month, day);

        // Verifica se a data atual está dentro do intervalo do evento
        if (eventEndDate) {
            if (currentDate < eventStartDate || currentDate > eventEndDate) {
                return false;
            }
        } else {
            if (currentDate < eventStartDate) {
                return false;
            }
        }

        // Implementação para eventos recorrentes
        const timeDifference = currentDate.getTime() - eventStartDate.getTime();
        const daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));

        if (event.recurrence === "diária") {
            return true;

        } else if (event.recurrence === "semanal") {
            if (getDayOfWeek(year, month, day) !== getDayOfWeek(event.start_date.getFullYear(), event.start_date.getMonth(), event.start_date.getDate())) {
                return false;
            }
            const weeksDifference = Math.floor(daysDifference / 7);
            return weeksDifference >= 0;

        } else if (event.recurrence === "biweekly") {
            if (getDayOfWeek(year, month, day) !== getDayOfWeek(event.start_date.getFullYear(), event.start_date.getMonth(), event.start_date.getDate())) {
                return false;
            }
            const weeksDifference = Math.floor(daysDifference / 7);
            return weeksDifference >= 0 && weeksDifference % 2 === 0;

        } else if (event.recurrence === "mensal") {
            return currentDate.getDate() === eventStartDate.getDate();

        } else if (event.recurrence === "anual") {
            return currentDate.getDate() === eventStartDate.getDate() &&
                   currentDate.getMonth() === eventStartDate.getMonth();

        } else {
            // Eventos não recorrentes
            return currentDate.getTime() === eventStartDate.getTime();
        }
    });
}

// Função para adicionar marcadores de evento 
export function addMarker(markersContainer, color) {
    const marker = document.createElement("span");
    marker.classList.add("marker");

    // Define a cor do marcador com base no evento
    marker.style.backgroundColor = color;

    /*
    const markersNumber = markersContainer.children.length;
    // Preenche a segunda linha do grid primeiro, depois a primeira
    if (markersNumber < 4) {
        marker.style.gridArea = `2 / ${markersNumber + 1}`; // Linha 2, coluna 1 a 4
    } 
    else {
        marker.style.gridArea = `1 / ${markersNumber - 3}`; // Linha 1, coluna 1 a 4
    }
    */

    markersContainer.appendChild(marker);
}
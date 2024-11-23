// Importa as novas funções que criei para manipular datas
import {
  getDayOfWeek,
  getDaysInMonth,
  getMonthName,
} from "./newDateFunction.js";
// Importa a função de exibição do pop-up de adicionar evento no calendário
// import { openCreateEventPopup } from './createEvent.js';

// Constantes globais para armazenar a data atual (hoje)
const currentDate = new Date();
const YEAR = currentDate.getFullYear();
const MONTH = currentDate.getMonth() + 1; // getMonth() retorna o mês de 0 a 11, então é adicionado 1
const DAY = currentDate.getDate();

// Objeto constante global para armazenar o estado do calendário (dia, mês e ano exibidos)
// Inicializa com o dia de hoje e é atualizado conforme algum dia for clicado/ tocado
export const calendarState = {
  year: YEAR,
  month: MONTH,
  day: DAY,
  selectedDayElement: null,
  dayEvents: [
    // Exemplo de evento
    {
      title: "Exemplo de Evento",
      description: "Descrição do evento",
      start_date: new Date(2024, 11, 15), // 15 de novembro de 2024
      frequency: "weekly",
      end_date: new Date(2026, 12, 14),
      color: "var(--green-marker-bg-color)",
    },
    // Adicione outros eventos aqui
  ],
};

// Captura os botões de controle do calendário
const previousButton = document.querySelector(".previous-month");
const nextButton = document.querySelector(".next-month");

// Função para lidar com o toque em um dia do mês (para smartphones e tablets)
function handleDayTouch(event) {
  // Atualiza o dia com o dia que foi tocado
  calendarState.selectedDayElement = event.target;
  calendarState.day = event.target.textContent;

  // Previne o comportamento padrão para evitar que "tap-and-hold" interfira
  event.preventDefault();

  // Define a cor de fundo ao iniciar o toque
  event.target.style.backgroundColor = "var(--days-clicked-bg-color)";

  function handleTouchEnd() {
    // Volta à cor original
    event.target.style.backgroundColor = "var(--days-bg-color)";
    // Abre o popup
    openCreateEventPopup();
    // Listas o eventos do dia tocado
    //listAllEvents();
    // Remove os event listeners após o toque
    removeTouchListeners();
  }

  function handleTouchCancel() {
    // Volta à cor original se o toque for cancelado
    event.target.style.backgroundColor = "var(--days-bg-color)";
    // Remove os event listeners
    removeTouchListeners();
  }

  function handleTouchMove(moveEvent) {
    const touch = moveEvent.touches[0];
    const targetRect = event.target.getBoundingClientRect();

    // Verifica se o toque ainda está dentro dos limites do elemento
    if (
      touch.clientX < targetRect.left ||
      touch.clientX > targetRect.right ||
      touch.clientY < targetRect.top ||
      touch.clientY > targetRect.bottom
    ) {
      handleTouchCancel();
    }
  }

  function removeTouchListeners() {
    event.target.removeEventListener("touchend", handleTouchEnd);
    event.target.removeEventListener("touchcancel", handleTouchCancel);
    event.target.removeEventListener("touchmove", handleTouchMove);
  }

  // Adiciona event listeners para touchend, touchcancel e touchmove
  event.target.addEventListener("touchend", handleTouchEnd, { passive: true });
  event.target.addEventListener("touchcancel", handleTouchCancel, {
    passive: true,
  });
  event.target.addEventListener("touchmove", handleTouchMove, {
    passive: true,
  });
}

// Função para lidar com o clique em um dia do mês (para computadores)
function handleDayClick(event) {
  // Se o botão pressionado do mouse não foi o esquerdo
  if (event.button !== 0) {
    return; // Não faz nada
  }

  // Atualiza o dia com o dia que foi clicado
  calendarState.selectedDayElement = event.target;
  calendarState.day = event.target.textContent;

  // Adiciona a cor de fundo ao pressionar o botão do mouse ou dedo
  event.target.style.backgroundColor = "var(--days-clicked-bg-color)";

  // Remover a cor de fundo ao soltar o botão do mouse
  function handleMouseUp() {
    event.target.style.backgroundColor = "var(--days-bg-color)"; // Volta à cor original
    // Abre o pop-up
    openCreateEventPopup();
    // Listas o eventos do dia clicado
    //listAllEvents();
    // Remove os event listeners após o clique
    event.target.removeEventListener("mouseup", handleMouseUp);
    event.target.removeEventListener("mouseleave", handleMouseLeave);
  }

  // Remove a cor de fundo se o mouse for movido para fora antes de soltar
  function handleMouseLeave() {
    event.target.style.backgroundColor = "var(--days-bg-color)"; // Volta à cor original
    event.target.removeEventListener("mouseup", handleMouseUp);
    event.target.removeEventListener("mouseleave", handleMouseLeave);
  }

  event.target.addEventListener("mouseup", handleMouseUp);
  event.target.addEventListener("mouseleave", handleMouseLeave);
}

// Função para adicionar marcadores de evento
function addMarker(markersContainer, color) {
  const marker = document.createElement("span");
  marker.classList.add("marker");

  // Define a cor do marcador com base no evento
  marker.style.backgroundColor = color;

  const markersNumber = markersContainer.children.length;
  // Preenche a segunda linha do grid primeiro, depois a primeira
  if (markersNumber < 4) {
    marker.style.gridArea = `2 / ${markersNumber + 1}`; // Linha 2, coluna 1 a 4
  } else {
    marker.style.gridArea = `1 / ${markersNumber - 3}`; // Linha 1, coluna 1 a 4
  }

  markersContainer.appendChild(marker);
}

function getEventsForDay(day, month, year) {
  // Filtra os eventos armazenados no calendário
  return calendarState.dayEvents.filter((event) => {
    const eventDate = event.start_date;
    const eventEndDate = event.end_date; // Adicionando a data de fim do evento
    const currentDate = new Date(year, month, day);

    // Verifica se o evento começa no dia atual
    if (
      eventDate.getFullYear() === year &&
      eventDate.getMonth() === month &&
      eventDate.getDate() === day
    ) {
      if (eventEndDate) {
        // Se a data de fim existe, verifica se o dia atual está dentro do intervalo
        return currentDate >= eventDate && currentDate <= eventEndDate;
      } else {
        return true; // Para eventos sem data de fim, considera o evento como válido
      }
    }

    // Implementação para eventos recorrentes
    if (
      eventEndDate &&
      (currentDate < eventDate || currentDate > eventEndDate)
    ) {
      return false; // Se a data atual não está dentro do intervalo de repetição, descarta
    }

    if (event.frequency === "daily") {
      return true; // Eventos diários ocorrem todos os dias
    } else if (event.frequency === "weekly") {
      // Eventos semanais: verifica se o dia da semana é o mesmo e a diferença em semanas é exata
      const daysDifference = Math.floor(
        (currentDate - eventDate) / (1000 * 60 * 60 * 24)
      );
      return (
        currentDate.getDay() === eventDate.getDay() && daysDifference % 7 === 0
      );
    } else if (event.frequency === "biweekly") {
      // Eventos quinzenais (a cada duas semanas): mesmo dia da semana e diferença em semanas é par
      const daysDifference = Math.floor(
        (currentDate - eventDate) / (1000 * 60 * 60 * 24)
      );
      return (
        currentDate.getDay() === eventDate.getDay() &&
        (daysDifference / 7) % 2 === 0
      );
    } else if (event.frequency === "monthly") {
      // Eventos mensais: ocorre no mesmo dia do mês
      return eventDate.getDate() === day;
    } else if (event.frequency === "yearly") {
      // Eventos anuais: ocorre no mesmo dia e mês
      return eventDate.getMonth() === month && eventDate.getDate() === day;
    }

    return false; // Para eventos não recorrentes que não se encaixam nas condições
  });
}

export function showCalendar(month, year) {
  const calendarTitle = document.querySelector(".calendar-title");
  const monthElement = document.querySelector(".month");
  const daysCells = monthElement.querySelectorAll(".days");

  const dayOfWeek = getDayOfWeek(year, month, 1); // Dia da semana do primeiro dia do mês
  const daysInMonth = getDaysInMonth(year, month); // Total de dias no mês
  const daysInPreviousMonth = getDaysInMonth(year, month - 1); // Total de dias no mês anterior

  // Atualiza o título do calendário com o mês e o ano
  calendarTitle.textContent = `${getMonthName(month)} de ${year}`;

  let dayCounter = 1;

  // Limpa as células antes de preencher
  daysCells.forEach((cell) => {
    // Remove o conteúdo anterior
    cell.textContent = "";
    // Remove os estilos anteriores
    cell.style.backgroundColor = "";
    cell.style.color = "";
    cell.style.border = "";
    cell.style.boxShadow = "";
    cell.style.cursor = "";
    // Remove os escutadores de eventos antigos
    cell.removeEventListener("mousedown", handleDayClick);
    cell.removeEventListener("touchstart", handleDayTouch);

    // Remove as divs de números e marcadores, se existirem
    const dayNumber = cell.querySelector(".day-number");
    if (dayNumber) {
      cell.removeChild(dayNumber);
    }

    const markersContainer = cell.querySelector(".markers-container");
    if (markersContainer) {
      cell.removeChild(markersContainer);
    }
  });

  // Preenche as células com os últimos dias do mês anterior
  for (let i = 0; i < dayOfWeek; i++) {
    daysCells[i].textContent = daysInPreviousMonth - dayOfWeek + i + 1; // Últimos dias do mês anterior
    daysCells[i].style.backgroundColor = "var(--other-days-bg-color)"; // Cor do mês anterior
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

    //daysCells[i].textContent = dayCounter;
    dayNumber.style.color = "black";
    daysCells[i].style.backgroundColor = "var(--days-bg-color)"; // Cor de fundo
    daysCells[i].style.cursor = "pointer"; // Cursor apontador

    //const currentDayOfWeek = (i % 7);
    // Pinta o texto dos dias de domingo com vermelho
    //if (currentDayOfWeek === 0) {
    //    dayNumber.style.color = 'var(--sun-color)';
    //}
    // Pinta o texto dos dias de sábado com azul
    //else if (currentDayOfWeek === 6) {
    //    dayNumber.style.color = 'var(--sat-color)';
    //}

    // Verifica se é o dia de hoje, se for, adiciona um fundo diferente
    if (dayCounter === DAY && month === MONTH && year === YEAR) {
      daysCells[i].style.backgroundColor = "var(--days-clicked-bg-color)";
    }

    // Verifica se tem evento, se tiver, adiciona os marcadores
    //if (daysCells[i].classList.contains("marked-day")) {
    //    addMarker(markersContainer);
    //}

    // Verifica eventos para o dia
    const eventsForDay = getEventsForDay(dayCounter, month, year);
    if (eventsForDay.length > 0) {
      daysCells[i].classList.add("marked-day");
      // Adiciona até 8 marcadores
      for (let j = 0; j < Math.min(eventsForDay.length, 8); j++) {
        addMarker(markersContainer, eventsForDay[j].color);
      }
    }

    // Adiciona um escutador de evento de segurar clique/ toque para os dias do mês
    daysCells[i].addEventListener("mousedown", handleDayClick); // Mouse segurando (para computadores)
    daysCells[i].addEventListener("touchstart", handleDayTouch); // Toque segurando (para celulares/ tablets)

    dayCounter++;
  }

  // Preenche as células restantes com os primeiros dias próximo mês
  let nextDayCounter = 1;
  for (let i = dayOfWeek + daysInMonth; i < daysCells.length; i++) {
    daysCells[i].textContent = nextDayCounter; // Dias do mês seguinte
    daysCells[i].style.backgroundColor = "var(--other-days-bg-color)"; // Cor do próximo mês
    nextDayCounter++;
  }
}

function updateCalendar(newMonth, newYear) {
  showCalendar(newMonth, newYear); // Atualiza o calendário com os novos valores de mês e ano
}

function main() {
  // Evento de clique pro botão anterior
  previousButton.addEventListener("click", () => {
    if (calendarState.month === 1) {
      calendarState.month = 12; // Se estiver em janeiro, vai para dezembro
      calendarState.year--; // Diminui o ano
    } else {
      calendarState.month--; // Apenas diminui o mês
    }
    updateCalendar(calendarState.month, calendarState.year); // Atualiza o calendário
  });

  // Evento de clique pro botão seguinte
  nextButton.addEventListener("click", () => {
    if (calendarState.month === 12) {
      calendarState.month = 1; // Se estiver em dezembro, vai para janeiro
      calendarState.year++; // Aumenta o ano
    } else {
      calendarState.month++; // Apenas aumenta o mês
    }
    updateCalendar(calendarState.month, calendarState.year); // Atualiza o calendário
  });

  // Inicializa o calendário na primeira chamada com o mês e o ano atuais
  showCalendar(MONTH, YEAR);
}

// Chama a função main ao carregar o script
main();

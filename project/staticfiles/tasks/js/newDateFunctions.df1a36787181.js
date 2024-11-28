// Função que recebe uma string data e retorna ela formatada (DD/MM/AAAA)
export function formatDate(date) {
    if (!date) return ''; // Retorna vazio se a data estiver indefinida

    // Divide a string da data em dia, mês e ano
    let [day, month, year] = date.split("/");

    // Garante que o dia e o mês tenham dois dígitos e o ano quatro dígitos
    day = day.padStart(2, "0");
    month = month.padStart(2, "0");
    year = year.padStart(4, "0");

    // Retorna a data formatada
    return `${day}/${month}/${year}`;
}

// Função que recebe um dia de um mês de ano específico e retorna o dia da semana que cai esse dia
export function getDayOfWeek(year, month, day) {
    // Cria o objeto data
    const data = new Date(year, month - 1, day);    // Lembre-se que o mês em JS é 0-indexado (0 = janeiro, 1 = fevereiro, ..., 11 = dezembro)
    // Obtém o dia da semana (0 = domingo, 1 = segunda, ..., 6 = sábado)
    const dayOfWeek = data.getDay();
    return dayOfWeek;
}

// Função que recebe um dia da semana (0, 1, ..., 6) e retorna o nome desse dia da semana (Dom., Seg., ..., Sáb.)
export function getDayOfWeekName(dayOfWeek) {
    const dayOfWeekNames = [
        "Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"
    ];
    return dayOfWeekNames[dayOfWeek];
}

// Função que recebe um mês e um ano e retorna o número de dias desse mês
export function getDaysInMonth(year, month) {
    return new Date(year, month, 0).getDate();
}

// Função um mês (0, 1, ..., 11) e retorna o nome desse mês (Janeiro, Fevereiro, ..., Dezembro)
export function getMonthName(month) {
    const monthNames = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ];
    return monthNames[month - 1];
}
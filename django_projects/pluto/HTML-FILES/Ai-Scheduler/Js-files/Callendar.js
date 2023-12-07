const calendarBody = document.getElementById("calendarBody");
const currentMonth = document.getElementById("currentMonth");
const prevMonthButton = document.getElementById("prevMonth");
const nextMonthButton = document.getElementById("nextMonth");
const currentDate = new Date();

let currentYear = currentDate.getFullYear();
let currentMonthIndex = currentDate.getMonth();
let selectedDate = currentDate;

function buildCalendar(year, month) {
    calendarBody.innerHTML = "";
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();

    currentMonth.textContent = `${getMonthName(month)} ${year}`;

    let date = 1;
    for (let i = 0; i < 6; i++) {
        const row = document.createElement("tr");
        for (let j = 0; j < 7; j++) {
            if (i === 0 && j < firstDay.getDay()) {
                const cell = document.createElement("td");
                row.appendChild(cell);
            } else if (date <= daysInMonth) {
                const cell = document.createElement("td");
                cell.textContent = date;
                cell.addEventListener("click", () => {
                    selectedDate = new Date(year, month, date);
                    console.log("Selected Date:", selectedDate);
                });
                row.appendChild(cell);
                date++;
            }
        }
        calendarBody.appendChild(row);
    }
}

function getMonthName(monthIndex) {
    const months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ];
    return months[monthIndex];
}

prevMonthButton.addEventListener("click", () => {
    currentMonthIndex--;
    if (currentMonthIndex < 0) {
        currentMonthIndex = 11;
        currentYear--;
    }
    buildCalendar(currentYear, currentMonthIndex);
});

nextMonthButton.addEventListener("click", () => {
    currentMonthIndex++;
    if (currentMonthIndex > 11) {
        currentMonthIndex = 0;
        currentYear++;
    }
    buildCalendar(currentYear, currentMonthIndex);
});

buildCalendar(currentYear, currentMonthIndex);
const monthYear = document.getElementById("maand_jaar");

let currentDate = new Date();
let selectedDate = new Date();

function renderCalendar(){
    monthYear.textContent = currentDate.toLocaleDateString("nl-BE", {
        month: "long",
        year: "numeric"
    });
}

function vorige_maand(){
    currentDate.setMonth(currentDate.getMonth() - 1);

    selectedDate = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth(),
        1
    );

    renderCalendar();
}

function volgende_maand(){
    currentDate.setMonth(currentDate.getMonth() + 1);

    selectedDate = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth(),
        1
    );

    renderCalendar();
}

document.addEventListener("DOMContentLoaded", function(){
    renderCalendar();

    document.getElementById("vorige_maand")
        .addEventListener("click", vorige_maand);

    document.getElementById("volgende_maand")
        .addEventListener("click", volgende_maand);
})
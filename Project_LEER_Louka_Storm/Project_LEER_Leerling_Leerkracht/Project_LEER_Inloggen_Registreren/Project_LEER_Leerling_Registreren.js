const form = document.getElementById("registreerform");

// 1. Validatie nummer
function valideerNummer(nummer) {
    if (nummer === "") return "Vul een nummer in.";
    if (!/^\d+$/.test(nummer)) {
        return "Het nummer mag alleen cijfers bevatten.";
    }
    return "";
}

// 2. Validatie voornaam
function valideerVoornaam(voornaam) {
    if (voornaam === "") return "Vul je voornaam in.";
    if (!/^[\p{L} '-]+$/u.test(voornaam)) {
        return "De voornaam bevat ongeldige tekens.";
    }
    return "";
}

// 3. Validatie achternaam
function valideerAchternaam(achternaam) {
    if (achternaam === "") return "Vul je achternaam in.";
    if (!/^[\p{L} '-]+$/u.test(achternaam)) {
        return "De achternaam bevat ongeldige tekens.";
    }
    return "";
}

// 4. Validatie e-mail
function valideerEmail(email) {
    if (email === "") return "Vul je e-mailadres in.";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        return "Vul een geldig e-mailadres in.";
    }
    return "";
}

// 5. Validatie wachtwoord
function valideerWachtwoord(wachtwoord) {
    if (wachtwoord.trim() === "") {
        return "Vul een wachtwoord in.";
    }
    if (wachtwoord.length < 8) {
        return "Het wachtwoord moet minstens 8 tekens bevatten.";
    }
    return "";
}

function valideerKlas(klas, klassen){
    if (klas.trim() === "") {
        return "Vul een klas in.";
    }
    if (!(klas in klassen)){
        return "Dit is geen geldige klas";
    }
}

// 6. Controleer alle invoervelden
function valideerFormulier() {
    const nummer = document.getElementById("nummer").value.trim();
    const voornaam = document.getElementById("voornaam").value.trim();
    const achternaam = document.getElementById("achternaam").value.trim();
    const email = document.getElementById("e-mail").value.trim();
    const wachtwoord = document.getElementById("wachtwoord").value;
    const klas = document.getElementById("wachtwoord").value.trim()
    const fouten = [
        valideerNummer(nummer),
        valideerVoornaam(voornaam),
        valideerAchternaam(achternaam),
        valideerEmail(email),
        valideerWachtwoord(wachtwoord),
        valideerKlas(klas,["5ICW6","5ICW5","6ICW6","6ICW6","6ET","6HW","5HW"])
    ].filter(fout => fout !== "");

    if (fouten.length > 0) {
        alert(fouten.join("\n"));
        return false;
    }

    return true;
}

// 7. Controleer en verstuur het formulier
form.addEventListener("submit", async function(event) {
    event.preventDefault();

    if (!valideerFormulier()) {
        return;
    }

    const gegevens = {
        nummer: document.getElementById("nummer").value.trim(),
        voornaam: document.getElementById("voornaam").value.trim(),
        achternaam: document.getElementById("achternaam").value.trim(),
        email: document.getElementById("e-mail").value.trim(),
        wachtwoord: document.getElementById("wachtwoord").value,
        klas: document.getElementById("klas").value.trim()
    };

    try {
        const antwoord = await fetch("/registreren", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(gegevens)
        });

        const resultaat = await antwoord.text();

        if (!antwoord.ok) {
            alert(resultaat);
            return;
        }

        alert("Registratie succesvol opgeslagen!");
        form.reset();

    } catch (fout) {
        alert("Er kon geen verbinding worden gemaakt met de server.");
        console.error(fout);
    }
});
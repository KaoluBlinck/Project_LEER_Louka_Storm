import csv
import os
from flask import Flask, render_template, request

app = Flask(__name__)

BASIS_MAP = os.path.dirname(os.path.abspath(__file__))
BESTAND = os.path.join(BASIS_MAP, "datalijst_Louka Bellinck_Storm_Deborger_project.csv")

REGISTREREN_PAGINA = "registreren_Louka Bellinck_Storm_Deborger_project.html"
LOGIN_PAGINA = "login_Louka Bellinck_Storm_Deborger_project.html"

VELDEN = [
    "leerlingnummer",
    "voornaam",
    "familienaam",
    "klas",
    "email",
    "username",
    "password",
    "vak"
]


def bestand_aanmaken():
    # Maakt het bestand met header aan als het nog niet bestaat
    if not os.path.exists(BESTAND):
        with open(BESTAND, "w", newline="", encoding="utf-8") as bestand:
            writer = csv.DictWriter(bestand, fieldnames=VELDEN)
            writer.writeheader()


bestand_aanmaken()


@app.route("/")
def home():
    return render_template(REGISTREREN_PAGINA)


@app.route("/login")
def login():
    return render_template(LOGIN_PAGINA)


@app.route("/resultaat", methods=["POST"])
def resultaat():
    leerling = registreren()

    # Alle velden moeten correct ingevuld zijn
    if "" in leerling.values():
        return 'Niet alle velden zijn correct ingevuld. <a href="/">Terug</a>'

    if gebruiker_bestaat(leerling["username"]):
        return 'Deze gebruikersnaam bestaat al. <a href="/">Terug</a>'

    bestand_aanmaken()

    with open(BESTAND, "a", newline="", encoding="utf-8") as bestand:
        writer = csv.DictWriter(bestand, fieldnames=VELDEN)
        writer.writerow(leerling)

    return 'Je bent succesvol geregistreerd! <a href="/login">Nu inloggen</a>'


@app.route("/inloggen", methods=["POST"])
def inloggen():
    gebruikersnaam = request.form.get("gebruikersnaam", "").strip()
    wachtwoord = request.form.get("wachtwoord", "").strip()

    bestand_aanmaken()

    with open(BESTAND, "r", newline="", encoding="utf-8") as bestand:
        reader = csv.DictReader(bestand)

        for rij in reader:
            if rij["username"] == gebruikersnaam and rij["password"] == wachtwoord:
                return f"Welkom terug, {rij['voornaam']}!"

    return 'Onjuiste gebruikersnaam of wachtwoord. <a href="/login">Opnieuw proberen</a>'


def gebruiker_bestaat(gebruikersnaam):
    bestand_aanmaken()

    with open(BESTAND, "r", newline="", encoding="utf-8") as bestand:
        reader = csv.DictReader(bestand)

        for rij in reader:
            if rij["username"] == gebruikersnaam:
                return True

    return False


def registreren():
    Leerlingnummer = leerlingnummer()
    Voornaam = voornaam()
    Familienaam = familienaam()
    Klas = klas()
    eMailadres = emailadres()
    Gebruikersnaam = gebruikersnaam()
    Wachtwoord = wachtwoord()
    Remediëringsvak = remediëringsvak()

    leerling = {
        "leerlingnummer": Leerlingnummer,
        "voornaam": Voornaam,
        "familienaam": Familienaam,
        "klas": Klas,
        "email": eMailadres,
        "username": Gebruikersnaam,
        "password": Wachtwoord,
        "vak": Remediëringsvak
    }

    return leerling


def leerlingnummer():
    leerlingnummer = request.form.get("leerlingnummer", "").strip()

    if leerlingnummer != "" and leerlingnummer.isdigit():
        return leerlingnummer

    return ""


def voornaam():
    voornaam = request.form.get("voornaam", "").strip()

    if voornaam != "" and voornaam.replace(" ", "").isalpha():
        return voornaam

    return ""


def familienaam():
    familienaam = request.form.get("familienaam", "").strip()

    if familienaam != "" and familienaam.replace(" ", "").isalpha():
        return familienaam

    return ""


def klas():
    klas = request.form.get("klas", "").strip()

    if klas in ["1", "2", "3", "4"]:
        return klas

    return ""


def emailadres():
    email = request.form.get("email", "").strip()

    if "@" in email and email.count("@") == 1:
        positie_at = email.index("@")

        if positie_at > 0 and "." in email[positie_at + 1:]:
            positie_punt = email.index(".", positie_at)

            if positie_punt > positie_at + 1 and positie_punt < len(email) - 1:
                return email

    return ""


def gebruikersnaam():
    gebruikersnaam = request.form.get("gebruikersnaam", "").strip()

    return gebruikersnaam


def wachtwoord():
    wachtwoord = request.form.get("wachtwoord", "").strip()

    return wachtwoord


def remediëringsvak():
    remediëringsvak = request.form.get("remediëringsvak", "").strip()

    if remediëringsvak in ["1", "2", "3"]:
        return remediëringsvak

    return ""


if __name__ == "__main__":
    app.run(debug=True)

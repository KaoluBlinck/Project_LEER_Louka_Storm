import csv
import os
from flask import Flask, render_template, request

app = Flask(__name__)

BASIS_MAP = os.path.dirname(os.path.abspath(__file__))
BESTAND = os.path.join(BASIS_MAP, "datalijst_leerkracht_Louka Bellinck_Storm_Deborger_project.csv")

REGISTREREN_PAGINA = "registreren_leerkracht_Louka Bellinck_Storm_Deborger_project.html"
LOGIN_PAGINA = "login_leerkracht_Louka Bellinck_Storm_Deborger_project.html"

VELDEN = [
    "leerkrachtnummer",
    "voornaam",
    "familienaam",
    "klassen",
    "email",
    "username",
    "password",
    "vakken"
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
    leerkracht = registreren()

    # Alle velden (behalve het nummer, dat wordt automatisch gegeven) moeten correct ingevuld zijn
    for veld, waarde in leerkracht.items():
        if veld != "leerkrachtnummer" and waarde == "":
            return 'Niet alle velden zijn correct ingevuld. <a href="/">Terug</a>'

    if gebruiker_bestaat(leerkracht["username"]):
        return 'Deze gebruikersnaam bestaat al. <a href="/">Terug</a>'

    # Nummer pas toekennen als alles klopt, zodat er geen nummers verloren gaan
    leerkracht["leerkrachtnummer"] = nieuw_leerkrachtnummer()

    bestand_aanmaken()

    with open(BESTAND, "a", newline="", encoding="utf-8") as bestand:
        writer = csv.DictWriter(bestand, fieldnames=VELDEN)
        writer.writerow(leerkracht)

    return (
        f"Je bent succesvol geregistreerd!"
        f'<a href="/login">Nu inloggen</a>'
    )


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


def nieuw_leerkrachtnummer():
    # Zoekt het hoogste bestaande nummer (LK001, LK002, ...) en telt er 1 bij
    bestand_aanmaken()

    hoogste = 0

    with open(BESTAND, "r", newline="", encoding="utf-8") as bestand:
        reader = csv.DictReader(bestand)

        for rij in reader:
            cijfers = rij["leerkrachtnummer"].replace("LK", "")

            if cijfers.isdigit() and int(cijfers) > hoogste:
                hoogste = int(cijfers)

    return f"LK{hoogste + 1:03d}"


def registreren():
    Voornaam = voornaam()
    Familienaam = familienaam()
    Klassen = klassen()
    eMailadres = emailadres()
    Gebruikersnaam = gebruikersnaam()
    Wachtwoord = wachtwoord()
    Vakken = vakken()

    leerkracht = {
        "leerkrachtnummer": "",  # wordt automatisch toegekend in resultaat()
        "voornaam": Voornaam,
        "familienaam": Familienaam,
        "klassen": Klassen,
        "email": eMailadres,
        "username": Gebruikersnaam,
        "password": Wachtwoord,
        "vakken": Vakken
    }

    return leerkracht


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


def klassen():
    # Meerdere klassen mogelijk (checkboxes), opgeslagen als bv. "1;3;4"
    gekozen = request.form.getlist("klassen")
    geldig = [k for k in ["1", "2", "3", "4"] if k in gekozen]

    return ";".join(geldig)


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


def vakken():
    # Meerdere vakken mogelijk (checkboxes), opgeslagen als bv. "1;3"
    gekozen = request.form.getlist("vakken")
    geldig = [v for v in ["1", "2", "3"] if v in gekozen]

    return ";".join(geldig)


if __name__ == "__main__":
    # Andere poort dan de leerlingenversie, zodat je beide tegelijk kan laten draaien
    app.run(debug=True, port=5001)

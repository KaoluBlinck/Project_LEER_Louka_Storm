import re
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)
DB_NAAM = "Project_LEER_database.db"
GELDIGE_KLASSEN = ["5ICW6", "6ICW5", "6ICW6", "6ET", "6HW", "5HW"]

# 1. Database en tabel aanmaken
def init_db():
    conn = sqlite3.connect(DB_NAAM)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gebruikers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nummer TEXT UNIQUE NOT NULL,
            rol TEXT NOT NULL,
            voornaam TEXT NOT NULL,
            achternaam TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            wachtwoord TEXT NOT NULL,
            klas TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Routes voor je twee HTML-pagina's (pas de bestandsnamen aan naar jouw situatie)
@app.route('/registreer-leerling')
def pagina_leerling():
    return render_template('registreer_leerling.html')

@app.route('/registreer-leerkracht')
def pagina_leerkracht():
    return render_template('registreer_leerkracht.html')

# 2. Gezamenlijke route voor opslag
@app.route('/registreren', methods=['POST'])
def registreren():
    data = request.get_json()
    if not data:
        return "Geen gegevens ontvangen.", 400

    nummer = data.get("nummer", "").strip().upper()
    voornaam = data.get("voornaam", "").strip()
    achternaam = data.get("achternaam", "").strip()
    email = data.get("email", "").strip()
    wachtwoord = data.get("wachtwoord", "")
    # Bij leerkrachten wordt 'klas' mogelijk niet meegestuurd, dus vangen we None veilig op
    klas = (data.get("klas") or "").strip()

    # Controleer het formaat van het nummer en bepaal de rol
    if not re.match(r"^(LK)?\d+$", nummer):
        return "Ongeldig nummerformaat.", 400

    is_leerkracht = nummer.startswith("LK")
    rol = "leerkracht" if is_leerkracht else "leerling"

    # Algemene validatie
    if not voornaam or not achternaam:
        return "Voornaam en achternaam zijn verplicht.", 400
    if len(wachtwoord) < 8:
        return "Het wachtwoord moet minstens 8 tekens bevatten.", 400

    # Specifieke validatie per rol
    if is_leerkracht:
        if not re.match(r"^[^\s@]+@glorieuxsecundair\.be$", email) or ".student@" in email:
            return "Vul een geldig e-mailadres voor leerkrachten in.", 400
        klas_waarde = None
    else:
        if not re.match(r"^[^\s@]+\.student@glorieuxsecundair\.be$", email):
            return "Vul een geldig e-mailadres voor leerlingen in.", 400
        if klas not in GELDIGE_KLASSEN:
            return "Dit is geen geldige klas.", 400
        klas_waarde = klas

    # Opslaan in SQLite
    try:
        conn = sqlite3.connect(DB_NAAM)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gebruikers (nummer, rol, voornaam, achternaam, email, wachtwoord, klas)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (nummer, rol, voornaam, achternaam, email, wachtwoord, klas_waarde))
        conn.commit()
        return f"Registratie als {rol} succesvol opgeslagen!", 200

    except sqlite3.IntegrityError:
        return "Dit nummer of e-mailadres is al geregistreerd.", 400
    except Exception as e:
        print("Databasefout:", e)
        return "Er ging iets mis op de server bij het opslaan.", 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

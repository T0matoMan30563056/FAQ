# FAQ Nettside

En nettside der brukere kan stille spørsmål og få svar fra en admin.

---

## Innhold

- [Prosjektidé og problemstilling](#1-prosjektidé-og-problemstilling)
- [Systembeskrivelse](#2-systembeskrivelse)
- [Server- og infrastrukturoppsett](#3-server--infrastruktur--og-nettverksoppsett)
- [Prosjektstyring](#4-prosjektstyring----github-projects-kanban)
- [Databasebeskrivelse](#5-databasebeskrivelse)
- [Programstruktur](#6-programstruktur)
- [Kodeforklaring](#7-kodeforklaring)
- [Sikkerhet og pålitelighet](#8-sikkerhet-og-pålitelighet)
- [Feilsøking og testing](#9-feilsøking-og-testing)
- [Konklusjon og refleksjon](#10-konklusjon-og-refleksjon)

---

## 1. Prosjektidé og problemstilling

Prosjektet handler om å lage en FAQ-nettside der brukere kan stille spørsmål. En admin kan slette kommentarer og svare på spørsmål som brukere stiller.

Funksjonaliteten inkluderer også at alle kan se profilene til hverandre, noe som gir mulighet til å jobbe med SQL-joins og databaserelasjoner.

🔗 [GitHub Project (Kanban)](https://github.com/users/T0matoMan30563056/projects/5)

---

## 2. Systembeskrivelse

### Brukerflyt

1. Brukeren logger inn eller registrerer en ny bruker som lagres i databasen.
2. Etter innlogging kommer brukeren til **Mainpage**, der alle spørsmål er synlige og nye spørsmål kan postes.
3. Brukeren kan gå til **profilen sin** for å slette egne kommentarer, logge ut eller slette kontoen.
4. Hvis en bruker sletter kontoen sin, blir spørsmålene liggende på nettsiden, men med `Deleted_User` som brukernavn.

### Teknologier brukt

- Python / Flask
- MariaDB
- HTML / CSS

---

## 3. Server-, infrastruktur- og nettverksoppsett

**Servermiljø:** Ubuntu VM

```
Klient → Waitress → MariaDB
```

---

## 4. Prosjektstyring — GitHub Projects (Kanban)

Kanban var til stor hjelp i dette prosjektet for å holde oversikten over arbeidsoppgavene. Det gjorde det lettere å strukturere tanker og ha god kontroll på hva som til enhver tid måtte gjøres.

---

## 5. Databasebeskrivelse

### Tabell: `User`

| Field    | Type         | Null | Key | Default | Extra          |
|----------|--------------|------|-----|---------|----------------|
| id       | int(11)      | NO   | PRI | NULL    | auto_increment |
| username | varchar(100) | NO   | UNI | NULL    |                |
| password | varchar(255) | NO   |     | NULL    |                |
| is_admin | tinyint(1)   | YES  |     | NULL    |                |
| Active   | tinyint(1)   | NO   |     | 1       |                |

### Tabell: `Question`

| Field    | Type         | Null | Key | Default | Extra          |
|----------|--------------|------|-----|---------|----------------|
| id       | int(11)      | NO   | PRI | NULL    | auto_increment |
| username | varchar(255) | NO   | MUL | NULL    |                |
| question | varchar(255) | NO   |     | NULL    |                |
| answer   | text         | YES  |     | NULL    |                |

### SQL-eksempel

```sql
CREATE TABLE User (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,
    Active TINYINT(1) DEFAULT 1,
    PRIMARY KEY (id)
);

CREATE TABLE Question (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    question VARCHAR(255) NOT NULL,
    answer VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (username) REFERENCES User(username)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

---

## 6. Programstruktur

```
HTML → Flask → MariaDB → Flask → HTML
```

---

## 7. Kodeforklaring

### Login-ruten

```python
@app.route('/', methods=['POST','GET'])
def Login():
    session.clear()
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']

        db = get_db()
        cursor = db.cursor(dictionary=True)
    
        try:
            cursor.execute("SELECT * FROM User WHERE username = %s", (username,))
            user = cursor.fetchone()

            if not user['Active']:
                flash('Account is disabled.')
                return render_template('Login.html')

            if user and check_password_hash(user['password'], password):
                session['username'] = username
                return redirect('Mainpage')
            else:
                flash('Invalid username or password')

        except Exception as e:
            print(e)
            flash('Something went wrong, try again.')

        finally:
            cursor.close()
            db.close()
    return render_template('Login.html')
```

Dette er en standard login-rute med flere sikkerhetstiltak:

- `session.clear()` — sørger for at det ikke ligger igjen gammel sesjonsinformasjon fra tidligere besøk.
- `try / except / finally` — gjør koden mer oversiktlig og enklere å feilsøke, siden feil fanges opp og skrives ut.
- Sjekk på `Active`-feltet — hindrer innlogging på deaktiverte eller slettede kontoer.
- **Hashing av passord** — passord lagres aldri i klartekst, noe som gjør kontoer vesentlig vanskeligere å kompromittere.

---

## 8. Sikkerhet og pålitelighet

- `.env`-fil for sensitiv konfigurasjon som databasepassord og hemmelige nøkler.
- `.gitignore` for å unngå at sensitiv informasjon blir pushet til GitHub.
- Passord hashes med `werkzeug.security` (`generate_password_hash` / `check_password_hash`).

---

## 9. Feilsøking og testing

**Vanlige feil:**

- Feil rutenavn i `form action` eller andre skrivefeil i HTML/Python.
- Feil rekkefølge på SQL-oppdateringer — for eksempel å oppdatere `username` før `Active` settes til `FALSE`, slik at den andre oppdateringen peker på et brukernavn som ikke lenger finnes.
- Glemt `db.commit()` — endringer lagres ikke i databasen uten dette kallet.

**Feilsøkingsmetode:**

1. Sjekk konsollen for feilmeldinger og stack traces.
2. Bruk `print("dette fungerer")` strategisk for å finne ut hvor koden stopper opp.

---

## 10. Konklusjon og refleksjon

Gjennom dette prosjektet ble det lagt stor vekt på at koden er oversiktlig og lett å bygge videre på. Bruk av `try / except / finally` bidro til bedre struktur og enklere feilsøking. Et annet mål var å lage en nettside som er enkel og intuitiv å navigere.

**Utfordrende:** Å håndtere rekkefølgen på SQL-spørringer og forstå hvordan fremmednøkler påvirker `UPDATE`- og `DELETE`-operasjoner.

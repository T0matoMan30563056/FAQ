# FAQ Nettside

Ein nettside der brukarar kan stille spørsmål og få svar frå ein admin.

---

## Innhald

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

Prosjektet handler om å lage ein FAQ-nettside der brukaren kan stille spørsmål. Ein admin kan slette kommentarar og svare på spørsmål som folk stiller.

Funksjonaliteten inkluderer òg at alle kan sjå profilane til kvarandre, for å jobbe med joins og databaserelasjonar.

🔗 [GitHub Project (Kanban)](https://github.com/users/T0matoMan30563056/projects/5)

---

## 2. Systembeskrivelse

### Brukarflyt

1. Brukaren loggar inn eller registrerer ein ny brukar som vert lagra i databasen.
2. Etter innlogging kjem brukaren til **Mainpage**, der alle spørsmål er synlege og nye spørsmål kan postast.
3. Brukaren kan gå til **profilen sin** for å slette eigne kommentarar, logge ut eller slette kontoen.
4. Viss ein brukar slettar kontoen sin, vert spørsmåla framleis liggande på nettsida, men med `Deleted_User` som brukarnamn.

### Teknologiar brukt

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

Kanban hjalp mykje i dette prosjektet for å styre tankane og gi ei betre oversikt over kva som måtte gjerast. Det vart lettare å få alt ned på «ark» og halde seg organisert gjennom heile utviklingsprosessen.

---

## 5. Databasebeskrivelse

### Tabell: `User`

| Field      | Type         | Null | Key | Default | Extra          |
|------------|--------------|------|-----|---------|----------------|
| id         | int(11)      | NO   | PRI | NULL    | auto_increment |
| username   | varchar(100) | NO   | UNI | NULL    |                |
| password   | varchar(255) | NO   |     | NULL    |                |
| is_admin   | tinyint(1)   | YES  |     | NULL    |                |
| Active     | tinyint(1)   | NO   |     | 1       |                |

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

### Login-ruta

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

Dette er ein vanleg login-rute med fleire sikkerheitstiltak:

- `session.clear()` — sørgjer for at det ikkje ligg att gammal sesjonsinformasjon.
- `try / except / finally` — gjer koden meir oversiktleg og enklare å feilsøke.
- Sjekk på `Active`-feltet — hindrar innlogging på sletta kontoar.
- **Hashing av passord** — passord vert aldri lagra i klartekst, noko som gjer kontoar vesentleg vanskelegare å kompromittere.

---

## 8. Sikkerhet og pålitelighet

- `.env`-fil for sensitiv konfigurasjon (t.d. databasepassord).
- `.gitignore` for å unngå at sensitiv informasjon vert pusha til GitHub.
- Hasha passord med `werkzeug.security` (`check_password_hash`).

---

## 9. Feilsøking og testing

**Vanlege feil:**

- Feil rutenamn i `form action` eller andre skrivefeil.
- Rekkjefølgje på SQL-oppdateringar — t.d. å oppdatere `username` før `Active` vert sett, slik at den siste oppdateringa peiker på eit brukarnamn som ikkje lenger finst.
- Gløymd `db.commit()` — endringar vert ikkje lagra i databasen utan dette.

**Feilsøkingsmetode:**

1. Sjekk konsollen for feilmeldingar.
2. Bruk `print("dette funker")` strategisk for å finne kvar koden stoppar opp.

---

## 10. Konklusjon og refleksjon

Gjennom dette prosjektet vart det lagt stor vekt på at koden er oversiktleg og lett å utvide. Bruk av `try / except / finally` bidrog til betre struktur og enklare feilsøking. Det var òg eit mål å lage ei nettside som er enkel og intuitiv å bruke.

> **Hva var utfordrende?** Å handtere rekkjefølgja på SQL-spørjingar og forstå korleis framandnøklar påverkar `UPDATE`- og `DELETE`-operasjonar.

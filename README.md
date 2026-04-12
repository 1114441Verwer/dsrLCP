## ⚠️ Problemen met virtual environment (.venv)

### ❌ Probleem 1: `.venv` map is incompleet

Als je in de map `.venv/Scripts` alleen `python.exe` ziet en geen bestanden zoals `Activate.ps1` of `activate.bat`, dan is de virtual environment niet goed aangemaakt.

👉 Dit betekent dat je project niet goed kan draaien.

---

### ✅ Oplossing (stap voor stap)

1. Verwijder de map `.venv` volledig
2. Open de terminal in je projectmap
3. Maak een nieuwe virtual environment:

```bash
python -m venv .venv
```

(of gebruik `py -m venv .venv` als `python` niet werkt)

---

### ❌ Probleem 2: `.venv` activeren lukt niet

Gebruik het juiste commando afhankelijk van je terminal:

**PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**CMD:**

```cmd
.venv\Scripts\activate.bat
```

👉 Als het goed is zie je nu `(.venv)` vooraan in je terminalregel.

---

### ❌ Probleem 3: Django werkt niet

Foutmelding zoals:

```
ModuleNotFoundError: No module named 'django'
```

👉 Dit betekent dat de benodigde pakketten nog niet geïnstalleerd zijn.

---

### ✅ Oplossing

Voer dit uit in de terminal (met je `.venv` actief):

```bash
pip install django pillow
```

---

### 📌 Belangrijk

* De `.venv` map staat **niet op GitHub**
* Iedereen moet deze zelf aanmaken
* Je moet de `.venv` **altijd activeren voordat je het project gebruikt**

---

## 🔄 Na het mergen / pullen

Na het ophalen van nieuwe code kunnen er aanpassingen zijn gedaan aan de database (bijvoorbeeld nieuwe tabellen of velden).

👉 Daarom moet je je lokale database bijwerken, zodat deze overeenkomt met de nieuwste code.
Doe je dit niet, dan kan de applicatie fouten geven.

### ✅ Stappen

Haal de nieuwste code binnen:

```bash
git pull
```

Werk je database bij:

```bash
python manage.py migrate
```

## 🚀 Applicatie starten

Volg deze stappen om de applicatie te draaien:

### 1. Activeer je `.venv`

(Zie hierboven)

---

### 2. Start de server

```bash
python manage.py runserver
```

---

### 3. Open de applicatie in je browser

Na het starten zie je in de terminal iets zoals:

```
Starting development server at http://127.0.0.1:8000/
```

👉 Kopieer deze link en plak hem in je browser
👉 Of klik erop als dat kan

---

### 🛑 Server stoppen

Druk in de terminal op:

```
CTRL + C
```

👉 Dit stopt de server

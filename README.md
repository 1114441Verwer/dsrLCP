## ⚠️ Problemen met virtual environment (.venv)

### ❌ Probleem 1: .venv map is incompleet

Als je in `.venv/Scripts` alleen `python.exe` ziet en geen `Activate.ps1` of `activate.bat`:

👉 Dan is je venv kapot of verkeerd aangemaakt.

---

### ✅ Oplossing (in terminal)

1. Verwijder de oude `.venv`

2. Maak een nieuwe:

```bash
python -m venv .venv
```

of

```bash
py -m venv .venv
```

---

### ❌ Probleem 2: venv activeert niet

Gebruik het juiste commando afhankelijk van je terminal:

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
.venv\Scripts\activate.bat
```

---

### ❌ Probleem 3: Django werkt niet

Error zoals:

```
ModuleNotFoundError: No module named 'django'
```

---

### ✅ Oplossing

```bash
pip install django pillow
```

---

### 📌 Belangrijk

- `.venv` wordt niet gedeeld via Git
- Iedereen moet zelf een `.venv` maken
- Activeer altijd eerst je `.venv` voordat je het project start


🔄 Na het mergen / pullen

Na het ophalen van nieuwe wijzigingen moet je je lokale database updaten:

✅ Stappen
```
git pull
```
```
python manage.py migrate
```

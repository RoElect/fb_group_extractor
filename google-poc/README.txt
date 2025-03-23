HOW TO USE:

1. Create a Custom Search Engine:

- Visit Google Custom Search Engine.
- Click "Add" and create a new search engine.
- Set the site to facebook.com/groups or any site you want to restrict searches to, or leave it open to search the entire web.
- After creating, go to Control Panel and copy the CX ID.

2. Get an API Key:

- Go to Google Cloud Console.
- Enable the Custom Search API from the APIs library.
- Go to Credentials, create a new API key, and copy it.

3. Replace your API KEY and CX ID in the python scripts

4. Run the GUI Version:

- Run the GUI script with:

  ```sh
  python3 search_from_gui.py
  ```

- A graphical interface will appear, allowing you to select the location and key_words files manually.
- Click the "Run Search" button to start the extraction process.
- The results will be saved in a CSV file automatically.
- If no files are selected, the script will use default values and notify the user.

5. Run the CMD script:

- Save your locations in a text file (one per line).
- Save your key_words in another text file (one per line).
- Run the script from the command line:

  ```sh
  python3 scraper.py locations.txt key_words.txt
  ```

- If no files are provided, default values will be used, and the user will be notified.
- The script will generate a CSV file with the extracted Facebook groups.



HOW TO CREATE AN EXECUTABLE:


Pentru a permite utilizatorilor non-tehnici să ruleze aplicația, putem transforma scriptul Python într-un executabil folosind **PyInstaller**.

NOTA: Asta trebuie facut folosind API KEY-ul si CX ID-ul asociate contului care va suporta costurile!

---

### **1. Instalarea PyInstaller**
Dacă nu este deja instalat, rulează următoarea comandă:
```bash
pip install pyinstaller
```

---

### **2. Crearea Executabilului**
Mergi în directorul unde se află `search_from_gui.py` și rulează:
```bash
pyinstaller --onefile --windowed search_from_gui.py
```

#### **Explicație:**
- `--onefile`: Creează un singur fișier executabil (fără fișiere adiționale necesare).
- `--windowed`: Ascunde fereastra de terminal (ideal pentru aplicațiile GUI).

---

### **3. Găsirea Executabilului**
După rulare, vei găsi executabilul în folderul `dist/`:
- **Windows:** `dist/search_from_gui.exe`
- **Mac/Linux:** `dist/search_from_gui`

---

### **4. Distribuirea Aplicației**

#### **Windows**
- Pune `search_from_gui.exe` într-un fișier ZIP și oferă-l utilizatorilor.

#### **Mac/Linux**
- Asigură-te că fișierul are permisiuni de rulare:
  ```bash
  chmod +x search_from_gui
  ./search_from_gui
  ```

---

### **5. Creare Installer (Opțional)**
Pentru o instalare mai elegantă, se pot folosi:
- **Windows:** [NSIS](https://nsis.sourceforge.io/Download) pentru a crea un installer.
- **Mac:** [create-dmg](https://github.com/create-dmg/create-dmg) pentru a genera un `.dmg`.

# 🧾 EISSA - Registre de Vendes

**EISSA** és una aplicació d'escriptori desenvolupada en **Python** amb **Tkinter**, pensada per gestionar el registre diari de vendes de manera senzilla i local. Les dades es guarden en una base de dades **SQLite** inclosa dins l'aplicació.

---

## 📦 Característiques

- Interfície gràfica amb Tkinter.
- Registre i visualització de vendes per dia.
- Base de dades SQLite local i autogestionada.
- Possibilitat d'exportació del registre de vendes diari en format Ecel [opcional].
- Preparada per convertir-se en executables per **Windows** i **macOS**.

---

## 🚀 Requisits

### 1. Entorn de desenvolupament

- Python 3.10 o superior
- pip
- [Tkinter](https://tkdocs.com/tutorial/install.html) (normalment inclòs amb Python)
- SQLite3 (també inclòs)

### 2. Instal·lació de dependències

```bash
pip install -r requirements.txt
```


## 💻 Instal·lació i execució dels executables

### Windows (`.exe`)

1. **Descarrega o copia** el fitxer executable `main.exe` (i, si n’hi ha, els fitxers complementaris) a la carpeta on vulguis instal·lar l’aplicació.

2. **No cal instal·lació prèvia de Python**, l’executable és independent.

3. Per executar:

   - Fes doble clic a `dist/main.exe`.
   - O obre una finestra CMD i executa:

     ```cmd
     path\to\dist\main.exe
     ```

4. Si vols crear una instal·lació més formal:

   - Utilitza eines com **Inno Setup** o **NSIS** per fer un instal·lador `.msi` o `.exe` que copiï els fitxers a `C:\Program Files\` i afegeixi accessos directes.

---

### macOS (`.app`)

1. **Descarrega o copia** el fitxer `dist/main.app` a la carpeta `Aplicacions` o a qualsevol carpeta on vulguis instal·lar l’aplicació.

2. En la primera execució, és possible que macOS bloquegi l’aplicació per seguretat (Gatekeeper). Per permetre l’execució:

   - Obre **Preferències del Sistema > Seguretat i Privacitat**.
   - A la pestanya **General**, trobaràs un missatge que diu que l’aplicació ha estat bloquejada.
   - Fes clic a **Permetre igualment**.
   - Torna a executar fent doble clic a `main.app`.

3. Alternativament, des de terminal pots executar:

   ```bash
   xattr -d com.apple.quarantine /ruta/a/main.app
   open /ruta/a/main.app


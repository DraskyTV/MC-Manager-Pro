# 🧊 MC-Manager Pro `v0.1.0-BETA`

**MC-Manager Pro** je elegantní, rychlý a open-source správce lokálních Minecraft serverů. Zapomeňte na zmatené příkazové řádky, ruční stahování `.jar` souborů a neustálé přepisování textových konfigurací. Tento program udělá všechnu těžkou práci za vás přes přehledné webové rozhraní.

---

## 🚀 Hlavní funkce (Features)

* **One-Click Instalace:** Stačí zadat složku, vybrat verzi a program sám stáhne správný `server.jar` z internetu.
* **Kompletní Web UI:** Ovládání a konfigurace serveru probíhá v čistém lokálním webovém rozhraní na `http://localhost:5000`.
* **Správa vlastností:** Vizuální nastavení obtížnosti, herního módu, maximálního počtu slotů a bleskový přepínač pro PVP.
* **Podpora Warez (Online Mode):** Integrovaná možnost přepnutí účtů jedním kliknutím, aby se připojili i kamarádi bez originální hry.
* **Správa Adminů (OP):** Jednoduché přidávání herních operátorů přímo přes textové pole (automatický zápis do `ops.json`).
* **Bezpečné vypnutí:** Tlačítko pro okamžité a bezpečné zastavení serveru na pozadí.

---

## 🛠️ Podporované verze v BETA verzi

Aplikace aktuálně podporuje rychlé nasazení těchto verzí:
* **Paper 26.1.2** (Nejnovější experimentální / optimalizovaná verze)
* **Paper 1.21.1** (Doporučená stabilní verze)
* **Paper 1.20.1** (Ideální verze pro starší mody a pluginy)

---

## 📦 Jak aplikaci spustit (Pro uživatele)

1.  Stáhněte si nejnovější verzi souboru z karty **Releases** (soubor `MC-Manager.exe`).
2.  Spusťte program. Automaticky se vám otevře okno v prohlížeči.
3.  Do pole **Cesta k instalaci** zadejte složku (např. `C:\MinecraftServer`).
4.  Zvolte verzi hry a klikněte na **Potvrdit a připravit složku**. (Program na pozadí stáhne potřebné soubory).
5.  Upravte konfiguraci podle sebe, odsouhlaste EULA podmínky a klikněte na **Spustit server**.

---

## 💻 Vývoj a spuštění ze zdrojových kódů (Pro vývojáře)

Pokud chcete kód upravovat nebo testovat lokálně v Pythonu:

### Požadavky
* Python 3.10 nebo novější
* Nainstalované knihovny (Flask)

### Spuštění
1. Klonujte tento repozitář:
   ```bash

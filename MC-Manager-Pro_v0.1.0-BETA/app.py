import os
import sys
import subprocess
import webbrowser
import urllib.request
import json
import threading
from flask import Flask, jsonify, render_template, request

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

server_process = None
TARGET_DIR = os.getcwd() 
OPS_FILE = "ops.json"

def get_file_path(filename):
    return os.path.join(TARGET_DIR, filename)

def read_properties():
    prop_path = get_file_path("server.properties")
    properties = {}
    if not os.path.exists(prop_path):
        return properties
    with open(prop_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                properties[key.strip()] = val.strip()
    return properties

def write_properties(new_props):
    prop_path = get_file_path("server.properties")
    current_props = read_properties()
    current_props.update(new_props)
    with open(prop_path, "w", encoding="utf-8") as f:
        f.write("# Upraveno pomoci MC Dashboardu\n")
        for key, val in current_props.items():
            f.write(f"{key}={val}\n")

def read_ops():
    ops_path = get_file_path(OPS_FILE)
    if not os.path.exists(ops_path):
        return []
    try:
        with open(ops_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [player["name"] for player in data if "name" in player]
    except:
        return []

def write_ops(names_list):
    ops_path = get_file_path(OPS_FILE)
    ops_data = []
    for name in names_list:
        if name.strip():
            ops_data.append({
                "uuid": "",
                "name": name.strip(),
                "level": 4,
                "bypassesPlayerLimit": False
            })
    with open(ops_path, "w", encoding="utf-8") as f:
        json.dump(ops_data, f, indent=4)

def download_server_jar(target_folder, version):
    """
    Stáhne server.jar přímo z garantovaného odkazu pro vybranou verzi.
    """
    jar_path = os.path.join(target_folder, "server.jar")
    if os.path.exists(jar_path):
        print(f"[MC-Manager] Soubor server.jar pro verzi {version} již existuje. Stahování přeskočeno.")
        return

    print(f"[MC-Manager] Zahajuji přímé stahování verze {version} do: {target_folder}")
    
    # Slovník s přímými prověřenými odkazy na stažení core souborů
    version_urls = {
        "26.1.2": "https://fill-data.papermc.io/v1/objects/0555a0b0468a5198d8fb1a16e1f9e95c81a917a2dc8f2e09867b4044742f6401/paper-26.1.2-72.jar",
        "1.21.1": "https://fill-data.papermc.io/v1/objects/39bd8c00b9e18de91dcabd3cc3dcfa5328685a53b7187a2f63280c22e2d287b9/paper-1.21.1-133.jar",
        "1.20.1": "https://fill-data.papermc.io/v1/objects/234a9b32098100c6fc116664d64e36ccdb58b5b649af0f80bcccb08b0255eaea/paper-1.20.1-196.jar"
    }

    # Pokud verzi nemáme v tabulce, zkusíme univerzální fallback
    download_url = version_urls.get(version, "https://piston-data.mojang.com/v1/objects/latest/server.jar")

    try:
        req = urllib.request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(jar_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[MC-Manager] Verze {version} byla úspěšně stažena a uložena do složky.")
    except Exception as e:
        print(f"[MC-Manager] Kritická chyba při stahování verze {version}: {e}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/properties", methods=["GET", "POST"])
def manage_properties():
    if request.method == "POST":
        data = request.json
        if "ops_list" in data:
            write_ops(data["ops_list"])
            del data["ops_list"]
        write_properties(data)
        return jsonify({"status": "success", "message": "Veškerá konfigurace uložena."})
    
    props = read_properties()
    props["ops_list"] = read_ops()
    return jsonify(props)

@app.route("/api/config/init", methods=["POST"])
def init_folder():
    global TARGET_DIR
    data = request.json
    chosen_path = data.get("path", "").strip()
    server_name = data.get("name", "world").strip()
    version = data.get("version", "1.21.1").strip()
    
    if not chosen_path:
        return jsonify({"status": "error", "message": "Musíte zadat platnou cestu ke složce!"}), 400

    chosen_path = os.path.abspath(chosen_path)

    try:
        os.makedirs(chosen_path, exist_ok=True)
        TARGET_DIR = chosen_path
    except Exception as e:
        return jsonify({"status": "error", "message": f"Nelze vytvořit složku: {str(e)}"}), 400

    bat_path = get_file_path("start.bat")
    if not os.path.exists(bat_path):
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write("@echo off\njava -Xmx2G -Xms2G -jar server.jar nogui\n")

    write_properties({
        "level-name": server_name, 
        "online-mode": "false",
        "difficulty": "easy",
        "gamemode": "survival",
        "max-players": "20",
        "pvp": "true"
    })

    # Spuštění stahování asynchronně, aby Flask neodpověděl timeoutem
    threading.Thread(target=download_server_jar, args=(TARGET_DIR, version)).start()

    return jsonify({
        "status": "success", 
        "message": f"Pracovní složka byla nastavena na: {TARGET_DIR}. Na pozadí probíhá kontrola a stahování verze {version}. Za moment můžete server spustit!"
    })

@app.route("/api/server/check-eula", methods=["GET"])
def check_eula():
    eula_path = get_file_path("eula.txt")
    if os.path.exists(eula_path):
        with open(eula_path, "r", encoding="utf-8") as f:
            if "eula=true" in f.read().lower():
                return jsonify({"accepted": True})
    return jsonify({"accepted": False})

@app.route("/api/server/accept-eula", methods=["POST"])
def accept_eula():
    try:
        with open(get_file_path("eula.txt"), "w", encoding="utf-8") as f:
            f.write("# Schvaleno uzivatelem pres web\neula=true\n")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/server/start", methods=["POST"])
def start_server():
    global server_process
    if server_process and server_process.poll() is None:
        return jsonify({"status": "error", "message": "Server již běží."}), 400

    if not os.path.exists(get_file_path("server.jar")):
        return jsonify({"status": "error", "message": "Soubor server.jar chybí nebo se stále stahuje na pozadí!"}), 404

    try:
        server_process = subprocess.Popen(
            [get_file_path("start.bat")],
            cwd=TARGET_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        return jsonify({"status": "success", "message": "Minecraft server se úspěšně spouští v novém okně!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/server/stop", methods=["POST"])
def stop_server():
    global server_process
    if server_process and server_process.poll() is None:
        # Na Windows se pokusíme o korektní ukončení, případně terminate
        server_process.terminate()
        server_process = None
        return jsonify({"status": "success", "message": "Požadavek na vypnutí odeslán. Server se zavírá."})
    return jsonify({"status": "error", "message": "Server momentálně neběží."}), 400

@app.route("/api/server/status", methods=["GET"])
def server_status():
    global server_process
    is_running = server_process is not None and server_process.poll() is None
    return jsonify({"running": is_running, "path": TARGET_DIR})

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        webbrowser.open("http://localhost:5000")
    app.run(port=5000)
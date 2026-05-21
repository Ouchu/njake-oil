from flask import Flask, request, redirect, url_for, session, Response
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_FILE = "station_data.db"

FUEL_PRICES = {"petrol": "4,212", "diesel": "4,345"}
STATION_CONTACT = {
    "location": "Boma Ng'ombe, Hai District, Kilimanjaro",
    "phone": "+255 696 686 139",
    "email": "info@njakeoil.co.tz",
    "hours": "24 Hours / 7 Days"
}

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, phone TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("CREATE TABLE IF NOT EXISTS system_config (key TEXT PRIMARY KEY, value TEXT)")
    cursor.execute("SELECT value FROM system_config WHERE key = 'admin_user'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO system_config VALUES ('admin_user', 'OchuArtz'), ('admin_pass', 'Ochu2026')")
    conn.commit()
    conn.close()

init_db()

@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\n", mimetype="text/plain")

@app.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="google-site-verification" content="o5iVHg_XvWS6EozrnCE-Bp8obEF1LQzH2FgVrYnMlw0" />
        <title>Njake Oil & Commercial Hub</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-stone-50 text-stone-800">
        <nav class="bg-emerald-950 text-white p-4">
            <div class="max-w-6xl mx-auto flex justify-between">
                <span class="font-black text-emerald-400">NJAKE OIL</span>
                <div class="space-x-4">
                    <a href="/">Station</a>
                    <a href="/hub">Hub</a>
                    <a href="/admin">Admin</a>
                </div>
            </div>
        </nav>
        <header class="py-20 text-center">
            <h1 class="text-4xl font-black uppercase">Njake Petrol Station</h1>
            <p class="text-lg">Premium fuel and local dining services.</p>
        </header>
        <main class="max-w-4xl mx-auto p-6 text-center">
            <div class="bg-white p-6 rounded-lg shadow border">
                <h2 class="font-bold text-xl mb-4">Live Price Board</h2>
                <div class="grid grid-cols-2 gap-4">
                    <div class="p-4 bg-emerald-50 rounded">Petrol: {FUEL_PRICES['petrol']}/=</div>
                    <div class="p-4 bg-emerald-50 rounded">Diesel: {FUEL_PRICES['diesel']}/=</div>
                </div>
            </div>
        </main>
    </body>
    </html>
    """

@app.route("/hub")
def hub():
    return "<h1>Business Hub</h1><a href='/'>Back Home</a>"

@app.route("/admin")
def admin():
    return "<h1>Admin Panel</h1><a href='/'>Back Home</a>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

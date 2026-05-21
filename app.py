from flask import Flask, request, redirect, url_for, session, Response
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_FILE = "station_data.db"

FUEL_PRICES = {
    "petrol": "4,212",
    "diesel": "4,345"
}

STATION_CONTACT = {
    "location": "Boma Ng'ombe, Hai District, Kilimanjaro (Along Moshi-Arusha Highway)",
    "phone": "+255 696 686 139",
    "email": "info@njakeoil.co.tz",
    "hours": "24 Hours / 7 Days a week"
}

CAR_WASH_PRICES = [
    {"service": "Body Wash (Normal)", "price": "5,000", "desc": "Exterior pressure wash, tire shine, and basic wipe down."},
    {"service": "Full Wash & Vacuum", "price": "10,000", "desc": "Body wash, undercarriage clean, and thorough interior vacuum."},
    {"service": "Engine & Machine Wash", "price": "15,000", "desc": "Degreasing and high-pressure steam cleaning of the engine bay."}
]

DINER_PRICES = [
    {"item": "Njake Special Pilau", "price": "6,000", "desc": "Spiced rice served with tender beef, kachumbari, and a ripe banana."},
    {"item": "Chipo Kuku (Full Meal)", "price": "8,500", "desc": "Crispy golden french fries served with quarter deep-fried chicken."},
    {"item": "African Ginger Tea / Coffee", "price": "2,500", "desc": "Hot brewed local Kilimanjaro coffee or spiced ginger milk tea."}
]

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT value FROM system_config WHERE key = 'admin_user'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO system_config (key, value) VALUES ('admin_user', 'OchuArtz')")
        cursor.execute("INSERT INTO system_config (key, value) VALUES ('admin_pass', 'Ochu2026')")
    conn.commit()
    conn.close()

init_db()

@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\n", mimetype="text/plain")

def get_db_credentials():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM system_config WHERE key = 'admin_user'")
    username = cursor.fetchone()[0]
    cursor.execute("SELECT value FROM system_config WHERE key = 'admin_pass'")
    password = cursor.fetchone()[0]
    conn.close()
    return username, password

def get_nav(active_page):
    home_class = "text-emerald-400 font-bold" if active_page == "home" else "hover:text-emerald-400 transition"
    hub_class = "text-emerald-400 font-bold" if active_page == "hub" else "hover:text-emerald-400 transition"
    admin_class = "text-emerald-400 font-bold" if active_page == "admin" else "hover:text-emerald-400 transition"
    
    admin_link_text = "Admin Panel 🔓" if session.get("logged_in") else "Admin Panel"
    return f"""
    <nav class="bg-emerald-950 text-white p-4 shadow-md sticky top-0 z-50">
        <div class="max-w-6xl mx-auto flex justify-between items-center px-4">
            <span class="text-xl font-black tracking-wider text-emerald-400">NJAKE OIL & HUB</span>
            <div class="space-x-6 text-sm font-semibold">
                <a href="/" class="{home_class}">Station & Dining</a>
                <a href="/hub" class="{hub_class}">Business Hub</a>
                <a href="/admin" class="{admin_class}">{admin_link_text}</a>
            </div>
        </div>
    </nav>
    """

def get_footer():
    return """
    <footer class="bg-emerald-950 text-emerald-200/60 py-8 text-center text-sm border-t border-emerald-900 mt-12">
        <p>&copy; 2026 Njake Oil Station & Commercial Hub. All rights reserved.</p>
    </footer>
    """

@app.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="google-site-verification" content="o5iVHg_XvWS6EozrnCE-Bp8obEF1LQzH2FgVrYnMlw0" />
        <title>Njake Oil</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-stone-50 text-stone-800 font-sans">
        {get_nav("home")}
        </body>
    </html>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

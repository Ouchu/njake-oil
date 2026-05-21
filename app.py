from flask import Flask, request, redirect, url_for, session, Response
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_FILE = "station_data.db"

@app.route("/robots.txt")
def robots():
    return Response("User-agent: *\nAllow: /\n", mimetype="text/plain")

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
        cursor.execute("INSERT INTO system_config (key, value) VALUES ('admin_user', 'OchuArtz'), ('admin_pass', 'Ochu2026')")
    conn.commit()
    conn.close()

init_db()

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
    car_wash_html = "".join([f'<div class="flex justify-between items-start border-b border-stone-100 pb-3 last:border-0 last:pb-0"><div><h4 class="font-bold text-stone-900 text-sm">{item["service"]}</h4><p class="text-xs text-stone-500 mt-0.5">{item["desc"]}</p></div><span class="text-sm font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded whitespace-nowrap">{item["price"]}/=</span></div>' for item in CAR_WASH_PRICES])
    diner_html = "".join([f'<div class="flex justify-between items-start border-b border-stone-100 pb-3 last:border-0 last:pb-0"><div><h4 class="font-bold text-stone-900 text-sm">{item["item"]}</h4><p class="text-xs text-stone-500 mt-0.5">{item["desc"]}</p></div><span class="text-sm font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded whitespace-nowrap">{item["price"]}/=</span></div>' for item in DINER_PRICES])
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="google-site-verification" content="o5iVHg_XvWS6EozrnCE-Bp8obEF1LQzH2FgVrYnMlw0" />
        <title>Njake Oil & Commercial Hub - Boma Ng'ombe</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-stone-50 text-stone-800 font-sans">
        {get_nav("home")}
        <header class="bg-emerald-950 text-white py-20 px-6 text-center relative overflow-hidden">
            <div class="relative z-10 max-w-3xl mx-auto">
                <h1 class="text-4xl md:text-5xl font-black tracking-tight mb-4 uppercase">Njake Petrol Station</h1>
                <p class="text-lg text-emerald-100/85 mb-8 max-w-xl mx-auto">Refuel your vehicle with premium fuel, refresh your body at the diner, and keep your ride spotless.</p>
                <a href="/hub" class="bg-emerald-500 hover:bg-emerald-600 font-bold px-6 py-3 rounded-lg shadow-md transition inline-block">Explore Our Business Hub →</a>
            </div>
        </header>
        <section class="max-w-2xl mx-auto px-6 -mt-8 mb-12 relative z-20">
            <div class="bg-white rounded-xl shadow-lg border border-stone-200 overflow-hidden">
                <div class="bg-emerald-800 text-white px-6 py-3 flex justify-between items-center">
                    <span class="font-bold tracking-wide text-sm uppercase">Live Station Price Board</span>
                    <span class="text-xs bg-emerald-900 px-2 py-1 rounded text-emerald-300 font-mono">Currency: TZS / Litre</span>
                </div>
                <div class="grid grid-cols-2 divide-x divide-stone-200 text-center py-6">
                    <div><p class="text-xs text-stone-500 font-bold uppercase tracking-wider">Petrol (Super)</p><p class="text-2xl font-black text-emerald-600 mt-1">{FUEL_PRICES['petrol']}/=</p></div>
                    <div><p class="text-xs text-stone-500 font-bold uppercase tracking-wider">Diesel</p><p class="text-2xl font-black text-emerald-600 mt-1">{FUEL_PRICES['diesel']}/=</p></div>
                </div>
            </div>
        </section>
        <main class="max-w-6xl mx-auto px-6 py-4 grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-white rounded-xl shadow-sm border border-stone-200 p-6"><h3 class="text-lg font-black text-emerald-950 uppercase border-b border-stone-100 pb-3 mb-4">Pro Car Wash</h3>{car_wash_html}</div>
            <div class="bg-white rounded-xl shadow-sm border border-stone-200 p-6"><h3 class="text-lg font-black text-emerald-950 uppercase border-b border-stone-100 pb-3 mb-4">Diner Menu</h3>{diner_html}</div>
        </main>
        {get_footer()}
    </body>
    </html>
    """

@app.route("/hub", methods=["GET", "POST"])
def hub():
    status_message = ""
    if request.method == "POST":
        customer_name = request.form.get("name")
        customer_phone = request.form.get("phone")
        customer_msg = request.form.get("message")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (name, phone, message) VALUES (?, ?, ?)", (customer_name, customer_phone, customer_msg))
        conn.commit()
        conn.close()
        status_message = '<div class="bg-emerald-100 border text-emerald-800 px-4 py-3 rounded-lg mb-6 text-sm font-semibold">Message saved successfully.</div>'
    return f"{get_nav('hub')} <main class='max-w-6xl mx-auto px-6 py-12'>{status_message}<h1 class='text-2xl font-bold'>Digital Reception</h1></main> {get_footer()}"

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"): return redirect(url_for("login"))
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, message, timestamp FROM feedback ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return f"{get_nav('admin')} <main class='p-12'><h1>Management Dashboard</h1></main> {get_footer()}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["logged_in"] = True
        return redirect(url_for("admin"))
    return f"{get_nav('admin')} <main class='p-12'><h1>Login</h1></main> {get_footer()}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

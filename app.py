from flask import Flask, request, redirect, url_for, session
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
    car_wash_html = ""
    for item in CAR_WASH_PRICES:
        car_wash_html += f"""
        <div class="flex justify-between items-start border-b border-stone-100 pb-3 last:border-0 last:pb-0">
            <div>
                <h4 class="font-bold text-stone-900 text-sm">{item['service']}</h4>
                <p class="text-xs text-stone-500 mt-0.5">{item['desc']}</p>
            </div>
            <span class="text-sm font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded whitespace-nowrap">{item['price']}/=</span>
        </div>
        """

    diner_html = ""
    for item in DINER_PRICES:
        diner_html += f"""
        <div class="flex justify-between items-start border-b border-stone-100 pb-3 last:border-0 last:pb-0">
            <div>
                <h4 class="font-bold text-stone-900 text-sm">{item['item']}</h4>
                <p class="text-xs text-stone-500 mt-0.5">{item['desc']}</p>
            </div>
            <span class="text-sm font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded whitespace-nowrap">{item['price']}/=</span>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="google-site-verification" content="google382db9a9f69dd8fa" />
        <meta name="description" content="Njake Petrol Station and Commercial Hub in Boma Ng'ombe, Hai District. Premium fuel, professional car wash, and local dining services available 24/7." />
        <title>Njake Oil & Commercial Hub - Boma Ng'ombe</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-stone-50 text-stone-800 font-sans">
        {get_nav("home")}
        
        <header class="bg-emerald-950 text-white py-20 px-6 text-center relative overflow-hidden">
            <div class="absolute inset-0 opacity-10 bg-cover bg-center" style="background-image: url('/static/station_bg.png');"></div>
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
                    <div>
                        <p class="text-xs text-stone-500 font-bold uppercase tracking-wider">Petrol (Super)</p>
                        <p class="text-2xl font-black text-emerald-600 mt-1">{FUEL_PRICES['petrol']}/=</p>
                    </div>
                    <div>
                        <p class="text-xs text-stone-500 font-bold uppercase tracking-wider">Diesel</p>
                        <p class="text-2xl font-black text-emerald-600 mt-1">{FUEL_PRICES['diesel']}/=</p>
                    </div>
                </div>
            </div>
        </section>

        <main class="max-w-6xl mx-auto px-6 py-4 grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="bg-white rounded-xl shadow-sm border border-stone-200 overflow-hidden">
                <div class="h-48 bg-stone-200 bg-cover bg-center" style="background-image: url('/static/carwash.png');"></div>
                <div class="p-6">
                    <h3 class="text-lg font-black text-emerald-950 uppercase border-b border-stone-100 pb-3 mb-4 flex items-center gap-2">
                        <span>🧽</span> Pro Car Wash Price Menu
                    </h3>
                    <div class="space-y-4">
                        {car_wash_html}
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-stone-200 overflow-hidden">
                <div class="h-48 bg-stone-200 bg-cover bg-center" style="background-image: url('/static/diner.png');"></div>
                <div class="p-6">
                    <h3 class="text-lg font-black text-emerald-950 uppercase border-b border-stone-100 pb-3 mb-4 flex items-center gap-2">
                        <span>🍽️</span> Njake Diner Daily Menu
                    </h3>
                    <div class="space-y-4">
                        {diner_html}
                    </div>
                </div>
            </div>
        </main>

        <section class="max-w-6xl mx-auto px-6 py-8">
            <h3 class="text-xl font-black text-emerald-950 uppercase border-b border-stone-200 pb-3 mb-6 tracking-wide">
                👥 Our Dedicated Staff & Happy Customers
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-white rounded-xl shadow-sm border border-stone-200 overflow-hidden">
                    <div class="h-64 bg-stone-200 bg-cover bg-center" style="background-image: url('/static/staff.png');"></div>
                    <div class="p-4 text-center">
                        <span class="text-xs font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 px-2 py-1 rounded">Station Team</span>
                        <h4 class="font-bold text-stone-900 mt-2">Professional Service</h4>
                        <p class="text-xs text-stone-500 mt-1">Ready to assist you at the pump or dining area 24/7.</p>
                    </div>
                </div>
                <div class="bg-white rounded-xl shadow-sm border border-stone-200 overflow-hidden">
                    <div class="h-64 bg-stone-200 bg-cover bg-center" style="background-image: url('/static/customer1.png');"></div>
                    <div class="p-4 text-center">
                        <span class="text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-800 px-2 py-1 rounded">Happy Client</span>
                        <h4 class="font-bold text-stone-900 mt-2">Trusted Quality</h4>
                        <p class="text-xs text-stone-500 mt-1">Satisfied with our premium grade fuel and fast car wash service.</p>
                    </div>
                </div>
                <div class="bg-white rounded-xl shadow-sm border border-stone-200 overflow-hidden">
                    <div class="h-64 bg-stone-200 bg-cover bg-center" style="background-image: url('/static/customer2.png');"></div>
                    <div class="p-4 text-center">
                        <span class="text-xs font-bold uppercase tracking-wider bg-amber-100 text-amber-800 px-2 py-1 rounded">Happy Client</span>
                        <h4 class="font-bold text-stone-900 mt-2">Diner Visitors</h4>
                        <p class="text-xs text-stone-500 mt-1">Enjoying local delicacies at the Njake Commercial Hub.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="max-w-6xl mx-auto px-6 py-8">
            <div class="bg-emerald-950 text-white rounded-2xl p-8 shadow-md grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                <div>
                    <span class="text-xs font-bold uppercase tracking-widest text-emerald-400">Find Us Safely</span>
                    <h3 class="text-2xl font-black mt-1 mb-4 uppercase">Location & Contact Details</h3>
                    <p class="text-sm text-emerald-100/70 mb-6">Visit our branch location or reach out via phone for corporate fueling accounts, tailoring requests, or dining reservations.</p>
                    <div class="space-y-3 font-medium text-sm text-emerald-200">
                        <p class="flex items-center gap-3">📍 <span>{STATION_CONTACT['location']}</span></p>
                        <p class="flex items-center gap-3">📞 <span>{STATION_CONTACT['phone']}</span></p>
                        <p class="flex items-center gap-3">✉️ <span>{STATION_CONTACT['email']}</span></p>
                    </div>
                </div>
                <div class="bg-emerald-900/50 p-6 rounded-xl border border-emerald-800/60 text-center">
                    <p class="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-1">Station Status</p>
                    <p class="text-xl font-extrabold text-white mb-2">OPERATIONAL 🟢</p>
                    <div class="w-12 h-0.5 bg-emerald-500 mx-auto my-3"></div>
                    <p class="text-xs text-emerald-200/70">Timings: {STATION_CONTACT['hours']}</p>
                </div>
            </div>
        </section>

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
        cursor.execute("INSERT INTO feedback (name, phone, message) VALUES (?, ?, ?)", 
                       (customer_name, customer_phone, customer_msg))
        conn.commit()
        conn.close()
        
        status_message = f"""
        <div class="bg-emerald-100 border border-emerald-400 text-emerald-800 px-4 py-3 rounded-lg mb-6 text-sm font-semibold">
            Thank you {customer_name}! Your message has been saved safely.
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Njake Hub</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-stone-50 text-stone-800 font-sans">
        {get_nav("hub")}
        <header class="bg-emerald-900 text-white py-12 px-6 text-center">
            <h1 class="text-4xl font-extrabold mb-4">The Njake Commercial Hub</h1>
            <p class="text-lg text-emerald-100/80">Bringing essential services closer to you.</p>
        </header>

        <main class="max-w-6xl mx-auto px-6 py-12">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="md:col-span-2 space-y-8">
                    <div class="bg-white p-8 rounded-xl shadow-sm border border-stone-100">
                        <h3 class="text-xl font-bold text-emerald-950 mb-2">🪡 Executive Tailoring</h3>
                        <p class="text-sm text-stone-600">Custom tailoring for suits, dresses, and local designs.</p>
                    </div>
                    <div class="bg-white p-8 rounded-xl shadow-sm border border-stone-100">
                        <h3 class="text-xl font-bold text-emerald-950 mb-2">💵 Financial Agency</h3>
                        <p class="text-sm text-stone-600">Secure terminal for banking and mobile money services.</p>
                    </div>
                </div>

                <div class="bg-white p-6 rounded-xl shadow-md border border-stone-200">
                    <h3 class="text-lg font-bold text-stone-900 mb-4">Digital Reception Desk</h3>
                    {status_message}
                    <form action="/hub" method="POST" class="space-y-4">
                        <div>
                            <label class="block text-xs font-bold uppercase text-stone-500 mb-1">Your Name</label>
                            <input type="text" name="name" required class="w-full border border-stone-300 rounded px-3 py-2 text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase text-stone-500 mb-1">Phone Number</label>
                            <input type="tel" name="phone" required class="w-full border border-stone-300 rounded px-3 py-2 text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase text-stone-500 mb-1">Message / Request</label>
                            <textarea name="message" required rows="4" class="w-full border border-stone-300 rounded px-3 py-2 text-sm"></textarea>
                        </div>
                        <button type="submit" class="w-full bg-emerald-600 text-white font-bold py-2 rounded text-sm shadow">
                            Send to Reception
                        </button>
                    </form>
                </div>
            </div>
        </main>
        {get_footer()}
    </body>
    </html>
    """

@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""
    if request.method == "POST":
        username_input = request.form.get("username")
        password_input = request.form.get("password")
        
        db_user, db_pass = get_db_credentials()
        
        if username_input == db_user and password_input == db_pass:
            session["logged_in"] = True
            return redirect(url_for("admin"))
        else:
            error_msg = '<p class="text-xs font-bold text-rose-600 bg-rose-50 p-2 rounded border border-rose-200 mb-4 text-center">Invalid Identity Credentials</p>'

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Gateway</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-stone-100 flex flex-col min-h-screen font-sans">
        {get_nav("admin")}
        <main class="flex-grow flex items-center justify-center p-6">
            <div class="bg-white p-8 rounded-xl shadow-md border border-stone-200 w-full max-w-sm">
                <div class="text-center mb-6">
                    <span class="text-2xl">🔒</span>
                    <h3 class="text-lg font-black text-emerald-950 uppercase tracking-wide mt-2">Management Gateway</h3>
                    <p class="text-xs text-stone-500 mt-1">Authorized corporate access desk only</p>
                </div>
                {error_msg}
                <form action="/login" method="POST" class="space-y-4">
                    <div>
                        <label class="block text-xs font-bold uppercase text-stone-500 mb-1">System User ID</label>
                        <input type="text" name="username" required class="w-full border border-stone-300 rounded px-3 py-2 text-sm">
                    </div>
                    <div>
                        <label class="block text-xs font-bold uppercase text-stone-500 mb-1">Security Token Key</label>
                        <input type="password" name="password" required class="w-full border border-stone-300 rounded px-3 py-2 text-sm">
                    </div>
                    <button type="submit" class="w-full bg-emerald-950 hover:bg-emerald-900 text-white font-bold py-2 rounded text-sm shadow tracking-wide uppercase">
                        Unlock Console
                    </button>
                </form>
            </div>
        </main>
        {get_footer()}
    </body>
    </html>
    """

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    pwd_status = ""
    if request.method == "POST" and request.form.get("action") == "change_pwd":
        current_user, current_pass = get_db_credentials()
        old_pwd = request.form.get("old_password")
        new_pwd = request.form.get("new_password")
        
        if old_pwd == current_pass:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("UPDATE system_config SET value = ? WHERE key = 'admin_pass'", (new_pwd,))
            conn.commit()
            conn.close()
            pwd_status = '<p class="text-xs font-bold text-emerald-700 bg-emerald-50 p-2 rounded border border-emerald-200 mb-4">Password saved permanently to Database.</p>'
        else:
            pwd_status = '<p class="text-xs font-bold text-rose-600 bg-rose-50 p-2 rounded border border-rose-200 mb-4">Verification failed: Old password incorrect.</p>'

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, message, timestamp FROM feedback ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    table_rows = ""
    for row in rows:
        table_rows += f"""
        <tr class="border-b border-stone-200 hover:bg-stone-50">
            <td class="px-4 py-3 text-sm font-semibold text-stone-900">{row[1]}</td>
            <td class="px-4 py-3 text-sm text-emerald-700 font-mono">{row[2]}</td>
            <td class="px-4 py-3 text-sm text-stone-600">{row[3]}</td>
            <td class="px-4 py-3 text-xs text-stone-400 font-mono">{row[4]}</td>
            <td class="px-4 py-3 text-right">
                <form action="/admin/delete/{row[0]}" method="POST" onsubmit="return confirm('Delete this record permanently?');" class="inline">
                    <button type="submit" class="text-xs bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold px-2 py-1 rounded transition border border-rose-200">
                        Dismiss
                    </button>
                </form>
            </td>
        </tr>
        """

    if not table_rows:
        table_rows = """<tr><td colspan="5" class="text-center py-8 text-stone-400 text-sm italic">No messages found in database.</td></tr>"""

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Njake Oil - Web Admin</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    </head>
    <body class="bg-stone-100 text-stone-800 font-sans">
        {get_nav("admin")}
        <main class="max-w-6xl mx-auto px-6 py-12 grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <div class="lg:col-span-2">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-xl font-black text-emerald-950 uppercase tracking-wide">Manager Dashboard Desk</h2>
                    <span class="bg-emerald-600 text-white text-xs font-bold px-2 py-0.5 rounded shadow">DB Mode</span>
                </div>
                <div class="bg-white rounded-xl shadow border border-stone-200 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="bg-emerald-900 text-white text-xs font-bold uppercase tracking-wider">
                                    <th class="px-4 py-3">Customer Name</th>
                                    <th class="px-4 py-3">Phone Contact</th>
                                    <th class="px-4 py-3">Message Details</th>
                                    <th class="px-4 py-3">Date/Time</th>
                                    <th class="px-4 py-3 text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-stone-100">
                                {table_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="space-y-6">
                <div class="bg-white p-6 rounded-xl shadow border border-stone-200">
                    <h3 class="text-sm font-black text-stone-900 uppercase tracking-wider mb-4 border-b border-stone-100 pb-2">🔑 Security Credentials Console</h3>
                    {pwd_status}
                    <form action="/admin" method="POST" class="space-y-4">
                        <input type="hidden" name="action" value="change_pwd">
                        <div>
                            <label class="block text-xs font-bold uppercase text-stone-500 mb-1">Verify Current Password</label>
                            <input type="password" name="old_password" required class="w-full border border-stone-300 rounded px-2 py-1.5 text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-bold uppercase text-stone-500 mb-1">New Secure Password</label>
                            <input type="password" name="new_password" required class="w-full border border-stone-300 rounded px-2 py-1.5 text-sm">
                        </div>
                        <button type="submit" class="w-full bg-emerald-950 hover:bg-emerald-900 text-white font-bold py-2 rounded text-xs uppercase tracking-wider transition shadow">
                            Update Token Key
                        </button>
                    </form>
                </div>

                <div class="bg-stone-50 p-4 rounded-xl border border-stone-200 text-center">
                    <p class="text-xs text-stone-500 font-medium">Session Controller</p>
                    <a href="/logout" class="mt-2 block w-full text-center text-xs bg-rose-600 hover:bg-rose-700 text-white font-bold py-2 rounded transition shadow uppercase tracking-wider">
                        Terminate Session
                    </a>
                </div>
            </div>

        </main>
        {get_footer()}
    </body>
    </html>
    """

@app.route("/admin/delete/<int:record_id>", methods=["POST"])
def delete_message(record_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedback WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

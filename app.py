from flask import Flask, request, redirect, url_for, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "njake_super_secure_key_2026")

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
    {
        "service": "Body Wash (Normal)",
        "price": "5,000",
        "desc": "Exterior pressure wash, tire shine, and body wipe down."
    },
    {
        "service": "Full Wash & Vacuum",
        "price": "10,000",
        "desc": "Interior vacuum, undercarriage cleaning, and body wash."
    },
    {
        "service": "Engine & Machine Wash",
        "price": "15,000",
        "desc": "Steam engine cleaning and degreasing service."
    }
]

DINER_PRICES = [
    {
        "item": "Njake Special Pilau",
        "price": "6,000",
        "desc": "Spiced rice with beef and fresh salad."
    },
    {
        "item": "Chips Kuku",
        "price": "8,500",
        "desc": "French fries with crispy fried chicken."
    },
    {
        "item": "Tea / Coffee",
        "price": "2,500",
        "desc": "Fresh Kilimanjaro tea or coffee."
    }
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

    cursor.execute("SELECT value FROM system_config WHERE key='admin_user'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO system_config (key,value) VALUES (?,?)",
            ("admin_user", os.environ.get("ADMIN_USER", "admin"))
        )

        cursor.execute(
            "INSERT INTO system_config (key,value) VALUES (?,?)",
            ("admin_pass", os.environ.get("ADMIN_PASS", "change_this_password"))
        )

    conn.commit()
    conn.close()

init_db()


def get_db_credentials():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT value FROM system_config WHERE key='admin_user'")
    username = cursor.fetchone()[0]

    cursor.execute("SELECT value FROM system_config WHERE key='admin_pass'")
    password = cursor.fetchone()[0]

    conn.close()

    return username, password

def get_nav(active_page):

    home_class = "text-emerald-400 font-bold" if active_page == "home" else "hover:text-emerald-400"
    hub_class = "text-emerald-400 font-bold" if active_page == "hub" else "hover:text-emerald-400"
    admin_class = "text-emerald-400 font-bold" if active_page == "admin" else "hover:text-emerald-400"

    admin_text = "Admin 🔓" if session.get("logged_in") else "Admin"

    return f"""
    <nav class="bg-emerald-950 text-white p-4 sticky top-0 z-50 shadow">
        <div class="max-w-6xl mx-auto flex justify-between items-center">
            <div class="font-black text-xl text-emerald-400">
                NJAKE OIL
            </div>

            <div class="space-x-5 text-sm font-semibold">
                <a href="/" class="{home_class}">Home</a>
                <a href="/hub" class="{hub_class}">Hub</a>
                <a href="/admin" class="{admin_class}">{admin_text}</a>
            </div>
        </div>
    </nav>
    """

def get_footer():
    year = datetime.now().year

    return f"""
    <footer class="bg-emerald-950 text-emerald-100 text-center py-8 mt-12">
        <p class="text-sm">
            © {year} Njake Oil & Commercial Hub. All rights reserved.
        </p>
    </footer>
    """


@app.route("/robots.txt")
def robots():
    return """
User-agent: *
Allow: /

Sitemap: https://njake-oil.onrender.com/sitemap.xml
""", 200, {'Content-Type': 'text/plain'}

@app.route("/sitemap.xml")
def sitemap():

    return """<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

<url>
<loc>https://njake-oil.onrender.com/</loc>
<priority>1.0</priority>
</url>

<url>
<loc>https://njake-oil.onrender.com/hub</loc>
<priority>0.8</priority>
</url>

</urlset>
""", 200, {'Content-Type': 'application/xml'}


@app.route("/")
def home():

    car_wash_html = ""

    for item in CAR_WASH_PRICES:
        car_wash_html += f"""
        <div class="border-b border-stone-100 pb-3">
            <div class="flex justify-between">
                <h4 class="font-bold">{item['service']}</h4>
                <span class="font-black text-emerald-700">
                    {item['price']}/=
                </span>
            </div>

            <p class="text-sm text-stone-500 mt-1">
                {item['desc']}
            </p>
        </div>
        """

    diner_html = ""

    for item in DINER_PRICES:
        diner_html += f"""
        <div class="border-b border-stone-100 pb-3">
            <div class="flex justify-between">
                <h4 class="font-bold">{item['item']}</h4>
                <span class="font-black text-emerald-700">
                    {item['price']}/=
                </span>
            </div>

            <p class="text-sm text-stone-500 mt-1">
                {item['desc']}
            </p>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>
Best Petrol Station in Boma Ng'ombe | Njake Oil
</title>

<meta name="description"
content="Njake Oil is a 24/7 petrol station in Boma Ng'ombe offering premium fuel, diner meals, car wash services, and commercial services in Kilimanjaro Tanzania.">

<meta name="keywords"
content="petrol station Tanzania, fuel station Kilimanjaro, Boma Ngombe fuel, Njake Oil, car wash Tanzania">

<meta name="robots" content="index, follow">

<link rel="canonical"
href="https://njake-oil.onrender.com/">

<meta property="og:title"
content="Njake Oil & Commercial Hub">

<meta property="og:description"
content="Fuel station, diner and car wash services in Boma Ng'ombe Tanzania">

<meta property="og:type"
content="website">

<meta property="og:url"
content="https://njake-oil.onrender.com/">

<meta name="google-site-verification"
content="b9hkInA3eYjlBFb0rPtxlf4vwsGy8ehSDPgleEamrSI">

<script type="application/ld+json">
{{
"@context": "https://schema.org",
"@type": "GasStation",
"name": "Njake Oil Station",
"address": {{
"@type": "PostalAddress",
"addressLocality": "Boma Ng'ombe",
"addressRegion": "Kilimanjaro",
"addressCountry": "TZ"
}},
"telephone": "+255696686139",
"openingHours": "Mo-Su 00:00-23:59"
}}
</script>

<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

</head>

<body class="bg-stone-50 text-stone-800 font-sans">

{get_nav("home")}

<header class="bg-emerald-950 text-white py-20 text-center px-6">

<h1 class="text-5xl font-black mb-5">
Best Petrol Station in Boma Ng'ombe
</h1>

<p class="max-w-2xl mx-auto text-lg text-emerald-100">
24/7 fuel station, premium diesel, restaurant meals,
professional car wash and commercial hub services in
Hai District, Kilimanjaro Tanzania.
</p>

<a href="/hub"
class="mt-8 inline-block bg-emerald-500 hover:bg-emerald-600 px-6 py-3 rounded-lg font-bold shadow">
Explore Commercial Hub →
</a>

</header>

<!-- rest unchanged -->
</body>
</html>
"""

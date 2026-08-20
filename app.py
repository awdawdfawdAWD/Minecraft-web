import os
import json
import time
import threading
import urllib.request
from functools import wraps
from flask import Flask, request, redirect, Response, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32).hex())

OWNER_USERNAME = os.environ.get("OWNER_USER", "owner")
OWNER_PASSWORD = os.environ.get("OWNER_PASS", "changeme")

CLIENT_URL = os.environ.get("CLIENT_URL", "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/unkk-62.0.0.20260820.085414.jar")
FABRIC_API_URL = os.environ.get("FABRIC_URL", "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/fabric-api-0.156.0+26.2.jar")
GITHUB_REPO = "awdawdfawdAWD/Minecraft-web"
GITHUB_SCREENSHOTS_FOLDER = "screenshots"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/" + GITHUB_REPO + "/main/" + GITHUB_SCREENSHOTS_FOLDER

DOWNLOAD_COUNT = 147
APP_START_TIME = time.time()
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def fetch_screenshots_from_github():
    try:
        url = "https://api.github.com/repos/" + GITHUB_REPO + "/contents/" + GITHUB_SCREENSHOTS_FOLDER
        req = urllib.request.Request(url, headers={"User-Agent": "unkk-client-site"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        images = []
        for item in data:
            name = item.get("name", "")
            if any(name.lower().endswith(ext) for ext in IMAGE_EXTS):
                images.append({"name": name, "url": GITHUB_RAW_BASE + "/" + name})
        return images
    except Exception as e:
        print("GitHub screenshot fetch error: " + str(e))
        return []


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated

SITE_CSS = '''
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#e0e0e0;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;min-height:100vh;overflow-x:hidden}
a{color:#7c3aed;text-decoration:none;transition:color .2s}
a:hover{color:#a78bfa}
.hero{position:relative;padding:120px 40px 80px;text-align:center;background:linear-gradient(135deg,#0a0a1a 0%,#1a0a2e 50%,#0a1a2e 100%);overflow:hidden}
.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at 30% 50%,rgba(124,58,237,.15) 0%,transparent 50%),radial-gradient(circle at 70% 50%,rgba(59,130,246,.1) 0%,transparent 50%);animation:pulse 8s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1);opacity:.7}50%{transform:scale(1.05);opacity:1}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes glow{0%,100%{box-shadow:0 0 20px rgba(124,58,237,.3)}50%{box-shadow:0 0 40px rgba(124,58,237,.6)}}
.hero h1{font-size:3.5em;font-weight:800;background:linear-gradient(135deg,#a78bfa,#7c3aed,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:fadeInUp .8s ease-out;position:relative;z-index:1}
.hero .tagline{font-size:1.3em;color:#94a3b8;margin-top:16px;animation:fadeInUp .8s ease-out .2s both;position:relative;z-index:1}
.hero .version-badge{display:inline-block;margin-top:20px;padding:8px 24px;background:rgba(124,58,237,.2);border:1px solid rgba(124,58,237,.4);border-radius:50px;color:#a78bfa;font-size:.9em;animation:fadeInUp .8s ease-out .4s both;position:relative;z-index:1}
.stats-bar{display:flex;justify-content:center;gap:60px;padding:30px;background:rgba(10,10,15,.8);border-bottom:1px solid rgba(124,58,237,.1);animation:fadeInUp .8s ease-out .6s both}
.stat-item{text-align:center}
.stat-number{font-size:2em;font-weight:700;color:#7c3aed}
.stat-label{font-size:.85em;color:#64748b;margin-top:4px}
nav{display:flex;justify-content:center;gap:8px;padding:16px;background:rgba(10,10,15,.9);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,.05);position:sticky;top:0;z-index:100}
nav a{padding:10px 24px;border-radius:12px;font-size:.9em;font-weight:500;color:#94a3b8;transition:all .3s ease;position:relative}
nav a:hover{color:#e0e0e0;background:rgba(124,58,237,.1)}
nav a.active{color:#a78bfa;background:rgba(124,58,237,.15);box-shadow:0 0 20px rgba(124,58,237,.1)}
.container{max-width:1100px;margin:0 auto;padding:60px 20px}
.section{margin-bottom:80px;animation:fadeInUp .8s ease-out}
.section-title{font-size:2.2em;font-weight:700;margin-bottom:12px;background:linear-gradient(135deg,#e0e0e0,#94a3b8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.section-desc{color:#64748b;font-size:1.05em;margin-bottom:32px;line-height:1.7}
.feature-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:24px}
.feature-card{background:rgba(20,20,30,.6);border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:32px;transition:all .3s ease;position:relative;overflow:hidden}
.feature-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#7c3aed,transparent);opacity:0;transition:opacity .3s}
.feature-card:hover{transform:translateY(-4px);border-color:rgba(124,58,237,.3);box-shadow:0 20px 60px rgba(0,0,0,.3)}
.feature-card:hover::before{opacity:1}
.feature-icon{font-size:2em;margin-bottom:16px}
.feature-card h3{font-size:1.2em;margin-bottom:8px;color:#e0e0e0}
.feature-card p{color:#64748b;font-size:.95em;line-height:1.6}
.screenshot-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}
.screenshot-card{border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,.06);transition:all .3s ease;background:rgba(20,20,30,.6)}
.screenshot-card:hover{transform:translateY(-4px);box-shadow:0 20px 60px rgba(0,0,0,.4);border-color:rgba(124,58,237,.3)}
.screenshot-card img{width:100%;height:200px;object-fit:cover;display:block}
.screenshot-card .caption{padding:12px 16px;color:#94a3b8;font-size:.85em}
.download-section{text-align:center;padding:80px 20px;background:linear-gradient(135deg,rgba(124,58,237,.05) 0%,rgba(59,130,246,.05) 100%);border-radius:24px;border:1px solid rgba(124,58,237,.1)}
.download-btn{display:inline-block;padding:18px 48px;background:linear-gradient(135deg,#7c3aed,#5b21b6);color:#fff;font-size:1.15em;font-weight:700;border-radius:16px;border:none;cursor:pointer;transition:all .3s ease;text-decoration:none;animation:glow 3s ease-in-out infinite}
.download-btn:hover{transform:scale(1.05);box-shadow:0 0 60px rgba(124,58,237,.5);color:#fff}
.download-btn:active{transform:scale(.98)}
.download-buttons{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:24px}
.secondary-btn{padding:14px 36px;background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.3);color:#a78bfa;font-weight:600;border-radius:14px;font-size:1em;cursor:pointer;transition:all .3s;text-decoration:none}
.secondary-btn:hover{background:rgba(124,58,237,.2);transform:translateY(-2px);color:#a78bfa}
.footer{text-align:center;padding:40px;color:#334155;font-size:.85em;border-top:1px solid rgba(255,255,255,.03)}
.auth-container{max-width:400px;margin:80px auto;padding:48px;background:rgba(20,20,30,.8);border:1px solid rgba(255,255,255,.06);border-radius:20px;animation:fadeInUp .6s ease-out}
.auth-container h2{text-align:center;margin-bottom:32px;font-size:1.8em}
.auth-container label{display:block;margin-bottom:8px;color:#94a3b8;font-size:.9em}
.auth-container input{width:100%;padding:14px 16px;background:rgba(10,10,15,.6);border:1px solid rgba(255,255,255,.08);border-radius:12px;color:#e0e0e0;font-size:1em;margin-bottom:20px;transition:border-color .2s}
.auth-container input:focus{outline:none;border-color:#7c3aed}
.auth-container .btn{width:100%;padding:14px;background:linear-gradient(135deg,#7c3aed,#5b21b6);border:none;color:#fff;font-size:1em;font-weight:600;border-radius:12px;cursor:pointer;transition:all .3s}
.auth-container .btn:hover{box-shadow:0 0 30px rgba(124,58,237,.4)}
.auth-error{color:#ef4444;text-align:center;margin-bottom:16px;font-size:.9em}
.dash-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}
.dash-card{background:rgba(20,20,30,.6);border:1px solid rgba(255,255,255,.06);border-radius:16px;padding:28px;text-align:center}
.dash-card h3{color:#94a3b8;font-size:.85em;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px}
.dash-card .num{font-size:2.5em;font-weight:700;color:#a78bfa}
.edit-section{max-width:800px;margin:0 auto}
.edit-group{margin-bottom:32px}
.edit-group label{display:block;margin-bottom:8px;color:#94a3b8;font-weight:500}
.edit-group input,.edit-group textarea{width:100%;padding:14px;background:rgba(10,10,15,.6);border:1px solid rgba(255,255,255,.08);border-radius:12px;color:#e0e0e0;font-size:1em;transition:border-color .2s}
.edit-group input:focus,.edit-group textarea:focus{outline:none;border-color:#7c3aed}
.edit-group textarea{min-height:100px;resize:vertical}
.link-list{list-style:none}
.link-list li{display:flex;align-items:center;gap:12px;padding:12px;background:rgba(10,10,15,.4);border-radius:10px;margin-bottom:8px}
.link-list li span{flex:1;color:#94a3b8}
.link-list a{color:#ef4444;font-size:.85em}
@media(max-width:768px){.hero h1{font-size:2.2em}.stats-bar{gap:30px;flex-wrap:wrap}nav{flex-wrap:wrap;gap:4px}.feature-grid,.screenshot-grid{grid-template-columns:1fr}}
'''
SITE_JS = '''
document.addEventListener('DOMContentLoaded',function(){
  var links=document.querySelectorAll('nav a[href^="#"]');
  function activate(){
    var scrollY=window.scrollY+120;
    links.forEach(function(l){
      var id=l.getAttribute('href').slice(1);
      var el=document.getElementById(id);
      if(el){
        if(el.offsetTop<=scrollY&&el.offsetTop+el.offsetHeight>scrollY){l.classList.add('active')}
        else{l.classList.remove('active')}
      }
    });
  }
  window.addEventListener('scroll',activate);
  activate();
  document.querySelectorAll('.feature-card,.screenshot-card').forEach(function(c,i){
    c.style.opacity='0';c.style.transform='translateY(30px)';
    c.style.transition='opacity .6s ease '+i*.1+'s, transform .6s ease '+i*.1+'s';
    setTimeout(function(){c.style.opacity='1';c.style.transform='translateY(0)'},100);
  });
});
'''

SITE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>unkk client | Minecraft Client</title>
<style>""" + SITE_CSS + """</style>
</head>
<body>

<section class="hero">
<h1>unkk client</h1>
<p class="tagline">A custom Minecraft client built for fun</p>
<div class="version-badge">v62.0.0 | Minecraft 1.21.8 | Fabric</div>
</section>

<div class="stats-bar">
<div class="stat-item"><div class="stat-number">""" + str(DOWNLOAD_COUNT) + """</div><div class="stat-label">Downloads</div></div>
<div class="stat-item"><div class="stat-number">1.21.8</div><div class="stat-label">Minecraft Version</div></div>
<div class="stat-item"><div class="stat-number">Fabric</div><div class="stat-label">Mod Loader</div></div>
<div class="stat-item"><div class="stat-number">""" + str(int(time.time() - APP_START_TIME) // 3600 + 1) + """h</div><div class="stat-label">Uptime</div></div>
</div>

<nav>
<a href="features">Features</a>
<a href="screenshots">Screenshots</a>
<a href="download">Download</a>
<a href="faq">FAQ</a>
<a href="dashboard" style="color:#7c3aed">Dashboard</a>
</nav>

<div class="container">

<section id="features" class="section">
<h2 class="section-title">What is unkk client?</h2>
<p class="section-desc">unkk client is a Fabric-based Minecraft client that includes a collection of mods and client-side features. It runs on Minecraft 1.21.8 and requires Fabric.</p>
<div class="feature-grid">
<div class="feature-card"><div class="feature-icon">&#x1f3ae;</div><h3>Client Mods</h3><p>Bundled client-side mods including performance improvements, utility mods, and more built-in.</p></div>
<div class="feature-card"><div class="feature-icon">&#x2699;&#xfe0f;</div><h3>Customizable</h3><p>Adjust settings and features to your preference through the mod configuration.</p></div>
<div class="feature-card"><div class="feature-icon">&#x1f680;</div><h3>Fabric Based</h3><p>Built on Fabric mod loader for broad mod compatibility and community support.</p></div>
<div class="feature-card"><div class="feature-icon">&#x1f512;</div><h3>Vanilla Compatible</h3><p>Join vanilla and modded servers without issues. No server-side modifications required.</p></div>
<div class="feature-card"><div class="feature-icon">&#x1f4e6;</div><h3>All-in-One</h3><p>Comes bundled with essential client mods so you don't need to install them separately.</p></div>
<div class="feature-card"><div class="feature-icon">&#x1f310;</div><h3>Multiplayer</h3><p>Full multiplayer support. Join any server running compatible Minecraft versions.</p></div>
</div>
</section>

<section id="screenshots" class="section">
<h2 class="section-title">Screenshots</h2>
<p class="section-desc">Check out what unkk client looks like in action.</p>
<div class="screenshot-grid" id="screenshot-grid">
<p style="color:#64748b">Loading screenshots...</p>
</div>
</section>

<section id="download" class="section">
<div class="download-section">
<h2 class="section-title">Download unkk client</h2>
<p class="section-desc">Get started with unkk client for Minecraft 1.21.8</p>
<div class="download-buttons">
<a href="""" + CLIENT_URL + """" class="download-btn">Download Client</a>
<a href="""" + FABRIC_API_URL + """" class="secondary-btn">Download Fabric API</a>
</div>
<p style="margin-top:20px;color:#64748b;font-size:.85em">Requires Minecraft 1.21.8 with Fabric mod loader installed</p>
</div>
</section>

<section id="faq" class="section">
<h2 class="section-title">FAQ</h2>
<div style="max-width:700px">
<div class="feature-card" style="margin-bottom:16px"><h3>What Minecraft version is this for?</h3><p>unkk client is built for Minecraft 1.21.8 using the Fabric mod loader.</p></div>
<div class="feature-card" style="margin-bottom:16px"><h3>Do I need Fabric installed?</h3><p>Yes. Install Fabric for Minecraft 1.21.8, then place both the unkk client jar and Fabric API jar in your mods folder.</p></div>
<div class="feature-card" style="margin-bottom:16px"><h3>Can I use this on multiplayer servers?</h3><p>Yes. unkk client is client-side only, so it works on vanilla and most multiplayer servers.</p></div>
<div class="feature-card" style="margin-bottom:16px"><h3>Is this an official Mojang product?</h3><p>No. unkk client is an independent fan project and is not affiliated with Mojang or Microsoft.</p></div>
</div>
</section>

</div>

<footer class="footer">
<p>unkk client is an independent fan project. Not affiliated with Mojang or Microsoft.</p>
<p style="margin-top:8px">Built with Fabric mod loader for Minecraft 1.21.8</p>
</footer>

<script>""" + SITE_JS + """
</script>
<script>
fetch('/api/screenshots').then(function(r){return r.json()}).then(function(imgs){
  var grid=document.getElementById('screenshot-grid');
  if(!imgs||imgs.length===0){grid.innerHTML='<p style="color:#64748b">No screenshots available yet. Add images to the screenshots folder in the GitHub repo.</p>';return}
  grid.innerHTML='';
  imgs.forEach(function(img){
    var card=document.createElement('div');card.className='screenshot-card';
    card.innerHTML='<img src="'+img.url+'" alt="'+img.name+'" loading="lazy" onerror="this.parentElement.style.display=none"><div class="caption">'+img.name+'</div>';
    grid.appendChild(card);
  });
}).catch(function(){document.getElementById('screenshot-grid').innerHTML='<p style="color:#64748b">Could not load screenshots.</p>'});
</script>
</body>
</html>"""

def build_main_page():
    return SITE_HTML

@app.route("/")
def home():
    return build_main_page()

@app.route("/api/screenshots")
def api_screenshots():
    return fetch_screenshots_from_github()

@app.route("/login", methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        user = request.form.get("username","")
        pw = request.form.get("password","")
        if user == OWNER_USERNAME and pw == OWNER_PASSWORD:
            session["logged_in"] = True
            session["username"] = user
            return redirect(url_for("dashboard"))
        return Response('<div class="auth-container"><h2>Login</h2><div class="auth-error">Invalid credentials</div>'
            '<form method="POST"><label>Username</label><input name="username" required>'
            '<label>Password</label><input type="password" name="password" required>'
            '<button class="btn" type="submit">Sign In</button></form></div>'
            '<style>.auth-container{margin:80px auto;max-width:400px;padding:48px;background:rgba(20,20,30,.8);border:1px solid rgba(255,255,255,.06);border-radius:20px}'
            '.auth-container h2{text-align:center;margin-bottom:24px}'
            '.auth-container label{display:block;margin-bottom:6px;color:#94a3b8}'
            '.auth-container input{width:100%;padding:12px;background:rgba(10,10,15,.6);border:1px solid rgba(255,255,255,.08);border-radius:10px;color:#e0e0e0;margin-bottom:16px}'
            '.auth-container .btn{width:100%;padding:12px;background:linear-gradient(135deg,#7c3aed,#5b21b6);border:none;color:#fff;border-radius:10px;cursor:pointer;font-weight:600}'
            '.auth-error{color:#ef4444;margin-bottom:16px;text-align:center}</style>',
            content_type="text/html")
    return Response('<div class="auth-container"><h2>Login</h2>'
        '<form method="POST"><label>Username</label><input name="username" required>'
        '<label>Password</label><input type="password" name="password" required>'
        '<button class="btn" type="submit">Sign In</button></form></div>'
        '<style>.auth-container{margin:80px auto;max-width:400px;padding:48px;background:rgba(20,20,30,.8);border:1px solid rgba(255,255,255,.06);border-radius:20px}'
        '.auth-container h2{text-align:center;margin-bottom:24px}'
        '.auth-container label{display:block;margin-bottom:6px;color:#94a3b8}'
        '.auth-container input{width:100%;padding:12px;background:rgba(10,10,15,.6);border:1px solid rgba(255,255,255,.08);border-radius:10px;color:#e0e0e0;margin-bottom:16px}'
        '.auth-container .btn{width:100%;padding:12px;background:linear-gradient(135deg,#7c3aed,#5b21b6);border:none;color:#fff;border-radius:10px;cursor:pointer;font-weight:600}</style>',
        content_type="text/html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
@require_login
def dashboard():
    uptime_h = int(time.time() - APP_START_TIME) // 3600
    return Response("""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard | unkk client</title>
<style>""" + SITE_CSS + """
.nav-link{display:inline-block;padding:8px 20px;margin:4px;background:rgba(124,58,237,.15);border:1px solid rgba(124,58,237,.3);border-radius:10px;color:#a78bfa;text-decoration:none;transition:all .2s}
.nav-link:hover{background:rgba(124,58,237,.25);color:#a78bfa}
.dash-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:40px}
</style></head><body>
<nav style="display:flex;justify-content:center;gap:8px;padding:16px;background:rgba(10,10,15,.9);border-bottom:1px solid rgba(255,255,255,.05)">
<a href="/" style="padding:10px 24px;border-radius:12px;color:#94a3b8">Home</a>
<a href="/dashboard" style="padding:10px 24px;border-radius:12px;color:#a78bfa;background:rgba(124,58,237,.15)">Dashboard</a>
<a href="/edit-links" style="padding:10px 24px;border-radius:12px;color:#94a3b8">Edit Links</a>
<a href="/logout" style="padding:10px 24px;border-radius:12px;color:#ef4444">Logout</a>
</nav>
<div class="container">
<div class="dash-header"><h1 class="section-title">Welcome, """ + session.get("username","owner") + """</h1></div>
<div class="dash-grid">
<div class="dash-card"><h3>Downloads</h3><div class="num">""" + str(DOWNLOAD_COUNT) + """</div></div>
<div class="dash-card"><h3>Uptime</h3><div class="num">""" + str(uptime_h) + """h</div></div>
<div class="dash-card"><h3>Status</h3><div class="num" style="color:#22c55e">Online</div></div>
</div>
<h2 class="section-title" style="margin-top:48px;margin-bottom:24px">Quick Actions</h2>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<a href="/edit-links" class="nav-link">Edit Download Links</a>
<a href="/" class="nav-link">View Site</a>
</div>
<h2 class="section-title" style="margin-top:48px;margin-bottom:24px">Server Info</h2>
<div class="feature-card" style="max-width:500px">
<p style="color:#94a3b8;margin-bottom:8px"><strong style="color:#e0e0e0">Python:</strong> """ + os.environ.get("PYTHON_VERSION","3.14.3") + """</p>
<p style="color:#94a3b8;margin-bottom:8px"><strong style="color:#e0e0e0">Platform:</strong> """ + os.environ.get("DYNO","local") + """</p>
<p style="color:#94a3b8"><strong style="color:#e0e0e0">Owner:</strong> """ + OWNER_USERNAME + """</p>
</div>
</div>
</body></html>""", content_type="text/html")

@app.route("/edit-links", methods=["GET","POST"])
@require_login
def edit_links():
    if request.method == "POST":
        global CLIENT_URL, FABRIC_API_URL
        new_client = request.form.get("client_url","").strip()
        new_fabric = request.form.get("fabric_url","").strip()
        if new_client:
            CLIENT_URL = new_client
        if new_fabric:
            FABRIC_API_URL = new_fabric
        return redirect(url_for("edit_links"))
    return Response("""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Edit Links | unkk client</title>
<style>""" + SITE_CSS + """
</style></head><body>
<nav style="display:flex;justify-content:center;gap:8px;padding:16px;background:rgba(10,10,15,.9);border-bottom:1px solid rgba(255,255,255,.05)">
<a href="/" style="padding:10px 24px;border-radius:12px;color:#94a3b8">Home</a>
<a href="/dashboard" style="padding:10px 24px;border-radius:12px;color:#94a3b8">Dashboard</a>
<a href="/edit-links" style="padding:10px 24px;border-radius:12px;color:#a78bfa;background:rgba(124,58,237,.15)">Edit Links</a>
<a href="/logout" style="padding:10px 24px;border-radius:12px;color:#ef4444">Logout</a>
</nav>
<div class="container">
<h1 class="section-title" style="margin-bottom:32px">Edit Download Links</h1>
<div class="edit-section">
<div class="edit-group">
<label>Client JAR URL</label>
<input type="url" name="client_url" value=""" + CLIENT_URL + """ form="linkform">
</div>
<div class="edit-group">
<label>Fabric API JAR URL</label>
<input type="url" name="fabric_url" value=""" + FABRIC_API_URL + """ form="linkform">
</div>
<form id="linkform" method="POST" style="margin-top:24px">
<button type="submit" class="download-btn" style="font-size:1em;padding:14px 36px">Save Changes</button>
</form>
<h2 class="section-title" style="margin-top:48px;margin-bottom:24px">Current Links</h2>
<ul class="link-list">
<li><span style="color:#94a3b8"><strong>Client:</strong> """ + CLIENT_URL + """</span></li>
<li><span style="color:#94a3b8"><strong>Fabric API:</strong> """ + FABRIC_API_URL + """</span></li>
</ul>
</div>
</div>
</body></html>""", content_type="text/html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

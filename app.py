import os
import json
import time
import threading
import uuid
import urllib.request
from functools import wraps
from flask import Flask, request, redirect, Response, session, url_for, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32).hex())

OWNER_USERNAME = os.environ.get("OWNER_USER", "owner")
OWNER_PASSWORD = os.environ.get("OWNER_PASS", "changeme")

CLIENT_URL = os.environ.get("CLIENT_URL", "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/unkk-62.0.0.20260820.085414.jar")
FABRIC_API_URL = os.environ.get("FABRIC_URL", "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/fabric-api-0.156.0+26.2.jar")
GITHUB_REPO = "awdawdfawdAWD/Minecraft-web"
GITHUB_SCREENSHOTS_FOLDER = "screenshots"
GITHUB_RAW_BASE = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{GITHUB_SCREENSHOTS_FOLDER}"

DOWNLOAD_COUNT = 147
APP_START_TIME = time.time()

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def fetch_screenshots_from_github():
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{GITHUB_SCREENSHOTS_FOLDER}"
        req = urllib.request.Request(url, headers={"User-Agent": "unkk-client-site"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        images = []
        for item in data:
            name = item.get("name", "")
            if any(name.lower().endswith(ext) for ext in IMAGE_EXTS):
                images.append({"name": name, "url": f"{GITHUB_RAW_BASE}/{name}"})
        return images
    except Exception as e:
        print(f"GitHub screenshot fetch error: {e}")
        return []


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated


SITE_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>unkk client</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#0c0c10;--paper:#f0ede8;--muted:#8a877e;--accent:#a855f7;--accent2:#6366f1;--green:#22c55e;--card:#16161c;--card-border:#2a2a35;--font:'Space Grotesk',system-ui,sans-serif;--mono:'JetBrains Mono',monospace}
html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--ink);color:var(--paper);overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;z-index:9999;opacity:0.5}
.topnav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:18px 40px;background:rgba(12,12,16,0.8);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.04);transition:transform 0.3s}
.topnav.hide{transform:translateY(-100%)}
.nav-logo{font-weight:700;font-size:1.1rem;letter-spacing:-0.5px}
.nav-logo span{color:var(--accent)}
.nav-links{display:flex;gap:8px;align-items:center}
.nav-links a,.nav-links button{font-family:var(--font);font-size:0.82rem;font-weight:500;color:var(--muted);text-decoration:none;padding:8px 16px;border-radius:8px;border:none;background:none;cursor:pointer;transition:all 0.2s}
.nav-links a:hover,.nav-links button:hover{color:var(--paper);background:rgba(255,255,255,0.05)}
.nav-dl-btn{background:var(--accent)!important;color:#fff!important;font-weight:600!important}
.nav-dl-btn:hover{background:#9333ea!important}
section{padding:120px 40px 80px;max-width:1100px;margin:0 auto}
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;position:relative;padding-top:80px}
.hero-tag{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:24px;opacity:0;animation:fadeUp 0.8s 0.2s forwards}
.hero-tag::before{content:'';width:24px;height:1px;background:var(--accent)}
.hero h1{font-size:clamp(3.5rem,9vw,7rem);font-weight:700;letter-spacing:-3px;line-height:0.95;margin-bottom:28px;opacity:0;animation:fadeUp 0.8s 0.4s forwards}
.hero h1 em{font-style:normal;color:var(--accent);position:relative}
.hero-desc{font-size:1.05rem;color:var(--muted);line-height:1.7;max-width:460px;margin-bottom:40px;opacity:0;animation:fadeUp 0.8s 0.6s forwards}
.hero-actions{display:flex;gap:14px;flex-wrap:wrap;opacity:0;animation:fadeUp 0.8s 0.8s forwards}
.btn-main{display:inline-flex;align-items:center;gap:10px;padding:14px 28px;border-radius:10px;font-family:var(--font);font-size:0.9rem;font-weight:600;text-decoration:none;border:none;cursor:pointer;transition:all 0.25s;background:var(--accent);color:#fff}
.btn-main:hover{background:#9333ea;transform:translateY(-2px);box-shadow:0 8px 30px rgba(168,85,247,0.3)}
.btn-main svg{width:18px;height:18px}
.btn-outline{background:none;border:1px solid var(--card-border);color:var(--paper)}
.btn-outline:hover{border-color:var(--muted);background:rgba(255,255,255,0.03)}
.hero-stats{display:flex;gap:40px;margin-top:60px;opacity:0;animation:fadeUp 0.8s 1s forwards}
.stat-block .num{font-size:1.8rem;font-weight:700;font-family:var(--mono);color:var(--paper)}
.stat-block .label{font-size:0.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-top:4px}
.marquee-wrap{overflow:hidden;padding:30px 0;border-top:1px solid rgba(255,255,255,0.04);border-bottom:1px solid rgba(255,255,255,0.04)}
.marquee{display:flex;gap:60px;animation:scroll 20s linear infinite;white-space:nowrap;width:max-content}
.marquee span{font-size:0.8rem;font-weight:600;text-transform:uppercase;letter-spacing:3px;color:rgba(255,255,255,0.08)}
@keyframes scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.tab-bar{display:flex;gap:4px;margin-bottom:40px;background:var(--card);border-radius:12px;padding:5px;width:fit-content}
.tab-btn{font-family:var(--font);font-size:0.82rem;font-weight:500;padding:10px 22px;border:none;border-radius:8px;background:none;color:var(--muted);cursor:pointer;transition:all 0.25s}
.tab-btn.active{background:var(--accent);color:#fff}
.tab-btn:hover:not(.active){color:var(--paper);background:rgba(255,255,255,0.04)}
.tab-content{display:none;animation:fadeUp 0.5s forwards}
.tab-content.active{display:block}
.showcase-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.showcase-item{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:16/10;background:var(--card);border:1px solid var(--card-border);cursor:pointer;transition:all 0.4s cubic-bezier(0.16,1,0.3,1)}
.showcase-item:hover{transform:scale(1.02);border-color:var(--accent);box-shadow:0 20px 60px rgba(0,0,0,0.5)}
.showcase-item img{width:100%;height:100%;object-fit:cover;display:block;transition:transform 0.5s}
.showcase-item:hover img{transform:scale(1.05)}
.showcase-item .overlay{position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,0.7) 0%,transparent 50%);display:flex;align-items:flex-end;padding:20px;opacity:0;transition:opacity 0.3s}
.showcase-item:hover .overlay{opacity:1}
.showcase-item .overlay span{font-size:0.85rem;font-weight:600}
.showcase-empty{grid-column:1/-1;text-align:center;padding:60px 20px;color:var(--muted);font-size:0.9rem}
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.feature-card{background:var(--card);border:1px solid var(--card-border);border-radius:14px;padding:28px;transition:all 0.3s;position:relative;overflow:hidden}
.feature-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);opacity:0;transition:opacity 0.3s}
.feature-card:hover::before{opacity:1}
.feature-card:hover{border-color:rgba(168,85,247,0.2);transform:translateY(-3px)}
.feature-card .f-icon{font-size:1.5rem;margin-bottom:16px}
.feature-card h4{font-size:0.95rem;font-weight:600;margin-bottom:8px}
.feature-card p{font-size:0.82rem;color:var(--muted);line-height:1.6}
.cl-item{display:flex;gap:24px;padding:24px 0;border-bottom:1px solid rgba(255,255,255,0.04)}
.cl-item:last-child{border-bottom:none}
.cl-version{font-family:var(--mono);font-size:0.8rem;color:var(--accent);min-width:80px;padding-top:2px}
.cl-body h4{font-size:0.95rem;font-weight:600;margin-bottom:6px}
.cl-body p{font-size:0.82rem;color:var(--muted);line-height:1.6}
.cl-body .cl-date{font-size:0.7rem;color:rgba(255,255,255,0.2);margin-top:8px;font-family:var(--mono)}
.cl-tag{display:inline-block;padding:3px 10px;border-radius:6px;font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;margin-right:6px}
.cl-tag.new{background:rgba(34,197,94,0.1);color:var(--green);border:1px solid rgba(34,197,94,0.2)}
.cl-tag.fix{background:rgba(250,204,21,0.1);color:#facc15;border:1px solid rgba(250,204,21,0.2)}
.install-flow{display:flex;gap:16px;flex-wrap:wrap}
.install-step{flex:1;min-width:180px;background:var(--card);border:1px solid var(--card-border);border-radius:14px;padding:24px}
.install-step .step-n{font-family:var(--mono);font-size:0.7rem;color:var(--accent);letter-spacing:1px;margin-bottom:12px}
.install-step h4{font-size:0.9rem;font-weight:600;margin-bottom:6px}
.install-step p{font-size:0.78rem;color:var(--muted);line-height:1.5}
.install-step code{font-family:var(--mono);font-size:0.75rem;background:rgba(168,85,247,0.1);color:var(--accent);padding:3px 8px;border-radius:5px}
.site-footer{padding:60px 40px;border-top:1px solid rgba(255,255,255,0.04);display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px}
.footer-left{font-size:0.78rem;color:var(--muted)}
.footer-links{display:flex;gap:20px}
.footer-links a{font-size:0.78rem;color:var(--muted);text-decoration:none;transition:color 0.2s}
.footer-links a:hover{color:var(--paper)}
.reveal{opacity:0;transform:translateY(30px);transition:all 0.7s cubic-bezier(0.16,1,0.3,1)}
.reveal.visible{opacity:1;transform:translateY(0)}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:10000;display:none;align-items:center;justify-content:center;backdrop-filter:blur(10px);cursor:pointer}
.lightbox.open{display:flex}
.lightbox img{max-width:90%;max-height:85vh;border-radius:12px;box-shadow:0 20px 80px rgba(0,0,0,0.5)}
.lightbox-close{position:absolute;top:24px;right:24px;width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.1);border:none;color:#fff;font-size:1.2rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background 0.2s}
.lightbox-close:hover{background:rgba(255,255,255,0.2)}
.lightbox-nav{position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;border-radius:50%;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.1);color:#fff;font-size:1.4rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s}
.lightbox-nav:hover{background:rgba(255,255,255,0.15)}
.lightbox-prev{left:24px}
.lightbox-next{right:24px}
.lightbox-counter{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);font-family:var(--mono);font-size:0.75rem;color:rgba(255,255,255,0.5)}
.trail{position:fixed;width:8px;height:8px;border-radius:50%;background:var(--accent);pointer-events:none;z-index:9998;opacity:0;mix-blend-mode:screen}
@media(max-width:768px){section{padding:100px 20px 60px}.topnav{padding:14px 20px}.nav-links a:not(.nav-dl-btn){display:none}.feature-grid{grid-template-columns:1fr}.install-flow{flex-direction:column}.hero-stats{gap:24px}.tab-bar{overflow-x:auto;width:100%}.site-footer{flex-direction:column;text-align:center}}
</style>
</head>
<body>
<div class="topnav" id="topnav">
  <div class="nav-logo">unk<span>k</span></div>
  <div class="nav-links">
    <a href="#showcase">Showcase</a>
    <a href="#features">Features</a>
    <a href="#changelog">Changelog</a>
    <a href="#install">Install</a>
    <a class="nav-dl-btn" href="%%CLIENT_URL%%">Download</a>
  </div>
</div>
<section class="hero">
  <div class="hero-tag">v62.0.0 stable release</div>
  <h1>unkk<br><em>client</em></h1>
  <p class="hero-desc">A fabric-based minecraft client made for people who actually care about how the game looks and feels. built different.</p>
  <div class="hero-actions">
    <a href="%%CLIENT_URL%%" class="btn-main">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      Download Client
    </a>
    <a href="%%FABRIC_URL%%" class="btn-main btn-outline">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
      Fabric API
    </a>
  </div>
  <div class="hero-stats">
    <div class="stat-block"><div class="num" id="dl-count">%%DOWNLOAD_COUNT%%</div><div class="label">Downloads</div></div>
    <div class="stat-block"><div class="num">62.0.0</div><div class="label">Latest Version</div></div>
    <div class="stat-block"><div class="num">1.21+</div><div class="label">Fabric</div></div>
  </div>
</section>
<div class="marquee-wrap"><div class="marquee"><span>unkk client</span><span>fabric</span><span>customizable</span><span>open source</span><span>smooth</span><span>modern</span><span>clean</span><span>unkk client</span><span>fabric</span><span>customizable</span><span>open source</span><span>smooth</span><span>modern</span><span>clean</span></div></div>
<section id="showcase">
  <div class="reveal">
    <div style="font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:12px">// screenshots</div>
    <h2 style="font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px">See it in action</h2>
  </div>
  <div class="showcase-grid reveal" id="showcase-grid"></div>
</section>
<section id="features">
  <div class="reveal">
    <div style="font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:12px">// what you get</div>
    <h2 style="font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px">Features</h2>
  </div>
  <div class="tab-bar reveal">
    <button class="tab-btn active" onclick="switchTab(this,'tab-general')">General</button>
    <button class="tab-btn" onclick="switchTab(this,'tab-perf')">Under the Hood</button>
    <button class="tab-btn" onclick="switchTab(this,'tab-visual')">Visuals</button>
  </div>
  <div class="tab-content active" id="tab-general">
    <div class="feature-grid">
      <div class="feature-card reveal"><div class="f-icon">&#128295;</div><h4>Mod Support</h4><p>Full fabric mod API support. Works with your favorite mods out of the box.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127912;</div><h4>Custom HUD</h4><p>Redesigned HUD elements. Clean, minimal, and actually readable.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#9881;</div><h4>Deep Settings</h4><p>Every setting where you expect it. No digging through menus.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128274;</div><h4>Legit Client</h4><p>No shady modules. Just a better Minecraft experience.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128640;</div><h4>Quick Launch</h4><p>Less waiting around. Get into your world faster.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127760;</div><h4>Multiplayer</h4><p>Works on any server. Hypixel, private, or your own.</p></div>
    </div>
  </div>
  <div class="tab-content" id="tab-perf">
    <div class="feature-grid">
      <div class="feature-card reveal"><div class="f-icon">&#128187;</div><h4>Memory Management</h4><p>Better garbage collection handling to reduce stuttering spikes.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127777;</div><h4>Entity Culling</h4><p>Skips rendering entities outside your view. Built-in, not a mod.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#9881;</div><h4>Thread Optimization</h4><p>Spreads workload across available CPU threads more evenly.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128230;</div><h4>Small Footprint</h4><p>Tiny jar size. No bundled junk you didn't ask for.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128200;</div><h4>Rendering Pipeline</h4><p>Modified rendering path. Still being worked on, but already better.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128296;</div><h4>Ongoing Work</h4><p>Performance is a priority. More optimizations coming every update.</p></div>
    </div>
  </div>
  <div class="tab-content" id="tab-visual">
    <div class="feature-grid">
      <div class="feature-card reveal"><div class="f-icon">&#127912;</div><h4>Custom Shaders</h4><p>Built-in shader support for that cinematic look.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127744;</div><h4>Color Themes</h4><p>Multiple UI color themes. Pick your vibe.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128065;</div><h4>Block Overlay</h4><p>Customizable block selection overlay. Thinner, cleaner, better.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127752;</div><h4>Hotbar Design</h4><p>Redesigned hotbar with cleaner textures.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128247;</div><h4>Screenshot Manager</h4><p>Built-in screenshot viewer with organization tools.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127916;</div><h4>Animations</h4><p>Smoother hand swing and item switch animations.</p></div>
    </div>
  </div>
</section>
<section id="changelog">
  <div class="reveal">
    <div style="font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:12px">// updates</div>
    <h2 style="font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px">Changelog</h2>
  </div>
  <div class="reveal">
    <div class="cl-item"><div class="cl-version">v62.0.0</div><div class="cl-body"><h4><span class="cl-tag new">new</span> Major Client Release</h4><p>Full rewrite of the rendering pipeline. New HUD system, entity culling, and custom shader support added.</p><div class="cl-date">aug 20 2026</div></div></div>
    <div class="cl-item"><div class="cl-version">v61.3.2</div><div class="cl-body"><h4><span class="cl-tag fix">fix</span> Fabric Compatibility</h4><p>Fixed crash on startup with fabric-api 0.156.0. Resolved mod loader conflict with Sodium.</p><div class="cl-date">aug 12 2026</div></div></div>
  </div>
</section>
<section id="install">
  <div class="reveal">
    <div style="font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:12px">// setup</div>
    <h2 style="font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px">How to install</h2>
  </div>
  <div class="install-flow reveal">
    <div class="install-step"><div class="step-n">01</div><h4>Install Fabric</h4><p>Get <a href="https://fabricmc.net/" style="color:var(--accent);text-decoration:none">Fabric Loader</a> for your Minecraft version.</p></div>
    <div class="install-step"><div class="step-n">02</div><h4>Download</h4><p>Grab the client JAR and Fabric API from the buttons above.</p></div>
    <div class="install-step"><div class="step-n">03</div><h4>Drop In</h4><p>Place both files in <code>.minecraft/mods</code></p></div>
    <div class="install-step"><div class="step-n">04</div><h4>Launch</h4><p>Open Minecraft with the Fabric profile. You're in.</p></div>
  </div>
</section>
<div class="marquee-wrap" style="margin-top:40px"><div class="marquee" style="animation-direction:reverse;animation-duration:25s"><span>download now</span><span>free</span><span>open source</span><span>no ads</span><span>just a good client</span><span>download now</span><span>free</span><span>open source</span><span>no ads</span><span>just a good client</span></div></div>
<footer class="site-footer">
  <div class="footer-left">unkk client &mdash; not affiliated with mojang or microsoft</div>
  <div class="footer-links">
    <a href="%%CLIENT_URL%%">Download</a>
    <a href="https://github.com/awdawdfawdAWD/MC-CLIENT" target="_blank">GitHub</a>
  </div>
</footer>
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <button class="lightbox-close">&times;</button>
  <button class="lightbox-nav lightbox-prev" onclick="navLightbox(-1)">&#8249;</button>
  <img id="lightbox-img" src="" alt="screenshot">
  <button class="lightbox-nav lightbox-next" onclick="navLightbox(1)">&#8250;</button>
  <div class="lightbox-counter" id="lightbox-counter"></div>
</div>
<script>
var currentImages = %%IMAGES_JSON%%;
var currentLightboxIndex = 0;

function buildShowcase() {
  var grid = document.getElementById('showcase-grid');
  if (!currentImages || currentImages.length === 0) {
    grid.innerHTML = '<div class="showcase-empty">No screenshots yet. Upload images to the <code style="color:var(--accent)">screenshots/</code> folder in the GitHub repo.</div>';
    return;
  }
  var html = '';
  currentImages.forEach(function(img, i) {
    html += '<div class="showcase-item" onclick="openLightboxAt(' + i + ')"><img src="' + img.url + '" alt="' + img.name + '" loading="lazy"><div class="overlay"><span>' + img.name + '</span></div></div>';
  });
  grid.innerHTML = html;
  grid.querySelectorAll('.reveal').forEach(function(el) { observer.observe(el); });
}
buildShowcase();

function switchTab(btn, tabId) {
  btn.parentElement.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  document.querySelectorAll('.tab-content').forEach(function(t) { t.classList.remove('active'); });
  var tab = document.getElementById(tabId);
  tab.classList.add('active');
  tab.querySelectorAll('.reveal').forEach(function(el, i) {
    el.classList.remove('visible');
    setTimeout(function() { el.classList.add('visible'); }, 80 * i);
  });
}

var reveals = document.querySelectorAll('.reveal');
var observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });
reveals.forEach(function(el) { observer.observe(el); });

var lastScroll = 0;
var nav = document.getElementById('topnav');
window.addEventListener('scroll', function() {
  var cur = window.scrollY;
  if (cur > lastScroll && cur > 200) nav.classList.add('hide');
  else nav.classList.remove('hide');
  lastScroll = cur;
});

function openLightboxAt(index) {
  event.stopPropagation();
  currentLightboxIndex = index;
  updateLightbox();
  document.getElementById('lightbox').classList.add('open');
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
}
function navLightbox(dir) {
  event.stopPropagation();
  currentLightboxIndex += dir;
  if (currentLightboxIndex < 0) currentLightboxIndex = currentImages.length - 1;
  if (currentLightboxIndex >= currentImages.length) currentLightboxIndex = 0;
  updateLightbox();
}
function updateLightbox() {
  document.getElementById('lightbox-img').src = currentImages[currentLightboxIndex].url;
  document.getElementById('lightbox-counter').textContent = (currentLightboxIndex + 1) + ' / ' + currentImages.length;
}

var trails = [];
for (var i = 0; i < 5; i++) {
  var t = document.createElement('div');
  t.className = 'trail';
  t.style.width = (8 - i) + 'px';
  t.style.height = (8 - i) + 'px';
  document.body.appendChild(t);
  trails.push({el: t, x: 0, y: 0});
}
var mouse = {x: 0, y: 0};
document.addEventListener('mousemove', function(e) { mouse.x = e.clientX; mouse.y = e.clientY; });
function animTrail() {
  trails.forEach(function(t, i) {
    var prev = i === 0 ? mouse : trails[i-1];
    t.x += (prev.x - t.x) * 0.35;
    t.y += (prev.y - t.y) * 0.35;
    t.el.style.left = t.x - 4 + 'px';
    t.el.style.top = t.y - 4 + 'px';
    t.el.style.opacity = (1 - i * 0.2);
  });
  requestAnimationFrame(animTrail);
}
animTrail();

var dlEl = document.getElementById('dl-count');
var dlTarget = %%DOWNLOAD_COUNT%%;
function animateCount(el, target) {
  var current = 0;
  var step = Math.max(1, Math.ceil(target / 60));
  var timer = setInterval(function() {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.innerText = current;
  }, 16);
}
var dlObs = new IntersectionObserver(function(entries) {
  if (entries[0].isIntersecting) { animateCount(dlEl, dlTarget); dlObs.disconnect(); }
}, { threshold: 0.5 });
dlObs.observe(dlEl);
</script>
</body>
</html>"""


LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>unkk - login</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Space Grotesk',sans-serif;background:#0c0c10;color:#f0ede8;min-height:100vh;display:flex;align-items:center;justify-content:center}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(168,85,247,0.08) 0%,transparent 60%),radial-gradient(ellipse at 70% 80%,rgba(99,102,241,0.06) 0%,transparent 60%);z-index:0}
.card{position:relative;z-index:1;background:rgba(22,22,28,0.8);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:40px;width:360px;backdrop-filter:blur(20px);box-shadow:0 20px 60px rgba(0,0,0,0.5)}
h2{font-size:1.3rem;font-weight:700;margin-bottom:6px;text-align:center}
.sub{font-size:0.8rem;color:#8a877e;text-align:center;margin-bottom:30px}
.error{background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);color:#ef4444;padding:10px;border-radius:8px;font-size:0.8rem;margin-bottom:20px;text-align:center}
label{display:block;font-size:0.72rem;color:#8a877e;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:8px}
input{width:100%;padding:12px 14px;background:rgba(12,12,16,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:8px;color:#f0ede8;font-family:'Space Grotesk',sans-serif;font-size:0.9rem;outline:none;transition:border-color 0.2s;margin-bottom:20px}
input:focus{border-color:#a855f7}
button{width:100%;padding:12px;background:#a855f7;color:#fff;border:none;border-radius:8px;font-family:'Space Grotesk',sans-serif;font-size:0.9rem;font-weight:600;cursor:pointer;transition:all 0.2s}
button:hover{background:#9333ea;transform:translateY(-1px);box-shadow:0 6px 20px rgba(168,85,247,0.3)}
.back{display:block;text-align:center;margin-top:16px;font-size:0.8rem;color:#8a877e;text-decoration:none;transition:color 0.2s}
.back:hover{color:#f0ede8}
</style>
</head>
<body>
<div class="bg"></div>
<div class="card">
  <h2>owner access</h2>
  <div class="sub">authenticate to continue</div>
  ERROR_PLACEHOLDER
  <form method="POST">
    <label>username</label>
    <input type="text" name="username" placeholder="username" required autofocus>
    <label>password</label>
    <input type="password" name="password" placeholder="password" required>
    <button type="submit">sign in</button>
  </form>
  <a href="/" class="back">&larr; back to site</a>
</div>
</body>
</html>"""


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>unkk - dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Space Grotesk',sans-serif;background:#0c0c10;color:#f0ede8;min-height:100vh}
.dash-nav{display:flex;align-items:center;justify-content:space-between;padding:16px 40px;background:rgba(12,12,16,0.9);border-bottom:1px solid rgba(255,255,255,0.04);backdrop-filter:blur(20px)}
.dash-nav .logo{font-weight:700;font-size:1rem}.dash-nav .logo span{color:#a855f7}
.dash-nav .right{display:flex;gap:12px;align-items:center}
.dash-nav a,.dash-nav button{font-size:0.8rem;color:#8a877e;text-decoration:none;padding:8px 16px;border-radius:8px;border:none;background:none;cursor:pointer;font-family:inherit;transition:all 0.2s}
.dash-nav a:hover,.dash-nav button:hover{color:#f0ede8;background:rgba(255,255,255,0.05)}
.dash-nav .logout{color:#ef4444;border:1px solid rgba(239,68,68,0.2)}
.dash-nav .logout:hover{background:rgba(239,68,68,0.1)}
.container{max-width:1000px;margin:0 auto;padding:40px}
.section-title{font-size:0.72rem;color:#a855f7;text-transform:uppercase;letter-spacing:2px;font-family:'JetBrains Mono',monospace;margin-bottom:8px}
h1{font-size:1.8rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px}
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:40px}
.stat-card{background:rgba(22,22,28,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:24px}
.stat-card .val{font-size:2rem;font-weight:700;font-family:'JetBrains Mono',monospace;margin-bottom:4px}
.stat-card .lbl{font-size:0.72rem;color:#8a877e;text-transform:uppercase;letter-spacing:1px}
.panel{background:rgba(22,22,28,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:30px;margin-bottom:20px}
.panel h3{font-size:0.95rem;font-weight:600;margin-bottom:20px}
.info-row{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.85rem;gap:20px;word-break:break-all}
.info-row:last-child{border-bottom:none}
.info-row .k{color:#8a877e;min-width:100px;flex-shrink:0}
.info-row .v{color:#f0ede8;font-family:'JetBrains Mono',monospace;font-size:0.75rem}
.code-block{background:#0a0a0e;border:1px solid rgba(255,255,255,0.04);border-radius:8px;padding:16px;font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#a855f7;overflow-x:auto;white-space:pre;margin-top:12px}
</style>
</head>
<body>
<div class="dash-nav">
  <div class="logo">unk<span>k</span> dashboard</div>
  <div class="right">
    <a href="/">view site</a>
    <a href="/dashboard/edit" style="color:#a855f7">edit links</a>
    <button class="logout" onclick="location.href='/logout'">sign out</button>
  </div>
</div>
<div class="container">
  <div class="section-title">// overview</div>
  <h1>Dashboard</h1>
  <div class="stat-row">
    <div class="stat-card"><div class="val">%%DOWNLOAD_COUNT%%</div><div class="lbl">Total Downloads</div></div>
    <div class="stat-card"><div class="val">v62.0.0</div><div class="lbl">Current Version</div></div>
    <div class="stat-card"><div class="val" id="uptime-val">--</div><div class="lbl">Uptime</div></div>
  </div>
  <div class="panel">
    <h3>Download Links</h3>
    <div class="info-row"><span class="k">Client JAR</span><span class="v">%%CLIENT_URL%%</span></div>
    <div class="info-row"><span class="k">Fabric API</span><span class="v">%%FABRIC_URL%%</span></div>
  </div>
  <div class="panel">
    <h3>Env Variables for Render</h3>
    <div class="info-row"><span class="k">FLASK_SECRET_KEY</span><span class="v">any random string (use os.urandom(32).hex())</span></div>
    <div class="info-row"><span class="k">OWNER_USER</span><span class="v">your login username</span></div>
    <div class="info-row"><span class="k">OWNER_PASS</span><span class="v">your login password</span></div>
  </div>
  <div class="panel">
    <h3>Screenshots</h3>
    <p style="font-size:0.85rem;color:#8a877e;margin-bottom:16px">Upload images to the <code style="color:#a855f7;background:rgba(168,85,247,0.1);padding:2px 8px;border-radius:4px">screenshots/</code> folder in your GitHub repo. The site auto-loads all image files from there.</p>
    <div class="code-block">Minecraft-web/
  screenshots/
    screenshot1.png
    screenshot2.jpg
    gameplay.gif
    ...</div>
    screenshot1.png
    screenshot2.jpg
    gameplay.gif
    ...</div>
  </div>
</div>
<script>
var start = %%SERVER_START%%;
function fmt(s){var d=Math.floor(s/86400),h=Math.floor((s%86400)/3600),m=Math.floor((s%3600)/60),sec=s%60,p=[];if(d)p.push(d+"d");if(h)p.push(h+"h");if(m)p.push(m+"m");p.push(sec+"s");return p.join(" ")}
setInterval(function(){document.getElementById("uptime-val").innerText=fmt(Math.floor(Date.now()/1000-start))},1000);
</script>
</body>
</html>"""


EDIT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>unkk - edit links</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Space Grotesk',sans-serif;background:#0c0c10;color:#f0ede8;min-height:100vh}
.dash-nav{display:flex;align-items:center;justify-content:space-between;padding:16px 40px;background:rgba(12,12,16,0.9);border-bottom:1px solid rgba(255,255,255,0.04)}
.dash-nav .logo{font-weight:700;font-size:1rem}.dash-nav .logo span{color:#a855f7}
.dash-nav a{font-size:0.8rem;color:#8a877e;text-decoration:none;padding:8px 16px;border-radius:8px;transition:all 0.2s}
.dash-nav a:hover{color:#f0ede8;background:rgba(255,255,255,0.05)}
.container{max-width:700px;margin:0 auto;padding:40px}
.section-title{font-size:0.72rem;color:#a855f7;text-transform:uppercase;letter-spacing:2px;font-family:'JetBrains Mono',monospace;margin-bottom:8px}
h1{font-size:1.8rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px}
.form-group{margin-bottom:24px}
.form-group label{display:block;font-size:0.72rem;color:#8a877e;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:8px}
.form-group input{width:100%;padding:12px 14px;background:rgba(22,22,28,0.8);border:1px solid rgba(255,255,255,0.06);border-radius:8px;color:#f0ede8;font-family:'JetBrains Mono',monospace;font-size:0.82rem;outline:none;transition:border-color 0.2s}
.form-group input:focus{border-color:#a855f7}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:8px;font-family:inherit;font-size:0.85rem;font-weight:600;border:none;cursor:pointer;transition:all 0.2s;text-decoration:none}
.btn-primary{background:#a855f7;color:#fff}
.btn-primary:hover{background:#9333ea}
.btn-secondary{background:rgba(255,255,255,0.05);color:#8a877e;border:1px solid rgba(255,255,255,0.06)}
.btn-secondary:hover{color:#f0ede8;background:rgba(255,255,255,0.08)}
.success{background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.2);color:#22c55e;padding:12px;border-radius:8px;font-size:0.85rem;margin-bottom:20px}
</style>
</head>
<body>
<div class="dash-nav">
  <div class="logo">unk<span>k</span> dashboard</div>
  <div style="display:flex;gap:12px"><a href="/dashboard">back</a></div>
</div>
<div class="container">
  <div class="section-title">// settings</div>
  <h1>Edit Download Links</h1>
  %%SAVED_MSG%%
  <form method="POST">
    <div class="form-group">
      <label>Client JAR URL</label>
      <input type="text" name="client_url" value="%%CLIENT_URL%%" placeholder="https://github.com/...jar">
    </div>
    <div class="form-group">
      <label>Fabric API URL</label>
      <input type="text" name="fabric_url" value="%%FABRIC_URL%%" placeholder="https://github.com/...jar">
    </div>
    <div style="display:flex;gap:12px">
      <button type="submit" class="btn btn-primary">Save Changes</button>
      <a href="/dashboard" class="btn btn-secondary">Cancel</a>
    </div>
  </form>
</div>
</body>
</html>"""


@app.route("/")
def home_redirect():
    screenshots = fetch_screenshots_from_github()
    page = SITE_HTML_TEMPLATE
    page = page.replace("%%CLIENT_URL%%", CLIENT_URL)
    page = page.replace("%%FABRIC_URL%%", FABRIC_API_URL)
    page = page.replace("%%DOWNLOAD_COUNT%%", str(DOWNLOAD_COUNT))
    page = page.replace("%%IMAGES_JSON%%", json.dumps(screenshots))
    return Response(page, content_type="text/html")


@app.route("/api/download/client")
def download_client():
    global DOWNLOAD_COUNT
    DOWNLOAD_COUNT += 1
    return redirect(CLIENT_URL)


@app.route("/api/download/fabric")
def download_fabric():
    return redirect(FABRIC_API_URL)


@app.route("/api/health", methods=["GET"])
def health():
    uptime_seconds = int(time.time() - APP_START_TIME)
    return {
        "status": "online",
        "uptime": uptime_seconds,
        "downloads": DOWNLOAD_COUNT,
        "client": CLIENT_URL,
        "fabric_api": FABRIC_API_URL
    }


@app.route("/api/screenshots")
def api_screenshots():
    return jsonify(fetch_screenshots_from_github())


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if session.get("logged_in"):
        return redirect(url_for("admin_dashboard"))
    error_html = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == OWNER_USERNAME and password == OWNER_PASSWORD:
            session["logged_in"] = True
            session["user"] = username
            return redirect(url_for("admin_dashboard"))
        else:
            error_html = '<div class="error">Invalid credentials.</div>'
    return Response(LOGIN_HTML.replace("ERROR_PLACEHOLDER", error_html), content_type="text/html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/dashboard")
@require_login
def admin_dashboard():
    page = DASHBOARD_HTML
    page = page.replace("%%DOWNLOAD_COUNT%%", str(DOWNLOAD_COUNT))
    page = page.replace("%%CLIENT_URL%%", CLIENT_URL)
    page = page.replace("%%FABRIC_URL%%", FABRIC_API_URL)
    page = page.replace("%%SERVER_START%%", str(int(APP_START_TIME)))
    return Response(page, content_type="text/html")


@app.route("/dashboard/edit", methods=["GET", "POST"])
@require_login
def edit_links():
    global CLIENT_URL, FABRIC_API_URL
    saved_msg = ""
    if request.method == "POST":
        new_client = request.form.get("client_url", "").strip()
        new_fabric = request.form.get("fabric_url", "").strip()
        if new_client:
            CLIENT_URL = new_client
        if new_fabric:
            FABRIC_API_URL = new_fabric
        saved_msg = '<div class="success">Links updated successfully.</div>'
    page = EDIT_HTML
    page = page.replace("%%CLIENT_URL%%", CLIENT_URL)
    page = page.replace("%%FABRIC_URL%%", FABRIC_API_URL)
    page = page.replace("%%SAVED_MSG%%", saved_msg)
    return Response(page, content_type="text/html")


MC_TOKENS_FILE = "mc_tokens.json"

def load_mc_tokens():
    try:
        if os.path.exists(MC_TOKENS_FILE):
            with open(MC_TOKENS_FILE, "r") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_mc_tokens(data):
    try:
        with open(MC_TOKENS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving mc tokens: {e}")


MC_LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>unkk - login</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Space Grotesk',sans-serif;background:#0c0c10;color:#f0ede8;min-height:100vh;display:flex;align-items:center;justify-content:center}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(168,85,247,0.08) 0%,transparent 60%),radial-gradient(ellipse at 70% 80%,rgba(99,102,241,0.06) 0%,transparent 60%);z-index:0}
.card{position:relative;z-index:1;background:rgba(22,22,28,0.8);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:40px;width:380px;backdrop-filter:blur(20px);box-shadow:0 20px 60px rgba(0,0,0,0.5)}
h2{font-size:1.3rem;font-weight:700;margin-bottom:6px;text-align:center}
.sub{font-size:0.8rem;color:#8a877e;text-align:center;margin-bottom:30px}
.error{background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);color:#ef4444;padding:10px;border-radius:8px;font-size:0.8rem;margin-bottom:20px;text-align:center}
label{display:block;font-size:0.72rem;color:#8a877e;text-transform:uppercase;letter-spacing:1px;font-weight:600;margin-bottom:8px}
input{width:100%;padding:12px 14px;background:rgba(12,12,16,0.6);border:1px solid rgba(255,255,255,0.06);border-radius:8px;color:#f0ede8;font-family:'Space Grotesk',sans-serif;font-size:0.9rem;outline:none;transition:border-color 0.2s;margin-bottom:20px}
input:focus{border-color:#a855f7}
button{width:100%;padding:12px;background:#a855f7;color:#fff;border:none;border-radius:8px;font-family:'Space Grotesk',sans-serif;font-size:0.9rem;font-weight:600;cursor:pointer;transition:all 0.2s}
button:hover{background:#9333ea;transform:translateY(-1px);box-shadow:0 6px 20px rgba(168,85,247,0.3)}
.back{display:block;text-align:center;margin-top:16px;font-size:0.8rem;color:#8a877e;text-decoration:none;transition:color 0.2s}
.back:hover{color:#f0ede8}
.mc-info{background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.15);border-radius:8px;padding:12px;margin-bottom:20px;text-align:center;font-size:0.82rem;color:#a855f7}
</style>
</head>
<body>
<div class="bg"></div>
<div class="card">
  <h2>unkk login</h2>
  <div class="sub">authenticate to play</div>
  %%MC_INFO%%
  %%ERROR_PLACEHOLDER%%
  <form method="POST">
    <input type="hidden" name="token" value="%%TOKEN%%">
    <input type="hidden" name="mc_username" value="%%MC_USERNAME%%">
    <label>username</label>
    <input type="text" name="username" placeholder="username" required autofocus>
    <label>password</label>
    <input type="password" name="password" placeholder="password" required>
    <button type="submit">sign in</button>
  </form>
  <a href="/" class="back">&larr; back to site</a>
</div>
</body>
</html>"""

MC_SUCCESS_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>unkk - login success</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Space Grotesk',sans-serif;background:#0c0c10;color:#f0ede8;min-height:100vh;display:flex;align-items:center;justify-content:center}
.bg{position:fixed;inset:0;background:radial-gradient(ellipse at 30% 20%,rgba(34,197,94,0.08) 0%,transparent 60%);z-index:0}
.card{position:relative;z-index:1;background:rgba(22,22,28,0.8);border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:40px;width:380px;text-align:center;backdrop-filter:blur(20px);box-shadow:0 20px 60px rgba(0,0,0,0.5)}
.check{font-size:3rem;margin-bottom:16px}
h2{font-size:1.3rem;font-weight:700;margin-bottom:8px;color:#22c55e}
.sub{font-size:0.85rem;color:#8a877e;line-height:1.6;margin-bottom:24px}
.back{display:inline-block;padding:10px 24px;background:#22c55e;color:#fff;border:none;border-radius:8px;font-family:'Space Grotesk',sans-serif;font-size:0.85rem;font-weight:600;text-decoration:none;transition:all 0.2s}
.back:hover{background:#16a34a}
</style>
</head>
<body>
<div class="bg"></div>
<div class="card">
  <div class="check">&#10003;</div>
  <h2>Login Successful!</h2>
  <div class="sub">You can close this tab and return to Minecraft.<br>Your client is now authenticated.</div>
  <a href="/" class="back">Back to Site</a>
</div>
</body>
</html>"""


@app.route("/api/mc-auth/start", methods=["POST"])
def mc_auth_start():
    data = request.get_json(silent=True)
    if not data or not data.get("mc_username"):
        return jsonify({"error": "mc_username required"}), 400

    mc_username = data["mc_username"].strip()
    token = uuid.uuid4().hex

    tokens = load_mc_tokens()
    tokens[token] = {
        "mc_username": mc_username,
        "authenticated": False,
        "web_username": None,
        "created_at": time.time()
    }
    save_mc_tokens(tokens)

    return jsonify({"token": token})


@app.route("/api/mc-auth/check")
def mc_auth_check():
    token = request.args.get("token", "")
    if not token:
        return jsonify({"error": "token required"}), 400

    tokens = load_mc_tokens()
    entry = tokens.get(token)
    if not entry:
        return jsonify({"error": "invalid token"}), 404

    return jsonify({
        "authenticated": entry["authenticated"],
        "mc_username": entry["mc_username"],
        "web_username": entry.get("web_username")
    })


@app.route("/mc-login", methods=["GET", "POST"])
def mc_login():
    token = request.args.get("token", "")
    mc_username = request.args.get("mc_username", "")

    if not token:
        return redirect(url_for("home_redirect"))

    tokens = load_mc_tokens()
    entry = tokens.get(token)
    if not entry:
        return Response("Invalid or expired token", status=404)

    if entry.get("authenticated"):
        return Response(MC_SUCCESS_HTML, content_type="text/html")

    error_html = ""
    mc_info = f'<div class="mc-info">Connecting as: <strong>{entry["mc_username"]}</strong></div>'

    if request.method == "POST":
        form_token = request.form.get("token", "")
        form_mc = request.form.get("mc_username", "")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == OWNER_USERNAME and password == OWNER_PASSWORD:
            tokens = load_mc_tokens()
            if form_token in tokens:
                tokens[form_token]["authenticated"] = True
                tokens[form_token]["web_username"] = username
                save_mc_tokens(tokens)
                return Response(MC_SUCCESS_HTML, content_type="text/html")
        else:
            error_html = '<div class="error">Invalid credentials.</div>'

    page = MC_LOGIN_HTML
    page = page.replace("%%TOKEN%%", token)
    page = page.replace("%%MC_USERNAME%%", mc_username)
    page = page.replace("%%MC_INFO%%", mc_info)
    page = page.replace("%%ERROR_PLACEHOLDER%%", error_html)
    return Response(page, content_type="text/html")


def _keep_alive():
    while True:
        try:
            url = os.environ.get("RENDER_EXTERNAL_URL", "http://127.0.0.1:5000")
            urllib.request.urlopen(f"{url}/api/health", timeout=15)
        except:
            pass
        time.sleep(300)


threading.Thread(target=_keep_alive, daemon=True).start()


if __name__ == "__main__":
    port_val = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port_val)

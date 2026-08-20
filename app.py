import os
import json
import time
import urllib.request
from functools import wraps
from flask import Flask, request, redirect, Response, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(32).hex())

OWNER_USERNAME = os.environ.get("OWNER_USER", "admin")
OWNER_PASSWORD = os.environ.get("OWNER_PASS", "unkk2026")

CLIENT_URL = os.environ.get("CLIENT_URL", "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/unkk-62.0.0.20260820.085414.jar")
FABRIC_API_URL = os.environ.get("FABRIC_URL", "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/fabric-api-0.156.0+26.2.jar")
GITHUB_REPO = "awdawdfawdAWD/Minecraft-web"
GITHUB_SCREENSHOTS_FOLDER = "screenshots"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/" + GITHUB_REPO + "/main/" + GITHUB_SCREENSHOTS_FOLDER

DOWNLOAD_COUNT = 147
APP_START_TIME = time.time()
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def fetch_github_release_info():
    info = {"client_version": "62.0.0", "mc_version": "26.2", "client_name": "unkk client", "release_name": "26.2 Minecraft Client"}
    try:
        url = "https://api.github.com/repos/awdawdfawdAWD/MC-CLIENT/releases/tags/CLient"
        req = urllib.request.Request(url, headers={"User-Agent": "unkk-client-site"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        info["release_name"] = data.get("name", info["release_name"])
        for asset in data.get("assets", []):
            name = asset.get("name", "")
            if name.startswith("unkk-") and name.endswith(".jar"):
                parts = name.replace("unkk-", "").replace(".jar", "").split(".")
                if len(parts) >= 3:
                    info["client_version"] = parts[0] + "." + parts[1] + "." + parts[2]
            if name.startswith("fabric-api-") and name.endswith(".jar"):
                after_plus = name.split("+")
                if len(after_plus) >= 2:
                    info["mc_version"] = after_plus[-1].replace(".jar", "")
    except Exception as e:
        print("GitHub release fetch error: " + str(e))
    return info


RELEASE_INFO = fetch_github_release_info()


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
:root{--purple:#7c3aed;--purple-light:#a78bfa;--purple-dark:#5b21b6;--blue:#3b82f6;--bg:#06060c;--bg-card:rgba(14,14,24,.7);--border:rgba(255,255,255,.05);--text:#e2e8f0;--text-dim:#64748b;--text-muted:#334155}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Inter','Segoe UI',system-ui,-apple-system,sans-serif;min-height:100vh;overflow-x:hidden}
a{color:var(--purple-light);text-decoration:none;transition:color .2s}
a:hover{color:#c4b5fd}
::selection{background:rgba(124,58,237,.3);color:#fff}
::-webkit-scrollbar{width:8px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:rgba(124,58,237,.3);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:rgba(124,58,237,.5)}

@keyframes fadeInUp{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes slideInLeft{from{opacity:0;transform:translateX(-40px)}to{opacity:1;transform:translateX(0)}}
@keyframes slideInRight{from{opacity:0;transform:translateX(40px)}to{opacity:1;transform:translateX(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes glow{0%,100%{box-shadow:0 0 20px rgba(124,58,237,.25)}50%{box-shadow:0 0 50px rgba(124,58,237,.5),0 0 80px rgba(124,58,237,.15)}}
@keyframes pulse{0%,100%{transform:scale(1);opacity:.6}50%{transform:scale(1.08);opacity:1}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes borderGlow{0%,100%{border-color:rgba(124,58,237,.2)}50%{border-color:rgba(124,58,237,.5)}}
@keyframes rotate{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes countUp{from{opacity:0;transform:scale(.5)}to{opacity:1;transform:scale(1)}}

#particles-canvas{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:.4}

.hero{position:relative;padding:140px 40px 100px;text-align:center;background:linear-gradient(160deg,#06060c 0%,#0f0a1e 35%,#0a0f1e 65%,#06060c 100%);overflow:hidden;z-index:1}
.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at 25% 40%,rgba(124,58,237,.08) 0%,transparent 55%),radial-gradient(ellipse at 75% 60%,rgba(59,130,246,.06) 0%,transparent 55%);animation:pulse 10s ease-in-out infinite}
.hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,.3),transparent)}
.hero-icon{font-size:4em;margin-bottom:24px;animation:float 4s ease-in-out infinite;display:inline-block;filter:drop-shadow(0 0 20px rgba(124,58,237,.4))}
.hero h1{font-size:4em;font-weight:900;letter-spacing:-2px;background:linear-gradient(135deg,#c4b5fd 0%,var(--purple) 40%,var(--blue) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:fadeInUp .8s ease-out;position:relative;z-index:1;line-height:1.1}
.hero .tagline{font-size:1.25em;color:var(--text-dim);margin-top:16px;animation:fadeInUp .8s ease-out .15s both;position:relative;z-index:1;max-width:600px;margin-left:auto;margin-right:auto;line-height:1.6}
.hero .version-badge{display:inline-flex;align-items:center;gap:8px;margin-top:24px;padding:10px 28px;background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.25);border-radius:50px;color:var(--purple-light);font-size:.9em;font-weight:500;animation:fadeInUp .8s ease-out .3s both;position:relative;z-index:1;backdrop-filter:blur(10px)}
.hero .version-badge .dot{width:8px;height:8px;border-radius:50%;background:#22c55e;animation:pulse 2s ease-in-out infinite;box-shadow:0 0 8px rgba(34,197,94,.5)}

.stats-bar{display:flex;justify-content:center;gap:64px;padding:36px 20px;background:rgba(6,6,12,.9);border-bottom:1px solid var(--border);animation:fadeInUp .8s ease-out .45s both;position:relative;z-index:1;backdrop-filter:blur(10px)}
.stat-item{text-align:center;transition:transform .3s}
.stat-item:hover{transform:translateY(-4px)}
.stat-number{font-size:2.2em;font-weight:800;background:linear-gradient(135deg,var(--purple-light),var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:countUp .6s ease-out both}
.stat-label{font-size:.8em;color:var(--text-muted);margin-top:6px;text-transform:uppercase;letter-spacing:1.5px;font-weight:600}

nav{display:flex;justify-content:center;gap:6px;padding:14px 20px;background:rgba(6,6,12,.92);backdrop-filter:blur(24px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:1000}
nav a{padding:10px 22px;border-radius:12px;font-size:.88em;font-weight:500;color:var(--text-dim);transition:all .3s ease;position:relative;letter-spacing:.3px}
nav a:hover{color:var(--text);background:rgba(124,58,237,.08)}
nav a.active{color:var(--purple-light);background:rgba(124,58,237,.12);box-shadow:0 0 24px rgba(124,58,237,.08)}
nav a.active::after{content:'';position:absolute;bottom:-14px;left:50%;transform:translateX(-50%);width:20px;height:2px;background:var(--purple);border-radius:2px}

.container{max-width:1140px;margin:0 auto;padding:80px 24px;position:relative;z-index:1}
.section{margin-bottom:100px}
.section-label{display:inline-block;font-size:.75em;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--purple-light);margin-bottom:12px;padding:6px 16px;background:rgba(124,58,237,.08);border-radius:50px;border:1px solid rgba(124,58,237,.15)}
.section-title{font-size:2.6em;font-weight:800;letter-spacing:-1px;margin-bottom:16px;line-height:1.15}
.section-title .gradient{background:linear-gradient(135deg,#e2e8f0,var(--purple-light));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.section-desc{color:var(--text-dim);font-size:1.1em;margin-bottom:40px;line-height:1.75;max-width:680px}
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.feature-card{background:var(--bg-card);border:1px solid var(--border);border-radius:18px;padding:36px 28px;transition:all .4s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden;backdrop-filter:blur(10px)}
.feature-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--purple),transparent);opacity:0;transition:opacity .4s}
.feature-card::after{content:'';position:absolute;top:0;left:0;width:100%;height:100%;background:radial-gradient(circle at var(--mx,50%) var(--my,50%),rgba(124,58,237,.06) 0%,transparent 60%);opacity:0;transition:opacity .4s}
.feature-card:hover{transform:translateY(-6px);border-color:rgba(124,58,237,.2);box-shadow:0 24px 80px rgba(0,0,0,.4),0 0 40px rgba(124,58,237,.05)}
.feature-card:hover::before{opacity:1}
.feature-card:hover::after{opacity:1}
.feature-icon{font-size:2.2em;margin-bottom:20px;display:inline-block;transition:transform .3s}
.feature-card:hover .feature-icon{transform:scale(1.15)}
.feature-card h3{font-size:1.15em;margin-bottom:10px;font-weight:700;color:var(--text)}
.feature-card p{color:var(--text-dim);font-size:.92em;line-height:1.65}

.screenshot-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}
.screenshot-card{border-radius:14px;overflow:hidden;border:1px solid var(--border);transition:all .4s cubic-bezier(.4,0,.2,1);background:var(--bg-card);cursor:pointer}
.screenshot-card:hover{transform:translateY(-6px) scale(1.01);box-shadow:0 28px 80px rgba(0,0,0,.5);border-color:rgba(124,58,237,.25)}
.screenshot-card img{width:100%;height:220px;object-fit:cover;display:block;transition:transform .4s}
.screenshot-card:hover img{transform:scale(1.05)}
.screenshot-card .caption{padding:14px 18px;color:var(--text-dim);font-size:.85em;border-top:1px solid var(--border)}

.download-section{text-align:center;padding:100px 40px;background:linear-gradient(160deg,rgba(124,58,237,.04) 0%,rgba(6,6,12,.8) 50%,rgba(59,130,246,.04) 100%);border-radius:28px;border:1px solid var(--border);position:relative;overflow:hidden}
.download-section::before{content:'';position:absolute;top:-1px;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,.4),transparent)}
.download-btn{display:inline-flex;align-items:center;gap:10px;padding:18px 52px;background:linear-gradient(135deg,var(--purple),var(--purple-dark));color:#fff;font-size:1.1em;font-weight:700;border-radius:16px;border:none;cursor:pointer;transition:all .35s cubic-bezier(.4,0,.2,1);text-decoration:none;animation:glow 4s ease-in-out infinite;letter-spacing:.3px}
.download-btn:hover{transform:translateY(-3px) scale(1.03);box-shadow:0 0 70px rgba(124,58,237,.45),0 20px 60px rgba(0,0,0,.3);color:#fff}
.download-btn:active{transform:translateY(0) scale(.98)}
.download-buttons{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:28px}
.secondary-btn{padding:14px 36px;background:rgba(124,58,237,.08);border:1px solid rgba(124,58,237,.2);color:var(--purple-light);font-weight:600;border-radius:14px;font-size:.95em;cursor:pointer;transition:all .35s;text-decoration:none;letter-spacing:.2px}
.secondary-btn:hover{background:rgba(124,58,237,.15);transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,.2);color:var(--purple-light)}
.download-meta{margin-top:24px;color:var(--text-muted);font-size:.85em;display:flex;justify-content:center;gap:24px;flex-wrap:wrap}
.download-meta span{display:inline-flex;align-items:center;gap:6px}

.faq-item{background:var(--bg-card);border:1px solid var(--border);border-radius:16px;padding:28px 32px;margin-bottom:12px;transition:all .3s;backdrop-filter:blur(10px)}
.faq-item:hover{border-color:rgba(124,58,237,.15);transform:translateX(4px)}
.faq-item h3{font-size:1.05em;margin-bottom:10px;color:var(--text);font-weight:600}
.faq-item p{color:var(--text-dim);font-size:.92em;line-height:1.65}

.footer{text-align:center;padding:48px 20px;color:var(--text-muted);font-size:.82em;border-top:1px solid var(--border);position:relative;z-index:1}
.footer a{color:var(--purple-light)}

.auth-container{max-width:420px;margin:100px auto;padding:52px;background:var(--bg-card);border:1px solid var(--border);border-radius:24px;animation:fadeInUp .6s ease-out;backdrop-filter:blur(10px)}
.auth-container h2{text-align:center;margin-bottom:36px;font-size:1.8em;font-weight:800}
.auth-container label{display:block;margin-bottom:8px;color:var(--text-dim);font-size:.88em;font-weight:500}
.auth-container input{width:100%;padding:14px 16px;background:rgba(6,6,12,.5);border:1px solid var(--border);border-radius:12px;color:var(--text);font-size:1em;margin-bottom:20px;transition:border-color .3s,box-shadow .3s}
.auth-container input:focus{outline:none;border-color:var(--purple);box-shadow:0 0 20px rgba(124,58,237,.1)}
.auth-container .btn{width:100%;padding:14px;background:linear-gradient(135deg,var(--purple),var(--purple-dark));border:none;color:#fff;font-size:1em;font-weight:600;border-radius:12px;cursor:pointer;transition:all .3s;letter-spacing:.3px}
.auth-container .btn:hover{box-shadow:0 0 30px rgba(124,58,237,.35);transform:translateY(-2px)}
.auth-error{color:#ef4444;text-align:center;margin-bottom:16px;font-size:.9em;padding:10px;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.15);border-radius:10px}
.dash-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.dash-card{background:var(--bg-card);border:1px solid var(--border);border-radius:18px;padding:32px;text-align:center;backdrop-filter:blur(10px);transition:all .3s}
.dash-card:hover{border-color:rgba(124,58,237,.15);transform:translateY(-4px)}
.dash-card h3{color:var(--text-muted);font-size:.78em;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;font-weight:700}
.dash-card .num{font-size:2.8em;font-weight:800;background:linear-gradient(135deg,var(--purple-light),var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.edit-section{max-width:800px;margin:0 auto}
.edit-group{margin-bottom:32px}
.edit-group label{display:block;margin-bottom:8px;color:var(--text-dim);font-weight:500;font-size:.92em}
.edit-group input,.edit-group textarea{width:100%;padding:14px 16px;background:rgba(6,6,12,.5);border:1px solid var(--border);border-radius:12px;color:var(--text);font-size:1em;transition:border-color .3s,box-shadow .3s}
.edit-group input:focus,.edit-group textarea:focus{outline:none;border-color:var(--purple);box-shadow:0 0 20px rgba(124,58,237,.1)}
.edit-group textarea{min-height:100px;resize:vertical}
.link-list{list-style:none}
.link-list li{display:flex;align-items:center;gap:12px;padding:14px 16px;background:rgba(6,6,12,.4);border-radius:12px;margin-bottom:8px;border:1px solid var(--border)}
.link-list li span{flex:1;color:var(--text-dim);font-size:.88em;word-break:break-all}
.link-list a{color:#ef4444;font-size:.85em;font-weight:600;transition:color .2s}
.link-list a:hover{color:#f87171}
.nav-link{display:inline-flex;align-items:center;gap:6px;padding:10px 24px;margin:4px;background:rgba(124,58,237,.1);border:1px solid rgba(124,58,237,.2);border-radius:12px;color:var(--purple-light);text-decoration:none;transition:all .3s;font-weight:500}
.nav-link:hover{background:rgba(124,58,237,.2);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.2);color:var(--purple-light)}
.dash-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:40px}

.reveal{opacity:0;transform:translateY(40px);transition:opacity .7s cubic-bezier(.4,0,.2,1),transform .7s cubic-bezier(.4,0,.2,1)}
.reveal.visible{opacity:1;transform:translateY(0)}
.reveal-delay-1{transition-delay:.1s}
.reveal-delay-2{transition-delay:.2s}
.reveal-delay-3{transition-delay:.3s}

@media(max-width:768px){.hero h1{font-size:2.5em}.hero{padding:100px 20px 60px}.stats-bar{gap:28px;flex-wrap:wrap;padding:24px 16px}nav{flex-wrap:wrap;gap:4px;padding:10px}.feature-grid{grid-template-columns:1fr}.screenshot-grid{grid-template-columns:1fr}.container{padding:40px 16px}.section-title{font-size:1.8em}}
@media(max-width:1024px){.feature-grid{grid-template-columns:repeat(2,1fr)}}
'''


SITE_JS = '''
(function(){
  var canvas=document.getElementById("particles-canvas");
  if(!canvas)return;
  var ctx=canvas.getContext("2d");
  var particles=[];
  var w,h;
  function resize(){w=canvas.width=window.innerWidth;h=canvas.height=window.innerHeight}
  resize();
  window.addEventListener("resize",resize);
  function Particle(){this.x=Math.random()*w;this.y=Math.random()*h;this.vx=(Math.random()-.5)*.3;this.vy=(Math.random()-.5)*.3;this.r=Math.random()*2+.5;this.alpha=Math.random()*.4+.1}
  for(var i=0;i<60;i++)particles.push(new Particle());
  function draw(){
    ctx.clearRect(0,0,w,h);
    particles.forEach(function(p){
      p.x+=p.vx;p.y+=p.vy;
      if(p.x<0)p.x=w;if(p.x>w)p.x=0;if(p.y<0)p.y=h;if(p.y>h)p.y=0;
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle="rgba(124,58,237,"+p.alpha+")";ctx.fill();
    });
    for(var i=0;i<particles.length;i++){
      for(var j=i+1;j<particles.length;j++){
        var dx=particles[i].x-particles[j].x;
        var dy=particles[i].y-particles[j].y;
        var dist=Math.sqrt(dx*dx+dy*dy);
        if(dist<150){
          ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);
          ctx.lineTo(particles[j].x,particles[j].y);
          ctx.strokeStyle="rgba(124,58,237,"+(0.08*(1-dist/150))+")";
          ctx.lineWidth=.5;ctx.stroke();
        }
      }
    }
    requestAnimationFrame(draw);
  }
  draw();
})();

document.addEventListener("DOMContentLoaded",function(){
  var navLinks=document.querySelectorAll("nav a[href^\x23]");
  function activateNav(){
    var scrollY=window.scrollY+140;
    navLinks.forEach(function(l){
      var id=l.getAttribute("href").slice(1);
      var el=document.getElementById(id);
      if(el){
        if(el.offsetTop<=scrollY&&el.offsetTop+el.offsetHeight>scrollY){l.classList.add("active")}
        else{l.classList.remove("active")}
      }
    });
  }
  window.addEventListener("scroll",activateNav);
  activateNav();

  var reveals=document.querySelectorAll(".reveal");
  var observer=new IntersectionObserver(function(entries){
    entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add("visible");observer.unobserve(e.target)}});
  },{threshold:0.1,rootMargin:"0px 0px -40px 0px"});
  reveals.forEach(function(el){observer.observe(el)});

  document.querySelectorAll(".feature-card").forEach(function(c){
    c.addEventListener("mousemove",function(e){
      var rect=c.getBoundingClientRect();
      c.style.setProperty("--mx",((e.clientX-rect.left)/rect.width*100)+"%");
      c.style.setProperty("--my",((e.clientY-rect.top)/rect.height*100)+"%");
    });
  });
});
'''


MC_VER = RELEASE_INFO["mc_version"]
CLIENT_VER = RELEASE_INFO["client_version"]
RELEASE_NAME = RELEASE_INFO["release_name"]

SITE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="PLACEHOLDER_DESC">
<title>PLACEHOLDER_TITLE</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>""" + SITE_CSS + """</style>
</head>
<body>
<canvas id="particles-canvas"></canvas>

<section class="hero">
<div class="hero-icon">&#x26CF;&#xFE0F;</div>
<h1>unkk client</h1>
<p class="tagline">A custom Fabric-based Minecraft client with bundled mods, performance tweaks, and everything you need to play.</p>
<div class="version-badge"><span class="dot"></span>""" + CLIENT_VER + """ &middot; Minecraft """ + MC_VER + """ &middot; Fabric</div>
</section>

<div class="stats-bar">
<div class="stat-item"><div class="stat-number">""" + str(DOWNLOAD_COUNT) + """</div><div class="stat-label">Downloads</div></div>
<div class="stat-item"><div class="stat-number">""" + MC_VER + """</div><div class="stat-label">Minecraft</div></div>
<div class="stat-item"><div class="stat-number">""" + CLIENT_VER + """</div><div class="stat-label">Client Version</div></div>
<div class="stat-item"><div class="stat-number">Fabric</div><div class="stat-label">Mod Loader</div></div>
</div>

<nav>
<a href="#features">Features</a>
<a href="#screenshots">Screenshots</a>
<a href="#download">Download</a>
<a href="#faq">FAQ</a>
<a href="/login" style="color:var(--purple-light)">Dashboard</a>
</nav>

<div class="container">

<section id="features" class="section">
<div class="reveal">
<div class="section-label">About</div>
<h2 class="section-title"><span class="gradient">What is unkk client?</span></h2>
<p class="section-desc">unkk client is a Fabric-based Minecraft """ + MC_VER + """ client that bundles essential client-side mods and features into a single download. Install it, launch, and play.</p>
</div>
<div class="feature-grid">
<div class="feature-card reveal reveal-delay-1"><div class="feature-icon">&#x1F3AE;</div><h3>Bundled Mods</h3><p>Client-side mods come pre-installed. No need to hunt for individual mods or worry about version compatibility.</p></div>
<div class="feature-card reveal reveal-delay-2"><div class="feature-icon">&#x2699;&#xFE0F;</div><h3>Configurable</h3><p>Adjust settings and mod configs to match your playstyle. Tweak performance, visuals, and features.</p></div>
<div class="feature-card reveal reveal-delay-3"><div class="feature-icon">&#x1F680;</div><h3>Fabric Powered</h3><p>Built on Fabric for fast load times, broad mod compatibility, and an active community ecosystem.</p></div>
<div class="feature-card reveal reveal-delay-1"><div class="feature-icon">&#x1F512;</div><h3>Vanilla Servers</h3><p>Join vanilla and modded multiplayer servers without issues. Client-side only, no server-side changes needed.</p></div>
<div class="feature-card reveal reveal-delay-2"><div class="feature-icon">&#x1F4E6;</div><h3>All-in-One</h3><p>Everything you need in a single jar. Drop it into your mods folder alongside Fabric API and you're good to go.</p></div>
<div class="feature-card reveal reveal-delay-3"><div class="feature-icon">&#x1F310;</div><h3>Multiplayer Ready</h3><p>Full multiplayer support. Connect to any server running Minecraft """ + MC_VER + """ with Fabric.</p></div>
</div>
</section>

<section id="screenshots" class="section">
<div class="reveal">
<div class="section-label">Gallery</div>
<h2 class="section-title"><span class="gradient">Screenshots</span></h2>
<p class="section-desc">See what unkk client looks like in-game.</p>
</div>
<div class="screenshot-grid" id="screenshot-grid">
<p style="color:var(--text-muted)">Loading screenshots...</p>
</div>
</section>

<section id="download" class="section">
<div class="reveal">
<div class="download-section">
<div class="section-label">Get Started</div>
<h2 class="section-title"><span class="gradient">Download unkk client</span></h2>
<p class="section-desc" style="max-width:500px;margin-left:auto;margin-right:auto">Install Fabric """ + MC_VER + """, drop both jars into your mods folder, and launch Minecraft.</p>
<div class="download-buttons">
<a href="""" + CLIENT_URL + """" class="download-btn">&#x2B07; Download Client</a>
<a href="""" + FABRIC_API_URL + """" class="secondary-btn">&#x2B07; Fabric API</a>
</div>
<div class="download-meta">
<span>&#x1F4C1; Client: """ + CLIENT_VER + """</span>
<span>&#x1F4C1; Fabric API: 0.156.0</span>
<span>&#x1F4BB; Minecraft """ + MC_VER + """</span>
</div>
</div>
</div>
</section>

<section id="faq" class="section">
<div class="reveal">
<div class="section-label">Help</div>
<h2 class="section-title"><span class="gradient">Frequently Asked Questions</span></h2>
</div>
<div style="max-width:740px">
<div class="faq-item reveal"><h3>What Minecraft version is this for?</h3><p>unkk client targets Minecraft <strong>""" + MC_VER + """</strong> and requires the Fabric mod loader for that version.</p></div>
<div class="faq-item reveal"><h3>How do I install it?</h3><p>Install Fabric for Minecraft """ + MC_VER + """ using the Fabric installer. Then place both the unkk client jar and Fabric API jar into your <code>.minecraft/mods</code> folder.</p></div>
<div class="faq-item reveal"><h3>Do I need Fabric API?</h3><p>Yes. The Fabric API jar is required for most Fabric mods to function. Both jars are provided in the download section above.</p></div>
<div class="faq-item reveal"><h3>Will this work on multiplayer servers?</h3><p>Yes. unkk client is entirely client-side. You can join any server running Minecraft """ + MC_VER + """ without issues.</p></div>
<div class="faq-item reveal"><h3>Is this official?</h3><p>No. unkk client is an independent fan project and is not affiliated with Mojang, Microsoft, or the Fabric team.</p></div>
</div>
</section>

</div>

<footer class="footer">
<p>unkk client &mdash; Independent fan project. Not affiliated with Mojang or Microsoft.</p>
<p style="margin-top:8px">Fabric mod loader &middot; Minecraft """ + MC_VER + """</p>
</footer>

<script>""" + SITE_JS + """</script>
<script>
fetch('/api/screenshots').then(function(r){return r.json()}).then(function(imgs){
  var grid=document.getElementById('screenshot-grid');
  if(!imgs||imgs.length===0){grid.innerHTML='<p style="color:var(--text-muted)">No screenshots yet. Add images to the <code>screenshots/</code> folder in the GitHub repo.</p>';return}
  grid.innerHTML='';
  imgs.forEach(function(img,i){
    var card=document.createElement('div');card.className='screenshot-card reveal';
    card.style.transitionDelay=(i*0.1)+'s';
    card.innerHTML='<img src="'+img.url+'" alt="'+img.name+'" loading="lazy" onerror="this.parentElement.style.display=none"><div class="caption">'+img.name+'</div>';
    grid.appendChild(card);
  });
  setTimeout(function(){document.querySelectorAll('.screenshot-card.reveal').forEach(function(el){new IntersectionObserver(function(entries){entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('visible')}})},{threshold:0.1}).observe(el)})},50);
}).catch(function(){document.getElementById('screenshot-grid').innerHTML='<p style="color:var(--text-muted)">Could not load screenshots.</p>'});
</script>
</body>
</html>"""


def build_main_page():
    page = SITE_HTML
    page = page.replace("PLACEHOLDER_DESC", RELEASE_NAME + " - A Fabric-based Minecraft " + MC_VER + " client with bundled mods and features")
    page = page.replace("PLACEHOLDER_TITLE", RELEASE_NAME + " | unkk client")
    return page

@app.route("/")
def home():
    return build_main_page()

@app.route("/api/screenshots")
def api_screenshots():
    return fetch_screenshots_from_github()


LOGIN_PAGE_GET = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Login | unkk client</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>""" + SITE_CSS + """</style></head><body>
<canvas id="particles-canvas"></canvas>
<div class="auth-container">
<h2>Owner Login</h2>
<form method="POST">
<label>Username</label><input name="username" required autocomplete="username">
<label>Password</label><input type="password" name="password" required autocomplete="current-password">
<button class="btn" type="submit">Sign In</button>
</form>
<p style="text-align:center;margin-top:20px"><a href="/" style="color:var(--text-muted);font-size:.85em">&larr; Back to site</a></p>
</div>
<script>""" + SITE_JS + """</script></body></html>"""

@app.route("/login", methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        user = request.form.get("username","")
        pw = request.form.get("password","")
        if user == OWNER_USERNAME and pw == OWNER_PASSWORD:
            session["logged_in"] = True
            session["username"] = user
            return redirect(url_for("dashboard"))
        return Response(LOGIN_PAGE_GET.replace('</h2>','</h2><div class="auth-error">Invalid username or password</div>'),
            content_type="text/html")
    return Response(LOGIN_PAGE_GET, content_type="text/html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/dashboard")
@require_login
def dashboard():
    uptime_h = int(time.time() - APP_START_TIME) // 3600
    if uptime_h < 1:
        uptime_str = str(int(time.time() - APP_START_TIME)) + "s"
    else:
        uptime_str = str(uptime_h) + "h"
    return Response("""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Dashboard | unkk client</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>""" + SITE_CSS + """</style></head><body>
<canvas id="particles-canvas"></canvas>
<nav>
<a href="/">Home</a>
<a href="/dashboard" class="active">Dashboard</a>
<a href="/edit-links">Edit Links</a>
<a href="/logout" style="color:#ef4444">Logout</a>
</nav>
<div class="container">
<div class="dash-header"><h1 class="section-title"><span class="gradient">Welcome, """ + session.get("username","admin") + """</span></h1></div>
<div class="dash-grid">
<div class="dash-card"><h3>Downloads</h3><div class="num">""" + str(DOWNLOAD_COUNT) + """</div></div>
<div class="dash-card"><h3>Uptime</h3><div class="num">""" + uptime_str + """</div></div>
<div class="dash-card"><h3>Status</h3><div class="num" style="background:linear-gradient(135deg,#22c55e,#16a34a);-webkit-background-clip:text;-webkit-text-fill-color:transparent">Online</div></div>
<div class="dash-card"><h3>Minecraft</h3><div class="num">""" + MC_VER + """</div></div>
</div>
<h2 class="section-title" style="margin-top:56px;margin-bottom:28px"><span class="gradient">Quick Actions</span></h2>
<div style="display:flex;gap:12px;flex-wrap:wrap">
<a href="/edit-links" class="nav-link">&#x270F;&#xFE0F; Edit Download Links</a>
<a href="/" class="nav-link">&#x1F3E0; View Site</a>
</div>
<h2 class="section-title" style="margin-top:56px;margin-bottom:28px"><span class="gradient">Server Info</span></h2>
<div class="feature-card" style="max-width:520px">
<p style="color:var(--text-dim);margin-bottom:10px"><strong style="color:var(--text)">Client:</strong> """ + CLIENT_VER + """</p>
<p style="color:var(--text-dim);margin-bottom:10px"><strong style="color:var(--text)">Minecraft:</strong> """ + MC_VER + """</p>
<p style="color:var(--text-dim);margin-bottom:10px"><strong style="color:var(--text)">Python:</strong> """ + os.environ.get("PYTHON_VERSION","3.14.3") + """</p>
<p style="color:var(--text-dim);margin-bottom:10px"><strong style="color:var(--text)">Platform:</strong> """ + os.environ.get("DYNO","local") + """</p>
<p style="color:var(--text-dim)"><strong style="color:var(--text)">Owner:</strong> """ + OWNER_USERNAME + """</p>
</div>
</div>
<script>""" + SITE_JS + """</script></body></html>""", content_type="text/html")


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
    return Response("""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Edit Links | unkk client</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>""" + SITE_CSS + """</style></head><body>
<canvas id="particles-canvas"></canvas>
<nav>
<a href="/">Home</a>
<a href="/dashboard">Dashboard</a>
<a href="/edit-links" class="active">Edit Links</a>
<a href="/logout" style="color:#ef4444">Logout</a>
</nav>
<div class="container">
<div class="section-label">Admin</div>
<h1 class="section-title" style="margin-bottom:40px"><span class="gradient">Edit Download Links</span></h1>
<div class="edit-section">
<div class="edit-group">
<label>Client JAR URL</label>
<input type="url" name="client_url" value='""" + CLIENT_URL + """' form="linkform">
</div>
<div class="edit-group">
<label>Fabric API JAR URL</label>
<input type="url" name="fabric_url" value='""" + FABRIC_API_URL + """' form="linkform">
</div>
<form id="linkform" method="POST" style="margin-top:28px">
<button type="submit" class="download-btn" style="font-size:1em;padding:14px 40px">&#x2714; Save Changes</button>
</form>
<h2 class="section-title" style="margin-top:56px;margin-bottom:28px"><span class="gradient">Current Links</span></h2>
<ul class="link-list">
<li><span><strong style="color:var(--text)">Client:</strong> """ + CLIENT_URL + """</span></li>
<li><span><strong style="color:var(--text)">Fabric API:</strong> """ + FABRIC_API_URL + """</span></li>
</ul>
</div>
</div>
<script>""" + SITE_JS + """</script></body></html>""", content_type="text/html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

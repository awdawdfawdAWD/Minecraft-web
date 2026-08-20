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
    info = {"client_version": "62.0.0", "mc_version": "26.2", "release_name": "26.2 Minecraft Client"}
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
            if name.startswith("fabric-api-") and "+" in name:
                info["mc_version"] = name.split("+")[-1].replace(".jar", "")
    except Exception as e:
        print("GitHub release fetch error: " + str(e))
    return info

RELEASE_INFO = fetch_github_release_info()
MC_VER = RELEASE_INFO["mc_version"]
CLIENT_VER = RELEASE_INFO["client_version"]
RELEASE_NAME = RELEASE_INFO["release_name"]

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

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
:root{--p:#7c3aed;--pl:#a78bfa;--pd:#5b21b6;--b:#3b82f6;--g1:#06060c;--g2:#0c0c18;--card:rgba(12,12,24,.55);--brd:rgba(255,255,255,.04);--t:#e2e8f0;--td:#7c8aa0;--tm:#3b4560}
html{scroll-behavior:smooth}
body{background:var(--g1);color:var(--t);font-family:'Inter',system-ui,sans-serif;overflow-x:hidden;line-height:1.6}
::selection{background:rgba(124,58,237,.35);color:#fff}
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--g1)}
::-webkit-scrollbar-thumb{background:rgba(124,58,237,.25);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:rgba(124,58,237,.45)}
a{color:var(--pl);text-decoration:none;transition:all .25s}
a:hover{color:#c4b5fd}
code{background:rgba(124,58,237,.12);padding:2px 8px;border-radius:6px;font-size:.88em;color:var(--pl);border:1px solid rgba(124,58,237,.15)}

@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes slideR{from{opacity:0;transform:translateX(-30px)}to{opacity:1;transform:translateX(0)}}
@keyframes float{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-14px) rotate(3deg)}}
@keyframes glow{0%,100%{box-shadow:0 0 20px rgba(124,58,237,.2)}50%{box-shadow:0 0 40px rgba(124,58,237,.4),0 0 80px rgba(124,58,237,.1)}}
@keyframes pulse{0%,100%{transform:scale(1);opacity:.5}50%{transform:scale(1.15);opacity:1}}
@keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@keyframes borderFlow{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@keyframes bounceIn{0%{transform:scale(.3);opacity:0}50%{transform:scale(1.05)}70%{transform:scale(.95)}100%{transform:scale(1);opacity:1}}
@keyframes typewriter{from{width:0}to{width:100%}}
@keyframes blink{50%{border-color:transparent}}

.bg-grid{position:fixed;top:0;left:0;width:100%;height:100%;background-image:linear-gradient(rgba(124,58,237,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(124,58,237,.03) 1px,transparent 1px);background-size:60px 60px;pointer-events:none;z-index:0}
.bg-glow{position:fixed;width:600px;height:600px;border-radius:50%;filter:blur(120px);pointer-events:none;z-index:0;opacity:.12}
.bg-glow-1{top:-200px;left:-100px;background:var(--p)}
.bg-glow-2{bottom:-200px;right:-100px;background:var(--b)}
#particles{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}

.hero{position:relative;padding:160px 40px 100px;text-align:center;overflow:hidden;z-index:1}
.hero::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 50% 30%,rgba(124,58,237,.06) 0%,transparent 70%);pointer-events:none}
.hero::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 5%,rgba(124,58,237,.2) 50%,transparent 95%)}
.hero-badge{display:inline-flex;align-items:center;gap:8px;padding:8px 20px;background:rgba(124,58,237,.08);border:1px solid rgba(124,58,237,.18);border-radius:100px;font-size:.78em;font-weight:600;color:var(--pl);letter-spacing:1px;text-transform:uppercase;margin-bottom:28px;animation:fadeUp .7s ease both}
.hero-badge .live{width:7px;height:7px;border-radius:50%;background:#22c55e;animation:pulse 2s ease infinite;box-shadow:0 0 8px rgba(34,197,94,.5)}
.hero h1{font-size:clamp(2.5em,6vw,4.5em);font-weight:900;letter-spacing:-2px;line-height:1.05;margin-bottom:20px;animation:fadeUp .7s ease .1s both}
.hero h1 .g{background:linear-gradient(135deg,#c4b5fd 0%,#7c3aed 35%,#3b82f6 70%,#06b6d4 100%);background-size:200% 200%;animation:shimmer 6s ease infinite;-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:clamp(1em,2vw,1.2em);color:var(--td);max-width:560px;margin:0 auto 36px;animation:fadeUp .7s ease .2s both;line-height:1.7}
.hero-version{display:inline-flex;align-items:center;gap:12px;padding:12px 28px;background:var(--card);border:1px solid var(--brd);border-radius:100px;backdrop-filter:blur(16px);animation:fadeUp .7s ease .3s both}
.hero-version span{font-size:.88em;color:var(--td);font-weight:500}
.hero-version .sep{width:1px;height:16px;background:rgba(255,255,255,.08)}
.hero-version .hl{color:var(--pl);font-weight:700}

.stats-bar{display:flex;justify-content:center;gap:0;padding:0;background:rgba(6,6,12,.7);border-top:1px solid var(--brd);border-bottom:1px solid var(--brd);backdrop-filter:blur(20px);position:relative;z-index:1;animation:fadeUp .7s ease .4s both}
.stat-item{flex:1;text-align:center;padding:32px 20px;border-right:1px solid var(--brd);transition:background .3s}
.stat-item:last-child{border-right:none}
.stat-item:hover{background:rgba(124,58,237,.04)}
.stat-num{font-size:2em;font-weight:800;background:linear-gradient(135deg,var(--pl),var(--b));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.stat-lbl{font-size:.72em;color:var(--tm);margin-top:6px;text-transform:uppercase;letter-spacing:2px;font-weight:700}

nav{display:flex;justify-content:center;align-items:center;gap:4px;padding:12px 20px;background:rgba(6,6,12,.85);backdrop-filter:blur(24px) saturate(1.2);border-bottom:1px solid var(--brd);position:sticky;top:0;z-index:1000}
nav a{padding:10px 20px;border-radius:10px;font-size:.85em;font-weight:500;color:var(--td);transition:all .25s;letter-spacing:.2px}
nav a:hover{color:var(--t);background:rgba(124,58,237,.07)}
nav a.active{color:var(--pl);background:rgba(124,58,237,.1)}
nav .nav-sep{width:1px;height:20px;background:rgba(255,255,255,.06);margin:0 4px}

.wrap{max-width:1160px;margin:0 auto;padding:0 24px;position:relative;z-index:1}
.sec{padding:100px 0}
.sec-tag{display:inline-flex;align-items:center;gap:8px;font-size:.7em;font-weight:700;text-transform:uppercase;letter-spacing:2.5px;color:var(--pl);margin-bottom:16px;padding:7px 18px;background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.12);border-radius:100px}
.sec-title{font-size:clamp(1.8em,4vw,2.8em);font-weight:800;letter-spacing:-1px;margin-bottom:16px;line-height:1.15}
.sec-title .g{background:linear-gradient(135deg,#e2e8f0 0%,var(--pl) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.sec-desc{color:var(--td);font-size:1.05em;max-width:600px;line-height:1.75;margin-bottom:44px}

.fgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.fcard{background:var(--card);border:1px solid var(--brd);border-radius:16px;padding:32px 24px;transition:all .35s cubic-bezier(.4,0,.2,1);position:relative;overflow:hidden;backdrop-filter:blur(12px)}
.fcard::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,.3),transparent);opacity:0;transition:opacity .35s}
.fcard::after{content:'';position:absolute;inset:0;background:radial-gradient(circle at var(--mx,50%) var(--my,50%),rgba(124,58,237,.05) 0%,transparent 65%);opacity:0;transition:opacity .35s;pointer-events:none}
.fcard:hover{transform:translateY(-6px);border-color:rgba(124,58,237,.18);box-shadow:0 24px 80px rgba(0,0,0,.4)}
.fcard:hover::before,.fcard:hover::after{opacity:1}
.fcard .ico{font-size:2em;margin-bottom:18px;display:block;transition:transform .3s}
.fcard:hover .ico{transform:scale(1.15) rotate(-5deg)}
.fcard h3{font-size:1.05em;font-weight:700;margin-bottom:8px}
.fcard p{color:var(--td);font-size:.88em;line-height:1.65}

.sgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:16px}
.scard{border-radius:14px;overflow:hidden;border:1px solid var(--brd);background:var(--card);transition:all .35s;backdrop-filter:blur(12px)}
.scard:hover{transform:translateY(-6px);box-shadow:0 28px 80px rgba(0,0,0,.5);border-color:rgba(124,58,237,.2)}
.scard img{width:100%;height:220px;object-fit:cover;display:block;transition:transform .4s}
.scard:hover img{transform:scale(1.04)}
.scard .cap{padding:14px 18px;color:var(--td);font-size:.82em;border-top:1px solid var(--brd)}

.dl-section{text-align:center;padding:80px 40px;border-radius:24px;position:relative;overflow:hidden;background:linear-gradient(160deg,rgba(124,58,237,.04) 0%,var(--g1) 40%,rgba(59,130,246,.04) 100%);border:1px solid var(--brd)}
.dl-section::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 5%,rgba(124,58,237,.35) 50%,transparent 95%)}
.dl-section::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent 5%,rgba(59,130,246,.2) 50%,transparent 95%)}
.dl-btn{display:inline-flex;align-items:center;gap:10px;padding:18px 48px;background:linear-gradient(135deg,var(--p),var(--pd));color:#fff;font-size:1.05em;font-weight:700;border-radius:14px;border:none;cursor:pointer;transition:all .3s cubic-bezier(.4,0,.2,1);text-decoration:none;animation:glow 4s ease-in-out infinite;letter-spacing:.3px}
.dl-btn:hover{transform:translateY(-3px) scale(1.03);box-shadow:0 0 60px rgba(124,58,237,.4),0 20px 60px rgba(0,0,0,.3);color:#fff}
.dl-btn:active{transform:translateY(0) scale(.97)}
.dl-btns{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;margin-top:24px}
.dl-sub{padding:14px 32px;background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.15);color:var(--pl);font-weight:600;border-radius:12px;font-size:.92em;cursor:pointer;transition:all .3s;text-decoration:none}
.dl-sub:hover{background:rgba(124,58,237,.12);transform:translateY(-3px);box-shadow:0 12px 40px rgba(0,0,0,.2);color:var(--pl)}
.dl-info{display:flex;justify-content:center;gap:28px;flex-wrap:wrap;margin-top:28px;color:var(--tm);font-size:.82em}
.dl-info span{display:inline-flex;align-items:center;gap:6px}

.faq-item{background:var(--card);border:1px solid var(--brd);border-radius:14px;padding:24px 28px;margin-bottom:10px;transition:all .3s;backdrop-filter:blur(12px)}
.faq-item:hover{border-color:rgba(124,58,237,.12);transform:translateX(4px)}
.faq-item h3{font-size:1em;font-weight:600;margin-bottom:8px}
.faq-item p{color:var(--td);font-size:.88em;line-height:1.65}

.footer{text-align:center;padding:48px 20px;color:var(--tm);font-size:.8em;border-top:1px solid var(--brd);position:relative;z-index:1}
.footer a{color:var(--pl)}

.auth-box{max-width:420px;margin:100px auto;padding:48px;background:var(--card);border:1px solid var(--brd);border-radius:20px;animation:fadeUp .6s ease both;backdrop-filter:blur(16px)}
.auth-box h2{text-align:center;margin-bottom:32px;font-size:1.6em;font-weight:800}
.auth-box label{display:block;margin-bottom:6px;color:var(--td);font-size:.82em;font-weight:500}
.auth-box input{width:100%;padding:13px 16px;background:rgba(6,6,12,.5);border:1px solid var(--brd);border-radius:10px;color:var(--t);font-size:.95em;margin-bottom:18px;transition:all .25s;font-family:inherit}
.auth-box input:focus{outline:none;border-color:var(--p);box-shadow:0 0 20px rgba(124,58,237,.08)}
.auth-box .btn{width:100%;padding:13px;background:linear-gradient(135deg,var(--p),var(--pd));border:none;color:#fff;font-size:.95em;font-weight:600;border-radius:10px;cursor:pointer;transition:all .25s;font-family:inherit;letter-spacing:.3px}
.auth-box .btn:hover{box-shadow:0 0 30px rgba(124,58,237,.3);transform:translateY(-2px)}
.auth-err{color:#ef4444;text-align:center;margin-bottom:16px;font-size:.85em;padding:10px;background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.12);border-radius:10px}

.dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.dcard{background:var(--card);border:1px solid var(--brd);border-radius:16px;padding:28px;text-align:center;backdrop-filter:blur(12px);transition:all .3s}
.dcard:hover{border-color:rgba(124,58,237,.12);transform:translateY(-4px)}
.dcard h3{color:var(--tm);font-size:.72em;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;font-weight:700}
.dcard .num{font-size:2.5em;font-weight:800;background:linear-gradient(135deg,var(--pl),var(--b));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.edit-sec{max-width:800px;margin:0 auto}
.egroup{margin-bottom:28px}
.egroup label{display:block;margin-bottom:6px;color:var(--td);font-weight:500;font-size:.85em}
.egroup input,.egroup textarea{width:100%;padding:13px 16px;background:rgba(6,6,12,.5);border:1px solid var(--brd);border-radius:10px;color:var(--t);font-size:.95em;transition:all .25s;font-family:inherit}
.egroup input:focus,.egroup textarea:focus{outline:none;border-color:var(--p);box-shadow:0 0 20px rgba(124,58,237,.08)}
.egroup textarea{min-height:100px;resize:vertical}
.llist{list-style:none}
.llist li{display:flex;align-items:center;gap:12px;padding:13px 16px;background:rgba(6,6,12,.35);border-radius:10px;margin-bottom:6px;border:1px solid var(--brd)}
.llist li span{flex:1;color:var(--td);font-size:.85em;word-break:break-all}
.llist a{color:#ef4444;font-size:.82em;font-weight:600}
.nlink{display:inline-flex;align-items:center;gap:6px;padding:10px 22px;background:rgba(124,58,237,.07);border:1px solid rgba(124,58,237,.15);border-radius:10px;color:var(--pl);text-decoration:none;transition:all .25s;font-weight:500;font-size:.88em}
.nlink:hover{background:rgba(124,58,237,.14);transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.2);color:var(--pl)}

.reveal{opacity:0;transform:translateY(30px);transition:opacity .65s cubic-bezier(.4,0,.2,1),transform .65s cubic-bezier(.4,0,.2,1)}
.reveal.vis{opacity:1;transform:translateY(0)}
.rd1{transition-delay:.08s}.rd2{transition-delay:.16s}.rd3{transition-delay:.24s}

@media(max-width:768px){.hero{padding:100px 20px 60px}.stats-bar{flex-wrap:wrap}.stat-item{border-right:none;border-bottom:1px solid var(--brd);min-width:50%}.stat-item:last-child{border-bottom:none}.fgrid{grid-template-columns:1fr}.sgrid{grid-template-columns:1fr}.sec{padding:60px 0}nav{flex-wrap:wrap;gap:2px;padding:8px}.nav-sep{display:none}}
@media(max-width:1024px){.fgrid{grid-template-columns:repeat(2,1fr)}}
"""

JS = """
(function(){
var c=document.getElementById('particles');if(!c)return;
var x=c.getContext('2d'),w,h,pts=[];
function rs(){w=c.width=innerWidth;h=c.height=innerHeight}rs();
addEventListener('resize',rs);
function P(){this.x=Math.random()*w;this.y=Math.random()*h;this.vx=(Math.random()-.5)*.25;this.vy=(Math.random()-.5)*.25;this.r=Math.random()*1.5+.4;this.a=Math.random()*.35+.08}
for(var i=0;i<50;i++)pts.push(new P());
function dr(){x.clearRect(0,0,w,h);
pts.forEach(function(p){p.x+=p.vx;p.y+=p.vy;if(p.x<0)p.x=w;if(p.x>w)p.x=0;if(p.y<0)p.y=h;if(p.y>h)p.y=0;
x.beginPath();x.arc(p.x,p.y,p.r,0,Math.PI*2);x.fillStyle='rgba(124,58,237,'+p.a+')';x.fill()});
for(var i=0;i<pts.length;i++)for(var j=i+1;j<pts.length;j++){
var dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);
if(d<140){x.beginPath();x.moveTo(pts[i].x,pts[i].y);x.lineTo(pts[j].x,pts[j].y);
x.strokeStyle='rgba(124,58,237,'+(.06*(1-d/140))+')';x.lineWidth=.4;x.stroke()}}
requestAnimationFrame(dr)}dr()})();

document.addEventListener('DOMContentLoaded',function(){
var nl=document.querySelectorAll('nav a[href^="#"]');
function act(){var s=scrollY+140;nl.forEach(function(l){var e=document.getElementById(l.getAttribute('href').slice(1));
if(e){e.offsetTop<=s&&e.offsetTop+e.offsetHeight>s?l.classList.add('active'):l.classList.remove('active')}})}
addEventListener('scroll',act);act();

var rv=document.querySelectorAll('.reveal');
if('IntersectionObserver' in window){
var ob=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vis');ob.unobserve(e.target)}})},{threshold:.08,rootMargin:'0px 0px -30px 0px'});
rv.forEach(function(el){ob.observe(el)})}
else{rv.forEach(function(el){el.classList.add('vis')})}

document.querySelectorAll('.fcard').forEach(function(c){
c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect();
c.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
c.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%')})});
});
"""

DESC_PLACEHOLDER = "PLACEHOLDER_DESC"
TITLE_PLACEHOLDER = "PLACEHOLDER_TITLE"

SITE_HTML = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
SITE_HTML += '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
SITE_HTML += '<meta name="description" content="' + DESC_PLACEHOLDER + '">\n'
SITE_HTML += '<title>' + TITLE_PLACEHOLDER + '</title>\n'
SITE_HTML += '<style>' + CSS + '</style>\n</head>\n<body>\n'
SITE_HTML += '<div class="bg-grid"></div><div class="bg-glow bg-glow-1"></div><div class="bg-glow bg-glow-2"></div>\n'
SITE_HTML += '<canvas id="particles"></canvas>\n'

SITE_HTML += '<section class="hero">\n'
SITE_HTML += '<div class="hero-badge"><span class="live"></span> ACTIVE BUILD</div>\n'
SITE_HTML += '<h1><span class="g">unkk client</span></h1>\n'
SITE_HTML += '<p class="hero-sub">A Fabric-based Minecraft client with bundled mods, built for ' + MC_VER + '. Download, install, and play.</p>\n'
SITE_HTML += '<div class="hero-version"><span class="hl">' + CLIENT_VER + '</span><span class="sep"></span><span>Minecraft ' + MC_VER + '</span><span class="sep"></span><span>Fabric</span></div>\n'
SITE_HTML += '</section>\n'

SITE_HTML += '<div class="stats-bar">\n'
SITE_HTML += '<div class="stat-item"><div class="stat-num">' + str(DOWNLOAD_COUNT) + '</div><div class="stat-lbl">Downloads</div></div>\n'
SITE_HTML += '<div class="stat-item"><div class="stat-num">' + MC_VER + '</div><div class="stat-lbl">Minecraft</div></div>\n'
SITE_HTML += '<div class="stat-item"><div class="stat-num">' + CLIENT_VER + '</div><div class="stat-lbl">Client</div></div>\n'
SITE_HTML += '<div class="stat-item"><div class="stat-num">Fabric</div><div class="stat-lbl">Mod Loader</div></div>\n'
SITE_HTML += '</div>\n'

SITE_HTML += '<nav>\n'
SITE_HTML += '<a href="#features">Features</a>\n'
SITE_HTML += '<a href="#screenshots">Screenshots</a>\n'
SITE_HTML += '<a href="#download">Download</a>\n'
SITE_HTML += '<a href="#faq">FAQ</a>\n'
SITE_HTML += '<div class="nav-sep"></div>\n'
SITE_HTML += '<a href="/login">Dashboard</a>\n'
SITE_HTML += '</nav>\n'

SITE_HTML += '<div class="wrap">\n'

SITE_HTML += '<section id="features" class="sec">\n'
SITE_HTML += '<div class="reveal"><div class="sec-tag">About</div>\n'
SITE_HTML += '<h2 class="sec-title"><span class="g">What is unkk client?</span></h2>\n'
SITE_HTML += '<p class="sec-desc">A Fabric-based client that bundles essential client-side mods into a single download for Minecraft ' + MC_VER + '.</p></div>\n'
SITE_HTML += '<div class="fgrid">\n'
features = [
    ("&#x1F3AE;", "Bundled Mods", "Client-side mods come pre-installed. No hunting for individual mods or version compatibility issues."),
    ("&#x2699;&#xFE0F;", "Configurable", "Adjust settings and mod configs to match your playstyle. Tweak performance, visuals, and features."),
    ("&#x1F680;", "Fabric Powered", "Built on Fabric for fast load times, broad mod compatibility, and an active community."),
    ("&#x1F512;", "Vanilla Servers", "Join vanilla and multiplayer servers without issues. Client-side only, no server changes needed."),
    ("&#x1F4E6;", "All-in-One", "Everything you need in one jar. Drop it into your mods folder with Fabric API and you're set."),
    ("&#x1F310;", "Multiplayer", "Full multiplayer support. Connect to any server running Minecraft " + MC_VER + " with Fabric."),
]
for i, (ico, title, desc) in enumerate(features):
    cls = "reveal"
    if i % 3 == 1: cls += " rd1"
    elif i % 3 == 2: cls += " rd2"
    SITE_HTML += '<div class="fcard ' + cls + '"><span class="ico">' + ico + '</span><h3>' + title + '</h3><p>' + desc + '</p></div>\n'
SITE_HTML += '</div></section>\n'

SITE_HTML += '<section id="screenshots" class="sec">\n'
SITE_HTML += '<div class="reveal"><div class="sec-tag">Gallery</div>\n'
SITE_HTML += '<h2 class="sec-title"><span class="g">Screenshots</span></h2>\n'
SITE_HTML += '<p class="sec-desc">See what unkk client looks like in action.</p></div>\n'
SITE_HTML += '<div class="sgrid" id="sgrid"><p style="color:var(--tm)">Loading screenshots...</p></div>\n'
SITE_HTML += '</section>\n'

SITE_HTML += '<section id="download" class="sec">\n'
SITE_HTML += '<div class="dl-section">\n'
SITE_HTML += '<div class="sec-tag">Get Started</div>\n'
SITE_HTML += '<h2 class="sec-title"><span class="g">Download unkk client</span></h2>\n'
SITE_HTML += '<p class="sec-desc" style="max-width:480px;margin-left:auto;margin-right:auto">Install Fabric ' + MC_VER + ', drop both jars into your mods folder, and launch.</p>\n'
SITE_HTML += '<div class="dl-btns">\n'
SITE_HTML += '<a href="' + CLIENT_URL + '" class="dl-btn">&#x2B07; Download Client</a>\n'
SITE_HTML += '<a href="' + FABRIC_API_URL + '" class="dl-sub">&#x2B07; Fabric API</a>\n'
SITE_HTML += '</div>\n'
SITE_HTML += '<div class="dl-info"><span>&#x1F4C1; Client ' + CLIENT_VER + '</span><span>&#x1F4C1; Fabric API 0.156.0</span><span>&#x1F4BB; Minecraft ' + MC_VER + '</span></div>\n'
SITE_HTML += '</div></section>\n'

SITE_HTML += '<section id="faq" class="sec">\n'
SITE_HTML += '<div class="reveal"><div class="sec-tag">Help</div>\n'
SITE_HTML += '<h2 class="sec-title"><span class="g">FAQ</span></h2></div>\n'
faq = [
    ("What Minecraft version is this?", "unkk client targets Minecraft <strong>" + MC_VER + "</strong> and requires the Fabric mod loader."),
    ("How do I install it?", "Install Fabric for Minecraft " + MC_VER + " using the Fabric installer, then place both the unkk client jar and Fabric API jar into your <code>.minecraft/mods</code> folder."),
    ("Do I need Fabric API?", "Yes. The Fabric API jar is required for most Fabric mods. Both jars are provided in the download section above."),
    ("Will this work on multiplayer servers?", "Yes. unkk client is entirely client-side. Join any server running Minecraft " + MC_VER + " without issues."),
    ("Is this official?", "No. unkk client is an independent fan project, not affiliated with Mojang or Microsoft."),
]
for i, (q, a) in enumerate(faq):
    cls = "reveal"
    if i % 2 == 1: cls += " rd1"
    SITE_HTML += '<div class="faq-item ' + cls + '"><h3>' + q + '</h3><p>' + a + '</p></div>\n'
SITE_HTML += '</section>\n'

SITE_HTML += '</div>\n'
SITE_HTML += '<footer class="footer"><p>unkk client &mdash; Independent fan project. Not affiliated with Mojang or Microsoft.</p>\n'
SITE_HTML += '<p style="margin-top:6px">Fabric mod loader &middot; Minecraft ' + MC_VER + '</p></footer>\n'
SITE_HTML += '<script>' + JS + '</script>\n'
SITE_HTML += "<script>\n"
SITE_HTML += "fetch('/api/screenshots').then(function(r){return r.json()}).then(function(imgs){\n"
SITE_HTML += "var g=document.getElementById('sgrid');\n"
SITE_HTML += "if(!imgs||!imgs.length){g.innerHTML='<p style=\"color:var(--tm)\">No screenshots yet. Add images to <code>screenshots/</code> in the GitHub repo.</p>';return}\n"
SITE_HTML += "g.innerHTML='';imgs.forEach(function(img,i){\n"
SITE_HTML += "var c=document.createElement('div');c.className='scard reveal vis';\n"
SITE_HTML += "c.style.animationDelay=(i*.1)+'s';\n"
SITE_HTML += "c.innerHTML='<img src=\"'+img.url+'\" alt=\"'+img.name+'\" loading=\"lazy\" onerror=\"this.parentElement.style.display=none\"><div class=\"cap\">'+img.name+'</div>';\n"
SITE_HTML += "g.appendChild(c)})\n"
SITE_HTML += ".catch(function(){document.getElementById('sgrid').innerHTML='<p style=\"color:var(--tm)\">Could not load screenshots.</p>'});\n"
SITE_HTML += "</script>\n</body>\n</html>\n"

def build_main_page():
    return SITE_HTML.replace(DESC_PLACEHOLDER, RELEASE_NAME + " - A Fabric-based Minecraft " + MC_VER + " client").replace(TITLE_PLACEHOLDER, RELEASE_NAME + " | unkk client")

@app.route("/")
def home():
    return build_main_page()

@app.route("/api/screenshots")
def api_screenshots():
    return fetch_screenshots_from_github()

def make_login_page(error_msg=""):
    err_html = '<div class="auth-err">' + error_msg + '</div>' if error_msg else ""
    return '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Login | unkk client</title><style>' + CSS + '</style></head><body>' \
        + '<div class="bg-grid"></div><div class="bg-glow bg-glow-1"></div><div class="bg-glow bg-glow-2"></div><canvas id="particles"></canvas>' \
        + '<div class="auth-box"><h2>Owner Login</h2>' + err_html \
        + '<form method="POST"><label>Username</label><input name="username" required autocomplete="username">' \
        + '<label>Password</label><input type="password" name="password" required autocomplete="current-password">' \
        + '<button class="btn" type="submit">Sign In</button></form>' \
        + '<p style="text-align:center;margin-top:18px"><a href="/" style="color:var(--tm);font-size:.82em">&larr; Back to site</a></p></div>' \
        + '<script>' + JS + '</script></body></html>'

@app.route("/login", methods=["GET","POST"])
def login_page():
    if request.method == "POST":
        user = request.form.get("username","")
        pw = request.form.get("password","")
        if user == OWNER_USERNAME and pw == OWNER_PASSWORD:
            session["logged_in"] = True
            session["username"] = user
            return redirect(url_for("dashboard"))
        return Response(make_login_page("Invalid username or password"), content_type="text/html")
    return Response(make_login_page(), content_type="text/html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/dashboard")
@require_login
def dashboard():
    up = int(time.time() - APP_START_TIME)
    uptime_str = str(up // 3600) + "h " + str((up % 3600) // 60) + "m" if up >= 3600 else str(up) + "s"
    return Response('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dashboard | unkk client</title><style>' + CSS + '</style></head><body>' \
        + '<div class="bg-grid"></div><div class="bg-glow bg-glow-1"></div><div class="bg-glow bg-glow-2"></div><canvas id="particles"></canvas>' \
        + '<nav><a href="/">Home</a><a href="/dashboard" class="active">Dashboard</a><a href="/edit-links">Edit Links</a><div class="nav-sep"></div><a href="/logout" style="color:#ef4444">Logout</a></nav>' \
        + '<div class="wrap" style="padding-top:60px">' \
        + '<div class="sec-tag">Admin</div><h1 class="sec-title" style="margin-bottom:40px"><span class="g">Welcome, ' + session.get("username","admin") + '</span></h1>' \
        + '<div class="dgrid">' \
        + '<div class="dcard"><h3>Downloads</h3><div class="num">' + str(DOWNLOAD_COUNT) + '</div></div>' \
        + '<div class="dcard"><h3>Uptime</h3><div class="num">' + uptime_str + '</div></div>' \
        + '<div class="dcard"><h3>Status</h3><div class="num" style="background:linear-gradient(135deg,#22c55e,#16a34a);-webkit-background-clip:text;-webkit-text-fill-color:transparent">Online</div></div>' \
        + '<div class="dcard"><h3>Minecraft</h3><div class="num">' + MC_VER + '</div></div>' \
        + '</div>' \
        + '<h2 class="sec-title" style="margin-top:56px;margin-bottom:24px"><span class="g">Quick Actions</span></h2>' \
        + '<div style="display:flex;gap:10px;flex-wrap:wrap">' \
        + '<a href="/edit-links" class="nlink">&#x270F;&#xFE0F; Edit Links</a>' \
        + '<a href="/" class="nlink">&#x1F3E0; View Site</a>' \
        + '</div>' \
        + '<h2 class="sec-title" style="margin-top:56px;margin-bottom:24px"><span class="g">Server Info</span></h2>' \
        + '<div class="fcard" style="max-width:500px">' \
        + '<p style="color:var(--td);margin-bottom:8px"><strong style="color:var(--t)">Client:</strong> ' + CLIENT_VER + '</p>' \
        + '<p style="color:var(--td);margin-bottom:8px"><strong style="color:var(--t)">Minecraft:</strong> ' + MC_VER + '</p>' \
        + '<p style="color:var(--td);margin-bottom:8px"><strong style="color:var(--t)">Python:</strong> ' + os.environ.get("PYTHON_VERSION","3.14.3") + '</p>' \
        + '<p style="color:var(--td);margin-bottom:8px"><strong style="color:var(--t)">Platform:</strong> ' + os.environ.get("DYNO","local") + '</p>' \
        + '<p style="color:var(--td)"><strong style="color:var(--t)">Owner:</strong> ' + OWNER_USERNAME + '</p>' \
        + '</div></div>' \
        + '<script>' + JS + '</script></body></html>', content_type="text/html")

@app.route("/edit-links", methods=["GET","POST"])
@require_login
def edit_links():
    if request.method == "POST":
        global CLIENT_URL, FABRIC_API_URL
        nc = request.form.get("client_url","").strip()
        nf = request.form.get("fabric_url","").strip()
        if nc: CLIENT_URL = nc
        if nf: FABRIC_API_URL = nf
        return redirect(url_for("edit_links"))
    return Response('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Edit Links | unkk client</title><style>' + CSS + '</style></head><body>' \
        + '<div class="bg-grid"></div><div class="bg-glow bg-glow-1"></div><div class="bg-glow bg-glow-2"></div><canvas id="particles"></canvas>' \
        + '<nav><a href="/">Home</a><a href="/dashboard">Dashboard</a><a href="/edit-links" class="active">Edit Links</a><div class="nav-sep"></div><a href="/logout" style="color:#ef4444">Logout</a></nav>' \
        + '<div class="wrap" style="padding-top:60px"><div class="sec-tag">Admin</div>' \
        + '<h1 class="sec-title" style="margin-bottom:40px"><span class="g">Edit Download Links</span></h1>' \
        + '<div class="edit-sec">' \
        + '<div class="egroup"><label>Client JAR URL</label><input type="url" name="client_url" value="' + CLIENT_URL.replace('"','&quot;') + '" form="lf"></div>' \
        + '<div class="egroup"><label>Fabric API JAR URL</label><input type="url" name="fabric_url" value="' + FABRIC_API_URL.replace('"','&quot;') + '" form="lf"></div>' \
        + '<form id="lf" method="POST" style="margin-top:24px"><button type="submit" class="dl-btn" style="font-size:.95em;padding:14px 40px">&#x2714; Save Changes</button></form>' \
        + '<h2 class="sec-title" style="margin-top:56px;margin-bottom:24px"><span class="g">Current Links</span></h2>' \
        + '<ul class="llist">' \
        + '<li><span><strong style="color:var(--t)">Client:</strong> ' + CLIENT_URL + '</span></li>' \
        + '<li><span><strong style="color:var(--t)">Fabric API:</strong> ' + FABRIC_API_URL + '</span></li>' \
        + '</ul></div></div>' \
        + '<script>' + JS + '</script></body></html>', content_type="text/html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

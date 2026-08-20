import os
import time
import json
import threading
import urllib.request
from flask import Flask, redirect, Response

app = Flask(__name__)

CLIENT_URL = "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/unkk-62.0.0.20260820.085414.jar"
FABRIC_API_URL = "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/fabric-api-0.156.0+26.2.jar"

DOWNLOAD_COUNT = 147
APP_START_TIME = time.time()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>unkk client</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --ink:#0c0c10;--paper:#f0ede8;--muted:#8a877e;
  --accent:#a855f7;--accent2:#6366f1;--green:#22c55e;
  --card:#16161c;--card-border:#2a2a35;
  --font:'Space Grotesk',system-ui,sans-serif;
  --mono:'JetBrains Mono',monospace;
}
html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--ink);color:var(--paper);overflow-x:hidden}

/*--- noise overlay ---*/
body::before{content:'';position:fixed;inset:0;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events:none;z-index:9999;opacity:0.5}

/*--- nav ---*/
.topnav{position:fixed;top:0;left:0;right:0;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:18px 40px;
  background:rgba(12,12,16,0.8);backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(255,255,255,0.04);
  transition:transform 0.3s}
.topnav.hide{transform:translateY(-100%)}
.nav-logo{font-weight:700;font-size:1.1rem;letter-spacing:-0.5px}
.nav-logo span{color:var(--accent)}
.nav-links{display:flex;gap:8px;align-items:center}
.nav-links a,.nav-links button{
  font-family:var(--font);font-size:0.82rem;font-weight:500;
  color:var(--muted);text-decoration:none;
  padding:8px 16px;border-radius:8px;border:none;background:none;
  cursor:pointer;transition:all 0.2s}
.nav-links a:hover,.nav-links button:hover{color:var(--paper);background:rgba(255,255,255,0.05)}
.nav-dl-btn{background:var(--accent)!important;color:#fff!important;font-weight:600!important}
.nav-dl-btn:hover{background:#9333ea!important}

/*--- sections ---*/
section{padding:120px 40px 80px;max-width:1100px;margin:0 auto}
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;position:relative;padding-top:80px}
.hero-tag{display:inline-flex;align-items:center;gap:8px;
  font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;
  color:var(--accent);margin-bottom:24px;opacity:0;animation:fadeUp 0.8s 0.2s forwards}
.hero-tag::before{content:'';width:24px;height:1px;background:var(--accent)}
.hero h1{font-size:clamp(3.5rem,9vw,7rem);font-weight:700;letter-spacing:-3px;line-height:0.95;margin-bottom:28px;
  opacity:0;animation:fadeUp 0.8s 0.4s forwards}
.hero h1 em{font-style:normal;color:var(--accent);position:relative}
.hero-desc{font-size:1.05rem;color:var(--muted);line-height:1.7;max-width:460px;margin-bottom:40px;
  opacity:0;animation:fadeUp 0.8s 0.6s forwards}
.hero-actions{display:flex;gap:14px;flex-wrap:wrap;
  opacity:0;animation:fadeUp 0.8s 0.8s forwards}

.btn-main{display:inline-flex;align-items:center;gap:10px;
  padding:14px 28px;border-radius:10px;font-family:var(--font);
  font-size:0.9rem;font-weight:600;text-decoration:none;border:none;cursor:pointer;
  transition:all 0.25s;background:var(--accent);color:#fff}
.btn-main:hover{background:#9333ea;transform:translateY(-2px);box-shadow:0 8px 30px rgba(168,85,247,0.3)}
.btn-main svg{width:18px;height:18px}
.btn-outline{background:none;border:1px solid var(--card-border);color:var(--paper)}
.btn-outline:hover{border-color:var(--muted);background:rgba(255,255,255,0.03)}

.hero-stats{display:flex;gap:40px;margin-top:60px;
  opacity:0;animation:fadeUp 0.8s 1s forwards}
.stat-block .num{font-size:1.8rem;font-weight:700;font-family:var(--mono);color:var(--paper)}
.stat-block .label{font-size:0.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-top:4px}

/*--- marquee ---*/
.marquee-wrap{overflow:hidden;padding:30px 0;border-top:1px solid rgba(255,255,255,0.04);border-bottom:1px solid rgba(255,255,255,0.04);margin:0}
.marquee{display:flex;gap:60px;animation:scroll 20s linear infinite;white-space:nowrap;width:max-content}
.marquee span{font-size:0.8rem;font-weight:600;text-transform:uppercase;letter-spacing:3px;color:rgba(255,255,255,0.08)}
@keyframes scroll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}

/*--- tabs ---*/
.tab-bar{display:flex;gap:4px;margin-bottom:40px;background:var(--card);border-radius:12px;padding:5px;width:fit-content}
.tab-btn{font-family:var(--font);font-size:0.82rem;font-weight:500;padding:10px 22px;border:none;
  border-radius:8px;background:none;color:var(--muted);cursor:pointer;transition:all 0.25s}
.tab-btn.active{background:var(--accent);color:#fff}
.tab-btn:hover:not(.active){color:var(--paper);background:rgba(255,255,255,0.04)}
.tab-content{display:none;animation:fadeUp 0.5s forwards}
.tab-content.active{display:block}

/*--- showcase grid ---*/
.showcase-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}
.showcase-item{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:16/10;
  background:var(--card);border:1px solid var(--card-border);cursor:pointer;
  transition:all 0.4s cubic-bezier(0.16,1,0.3,1)}
.showcase-item:hover{transform:scale(1.02);border-color:var(--accent);box-shadow:0 20px 60px rgba(0,0,0,0.5)}
.showcase-item img{width:100%;height:100%;object-fit:cover;display:block}
.showcase-item .overlay{position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,0.7) 0%,transparent 50%);
  display:flex;align-items:flex-end;padding:20px;opacity:0;transition:opacity 0.3s}
.showcase-item:hover .overlay{opacity:1}
.showcase-item .overlay span{font-size:0.85rem;font-weight:600}
.showcase-placeholder{width:100%;height:100%;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#1a1a2e,#16162a);color:var(--muted);font-size:0.8rem;text-align:center;
  padding:20px;flex-direction:column;gap:8px}
.showcase-placeholder .ph-icon{font-size:2rem;opacity:0.3}

/*--- features ---*/
.feature-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.feature-card{background:var(--card);border:1px solid var(--card-border);border-radius:14px;padding:28px;
  transition:all 0.3s;position:relative;overflow:hidden}
.feature-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--accent),transparent);opacity:0;transition:opacity 0.3s}
.feature-card:hover::before{opacity:1}
.feature-card:hover{border-color:rgba(168,85,247,0.2);transform:translateY(-3px)}
.feature-card .f-icon{font-size:1.5rem;margin-bottom:16px}
.feature-card h4{font-size:0.95rem;font-weight:600;margin-bottom:8px}
.feature-card p{font-size:0.82rem;color:var(--muted);line-height:1.6}

/*--- changelog ---*/
.cl-item{display:flex;gap:24px;padding:24px 0;border-bottom:1px solid rgba(255,255,255,0.04)}
.cl-item:last-child{border-bottom:none}
.cl-version{font-family:var(--mono);font-size:0.8rem;color:var(--accent);min-width:80px;padding-top:2px}
.cl-body h4{font-size:0.95rem;font-weight:600;margin-bottom:6px}
.cl-body p{font-size:0.82rem;color:var(--muted);line-height:1.6}
.cl-body .cl-date{font-size:0.7rem;color:rgba(255,255,255,0.2);margin-top:8px;font-family:var(--mono)}
.cl-tag{display:inline-block;padding:3px 10px;border-radius:6px;font-size:0.68rem;font-weight:600;
  text-transform:uppercase;letter-spacing:0.5px;margin-right:6px}
.cl-tag.new{background:rgba(34,197,94,0.1);color:var(--green);border:1px solid rgba(34,197,94,0.2)}
.cl-tag.fix{background:rgba(250,204,21,0.1);color:#facc15;border:1px solid rgba(250,204,21,0.2)}
.cl-tag.perf{background:rgba(99,102,241,0.1);color:var(--accent2);border:1px solid rgba(99,102,241,0.2)}

/*--- install steps ---*/
.install-flow{display:flex;gap:16px;flex-wrap:wrap}
.install-step{flex:1;min-width:180px;background:var(--card);border:1px solid var(--card-border);
  border-radius:14px;padding:24px;position:relative}
.install-step .step-n{font-family:var(--mono);font-size:0.7rem;color:var(--accent);
  letter-spacing:1px;margin-bottom:12px}
.install-step h4{font-size:0.9rem;font-weight:600;margin-bottom:6px}
.install-step p{font-size:0.78rem;color:var(--muted);line-height:1.5}
.install-step code{font-family:var(--mono);font-size:0.75rem;background:rgba(168,85,247,0.1);
  color:var(--accent);padding:3px 8px;border-radius:5px}

/*--- footer ---*/
.site-footer{padding:60px 40px;border-top:1px solid rgba(255,255,255,0.04);
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:20px}
.footer-left{font-size:0.78rem;color:var(--muted)}
.footer-links{display:flex;gap:20px}
.footer-links a{font-size:0.78rem;color:var(--muted);text-decoration:none;transition:color 0.2s}
.footer-links a:hover{color:var(--paper)}

/*--- scroll reveal ---*/
.reveal{opacity:0;transform:translateY(30px);transition:all 0.7s cubic-bezier(0.16,1,0.3,1)}
.reveal.visible{opacity:1;transform:translateY(0)}

/*--- keyframes ---*/
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

/*--- lightbox ---*/
.lightbox{position:fixed;inset:0;background:rgba(0,0,0,0.9);z-index:10000;display:none;
  align-items:center;justify-content:center;backdrop-filter:blur(10px);cursor:pointer}
.lightbox.open{display:flex}
.lightbox img{max-width:90%;max-height:85vh;border-radius:12px;box-shadow:0 20px 80px rgba(0,0,0,0.5)}
.lightbox-close{position:absolute;top:24px;right:24px;width:40px;height:40px;border-radius:50%;
  background:rgba(255,255,255,0.1);border:none;color:#fff;font-size:1.2rem;cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:background 0.2s}
.lightbox-close:hover{background:rgba(255,255,255,0.2)}

/*--- mobile ---*/
@media(max-width:768px){
  section{padding:100px 20px 60px}
  .topnav{padding:14px 20px}
  .nav-links a:not(.nav-dl-btn){display:none}
  .feature-grid{grid-template-columns:1fr}
  .install-flow{flex-direction:column}
  .hero-stats{gap:24px}
  .tab-bar{overflow-x:auto;width:100%}
  .site-footer{flex-direction:column;text-align:center}
}

/*--- cursor trail ---*/
.trail{position:fixed;width:8px;height:8px;border-radius:50%;background:var(--accent);
  pointer-events:none;z-index:9998;opacity:0;transition:opacity 0.3s;mix-blend-mode:screen}
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
    <a class="nav-dl-btn" href="CLIENT_URL">Download</a>
  </div>
</div>

<section class="hero">
  <div class="hero-tag">v62.0.0 stable release</div>
  <h1>unkk<br><em>client</em></h1>
  <p class="hero-desc">A fabric-based minecraft client made for people who actually care about how the game looks and feels. built different.</p>
  <div class="hero-actions">
    <a href="CLIENT_URL" class="btn-main">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      Download Client
    </a>
    <a href="FABRIC_URL" class="btn-main btn-outline">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
      Fabric API
    </a>
  </div>
  <div class="hero-stats">
    <div class="stat-block"><div class="num" id="dl-count">""" + str(DOWNLOAD_COUNT) + """</div><div class="label">Downloads</div></div>
    <div class="stat-block"><div class="num">62.0.0</div><div class="label">Latest Version</div></div>
    <div class="stat-block"><div class="num">1.21+</div><div class="label">Fabric</div></div>
  </div>
</section>

<div class="marquee-wrap"><div class="marquee"><span>unkk client</span><span>optimized</span><span>fabric</span><span>customizable</span><span>open source</span><span>fast</span><span>smooth</span><span>lightweight</span><span>unkk client</span><span>optimized</span><span>fabric</span><span>customizable</span><span>open source</span><span>fast</span><span>smooth</span><span>lightweight</span></div></div>

<section id="showcase">
  <div class="reveal">
    <div style="font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:12px">// screenshots</div>
    <h2 style="font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px">See it in action</h2>
  </div>
  <div class="showcase-grid reveal">
    <div class="showcase-item" onclick="openLightbox(this)">
      <!-- REPLACE: put your screenshot here <img src="screenshot1.jpg" alt="client screenshot"> -->
      <div class="showcase-placeholder"><div class="ph-icon">&#127912;</div>Click to add screenshot<br><code style="font-family:var(--mono);font-size:0.7rem;color:var(--accent)">&lt;img src="your-image.jpg"&gt;</code></div>
      <div class="overlay"><span>Main Menu</span></div>
    </div>
    <div class="showcase-item" onclick="openLightbox(this)">
      <!-- REPLACE: put your screenshot here <img src="screenshot2.jpg" alt="client screenshot"> -->
      <div class="showcase-placeholder"><div class="ph-icon">&#9889;</div>Click to add screenshot<br><code style="font-family:var(--mono);font-size:0.7rem;color:var(--accent)">&lt;img src="your-image.jpg"&gt;</code></div>
      <div class="overlay"><span>In-Game HUD</span></div>
    </div>
    <div class="showcase-item" onclick="openLightbox(this)">
      <!-- REPLACE: put your screenshot here <img src="screenshot3.jpg" alt="client screenshot"> -->
      <div class="showcase-placeholder"><div class="ph-icon">&#127744;</div>Click to add screenshot<br><code style="font-family:var(--mono);font-size:0.7rem;color:var(--accent)">&lt;img src="your-image.jpg"&gt;</code></div>
      <div class="overlay"><span>Settings Panel</span></div>
    </div>
    <div class="showcase-item" onclick="openLightbox(this)">
      <!-- REPLACE: put your screenshot here <img src="screenshot4.jpg" alt="client screenshot"> -->
      <div class="showcase-placeholder"><div class="ph-icon">&#128187;</div>Click to add screenshot<br><code style="font-family:var(--mono);font-size:0.7rem;color:var(--accent)">&lt;img src="your-image.jpg"&gt;</code></div>
      <div class="overlay"><span>Mod Menu</span></div>
    </div>
  </div>
</section>

<section id="features">
  <div class="reveal">
    <div style="font-family:var(--mono);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:12px">// what you get</div>
    <h2 style="font-size:2rem;font-weight:700;letter-spacing:-1px;margin-bottom:40px">Features</h2>
  </div>

  <div class="tab-bar reveal">
    <button class="tab-btn active" onclick="switchTab(this,'tab-general')">General</button>
    <button class="tab-btn" onclick="switchTab(this,'tab-perf')">Performance</button>
    <button class="tab-btn" onclick="switchTab(this,'tab-visual')">Visuals</button>
  </div>

  <div class="tab-content active" id="tab-general">
    <div class="feature-grid">
      <div class="feature-card reveal"><div class="f-icon">&#128295;</div><h4>Mod Support</h4><p>Full fabric mod API support. Works with your favorite mods out of the box.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127912;</div><h4>Custom HUD</h4><p>Redesigned HUD elements. Clean, minimal, and actually readable.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#9881;</div><h4>Settings</h4><p>Deep customization without the bloat. Every setting where you expect it.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128274;</div><h4>Anti-Cheat Friendly</h4><p>Legit client. No shady modules. Just a better Minecraft experience.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128640;</div><h4>Quick Launch</h4><p>Faster startup than vanilla. Less waiting, more playing.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127760;</div><h4>Multiplayer</h4><p>Works on any server. Hypixel, private, or your own.</p></div>
    </div>
  </div>

  <div class="tab-content" id="tab-perf">
    <div class="feature-grid">
      <div class="feature-card reveal"><div class="f-icon">&#9889;</div><h4>FPS Boost</h4><p>Optimized rendering pipeline. Expect noticeably higher framerates.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128187;</div><h4>Low RAM</h4><p>Reduced memory footprint. Runs on weaker machines without issues.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128200;</div><h4>Chunk Loading</h4><p>Smarter chunk loading. Less stuttering when flying or exploring.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#127777;</div><h4>Entity Culling</h4><p>Skips rendering entities you can't see. Pure performance gain.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#9881;</div><h4>Thread Optimization</h4><p>Better CPU utilization across all cores.</p></div>
      <div class="feature-card reveal"><div class="f-icon">&#128230;</div><h4>Lightweight</h4><p>Small jar size. No bloatware. Just what you need.</p></div>
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
    <div class="cl-item">
      <div class="cl-version">v62.0.0</div>
      <div class="cl-body">
        <h4><span class="cl-tag new">new</span> Major Client Release</h4>
        <p>Full rewrite of the rendering pipeline. New HUD system, improved chunk loading, and custom shader support added.</p>
        <div class="cl-date">aug 20 2026</div>
      </div>
    </div>
    <div class="cl-item">
      <div class="cl-version">v61.3.2</div>
      <div class="cl-body">
        <h4><span class="cl-tag fix">fix</span> Fabric Compatibility</h4>
        <p>Fixed crash on startup with fabric-api 0.156.0. Resolved mod loader conflict with Sodium.</p>
        <div class="cl-date">aug 12 2026</div>
      </div>
    </div>
    <div class="cl-item">
      <div class="cl-version">v61.3.0</div>
      <div class="cl-body">
        <h4><span class="cl-tag perf">perf</span> Performance Update</h4>
        <p>Entity culling improvements, reduced memory usage by 15%, faster chunk rendering on AMD GPUs.</p>
        <div class="cl-date">aug 01 2026</div>
      </div>
    </div>
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

<div class="marquee-wrap" style="margin-top:40px"><div class="marquee" style="animation-direction:reverse;animation-duration:25s"><span>download now</span><span>free</span><span>open source</span><span>no ads</span><span>no malware</span><span>just a good client</span><span>download now</span><span>free</span><span>open source</span><span>no ads</span><span>no malware</span><span>just a good client</span></div></div>

<footer class="site-footer">
  <div class="footer-left">unkk client &mdash; not affiliated with mojang or microsoft</div>
  <div class="footer-links">
    <a href="CLIENT_URL">Download</a>
    <a href="https://github.com/awdawdfawdAWD/MC-CLIENT" target="_blank">GitHub</a>
  </div>
</footer>

<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <button class="lightbox-close">&times;</button>
  <img id="lightbox-img" src="" alt="screenshot">
</div>

<script>
/*--- tab switching ---*/
function switchTab(btn, tabId) {
  btn.parentElement.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  var tab = document.getElementById(tabId);
  tab.classList.add('active');
  tab.querySelectorAll('.reveal').forEach((el, i) => {
    el.classList.remove('visible');
    setTimeout(() => el.classList.add('visible'), 80 * i);
  });
}

/*--- scroll reveal ---*/
var reveals = document.querySelectorAll('.reveal');
var observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), 60 * i);
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });
reveals.forEach(el => observer.observe(el));

/*--- navbar hide on scroll ---*/
var lastScroll = 0;
var nav = document.getElementById('topnav');
window.addEventListener('scroll', () => {
  var cur = window.scrollY;
  if (cur > lastScroll && cur > 200) nav.classList.add('hide');
  else nav.classList.remove('hide');
  lastScroll = cur;
});

/*--- lightbox ---*/
function openLightbox(el) {
  var img = el.querySelector('img');
  if (!img) return;
  document.getElementById('lightbox-img').src = img.src;
  document.getElementById('lightbox').classList.add('open');
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
}

/*--- cursor trail ---*/
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
document.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
function animTrail() {
  trails.forEach((t, i) => {
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

/*--- download counter ---*/
var dlEl = document.getElementById('dl-count');
var dlTarget = """ + str(DOWNLOAD_COUNT) + """;
function animateCount(el, target) {
  var current = 0;
  var step = Math.ceil(target / 60);
  var timer = setInterval(() => {
    current += step;
    if (current >= target) { current = target; clearInterval(timer); }
    el.innerText = current;
  }, 16);
}
var dlObs = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) { animateCount(dlEl, dlTarget); dlObs.disconnect(); }
}, { threshold: 0.5 });
dlObs.observe(dlEl);
</script>
</body>
</html>"""


@app.route("/")
def home_redirect():
    page = HTML.replace("CLIENT_URL", CLIENT_URL).replace("FABRIC_URL", FABRIC_API_URL)
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

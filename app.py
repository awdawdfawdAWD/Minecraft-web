import os
import time
import threading
import urllib.request
from flask import Flask, redirect, Response

app = Flask(__name__)

CLIENT_URL = "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/unkk-62.0.0.20260820.085414.jar"
FABRIC_API_URL = "https://github.com/awdawdfawdAWD/MC-CLIENT/releases/download/CLient/fabric-api-0.156.0+26.2.jar"

APP_START_TIME = time.time()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>unkk - Minecraft Client</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --bg: #0a0a0f;
            --surface: #12121a;
            --border: #1e1e2e;
            --text: #e4e4ef;
            --text-dim: #8888a0;
            --accent: #7c5cfc;
            --accent-glow: #7c5cfc44;
            --green: #22c55e;
            --green-glow: #22c55e33;
        }
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
        }
        .bg-grid {
            position: fixed; inset: 0;
            background-image:
                linear-gradient(var(--border) 1px, transparent 1px),
                linear-gradient(90deg, var(--border) 1px, transparent 1px);
            background-size: 60px 60px;
            opacity: 0.3; pointer-events: none; z-index: 0;
        }
        .bg-glow {
            position: fixed; width: 600px; height: 600px; border-radius: 50%;
            filter: blur(150px); opacity: 0.15; pointer-events: none; z-index: 0;
        }
        .bg-glow-1 { top: -200px; left: 50%; transform: translateX(-50%); background: var(--accent); }
        .bg-glow-2 { bottom: -200px; right: -100px; background: #22c55e; }
        .container { position: relative; z-index: 1; max-width: 900px; margin: 0 auto; padding: 60px 24px 80px; }
        nav { display: flex; align-items: center; justify-content: space-between; margin-bottom: 100px; }
        .logo { font-size: 1.5rem; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(135deg, var(--accent), #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .nav-badge { font-size: 0.75rem; font-weight: 500; color: var(--green); background: var(--green-glow); border: 1px solid #22c55e44; padding: 6px 14px; border-radius: 999px; }
        .status-badge { display: inline-flex; align-items: center; gap: 8px; font-size: 0.75rem; font-weight: 600; color: var(--green); padding: 6px 14px; border-radius: 999px; }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); box-shadow: 0 0 8px var(--green); animation: pulse-dot 2s infinite; }
        @keyframes pulse-dot { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
        .hero { text-align: center; margin-bottom: 80px; }
        .hero-tag { display: inline-flex; align-items: center; gap: 8px; font-size: 0.8rem; font-weight: 500; color: var(--accent); background: var(--accent-glow); border: 1px solid #7c5cfc33; padding: 6px 16px; border-radius: 999px; margin-bottom: 28px; }
        .hero-tag .dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); }
        .hero h1 { font-size: clamp(3rem, 8vw, 5.5rem); font-weight: 900; letter-spacing: -2px; line-height: 1.05; margin-bottom: 20px; }
        .hero h1 span { background: linear-gradient(135deg, var(--accent), #c084fc, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { font-size: 1.15rem; color: var(--text-dim); max-width: 520px; margin: 0 auto; line-height: 1.7; }
        .downloads { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 60px; }
        .card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 32px; display: flex; flex-direction: column; transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s; }
        .card:hover { border-color: #7c5cfc55; box-shadow: 0 0 40px var(--accent-glow); transform: translateY(-2px); }
        .card-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; margin-bottom: 20px; }
        .card-icon.purple { background: var(--accent-glow); border: 1px solid #7c5cfc33; }
        .card-icon.green { background: var(--green-glow); border: 1px solid #22c55e33; }
        .card h3 { font-size: 1.15rem; font-weight: 700; margin-bottom: 8px; }
        .card .version { font-size: 0.78rem; color: var(--text-dim); margin-bottom: 12px; }
        .card .desc { font-size: 0.88rem; color: var(--text-dim); line-height: 1.6; margin-bottom: 24px; flex: 1; }
        .btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 12px 24px; border-radius: 10px; font-family: inherit; font-size: 0.88rem; font-weight: 600; text-decoration: none; border: none; cursor: pointer; transition: all 0.2s; }
        .btn-primary { background: var(--accent); color: #fff; }
        .btn-primary:hover { background: #6a4ce0; box-shadow: 0 0 24px var(--accent-glow); }
        .btn-secondary { background: transparent; color: var(--text); border: 1px solid var(--border); }
        .btn-secondary:hover { border-color: #7c5cfc55; background: #ffffff08; }
        .btn svg { width: 16px; height: 16px; }
        .features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 60px; }
        .feature { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; text-align: center; }
        .feature .icon { font-size: 1.6rem; margin-bottom: 12px; }
        .feature h4 { font-size: 0.9rem; font-weight: 600; margin-bottom: 6px; }
        .feature p { font-size: 0.78rem; color: var(--text-dim); line-height: 1.5; }
        .install-section { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 36px; }
        .install-section h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; }
        .steps { display: flex; flex-direction: column; gap: 14px; }
        .step { display: flex; align-items: flex-start; gap: 14px; font-size: 0.88rem; color: var(--text-dim); line-height: 1.6; }
        .step-num { min-width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; background: var(--accent-glow); border: 1px solid #7c5cfc33; color: var(--accent); border-radius: 8px; font-size: 0.75rem; font-weight: 700; margin-top: 1px; }
        .step code { background: #ffffff0a; border: 1px solid var(--border); padding: 2px 8px; border-radius: 6px; font-size: 0.82rem; color: var(--text); }
        .top-bar { background: var(--surface); border-bottom: 1px solid var(--border); padding: 14px 40px; display: flex; gap: 40px; align-items: center; position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px); }
        .metric { font-size: 11px; color: var(--text-dim); text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
        .metric span { display: block; font-size: 14px; color: #fff; font-weight: 700; margin-top: 3px; font-family: monospace; }
        footer { text-align: center; margin-top: 60px; padding-top: 32px; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.8rem; }
        @media (max-width: 640px) {
            .downloads { grid-template-columns: 1fr; }
            .features { grid-template-columns: 1fr; }
            .top-bar { padding: 14px 20px; gap: 20px; flex-wrap: wrap; }
            nav { margin-bottom: 60px; }
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="bg-glow bg-glow-1"></div>
    <div class="bg-glow bg-glow-2"></div>

    <div class="top-bar">
        <div class="metric">Status <span><span class="status-dot" style="display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse-dot 2s infinite;vertical-align:middle;margin-right:6px;"></span>Online</span></div>
        <div class="metric">Version <span>62.0.0</span></div>
        <div class="metric">Uptime <span id="uptime">--</span></div>
        <div class="metric">Platform <span>Java Edition</span></div>
    </div>

    <div class="container">
        <nav>
            <div class="logo">unkk</div>
            <div class="nav-badge">Fabric 1.21+</div>
        </nav>

        <section class="hero">
            <div class="hero-tag"><span class="dot"></span> Now Available</div>
            <h1>unkk<br><span>Minecraft Client</span></h1>
            <p>A custom Minecraft client built for performance and style. Download now and start playing.</p>
        </section>

        <section class="downloads">
            <div class="card">
                <div class="card-icon purple">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                </div>
                <h3>Client JAR</h3>
                <div class="version">unkk-62.0.0 &middot; JAR &middot; """ + "CLIENT_URL" + """</div>
                <div class="desc">The main client file. Drop it into your Minecraft mods folder and launch.</div>
                <a href="CLIENT_URL" class="btn btn-primary">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    Download Client
                </a>
            </div>
            <div class="card">
                <div class="card-icon green">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <h3>Fabric API</h3>
                <div class="version">fabric-api-0.156.0+26.2 &middot; JAR</div>
                <div class="desc">Required dependency for the client. Install this alongside the client JAR.</div>
                <a href="FABRIC_URL" class="btn btn-secondary">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                    Download Fabric API
                </a>
            </div>
        </section>

        <section class="features">
            <div class="feature">
                <div class="icon">&#9889;</div>
                <h4>Optimized</h4>
                <p>Built for maximum FPS and smooth gameplay</p>
            </div>
            <div class="feature">
                <div class="icon">&#127912;</div>
                <h4>Customizable</h4>
                <p>Full HUD and mod customization support</p>
            </div>
            <div class="feature">
                <div class="icon">&#128274;</div>
                <h4>Secure</h4>
                <p>Open source and safe to use</p>
            </div>
        </section>

        <section class="install-section">
            <h3>Installation Guide</h3>
            <div class="steps">
                <div class="step">
                    <div class="step-num">1</div>
                    <div>Download and install <a href="https://fabricmc.net/" style="color:var(--accent);text-decoration:none;">Fabric Loader</a> for your Minecraft version.</div>
                </div>
                <div class="step">
                    <div class="step-num">2</div>
                    <div>Click <strong style="color:var(--text);">Download Client</strong> above and save the JAR file.</div>
                </div>
                <div class="step">
                    <div class="step-num">3</div>
                    <div>Click <strong style="color:var(--text);">Download Fabric API</strong> and save that JAR file too.</div>
                </div>
                <div class="step">
                    <div class="step-num">4</div>
                    <div>Place both JAR files into your <code>.minecraft/mods</code> folder.</div>
                </div>
                <div class="step">
                    <div class="step-num">5</div>
                    <div>Launch Minecraft with the Fabric profile. Done!</div>
                </div>
            </div>
        </section>

        <footer>
            unkk Minecraft Client &middot; Not affiliated with Mojang or Microsoft
        </footer>
    </div>

    <script>
        function formatUptime(seconds) {
            var d = Math.floor(seconds / 86400);
            var h = Math.floor((seconds % 86400) / 3600);
            var m = Math.floor((seconds % 3600) / 60);
            var s = seconds % 60;
            var parts = [];
            if (d) parts.push(d + "d");
            if (h) parts.push(h + "h");
            if (m) parts.push(m + "m");
            parts.push(s + "s");
            return parts.join(" ");
        }

        var startTime = Math.floor(Date.now() / 1000);

        function updateUptime() {
            var now = Math.floor(Date.now() / 1000);
            document.getElementById("uptime").innerText = formatUptime(now - startTime);
        }

        setInterval(updateUptime, 1000);
        updateUptime();
    </script>
</body>
</html>"""


@app.route("/")
def home_redirect():
    page = HTML.replace("CLIENT_URL", CLIENT_URL).replace("FABRIC_URL", FABRIC_API_URL)
    return Response(page, content_type="text/html")


@app.route("/api/download/client")
def download_client():
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
        "formattedUptime": format_uptime(uptime_seconds),
        "client": CLIENT_URL,
        "fabric_api": FABRIC_API_URL
    }


def format_uptime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


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

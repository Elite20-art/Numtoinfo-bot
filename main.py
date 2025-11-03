from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RoyalOfficial OSINT Portal</title>
<style>
:root {
  --bg: #000; --text: #00ff66; --border: #00ff66; --shadow: #00ff66;
}
body { background:var(--bg); color:var(--text); font-family:'Courier New',monospace; text-align:center; margin-top:30px; transition:all .3s }
h1 { color:var(--text); text-shadow:0 0 10px var(--shadow) }
form { background:#0f0f0f; padding:20px; border-radius:12px; box-shadow:0 0 20px var(--shadow); display:inline-block; transition:all .3s }
select, input { background:#000; color:var(--text); border:1px solid var(--border); padding:10px; width:260px; margin:8px; text-align:center; border-radius:6px }
button { background:var(--text); color:#000; border:none; padding:10px 18px; margin:6px; cursor:pointer; font-weight:bold; border-radius:6px }
.output { background:#0f0f0f; margin-top:20px; padding:15px; border-radius:12px; border:2px solid var(--border); box-shadow:0 0 18px var(--shadow); width:90%; max-width:760px; margin-left:auto; margin-right:auto; min-height:150px; white-space:pre-wrap; text-align:left; position:relative; font-size:14px; transition:all .3s }
.error { color:#ff4444 }
.loader { border:4px solid #111; border-top:4px solid var(--text); border-radius:50%; width:34px; height:34px; animation:spin 1s linear infinite; display:none; position:absolute; top:45%; left:50%; transform:translate(-50%,-50%) }
@keyframes spin { 0%{transform:translate(-50%,-50%) rotate(0deg)} 100%{transform:translate(-50%,-50%) rotate(360deg)} }
.footer { color:#888; margin-top:18px; font-size:13px }
.theme-toggle { position:fixed; top:15px; right:20px; background:var(--text); color:#000; border:none; padding:8px 12px; border-radius:20px; font-weight:bold; cursor:pointer; box-shadow:0 0 10px var(--shadow) }
.small-btn { background:var(--text); color:#000; padding:8px 12px; border-radius:6px; border:none; cursor:pointer }
</style>

<script>
let darkMode = false;
function toggleTheme() {
  darkMode = !darkMode;
  if (darkMode) {
    document.documentElement.style.setProperty('--bg', '#0b0b0b');
    document.documentElement.style.setProperty('--text', '#aaaaaa');
    document.documentElement.style.setProperty('--border', '#444');
    document.documentElement.style.setProperty('--shadow', '#222');
    document.getElementById('themeBtn').innerText = '💚 Hacker Mode';
  } else {
    document.documentElement.style.setProperty('--bg', '#000');
    document.documentElement.style.setProperty('--text', '#00ff66');
    document.documentElement.style.setProperty('--border', '#00ff66');
    document.documentElement.style.setProperty('--shadow', '#00ff66');
    document.getElementById('themeBtn').innerText = '⚫ Dark Mode';
  }
}

async function fetchInfo(e){
  e.preventDefault();
  const type = document.getElementById('type').value;
  const term = document.getElementById('term').value.trim();
  const output = document.getElementById('output');
  const loader = document.getElementById('loader');
  const status = document.getElementById('status');
  // ensure UI reset each search
  output.innerHTML = 'Preparing...';
  loader.style.display = 'block';
  status.innerText = 'Fetching... ⏳';
  status.style.color = 'var(--text)';

  if(!term) {
    loader.style.display = 'none';
    output.innerHTML = '<span class="error">❌ Please enter a value.</span>';
    status.innerText = 'Error ❌';
    status.style.color = '#ff4444';
    return;
  }

  try {
    const res = await fetch('/lookup', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({type, term})
    });
    const data = await res.json();
    loader.style.display = 'none';
    if (data.error) {
      output.innerHTML = '<span class="error">❌ ' + data.error + '</span>';
      status.innerText = 'Error ❌';
      status.style.color = '#ff4444';
    } else {
      // show the formatted result (preserve newlines)
      output.innerText = data.result || '(no result)';
      status.innerText = 'Done ✅';
      status.style.color = 'var(--text)';
      // set download filename data attribute for the download button
      document.getElementById('downloadBtn').dataset.filename = data.filename || 'result.txt';
    }
  } catch (err) {
    loader.style.display = 'none';
    output.innerHTML = '<span class="error">❌ ' + err + '</span>';
    status.innerText = 'Error ❌';
    status.style.color = '#ff4444';
  }
}

function clearOutput(){
  document.getElementById('term').value = '';
  document.getElementById('output').innerHTML = 'Result will appear here — info stays in this box only.';
  document.getElementById('status').innerText = 'Idle';
  document.getElementById('status').style.color = '#888';
  // reset download filename
  document.getElementById('downloadBtn').dataset.filename = 'result.txt';
}

function copyOutput(){
  const text = document.getElementById('output').innerText;
  navigator.clipboard.writeText(text).then(()=> alert('Copied to clipboard!'));
}

function downloadOutput(){
  const text = document.getElementById('output').innerText;
  const filename = document.getElementById('downloadBtn').dataset.filename || 'result.txt';
  const blob = new Blob([text], {type:'text/plain'});
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}
</script>
</head>
<body>
  <button id="themeBtn" class="theme-toggle" onclick="toggleTheme()">⚫ Dark Mode</button>
  <h1>RoyalOfficial OSINT Portal</h1>

  <form onsubmit="fetchInfo(event)">
    <select id="type" name="type">
      <option value="mobile">📱 Mobile Info</option>
      <option value="aadhaar">🆔 Aadhaar Info</option>
      <option value="vehicle">🚗 Vehicle Info</option>
      <option value="upi">💳 UPI Info</option>
      <option value="email">✉️ Email Info</option>
      <option value="pan">🧾 PAN Info</option>
    </select><br>
    <input id="term" name="term" type="text" placeholder="Enter value..." required><br>
    <button type="submit">Fetch Info</button>
    <button type="button" onclick="clearOutput()">Clear</button>
  </form>

  <div id="output" class="output"><div id="loader" class="loader"></div>Result will appear here — info stays in this box only.</div>

  <div style="margin-top:12px">
    <button id="copyBtn" class="small-btn" onclick="copyOutput()">Copy</button>
    <button id="downloadBtn" class="small-btn" onclick="downloadOutput()" data-filename="result.txt">Download (.txt)</button>
  </div>

  <div id="status" class="footer">Idle</div>
  <div class="footer">© RoyalOfficial Intelligence Portal</div>
</body>
</html>
"""

# ---------------- BACKEND ---------------- #

@app.route('/')
def home():
    return render_template_string(HTML)

def flatten_and_format(lookup_type, data):
    """
    Convert nested dicts/lists into line-by-line string with emojis and separators.
    """
    emoji_map = {
        "mobile": {"number":"📞","name":"👤","father":"👨‍👦","address":"🏠","alt":"📞","circle":"📍","id":"🆔","email":"📧","success":"✅","carrier":"📡","region":"📍","connection":"🔌","active":"💚","lookup":"🔎"},
        "vehicle":{"rc":"🚘","owner":"👤","registration":"📅","class":"🛻","fuel":"⛽","maker":"🏷️","engine":"⚙️","chassis":"🔩","fitness":"🧾","insurance":"🛡️","registered":"📍","status":"✅"},
        "aadhaar":{"aadhaar":"🆔","name":"👤","dob":"📅","state":"📍","status":"✅"},
        "upi":{"upi":"💳","holder":"👤","bank":"🏦","verified":"✅","created":"📅"},
        "email":{"email":"✉️","valid":"✅","disposable":"🚫","domain":"🌍","created":"📅"},
        "pan":{"pan":"🧾","name":"👤","dob":"📅","ao":"🏦","status":"✅"}
    }
    emap = emoji_map.get(lookup_type, {})
    def best_emoji(key):
        keyl = key.lower().replace("_"," ")
        for kw, em in emap.items():
            if kw in keyl:
                return em
        return "•"

    out_lines = []

    def format_item(item, prefix=None):
        # item can be dict, list or scalar
        if isinstance(item, dict):
            for k, v in item.items():
                if isinstance(v, (dict, list)):
                    # nested: print header then nested content
                    header = f"{best_emoji(k)} {k.replace('_',' ').title()}:"
                    out_lines.append(header)
                    format_item(v, prefix=k)
                else:
                    val = "(not available)" if v in [None, "", "null"] else str(v)
                    out_lines.append(f"{best_emoji(k)} {k.replace('_',' ').title()}: {val}")
        elif isinstance(item, list):
            for idx, element in enumerate(item, start=1):
                # show record header if list of dicts
                if isinstance(element, dict):
                    out_lines.append(f"Record {idx}:")
                    format_item(element, prefix=prefix)
                    # separator between records
                    out_lines.append("────────────────────────────")
                else:
                    out_lines.append(str(element))
        else:
            out_lines.append(str(item))

    format_item(data)
    # remove trailing separator if exists
    if out_lines and out_lines[-1] == "────────────────────────────":
        out_lines = out_lines[:-1]
    return "\n".join(out_lines)

@app.route('/lookup', methods=['POST'])
def lookup():
    req = request.get_json(force=True)
    lookup_type = req.get('type')
    term = req.get('term')
    if not lookup_type or not term:
        return jsonify({"error":"Missing input"}), 400
    try:
        if lookup_type == "vehicle":
            url = f"https://vehicle-info-api-hexabhi.onrender.com/?rc_number={term}"
            r = requests.get(url, timeout=12)
            if r.status_code != 200:
                return jsonify({"error":f"Vehicle API error {r.status_code}"})
            try:
                j = r.json()
                formatted = flatten_and_format("vehicle", j)
                filename = f"vehicle_{term}.txt"
                return jsonify({"result": formatted, "filename": filename})
            except Exception:
                txt = r.text or "(no data)"
                return jsonify({"result": txt, "filename": f"vehicle_{term}.txt"})
        else:
            url = f"https://siwammodz.vercel.app/api?key=Siwam_9832&type={lookup_type}&term={term}"
            r = requests.get(url, timeout=12)
            if r.status_code != 200:
                return jsonify({"error":f"Siwam API error {r.status_code}"})
            try:
                j = r.json()
                formatted = flatten_and_format(lookup_type, j)
                filename = f"{lookup_type}_{term}.txt"
                return jsonify({"result": formatted, "filename": filename})
            except Exception:
                txt = r.text or "(no data)"
                return jsonify({"result": txt, "filename": f"{lookup_type}_{term}.txt"})
    except requests.exceptions.Timeout:
        return jsonify({"error":"Upstream request timed out"}), 504
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
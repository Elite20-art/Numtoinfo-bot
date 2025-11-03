from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RoyalOfficial OSINT Portal</title>
<style>
:root {
  --bg: #000;
  --text: #00ff66;
  --border: #00ff66;
  --shadow: #00ff66;
}
body {
  background: var(--bg);
  color: var(--text);
  font-family:'Courier New',monospace;
  text-align:center;
  margin-top:30px;
  transition: all 0.4s ease;
}
h1 { color: var(--text); text-shadow: 0 0 10px var(--shadow); }
form {
  background:#0f0f0f;
  padding:20px;
  border-radius:12px;
  box-shadow:0 0 20px var(--shadow);
  display:inline-block;
  transition: all 0.4s ease;
}
select, input {
  background:#000;
  color:var(--text);
  border:1px solid var(--border);
  padding:10px;
  width:260px;
  margin:8px;
  text-align:center;
  border-radius:6px;
  transition: all 0.3s ease;
}
button {
  background:var(--text);
  color:#000;
  border:none;
  padding:10px 18px;
  margin:6px;
  cursor:pointer;
  font-weight:bold;
  border-radius:6px;
  transition: all 0.3s ease;
}
.output {
  background:#0f0f0f;
  margin-top:20px;
  padding:15px;
  border-radius:12px;
  border:2px solid var(--border);
  box-shadow:0 0 18px var(--shadow);
  width:90%;
  max-width:680px;
  margin-left:auto;
  margin-right:auto;
  min-height:150px;
  white-space:pre-wrap;
  text-align:left;
  position:relative;
  font-size:14px;
  transition: all 0.4s ease;
}
.error { color:#ff4444 }
.loader {
  border:4px solid #111;
  border-top:4px solid var(--text);
  border-radius:50%;
  width:34px;
  height:34px;
  animation:spin 1s linear infinite;
  display:none;
  position:absolute;
  top:45%;
  left:50%;
  transform:translate(-50%,-50%);
}
@keyframes spin {
  0%{transform:translate(-50%,-50%) rotate(0deg)}
  100%{transform:translate(-50%,-50%) rotate(360deg)}
}
.footer { color:#666; margin-top:18px; font-size:13px }
.theme-toggle {
  position:fixed;
  top:15px; right:20px;
  background:var(--text);
  color:#000;
  border:none;
  padding:8px 12px;
  border-radius:20px;
  font-weight:bold;
  cursor:pointer;
  box-shadow:0 0 10px var(--shadow);
  transition: all 0.4s ease;
}
</style>

<script>
let darkMode = false;
function toggleTheme() {
  darkMode = !darkMode;
  if(darkMode) {
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

  output.innerHTML = '';
  loader.style.display = 'block';
  status.innerText = 'Fetching... ⏳';
  status.style.color = '#00ff66';

  if(!term){
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
    if(data.error){
      output.innerHTML = '<span class="error">❌ ' + data.error + '</span>';
      status.innerText = 'Error ❌';
      status.style.color = '#ff4444';
    } else {
      output.textContent = data.result;
      status.innerText = 'Done ✅';
      status.style.color = '#00ff66';
    }
  } catch(err){
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
}
function copyOutput(){
  const text = document.getElementById('output').innerText;
  navigator.clipboard.writeText(text);
  alert('Copied to clipboard!');
}
function downloadOutput(){
  const text = document.getElementById('output').innerText;
  const blob = new Blob([text], {type:'text/plain'});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'result.txt';
  link.click();
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

  <div id="output" class="output">
    <div id="loader" class="loader"></div>
    Result will appear here — info stays in this box only.
  </div>

  <div style="margin-top:12px">
    <button onclick="copyOutput()" style="background:#00ff66;color:#000;padding:8px 14px;border-radius:6px;border:none;margin-right:8px">Copy</button>
    <button onclick="downloadOutput()" style="background:#00ff66;color:#000;padding:8px 14px;border-radius:6px;border:none">Download (.txt)</button>
  </div>

  <div id="status" class="footer">Idle</div>
  <div class="footer">© RoyalOfficial Intelligence Portal</div>
</body>
</html>
"""

# -------------- BACKEND --------------
@app.route('/')
def home():
    return render_template_string(HTML)

def emoji_format(lookup_type, data):
    # Emoji mapping
    emoji_map = {
        "mobile": {"mobile":"📞","name":"👤","father":"👨‍👦","address":"🏠","alt":"📞","circle":"📍","id":"🆔","email":"📧","success":"✅"},
        "vehicle":{"rc":"🚘","owner":"👤","registration":"📅","class":"🛻","fuel":"⛽","maker":"🏷️","engine":"⚙️","chassis":"🔩","fitness":"🧾","insurance":"🛡️","registered":"📍","status":"✅"},
        "aadhaar":{"aadhaar":"🆔","name":"👤","dob":"📅","state":"📍","status":"✅"},
        "upi":{"upi":"💳","holder":"👤","bank":"🏦","verified":"✅","created":"📅"},
        "email":{"email":"✉️","valid":"✅","disposable":"🚫","domain":"🌍","created":"📅"},
        "pan":{"pan":"🧾","name":"👤","dob":"📅","ao":"🏦","status":"✅"}
    }

    emap = emoji_map.get(lookup_type, {})

    def format_dict(d):
        lines = []
        for k, v in d.items():
            key_lower = k.lower()
            emoji = next((e for kw, e in emap.items() if kw in key_lower), "•")
            value = str(v) if v not in [None, "", "null"] else "(not available)"
            lines.append(f"{emoji} {k.replace('_',' ').title()}: {value}")
        return "\n".join(lines)

    # Clean format for list/dict
    formatted = ""
    if isinstance(data, list):
        for i, item in enumerate(data, start=1):
            formatted += f"Record {i}:\n{format_dict(item)}\n"
            if i < len(data):
                formatted += "────────────────────────────\n"
    elif isinstance(data, dict):
        formatted += format_dict(data)
    else:
        formatted += str(data)

    return formatted.strip()

@app.route('/lookup', methods=['POST'])
def lookup():
    req = request.get_json(force=True)
    lookup_type = req.get('type')
    term = req.get('term')
    if not lookup_type or not term:
        return jsonify({"error":"Missing input"}),400
    try:
        if lookup_type=="vehicle":
            url = f"https://vehicle-info-api-hexabhi.onrender.com/?rc_number={term}"
        else:
            url = f"https://siwammodz.vercel.app/api?key=Siwam_9832&type={lookup_type}&term={term}"
        res = requests.get(url,timeout=10)
        if res.status_code!=200:
            return jsonify({"error":f"API Error {res.status_code}"})
        try:
            j = res.json()
            return jsonify({"result":emoji_format(lookup_type,j)})
        except:
            return jsonify({"result":res.text})
    except Exception as e:
        return jsonify({"error":str(e)})

if __name__ == "__main__":

    app.run(host="0.0.0.0",port=8080)

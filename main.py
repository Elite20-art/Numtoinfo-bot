from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RoyalOfficial OSINT Portal</title>
<style>
body {
  background-color: #000;
  color: #00ff66;
  font-family: 'Courier New', monospace;
  text-align: center;
  margin-top: 40px;
}
h1 {
  color: #00ff66;
  text-shadow: 0 0 10px #00ff66;
}
form {
  background: #0f0f0f;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px #00ff66;
  display: inline-block;
}
select, input {
  background: #000;
  color: #00ff66;
  border: 1px solid #00ff66;
  padding: 10px;
  width: 250px;
  margin: 8px;
  text-align: center;
}
button {
  background: #00ff66;
  color: #000;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  cursor: pointer;
  font-weight: bold;
}
.output {
  background: #0f0f0f;
  margin-top: 20px;
  padding: 15px;
  border-radius: 10px;
  border: 2px solid #00ff66;
  box-shadow: 0 0 15px #00ff66;
  width: 90%;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  min-height: 100px;
  white-space: pre-wrap;
  text-align: left;
}
.error { color: #ff4444; }
.loader {
  border: 4px solid #111;
  border-top: 4px solid #00ff66;
  border-radius: 50%;
  width: 30px; height: 30px;
  animation: spin 1s linear infinite;
  display: none;
  margin: 10px auto;
}
@keyframes spin { 0% { transform: rotate(0deg);} 100% { transform: rotate(360deg);} }
</style>
<script>
async function fetchInfo(event) {
  event.preventDefault();
  const type = document.getElementById('type').value;
  const term = document.getElementById('term').value.trim();
  const output = document.getElementById('output');
  const loader = document.getElementById('loader');
  output.innerHTML = '';
  loader.style.display = 'block';

  if (!term) {
    output.innerHTML = '<span class="error">❌ Please enter a value!</span>';
    loader.style.display = 'none';
    return;
  }

  try {
    const res = await fetch('/lookup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type, term })
    });
    const data = await res.json();
    loader.style.display = 'none';
    if (data.error) {
      output.innerHTML = '<span class="error">❌ ' + data.error + '</span>';
    } else {
      output.textContent = data.result;
    }
  } catch (err) {
    loader.style.display = 'none';
    output.innerHTML = '<span class="error">❌ ' + err + '</span>';
  }
}
function clearOutput() {
  document.getElementById('term').value = '';
  document.getElementById('output').innerHTML = '';
}
</script>
</head>
<body>
<h1>RoyalOfficial OSINT Portal</h1>
<form onsubmit="fetchInfo(event)">
  <select id="type">
    <option value="mobile">📱 Mobile Info</option>
    <option value="aadhaar">🆔 Aadhaar Info</option>
    <option value="vehicle">🚗 Vehicle Info</option>
    <option value="upi">💳 UPI Info</option>
    <option value="email">✉️ Email Info</option>
    <option value="pan">🧾 PAN Info</option>
  </select><br>
  <input type="text" id="term" placeholder="Enter value..." required><br>
  <button type="submit">Fetch Info</button>
  <button type="button" onclick="clearOutput()">Clear</button>
</form>

<div id="loader" class="loader"></div>
<div id="output" class="output">Result will appear here — info stays in this box only.</div>

<p style="color:#888;font-size:0.8rem;margin-top:20px">© RoyalOfficial Intelligence Portal</p>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.get_json()
    lookup_type = data.get('type')
    term = data.get('term')
    if not lookup_type or not term:
        return jsonify({"error": "Missing input!"})

    api_url = f"https://siwammodz.vercel.app/api?key=Siwam_9832&type={lookup_type}&term={term}"
    try:
        res = requests.get(api_url, timeout=10)
        if res.status_code == 200:
            return jsonify({"result": res.text})
        else:
            return jsonify({"error": f"API returned status {res.status_code}"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

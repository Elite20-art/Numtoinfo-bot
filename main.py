from flask import Flask, request, render_template_string
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
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
    }
    h1 {
        color: #00ff66;
        text-shadow: 0 0 10px #00ff66;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    form {
        background: #0f0f0f;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 0 25px #00ff66;
        text-align: center;
        width: 90%;
        max-width: 450px;
    }
    select, input {
        background: #000;
        color: #00ff66;
        border: 1px solid #00ff66;
        padding: 10px;
        width: 90%;
        font-size: 1rem;
        margin-bottom: 10px;
        text-align: center;
        border-radius: 4px;
    }
    button {
        background: #00ff66;
        color: #000;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        cursor: pointer;
        margin: 5px;
        border-radius: 4px;
    }
    button:hover {
        background: #0f0;
    }
    /* animated glowing border */
    @keyframes glowBorder {
        0% { box-shadow: 0 0 5px #00ff66, 0 0 10px #00ff66, 0 0 20px #00ff66; }
        50% { box-shadow: 0 0 15px #00ffcc, 0 0 30px #00ff66, 0 0 45px #00ffcc; }
        100% { box-shadow: 0 0 5px #00ff66, 0 0 10px #00ff66, 0 0 20px #00ff66; }
    }
    .output {
        margin-top: 20px;
        padding: 15px;
        border: 2px solid #00ff66;
        border-radius: 12px;
        width: 90%;
        max-width: 450px;
        background: #0f0f0f;
        text-align: left;
        min-height: 150px;
        overflow-x: auto;
        white-space: pre-wrap;
        color: #00ff66;
        position: relative;
        animation: glowBorder 3s infinite ease-in-out;
    }
    .error {
        color: #ff4444;
    }
    .footer {
        margin-top: 40px;
        font-size: 0.8rem;
        color: #333;
    }
    .loader {
        border: 4px solid #222;
        border-top: 4px solid #00ff66;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        position: absolute;
        top: 45%;
        left: 50%;
        transform: translate(-50%, -50%);
        display: none;
    }
    @keyframes spin {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
</style>

<script>
async function fetchInfo(event) {
    event.preventDefault();
    const form = document.getElementById('lookupForm');
    const type = form.type.value;
    const term = form.term.value.trim();
    const output = document.getElementById('output');
    const loader = document.getElementById('loader');
    const status = document.getElementById('status');

    if (!term) {
        output.innerHTML = '<span class="error">❌ Please enter a value.</span>';
        return;
    }

    output.innerText = '';
    loader.style.display = 'block';
    status.innerText = 'Fetching info... ⏳';
    status.style.color = '#00ff66';

    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ type, term })
        });
        const text = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        const newOutput = doc.getElementById('output').innerHTML;

        output.innerHTML = newOutput;
        loader.style.display = 'none';
        status.innerText = 'Done ✅';
        status.style.color = '#00ff66';
    } catch (err) {
        loader.style.display = 'none';
        output.innerHTML = '<span class="error">❌ Error: ' + err + '</span>';
        status.innerText = 'Error ❌';
        status.style.color = '#ff4444';
    }
}

function clearOutput() {
    document.getElementById('term').value = '';
    document.getElementById('output').innerText = '';
    document.getElementById('status').innerText = 'Idle';
    document.getElementById('status').style.color = '#555';
}
function copyOutput() {
    const text = document.getElementById('output').innerText;
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
}
function downloadOutput() {
    const text = document.getElementById('output').innerText;
    const blob = new Blob([text], {type: 'text/plain'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'result.txt';
    link.click();
}
</script>
</head>
<body>
    <h1>RoyalOfficial OSINT Portal</h1>
    <form id="lookupForm" onsubmit="fetchInfo(event)">
        <select name="type" required>
            <option value="mobile">📱 Mobile Info</option>
            <option value="aadhaar">🆔 Aadhaar Info</option>
            <option value="vehicle">🚗 Vehicle Info</option>
            <option value="upi">💳 UPI Info</option>
            <option value="email">✉️ Email Info</option>
            <option value="pan">🧾 PAN Info</option>
        </select>
        <input type="text" id="term" name="term" placeholder="Enter value..." required>
        <br>
        <button type="submit">Fetch Info</button>
        <button type="button" onclick="clearOutput()">Clear</button>
    </form>

    <div class="output" id="output">
        <div class="loader" id="loader"></div>
        Result will appear here — info stays in this box only.
    </div>

    <div>
        <button type="button" onclick="copyOutput()">Copy</button>
        <button type="button" onclick="downloadOutput()">Download (.txt)</button>
    </div>

    <div id="status" class="footer">Idle</div>
    <div class="footer">© RoyalOfficial Intelligence Portal</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        lookup_type = request.form.get('type')
        term = request.form.get('term')
        if lookup_type and term:
            try:
                api_url = f"https://siwammodz.vercel.app/api?key=Siwam_9832&type={lookup_type}&term={term}"
                res = requests.get(api_url, timeout=10)
                if res.status_code == 200:
                    data = res.text
                else:
                    data = f"<span class='error'>❌ API Error: {res.status_code}</span>"
            except Exception as e:
                data = f"<span class='error'>❌ Error: {e}</span>"
        else:
            data = "<span class='error'>❌ Missing input.</span>"
    return render_template_string(HTML, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
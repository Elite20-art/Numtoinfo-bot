from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HexaVault Number OSINT</title>
<style>
    body {
        background-color: #0a0a0a;
        color: #00ff88;
        font-family: 'Courier New', monospace;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
    h1 {
        color: #00ff88;
        text-shadow: 0 0 10px #00ff88;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    form {
        background: #111;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 20px #00ff88;
        text-align: center;
    }
    input {
        background: black;
        color: #00ff88;
        border: 1px solid #00ff88;
        padding: 10px;
        width: 250px;
        font-size: 1rem;
        margin-bottom: 10px;
    }
    button {
        background: #00ff88;
        color: #000;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }
    button:hover {
        background: #0f0;
    }
    .result {
        margin-top: 20px;
        padding: 15px;
        border: 1px solid #00ff88;
        border-radius: 8px;
        width: 300px;
        word-wrap: break-word;
        background: #111;
        text-align: left;
    }
    .footer {
        margin-top: 40px;
        font-size: 0.8rem;
        color: #444;
    }
</style>
</head>
<body>
    <h1>HexaVault Number OSINT</h1>
    <form method="post">
        <input type="text" name="number" placeholder="Enter phone number" required>
        <br>
        <button type="submit">Lookup</button>
    </form>
    {% if data %}
    <div class="result">
        <strong>Number Info:</strong><br><br>
        <pre>{{ data }}</pre>
    </div>
    {% endif %}
    <div class="footer">© HexaVault DarkNet Intelligence</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    if request.method == 'POST':
        number = request.form.get('number')
        if number:
            try:
                api_url = f"https://siwammodz.vercel.app/api?key=Siwam_9832&type=mobile&term={number}"
                res = requests.get(api_url, timeout=10)
                data = res.text
            except Exception as e:
                data = f"Error: {e}"
    return render_template_string(HTML, data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
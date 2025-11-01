from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RoyalOfficial Number Info</title>
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
        max-width: 400px;
    }
    input {
        background: #000;
        color: #00ff66;
        border: 1px solid #00ff66;
        padding: 10px;
        width: 90%;
        font-size: 1rem;
        margin-bottom: 10px;
        text-align: center;
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
    .output {
        margin-top: 20px;
        padding: 15px;
        border: 1px solid #00ff66;
        border-radius: 8px;
        width: 90%;
        max-width: 400px;
        background: #0f0f0f;
        text-align: left;
        min-height: 120px;
        overflow-x: auto;
        white-space: pre-wrap;
    }
    .footer {
        margin-top: 40px;
        font-size: 0.8rem;
        color: #333;
    }
</style>
<script>
function clearOutput() {
    document.getElementById('number').value = '';
    document.getElementById('output').innerText = '';
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
    <h1>RoyalOfficial Number Info</h1>
    <form method="post">
        <input type="text" id="number" name="number" placeholder="e.g. 919812345678" required>
        <br>
        <button type="submit">Fetch Info</button>
        <button type="button" onclick="clearOutput()">Clear</button>
    </form>

    <div class="output" id="output">
        {% if data %}
        {{ data }}
        {% else %}
        Result will appear here — info stays in this box only.
        {% endif %}
    </div>

    <div>
        <button type="button" onclick="copyOutput()">Copy</button>
        <button type="button" onclick="downloadOutput()">Download (.txt)</button>
    </div>

    <div class="footer">Status: idle — © RoyalOfficial</div>
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
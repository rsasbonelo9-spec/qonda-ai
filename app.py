from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Qonda AI</title>
<style>
body{font-family:Arial;background:#0a0a0a;color:white;text-align:center;padding:50px}
h1{color:#00ff88} .box{background:#1a1a1a;padding:20px;border-radius:15px;max-width:500px;margin:auto}
input{width:80%;padding:12px;border-radius:10px;border:none;margin:10px}
button{padding:12px 25px;background:#00ff88;border:none;border-radius:10px;font-weight:bold;cursor:pointer}
</style>
</head>
<body>
<h1>🔥 QONDA AI 🔥</h1>
<p>From Durban to the World 🌍</p>
<div class="box">
<input id="q" placeholder="Ask Qonda anything...">
<br><button onclick="ask()">Ask Qonda</button>
<p id="a"></p>
</div>
<script>
async function ask(){
 let q=document.getElementById('q').value;
 document.getElementById('a').innerText='Thinking...';
 let r=await fetch('/ask?q='+q);
 let d=await r.json();
 document.getElementById('a').innerText=d.answer;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask")
def ask():
    q = request.args.get("q","")
    return jsonify({"answer": f"Qonda AI says: You asked '{q}' — I am LIVE from Durban! 🚀🔥 Durban's first AI is here!"})

if __name__ == "__main__":
    app.run()

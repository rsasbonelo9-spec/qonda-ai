from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Qonda AI</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#0a0a0a;color:white;text-align:center;padding:20px}
h1{color:#00ff88}
.box{background:#1a1a1a;padding:20px;border-radius:15px;max-width:600px;margin:auto}
input{width:85%;padding:12px;border-radius:10px;border:none;margin:10px}
button{padding:12px 25px;background:#00ff88;border:none;border-radius:10px;font-weight:bold;cursor:pointer}
#a{margin-top:15px;text-align:left;white-space:pre-wrap}
</style>
</head>
<body>
<h1>🔥 QONDA AI 🔥</h1>
<p>From Durban to the World 🌍</p>
<div class="box">
<input id="q" placeholder="Ask Qonda anything...">
<br><button onclick="ask()">Send</button>
<p id="a"></p>
</div>
<script>
async function ask(){
 let q=document.getElementById('q').value;
 if(!q)return;
 document.getElementById('a').innerText='Qonda is thinking... 🧠';
 let r=await fetch('/ask?q='+encodeURIComponent(q));
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
    ql = q.lower()
    if "dna" in ql:
        ans = "DNA is Deoxyribonucleic Acid - the double helix that stores your genetic code. Made of A,T,C,G bases. It tells your body how to build itself!\n\n— Qonda AI 🔥 From Durban"
    elif "who are you" in ql:
        ans = "I am QONDA AI — built in Durban, South Africa! 🇿🇦 Your AI from Durban to the World! 🌍"
    else:
        ans = f"You asked: '{q}' — I am Qonda AI LIVE from Durban! 🚀 I am working! Ask me about DNA, science, etc."
    return jsonify({"answer": ans})

if __name__ == "__main__":
    app.run()

This one?

from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Qonda AI</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font-family:Arial;background:#0a0a0a;color:white;text-align:center;padding:20px}
h1{color:#00ff88} .box{background:#1a1a1a;padding:20px;border-radius:15px;max-width:600px;margin:auto}
input{width:85%;padding:12px;border-radius:10px;border:none;margin:10px}
button{padding:12px 25px;background:#00ff88;border:none;border-radius:10px;font-weight:bold;cursor:pointer}
#a{margin-top:15px;text-align:left;white-space:pre-wrap}
</style>
</head>
<body>
<h1>🔥 QONDA AI 🔥</h1>
<p>From Durban to the World 🌍</p>
<div class="box">
<input id="q" placeholder="Ask Qonda anything... e.g. What is DNA?">
<br><button onclick="ask()">Ask Qonda</button>
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

def get_smart_answer(question):
    try:
        # Try Wikipedia for real knowledge - FREE no API key needed!
        search = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={question}&limit=1&namespace=0&format=json", timeout=5).json()
        if search[1]:
            title = search[1][0]
            summary = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}", timeout=5).json()
            if 'extract' in summary:
                return f"{summary['extract']}\n\n— Qonda AI 🔥 | Source: Wikipedia"
    except:
        pass
    # Fallback smart answers
    q = question.lower()
    if "dna" in q:
        return "DNA (Deoxyribonucleic Acid) is the molecule that carries genetic instructions in all living things. It's a double helix made of 4 bases: A, T, C, G. It stores how to build and maintain your body.\n\n— Qonda AI 🔥 From Durban!"
    if "who are you" in q:
        return "I am QONDA AI — built in Durban, South Africa! 🇿🇦 Durban's first AI assistant, created to help the world learn. From Durban to the World! 🌍"
    return f"Qonda AI received: '{question}'. I am learning! Ask me about science, history, tech, etc. My full AI brain upgrade is coming soon with API key!\n\n— Live from Durban! 🚀"

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask")
def ask():
    q = request.args.get("q","")
    answer = get_smart_answer(q)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run()

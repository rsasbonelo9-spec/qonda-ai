from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("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", "")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = "You are QONDA AI, built in Durban, South Africa. You are proud SA AI. Helpful, smart, friendly. Keep answers short."

@app.route("/")
def home():
    return """
    <html>
    <head><title>QONDA AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:Arial;max-width:700px;margin:0 auto;padding:20px;background:#0f172a;color:white}
    h1{color:#38bdf8;text-align:center}
    #chat{background:#1e293b;padding:15px;border-radius:10px;height:400px;overflow-y:auto;margin:10px 0}
    .user{color:#7dd3fc;text-align:right;margin:8px}.bot{color:#86efac;margin:8px}
    input{width:70%;padding:12px;border-radius:8px;border:none}
    button{padding:12px 20px;background:#38bdf8;border:none;border-radius:8px;cursor:pointer;font-weight:bold}
    </style></head>
    <body>
    <h1>QONDA AI - REAL AI</h1>
    <p style="text-align:center">Ngilungele Ukukusiza!</p>
    <div id="chat"><div class="bot">Sawubona! I am QONDA AI - How Can I Help You?</div></div>
    <div style="display:flex;gap:10px"><input id="q" placeholder="Ask QONDA..."><button onclick="send()">Send</button></div>
    <script>
    async function send(){
      const q=document.getElementById('q').value; if(!q) return;
      const chat=document.getElementById('chat');
      chat.innerHTML+='<div class="user">You: '+q+'</div>';
      document.getElementById('q').value='';
      chat.innerHTML+='<div class="bot" id="thinking">Thinking...</div>';
      const res=await fetch('/ask?q='+encodeURIComponent(q));
      const data=await res.json();
      document.getElementById('thinking').remove();
      chat.innerHTML+='<div class="bot">QONDA: '+data.answer+'</div>';
      chat.scrollTop=chat.scrollHeight;
    }
    document.getElementById('q').addEventListener('keypress',e=>{if(e.key==='Enter')send()});
    </script>
    </body></html>
    """

@app.route("/ask")
def ask():
    q = request.args.get("q","")
    if not q:
        return jsonify({"answer": "Ask me something!"})
    if not GROQ_API_KEY:
        return jsonify({"answer": "Add GROQ_API_KEY in Render Environment!"})
    try:
        headers = {"Authorization": "Bearer " + GROQ_API_KEY, "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        r = requests.post(GROQ_URL, json=payload, headers=headers, timeout=20)
        data = r.json()
        ans = data["choices"][0]["message"]["content"]
        return jsonify({"answer": ans})
    except Exception as e:
        return jsonify({"answer": "Error: " + str(e)[:200]})

if __name__ == "__main__":
    app.run()

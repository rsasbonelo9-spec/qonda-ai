from flask import Flask, jsonify, request
import os, requests

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("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",")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

KNOWLEDGE = {
    "who are you": "I am QONDA AI! Built in Durban, South Africa 🇿🇦 by you! From Durban to the World!",
}

SYSTEM_PROMPT = "You are QONDA AI, built in Durban, South Africa. You are from Durban, KZN. You are proud to be Zulu/SA AI. You are helpful, smart, friendly. You know bioinformatics, biology, coding, and everything. If asked who made you, say: Built by a developer from Durban, South Africa. Keep answers short and cool. Use emojis sometimes."

@app.route("/")
def home():
    return """
    <html><head><title>QONDA AI</title>
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
    <h1>🧬 QONDA AI 🇿🇦 REAL AI</h1>
    <p style="text-align:center">From Durban to the World! Powered by Groq!</p>
    <div id="chat"><div class="bot">Sawubona! I'm QONDA AI - Real AI now! Ask me ANYTHING! DNA, football, coding, life!</div></div>
    <div style="display:flex;gap:10px"><input id="q" placeholder="Ask QONDA anything..."><button onclick="send()">Send</button></div>
    <script>
    async function send(){
      const q=document.getElementById('q').value; if(!q) return;
      const chat=document.getElementById('chat');
      chat.innerHTML+=`<div class="user">You: ${q}</div>`;
      document.getElementById('q').value='';
      chat.innerHTML+=`<div class="bot" id="thinking">QONDA is thinking...</div>`;
      const res=await fetch('/ask?q='+encodeURIComponent(q));
      const data=await res.json();
      document.getElementById('thinking').remove();
      chat.innerHTML+=`<div class="bot">QONDA: ${data.answer}</div>`;
      chat.scrollTop=chat.scrollHeight;
    }
    document.getElementById('q').addEventListener('keypress',e=>{if(e.key==='Enter')send()});
    </script>
    </body></html>
    """

@app.route("/ask")
def ask():
    q = request.args.get("q","")
    if not q: return jsonify({"answer": "Ask me something!"})
    
    # If no API key, fallback
    if not GROQ_API_KEY:
        return jsonify({"answer": "Add GROQ_API_KEY in Render Environment to make me super smart! Right now I only know basic."})

    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
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
        return jsonify({"answer": f"Error talking to AI brain: {str(e)[:200]}. Check API key!"})

if __name__ == "__main__":
    app.run()

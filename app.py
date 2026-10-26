from flask import Flask, request, jsonify
from groq import Groq
import os

app = Flask(__name__)

# PUT YOUR GROQ KEY HERE
GROQ_API_KEY = "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"  # <-- change this!

client = Groq(api_key=GROQ_API_KEY)

history = [{"role": "system", "content": "You are QONDA AI. Speak in casual mix of English and Zulu, like 'bhuti', 'sawubona'. Be helpful, smart, friendly. Explain things simply."}]

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Qonda AI</title>
<style>
body{background:#0a0f1e;color:white;font-family:Arial;margin:0}
.top{background:#000;padding:15px;text-align:center;font-weight:bold}
.top span{color:#00ff88}
#chat{padding:15px;height:75vh;overflow-y:auto}
.user{background:#00ff88;color:#000;padding:10px;border-radius:15px;margin:8px 0 8px 30%;text-align:right}
.bot{background:#1e2a45;padding:10px;border-radius:15px;margin:8px 30% 8px 0}
#box{position:fixed;bottom:0;width:100%;display:flex;background:#000;padding:10px}
input{flex:1;padding:12px;border-radius:20px;border:none}
button{padding:12px 20px;margin-left:8px;border-radius:20px;background:#00ff88;border:none;font-weight:bold}
</style>
</head>
<body>
<div class="top"><span>QONDA AI</span></div>
<div id="chat"><div class="bot">Sawubona bhuti! I am Qonda AI. Ask me anything!</div></div>
<div id="box"><input id="q" placeholder="Ask Qonda anything..." onkeypress="if(event.key==='Enter')ask()"><button onclick="ask()">Send</button></div>
<script>
async function ask(){
 let i=document.getElementById('q'); let txt=i.value; if(!txt)return;
 let c=document.getElementById('chat'); c.innerHTML+=`<div class="user">${txt}</div>`; i.value='';
 let r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg:txt})});
 let d=await r.json(); c.innerHTML+=`<div class="bot">${d.reply}</div>`; c.scrollTop=c.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/ask", methods=["POST"])
def ask():
    global history
    data = request.json
    user_msg = data.get("msg","")
    history.append({"role": "user", "content": user_msg})
    try:
        # FIXED MODEL NAME
        chat = client.chat.completions.create(model="openai/gpt-oss-20b", messages=history)
        reply = chat.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    history.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"Qonda AI Link: http://127.0.0.1:{port}")
    print(f"For PHONE: http://10.116.226.96:{port}")
    app.run(host="0.0.0.0", port=port)
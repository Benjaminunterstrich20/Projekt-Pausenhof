from flask import Flask, render_template, request, redirect, url_for, session
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "geheimer_pauser_schlüssel"

# In-Memory Speicherung von Chatcodes
codes = {}  # z.B. {"coolcode": {"users": [], "messages": []}}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form["code"].strip()
        if code not in codes:
            codes[code] = {"users": [], "messages": []}
        
        # Nutzer registrieren
        if len(codes[code]["users"]) < 2:
            user_id = str(uuid4())
            session["user_id"] = user_id
            session["code"] = code
            codes[code]["users"].append(user_id)
            return redirect(url_for("chat"))
        else:
            return render_template("index.html", error="Dieser Code ist schon voll.")
    
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    code = session.get("code")
    user_id = session.get("user_id")

    if not code or not user_id or code not in codes:
        return redirect(url_for("index"))
    
    chat_data = codes[code]
    has_sent = any(msg["user"] == user_id for msg in chat_data["messages"])

    if request.method == "POST" and not has_sent:
        msg = request.form["message"]
        chat_data["messages"].append({"user": user_id, "text": msg})

    # Wenn beide geschrieben haben → löschen
    if len(chat_data["messages"]) >= 2:
        del codes[code]

    return render_template("chat.html", messages=chat_data["messages"], has_sent=has_sent)

# ✅ NEUE SEITE: Alle aktiven Räume
@app.route("/räume")
def raeume():
    offene_codes = [code for code, data in codes.items() if len(data["messages"]) < 2]
    return render_template("raeume.html", codes=offene_codes)

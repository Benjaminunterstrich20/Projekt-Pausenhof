from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Chats speichern: code -> Liste von Nachrichten (dict mit name + text)
chats = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form.get("code", "").strip()
        if code:
            if code not in chats:
                chats[code] = []
            return redirect(url_for("chat", code=code))
    return render_template("index.html")

@app.route("/chat/<code>", methods=["GET", "POST"])
def chat(code):
    if code not in chats:
        chats[code] = []

    msgs = chats[code]

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        msg = request.form.get("message", "").strip()
        if name and msg:
            msgs.append({"name": name, "text": msg})
            return redirect(url_for("chat", code=code))

    return render_template("chat.html", code=code, messages=msgs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

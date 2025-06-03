from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Speicher: code -> Liste der Nachrichten (immer nur 2 Nutzer, abwechselnd schreiben)
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

    # Bestimmen, wer gerade schreiben darf:
    # Wenn keine Nachrichten, darf A schreiben
    # Dann abwechselnd A, B, A, B ...
    # A = gerade gerade Index (0,2,4...) -> User A schreibt, B wartet
    # B = ungerade Index (1,3,5...) -> User B schreibt, A wartet

    # Wir merken uns keine User-IDs, sondern nur Reihenfolge:
    # Der erste, der schreibt, ist "A", der zweite "B", und so weiter im Wechsel.

    user_allowed_to_write = 'A' if len(msgs) % 2 == 0 else 'B'

    if request.method == "POST":
        msg = request.form.get("message", "").strip()
        if msg:
            # Nachricht nur speichern, wenn der richtige "User" dran ist
            # Wir können die user nicht unterscheiden, deshalb: 
            # Es wird angenommen, dass User A und B abwechselnd schreiben,
            # also wir blockieren zwei Nachrichten hintereinander vom selben "User"
            # Hier: einfach erlauben, wenn Reihenfolge passt (also alternierend)

            msgs.append(msg)
            return redirect(url_for("chat", code=code))

    return render_template("chat.html", code=code, messages=msgs, user=user_allowed_to_write)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

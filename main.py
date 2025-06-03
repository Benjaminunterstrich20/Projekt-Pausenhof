from flask import Flask, render_template, request, redirect
app = Flask(__name__)
chats = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        code = request.form['code']
        return redirect(f'/chat/{code}')
    return render_template('index.html')

@app.route('/chat/<code>', methods=['GET', 'POST'])
def chat(code):
    if code not in chats:
        chats[code] = {"messages": [], "sent_users": set()}

    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']

        if user not in chats[code]['sent_users']:
            chats[code]['messages'].append((user, message))
            chats[code]['sent_users'].add(user)

    return render_template('chat.html', code=code, messages=chats[code]['messages'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheimcode123'

socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}  # Raum-Code : list von Usernames

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    room = request.form.get('room')
    username = request.form.get('username')
    if not room or not username:
        return redirect(url_for('index'))
    return render_template('chat.html', room=room, username=username)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)

    if room not in rooms:
        rooms[room] = []
    rooms[room].append(username)

    emit('system_message', {'msg': f'{username} ist dem Raum beigetreten'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    username = data['username']
    msg = data['msg']
    is_image = data.get('is_image', False)

    emit('message', {
        'username': username,
        'msg': msg,
        'is_image': is_image
    }, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)

    if room in rooms and username in rooms[room]:
        rooms[room].remove(username)
        if len(rooms[room]) == 0:
            del rooms[room]

    emit('system_message', {'msg': f'{username} hat den Raum verlassen'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)

from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect, join_room, rooms
from threading import Lock


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
user_name = ''
character = ''


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)

@app.route('/battle_menu/<nickname>')
def battle(nickname):
    return render_template('battle_menu.html', async_mode=socket_.async_mode)


@socket_.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    print("_____________________________")
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

@socket_.on('username_event', namespace='/test')
def test_username_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['username'] = message['data']
    user_name = message['data']
    print(user_name)
    emit('my_response',
         {'data': message['data'] + " has joined", 'count': session['receive_count']},
         broadcast=True)

@socket_.on('join', namespace='/test')
def join(message):
    print("__________________")
    print("In Join Function")
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

@socket_.on('character_chosen', namespace='/test')
def character_chosen(id):
    session['character'] = id['data']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('character_chosen_local',
         {'data': id['data'], 'count': session['receive_count']})
    emit('character_chosen_global',
         {'data': id['data'], 'count': session['receive_count'],'username':session['username']},
         broadcast=True)

if __name__ == '__main__':
    socket_.run(app, debug=True)
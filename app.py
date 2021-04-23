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


@socket_.on('my_event')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('my_broadcast_event')
def test_broadcast_message(message):
    print("_____________________________")
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

@socket_.on('username_event')
def test_username_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['username'] = message['username']
    user_name = message['username']
    print(user_name)
    emit('my_response',
         {'data': message['username'] + " has joined", 'count': session['receive_count']},
         broadcast=True)
    emit('username_global_response',
         {'username': message['username'], 'id':message['id'],},
         broadcast=True)

@socket_.on('join')
def join(message):
    print("__________________")
    print("In Join Function")
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})
    emit('join_response_global', 
            {'username':session['username'], 'user_id':message['id']},
            broadcast=True)
    emit('join_response_local')

@socket_.on('first_ready')
def first_ready(message):
    print("______________________")
    print("room size of at least 1")
    print("being sent to{}",message['first_id_ready'])
    emit('alert_first_user',{'first_id':message['first_id_ready']}, broadcast=True)


@socket_.on('character_chosen')
def character_chosen(message):
    session['character'] = message['character_id']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('character_chosen_local',
         {'character_id': message['character_id'], 'count': session['receive_count']})
    emit('character_chosen_global',
         {'character_id': message['character_id'], 'user_id': message['user_id'],'count': session['receive_count'],'username':session['username']},
         broadcast=True)

@socket_.on('start_battle')
def start_battle(message):
    emit('room_battle_start',room=message['room'])

if __name__ == '__main__':
    socket_.run(app, debug=True)
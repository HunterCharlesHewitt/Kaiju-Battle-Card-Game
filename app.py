from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)


@socket_.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

@socket_.on('character_chosen', namespace='/test')
def character_chosen(id):
    session['character'] = id['data']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('character_chosen_local',
         {'data': id['data'], 'count': session['receive_count']})
    emit('character_chosen_global',
         {'data': id['data'], 'count': session['receive_count']},
         broadcast=True)

if __name__ == '__main__':
    socket_.run(app, debug=True)
from flask import Flask, render_template, session, copy_current_request_context, url_for
from flask_socketio import SocketIO, emit, disconnect, join_room, rooms
from utils.Godzilla import Godzilla
from utils.Soda_Bottle import Soda_Bottle
from threading import Lock
import json
import logging

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

@app.route('/')
def index():
    return render_template('index.html', async_mode=socket.async_mode, filenames=
        {
            'Bard':url_for('static',filename='images/creatures/Bard.PNG'),
            'Beholder':url_for('static',filename='images/creatures/Beholder.PNG'),
            'Boomhauer':url_for('static',filename='images/creatures/Boomhauer.PNG'),
            'SodaBottle':url_for('static',filename='images/creatures/SodaBottle.PNG'),
            'Donut':url_for('static',filename='images/creatures/Donut.PNG'),
            'Mothra':url_for('static',filename='images/creatures/Mothra.PNG'),
            'Gamera':url_for('static',filename='images/creatures/Gamera.PNG'),
            'Gamora':url_for('static',filename='images/creatures/Gamora.PNG'),
            'Jaeger':url_for('static',filename='images/creatures/Jaeger.PNG'),
            'KingKong':url_for('static',filename='images/creatures/KingKong.PNG'),
            'Ghedora':url_for('static',filename='images/creatures/Ghedora.PNG'),
            'Rogue':url_for('static',filename='images/creatures/Rogue.PNG'),
            'Wizard':url_for('static',filename='images/creatures/Wizard.PNG'),
            'Zombie':url_for('static',filename='images/creatures/Zombie.PNG'),
            'MechaGodzilla':url_for('static',filename='images/creatures/MechaGodzilla.PNG'),
            'Godzilla':url_for('static',filename='images/creatures/Godzilla.PNG'),
        }
    )

#message['data']
@socket.on('log_message_event')
def log_message(message):
    emit('log_message_response',
         {'data': message['data']})

#message['data']
@socket.on('broadcast_event')
def log_broadcast_message(message):
    emit('log_message_response',
         {'data': message['data']},
         broadcast=True)

#message['username']
#message['user_id']
@socket.on('username_event')
def test_username_message(message):
    session['username'] = message['username']
    session['user_id'] = message['user_id']
    print(session)
    print('/n')
    emit('log_message_response',
         {'data': message['username'] + " has joined"},
         broadcast=True)
    emit('username_global_response',
         {'username': message['username'], 'user_id':message['user_id'],},
         broadcast=True)

#message['room']
#message['room_size']
#message['user_id']
#message['first_user_id']
#message['users_in_room']
@socket.on('join')
def join(message):
    join_room(message['room'])
    emit('log_message_response',
         {'data': 'In rooms: ' + ', '.join(rooms())})
    emit('join_response_global', 
            {'username':session['username'], 'user_id':message['user_id']},
            broadcast=True)
    emit('join_response_local')

@socket.on('first_ready')
def first_ready(message):
    emit('alert_first_user',{'first_id':message['first_id_ready']}, broadcast=True)

# message['remove_character']
# message['character_id']
# message['user_id']
@socket.on('character_chosen_event')
def character_chosen_event(message):
    print("Character Chosen Event")
    emit('character_chosen_local',
         {'character_id': message['character_id'], 'user_id': message['user_id']})
    emit('character_chosen_global',
         {'character_id': message['character_id'], 'user_id': message['user_id'],'username':session['username'],'remove_character':message['remove_character']},
         broadcast=True)

# session variable will be given a user Creature pair here, this will determine how the local will keep track of global changes
# message['character_id']
# message['user_id'] 
@socket.on('character_chosen_event_session')
def character_chosen_event_session(message):
    user_id = message['user_id']
    char_id = message['character_id']
    if(char_id == 'Godzilla'):
        session[user_id] = Godzilla(user_id)
    elif(char_id == 'SodaBottle'):
        session[user_id] = Soda_Bottle(user_id)


@socket.on('start_battle')
def start_battle(message):
    emit('room_battle_start_response',room=message['room'])

# message['action']
# message['target_user_id']
# message['target_creature']
# message['user_id']
# message['user_creature']
@socket.on('local_action_event')
def local_action_event(message):
    emit('local_action_response',{
        'action' : message['action'],
        'target_user_id' : message['target_user_id'],
        'target_creature' : message['target_creature'],
        'user_id' : message['user_id'],
        'user_creature' : message['user_creature']
    }, broadcast=True)

@socket.on('global_action_event')
def global_action_event(message):
    action = message['action']
    target = message['target_user_id']
    user_id = message['user_id']
    if(action == 'defend'):
        session[user_id].defend(target)
    elif(action == 'heal'):
        session[user_id].heal(target)
    elif(action == 'attack'):
        session[user_id].attack(target)
    elif(action == 'sp'):
        session[user_id].sp(target)

    print(str(session[target]))
    print(str(session[user_id]))

if __name__ == '__main__':
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
    socket.run(app, debug=True)
    
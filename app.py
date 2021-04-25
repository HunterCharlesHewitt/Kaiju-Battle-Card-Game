from flask import Flask, render_template, session, copy_current_request_context, url_for
from flask_socketio import SocketIO, emit, disconnect, join_room, rooms
from threading import Lock
from utils.actions import perform_action
import json

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
            'Donut':url_for('static',filename='images/creatures/Donut.PNG')
        }
    )

#message['data']
@socket.on('log_message_event')
def log_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('log_message_response',
         {'data': message['data'], 'count': session['receive_count']})

#message['data']
@socket.on('broadcast_event')
def log_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('log_message_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

#message['username']
#message['user_id']
@socket.on('username_event')
def test_username_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['username'] = message['username']
    emit('log_message_response',
         {'data': message['username'] + " has joined", 'count': session['receive_count']},
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
    print("__________________")
    print("In Join Function")
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('log_message_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})
    emit('join_response_global', 
            {'username':session['username'], 'user_id':message['user_id']},
            broadcast=True)
    emit('join_response_local')

@socket.on('first_ready')
def first_ready(message):
    print("______________________")
    print("room size of at least 1")
    print("being sent to{}",message['first_id_ready'])
    emit('alert_first_user',{'first_id':message['first_id_ready']}, broadcast=True)


# message['user_id']
# message['character_id']
# message['current_creature_selected']
# message['current_action_selected']
# message['target_user_id']
@socket.on('play_cards')
def play_cards(message):
    #fixme,add sp and passive
    user_health_modifier,target_health_modifier,defense_modifier = perform_action(message['current_action_selected'])
    if(target_health_modifier != 0):
        emit('action_response',{'user_health_modifier':target_health_modifier,'acting_user': message['user_id']},room=message['target_user_id'])
    elif(defense_modifier != 0 ):
        emit('action_response',{'user_health_modifier':user_health_modifier,'defense_modifier':defense_modifier},room=message['user_id'])
    elif(user_health_modifier != 0):
        emit('action_response',{'user_health_modifier':target_health_modifier},room=message['user_id'])
    emit('action_global_response', broadcast=True)

# message['target_user_id']
# message['acting_user_id']
@socket.on('block_damage_event')
def block_damage_event(message):
    emit('block_damage_response', {'acting_user_id': message['acting_user_id'], 'target_user_id': message['target_user_id']},room=message['target_user_id'])


@socket.on('character_chosen')
def character_chosen(message):
    session['character'] = message['character_id']
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('character_chosen_local',
         {'character_id': message['character_id'], 'count': session['receive_count']})
    emit('character_chosen_global',
         {'character_id': message['character_id'], 'user_id': message['user_id'],'count': session['receive_count'],'username':session['username'],'remove_character':message['remove_character']},
         broadcast=True)

@socket.on('start_battle')
def start_battle(message):
    emit('room_battle_start_response',room=message['room'])

@socket.on('calculate_data_event')
def calculate_data(message):
    print("here")
    emit('calculate_data_response')


# message['user_id']
# message['character_id']
# message['current_creature_selected']
# message['current_action_selected']
# message['target_user_id']
@socket.on('action_notice_event')
def action_notice(message):
    emit('action_notice_response',{'acting_user_id':message['user_id'],'target_user_id':message['target_user_id'],'action_performed':message['current_action_selected']},room=message['target_user_id'])
    emit('action_notice_response',{'acting_user_id':message['user_id'],'target_user_id':message['target_user_id'],'action_performed':message['current_action_selected']},room=message['user_id'])

if __name__ == '__main__':
    socket.run(app, debug=True)
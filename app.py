from utils.Gamera import Gamera
from flask import Flask, render_template, session, copy_current_request_context, url_for
from flask_socketio import SocketIO, emit, disconnect, join_room, rooms
from utils.Godzilla import Godzilla
from utils.Soda_Bottle import Soda_Bottle
from utils.Creature import Creature
# from models import db, User, Room
from utils.utils import round_finished, perform_defense
from threading import Lock
import json
import logging

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20),unique=True,nullable=False)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(20),nullable=False)
    current_room = db.Column(db.Integer,db.ForeignKey('room.id'))


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    socket_key = db.Column(db.String(100),unique=True,nullable=False)
    is_open = db.Column(db.Boolean, nullable=False,default=False)
    has_battle_started = db.Column(db.Boolean, nullable=False,default=False)
    users = db.relationship('User',backref='room',lazy=True)

with app.app_context():
    db.create_all()


room = Room.query.filter_by(socket_key='room1').first()
if(room):
    db.session.delete(room)
    db.session.commit()

user = User.query.filter_by(username='michael').first()
if(not user):
    db.session.add(User(username='michael',password='1234567',email="1"))
    db.session.commit()
    db.session.add(User(username='hunter',password='1234567',email="2"))
    db.session.commit()
    db.session.add(User(username='nishan',password='1234567',email="3"))
    db.session.commit()
    db.session.add(User(username='hayden',password='1234567',email="4"))
    db.session.commit()



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

#message['username']
@socket.on('client_disconnecting')
def client_disconnecting(message):
    print("client is disconnecting: ")
    print( message['username'])

#message['username']
#message['user_id']
@socket.on('connect_response')
def connect(message):
    if(message["username"]):
        session['username'] = message['username']
    session["user_id"] = message["user_id"]

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

    emit('log_message_response',
         {'data': message['username'] + " has joined"},
         broadcast=True)
    emit('username_global_response',
         {'username': message['username']},
         broadcast=True)

#message['room']
#message['room_size']
#message['username']
#message['first_username']
#message['users_in_room']
#message['rejoin']
@socket.on('join')
def join(message):
    if('username' not in session):
        session["username"] = message['username']
    session['room'] = message['room']
    room = Room.query.filter_by(socket_key=message['room']).first()
    if(message['rejoin']):
        json_users = [ob.username for ob in room.users]
        emit('rejoin_room',{"users": json_users})
        emit('join_response_local')
    else:
        if(not room):
            room = Room(is_open=True, has_battle_started=False,socket_key=message['room'])
            user = User.query.filter_by(username=session['username'].lower()).first()
            user.current_room = message['room']
            db.session.commit() #need to commmit but not just add for a new user
            room.users.append(user)
            db.session.add(room)
            db.session.commit()
        join_room(message['room'])
        emit('log_message_response',
            {'data': 'In rooms: ' + ', '.join(rooms())})
        emit('join_response_global', 
                {'username':session['username']},
                broadcast=True)
        emit('join_response_local')

# message['room']
@socket.on('populate_existing_room_data')
def populate_existing_room_data(message):
    room = Room.query.filter_by(socket_key=message['room']).first()

# message['num_in_room']
@socket.on('num_in_room')
def num_in_room(message):
    session['num_in_room'] = message['num_in_room']

@socket.on('first_ready')
def first_ready(message):
    emit('alert_first_user',{'first_id':message['first_id_ready']}, broadcast=True)

# message['remove_character']
# message['character_id']
# message['username']
@socket.on('character_chosen_event')
def character_chosen_event(message):
    session['stage1_cards_played'] = 0
    session['stage2_cards_played'] = 0
    emit('character_chosen_local',
         {'character_id': message['character_id'], 'username': message['username']})
    emit('character_chosen_global',
         {'character_id': message['character_id'], 'username': message['username'],'username':session['username'],'remove_character':message['remove_character']},
         broadcast=True)

# session variable will be given a user Creature pair here, this will determine how the local will keep track of global changes
# message['character_id']
# message['username'] 
@socket.on('character_chosen_event_session')
def character_chosen_event_session(message):
    username = message['username']
    char_id = message['character_id']
    if(char_id == 'Godzilla'):
        session[username] = Godzilla(username)
    elif(char_id == 'SodaBottle'):
        session[username] = Soda_Bottle(username)
    elif(char_id == 'Gamera'):
        session[username] = Gamera(username)


@socket.on('start_battle')
def start_battle(message):
    emit('room_battle_start_response',room=message['room'])

# message['action']
# message['target_username']
# message['target_creature']
# message['username']
# message['user_creature']
@socket.on('local_action_event')
def local_action_event(message):
    emit('local_action_response',message, room=session['room'])

@socket.on('global_action_event')
def global_action_event(message):

    action = message['action']
    target = message['target_username']
    username = message['username']
    if(action == 'defend'):
        session[username].defend(target)
    elif(action == 'heal'):
        session[username].heal(target)
    elif(action == 'attack'):
        session[username].attack(target)
    elif(action == 'sp'):
        session[username].sp(target)

    session['stage1_cards_played'] += 1
    if(session['stage1_cards_played'] == session['num_in_room']):
        session['stage1_cards_played'] = 0
        socket.emit('stage1_response',message,room=session['username'])

#perform defensive actions here, everyone has full state up to date local map of actions
#every event is calculated locally and no need for propagation
@socket.on('stage1_finished_event')
def stage1_finished_event():
    perform_defense()
    # the below code will need to be moved as more cards are added and more stages are available
    hp_message = round_finished()
    socket.emit('round_finished',hp_message,room=session['user_id'])    


if __name__ == '__main__':
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)
    socket.run(app, debug=False)
    
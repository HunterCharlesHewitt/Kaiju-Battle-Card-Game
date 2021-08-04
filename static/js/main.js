

var socket = io();

$(document).ready(function() {

    console.log("here")
    if(localStorage.getItem("username")){
        if(!localStorage.getItem("in_room") && localStorage.getItem("in_game") != "true") {
            $('#username').hide();
            $('#join').show();
        }
        else if (localStorage.getItem("in_room") && localStorage.getItem("in_game") != "true") {
            $('#username').hide();
            socket.emit('join',{room:localStorage.getItem("in_room"),username:localStorage.getItem("username"),rejoin:true,'socket_id':socket.id,'in_game':false})      
            character_id = localStorage.getItem("character_id")
        }
        else if (localStorage.getItem("in_room") && localStorage.getItem("in_game") == "true"){
            $('#username').hide();
            socket.emit('join',{room:localStorage.getItem("in_room"),username:localStorage.getItem("username"),rejoin:true,'socket_id':socket.id,'in_game':true})      
            socket.emit('rejoin_battle_event',{username:localStorage.getItem("username"),room:localStorage.getItem("in_room")})
        }

    }

    $('.creatureButton').hover(creature_hover_enter, creature_hover_exit);
    
    //global information
    socket.room = [];
    socket.username_to_character = {}; //should be username to character
    socket.username_to_hp = {}; //username to hp
    socket.character_to_username = {}; //character to username
    socket.stage1_cards_played = 0;
    socket.global_round_actions = [];



    //local information
    socket.character;
    socket.removeCharacter = null;
    socket.hp;
    socket.attackers = [];
    socket.action_selected;
    socket.target_creature_selected;
    socket.in_room = false;

//__________________connect.js__________________________________
    $('form#broadcast').submit(broadcast);
    $('#logout').click(function() {
        localStorage.clear()
        location.reload()
    })
    $('#leaveRoom').click(function() {
        localStorage.removeItem("character_id")
        localStorage.removeItem("in_room")
        localStorage.removeItem("in_game")
        location.reload()
    })
    socket.on('connect',connect);
    socket.on('log_message_response', log_message_response);

//__________________choose_username.js___________________________
    $('form#username').submit(submit_username);
    socket.on('username_global_response',username_global_response)


//__________________join_room.js_________________________________
    $('form#join').submit(submit_join_room);
    socket.on('join_response_global', join_response_global)  
    socket.on('rejoin_room',rejoin_room)
    socket.on('join_response_local', join_response_local);


//__________________choose_character.js____________________________
    $('.creatureButton').click(choose_character_button);
    socket.on('character_chosen_local', character_chosen_local)
    socket.on('character_chosen_global', character_chosen_global)

//__________________start_battle.js________________________________
    $('form#startBattle').submit(submit_start_battle);
    socket.on('rejoin_battle_response',rejoin_battle_response)
    socket.on('alert_first_user',alert_first_user_to_start_battle);
    socket.on('room_battle_start_response',room_battle_start_response);

//__________________action.js______________________________________
    $('.actionButton').click(choose_action)
    $('#userButton').on('click','.creatureSelectButton',choose_target);
    $('#playCards').submit(play_cards)
    socket.on('local_action_response', local_action_response)
    socket.on('stage1_response', stage1_response)
    socket.on('round_finished', round_finished)
});

window.onbeforeunload = function () {
    socket.emit('client_disconnecting', {'username':localStorage.getItem('username')});
}
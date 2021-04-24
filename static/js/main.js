

var socket = io();

$(document).ready(function() {

    socket.room = [];
    socket.character;
    socket.removeCharacter = null;
    socket.hp;
    socket.round_defense = 0;
    socket.charge = 0;
    socket.round_damage = 0;
    socket.cards_played = 0;
    socket.first_attacker;
    socket.id_to_username = {};
    socket.id_to_character = {};
    socket.character_to_id = {};
    socket.character_to_id = {};
    socket.current_action_selected;
    socket.current_creature_selected;
    socket.current_creature_playing;
    socket.in_room = false;

//__________________connect.js__________________________________
    $('form#broadcast').submit(broadcast);
    socket.on('connect',connect);
    socket.on('log_message_response', log_message_response);

//__________________choose_username.js___________________________
    $('form#username').submit(submit_username);
    socket.on('username_global_response',username_global_response)

//__________________join_room.js_________________________________
    $('form#join').submit(submit_join_room);
    socket.on('join_response_global', join_response_global)  
    socket.on('join_response_local', join_response_local);


//__________________choose_character.js____________________________
    $('.creatureButton').click(choose_character_button);
    socket.on('character_chosen_local', character_chosen_local)
    socket.on('character_chosen_global', character_chosen_global)

//__________________start_battle.js________________________________
    $('form#startBattle').submit(submit_start_battle);
    socket.on('alert_first_user',alert_first_user_to_start_battle);
    socket.on('room_battle_start_response',room_battle_start_response);

//__________________action.js______________________________________
    $('.actionButton').click(choose_action)
    $('#userButton').on('click','.creatureSelectButton',choose_target);
    $('#playCards').submit(play_cards)
    socket.on('action_response',action_response)
    socket.on('action_notice_response',action_notice_response)
    socket.on('action_global_response',action_global_response)
    socket.on('calculate_data_response',calculcate_data_response)
    socket.on('block_damage_response',block_damage_response)
});
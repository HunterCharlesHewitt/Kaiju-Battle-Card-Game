

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

//__________________choose_username.js___________________________

    $('form#username').submit(submit_username);

    //msg.user_id
    //msg.username
    socket.on('username_global_response',username_global_response)




//__________________join_room.js_________________________________
    
    $('form#join').submit(submit_join_room);

    //msg.username
    //msg.user_id
    socket.on('join_response_global', join_response_global)  

    socket.on('join_response_local', join_response_local);



//__________________choose_character.js____________________________

    socket.on('character_chosen_local', character_chosen_local)

    socket.on('character_chosen_global', character_chosen_global)



    //msg.acting_user_id
    //msg.target_user_id
    //msg.action_performed
    socket.on('action_notice_response',function(msg,cb) {
        console.log(msg)
        $('body').append('<br>'+'<p class=hidden actionNotice> logs #' + socket.id_to_username[msg.acting_user_id] + ' performed ' + socket.id_to_username[msg.action_performed] +' on' + msg.target_user_id+ '. Your hp is' + socket.hp + '</p>');
    })
    
    // msg.user_health_modifier
    // msg.defense_modifier
    // msg.acting_user
    socket.on('action_response',function(msg){
        console.log("action from " + socket.id_to_username[msg.acting_user])
        console.log("health: " + msg.user_health_modifier)
        console.log("defense: " + msg.defense_modifier)

        if(msg.user_health_modifier >= 0) {
            console.log("here")
            socket.hp += msg.user_health_modifier;
        }
        else {
            console.log("here")
            socket.round_damage += msg.user_health_modifier;
            socket.first_attacker = msg.acting_user;
            console.log(socket.first_attacker)
        }

        if(msg.defense_modifier) {
            console.log(msg.defense_modifier)
            console.log(socket.round_defense)
            socket.round_defense += msg.defense_modifier
        }
    })

    //msg.target_user_id
    //msg.acting_user_id
    socket.on('block_damage_response',function(msg) {
        socket.hp -= 1;
        console.log("You take one damage from" + socket.id_to_username[msg.acting_user_id])
        console.log(socket.hp)
    })

    socket.on('calculate_data_response',function(){
        if(socket.first_attacker && socket.round_defense > 0) {
            console.log(socket.round_damage)
            console.log(socket.round_defense)
            socket.hp += (socket.round_damage + socket.round_defense)
            console.log("sending block damage")
            console.log("first attacker" + socket.first_attacker)
            console.log("sent by" + socket.id)
            socket.emit('block_damage_event',{'target_user_id': socket.first_attacker, 'acting_user_id':socket.id})
        }
        else if(socket.round_damage != 0) {
            socket.hp += (socket.round_damage)
        }
        $("p").show();
        socket.current_action_selected = "";
        socket.current_creature_selected = "";
        console.log(socket.id)
        console.log(socket)
        console.log(socket.hp)
    })

    socket.on('action_global_response',function(msg){
        socket.cards_played += 1;
        if(socket.cards_played == socket.room.length) {
            socket.cards_played = 0
            $('#userButton .creatureSelectButton').css('background-color','')
            $('#userButton .creatureSelectButton').attr('disabled','disabled')
            $('.actionButton').attr('disabled','disabled')
            $('.actionButton').css('background-color','unset')
            $('#playCards').hide()
            console.log("ready for calculations")
            socket.emit('calculate_data_event',{})
        }
        
    })

    socket.on('room_battle_start_response',function() {
        console.log("room battle start")
        console.log("__________________")
        $('#startBattle').hide()
        $('#header').hide()
        $('.creatureButton').hide()
        $('#waiting').hide()
        $('.battle').show()
        socket.room.forEach(function(item,index) {
            innerItem = socket.id_to_character[item]
            $('#userButton').append(`<button id="${innerItem + "SelectButton"}" class="creatureSelectButton">${innerItem}</button>`)
        })
    });


    socket.on('alert_first_user',function(msg,cb) {
        console.log(socket.id)
        if(msg.first_id == socket.id)
        {
            console.log(socket.id)
            $('#startBattle').show()
        }
        $('#waiting').hide()
        if (cb)
            cb();
    });

    socket.on('connect', function() {
        socket.emit('log_message_event', {data: 'connected to the SocketServer...'});
    });

    socket.on('log_message_response', function(msg, cb) {
        $('#log').append('<br>' + $('<div/>').text('logs #' + msg.count + ': ' + msg.data).html());
        if (cb)
            cb();
    });





    $('form#broadcast').submit(function(event) {
        socket.emit('broadcast_event', {data: $('#broadcast_data').val()});
        return false;
    });



    $('form#startBattle').submit(function(event) {
        socket.emit('start_battle',{'room':'room1'})
        return false;
    });

    //this defines that all button clicks perform this event
    $('.creatureButton').click(function(event) {
        id_str = $(this).attr('id');
        if(socket.character){
            socket.removeCharacter = socket.character
        }
        socket.character = id_str;
        
        //FIXME
        socket.hp = 20
        socket.emit('character_chosen', {'character_id': $(this).attr('id'), 'user_id': socket.id, 'remove_character': socket.removeCharacter});
        return false;
    });

    $('#playCards').submit(function(event){
        socket.current_creature_playing = socket.id_to_character[socket.id]
        socket.emit('play_cards',{'user_id':socket.id, 'character_id' : socket.current_creature_playing, 
            'target_user_id' : socket.character_to_id[socket.current_creature_selected],
            'current_creature_selected':socket.current_creature_selected, 
            'current_action_selected':socket.current_action_selected})
        $('#playCards').hide();
        $('#waiting').show()
        socket.emit('action_notice_event',{'user_id':socket.id, 'character_id' : socket.current_creature_playing, 
            'target_user_id' : socket.character_to_id[socket.current_creature_selected],
            'current_creature_selected':socket.current_creature_selected, 
            'current_action_selected':socket.current_action_selected})
        return false;
    })

    $('.actionButton').click(function(event){
        console.log('action button')
        socket.current_action_selected = $(this).attr('id');
        $('.actionButton').css('background-color','unset')
        $(this).css('background-color','SeaGreen');
        if(socket.current_action_selected && socket.current_creature_selected)
        {
            $('#playCards').show();
        }
        return false;
    })

    $('#userButton').on('click','.creatureSelectButton',function(event){
        console.log($(this).attr('id'))
        console.log("creature select")
        socket.current_creature_selected = $(this).attr('id').replace('SelectButton','');
        $('#userButton .creatureSelectButton').css('background-color','')
        $(this).css('background-color','SeaGreen');
        if(socket.current_action_selected && socket.current_creature_selected)
        {
            $('#playCards').show();
        }
        return false;
    });


});
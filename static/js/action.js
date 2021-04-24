play_cards = function(event){
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
}

choose_action = function(event){
    console.log('action button')
    socket.current_action_selected = $(this).attr('id');
    $('.actionButton').css('background-color','unset')
    $(this).css('background-color','SeaGreen');
    if(socket.current_action_selected && socket.current_creature_selected)
    {
        $('#playCards').show();
    }
    return false;
}

choose_target = function(event){
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
}


//msg.acting_user_id
//msg.target_user_id
//msg.action_performed
action_notice_response = function(msg,cb) {
    console.log(msg)
    $('body').append('<br>'+'<p class=hidden actionNotice> logs #' + socket.id_to_username[msg.acting_user_id] + ' performed ' + socket.id_to_username[msg.action_performed] +' on' + msg.target_user_id+ '. Your hp is' + socket.hp + '</p>');
}

// msg.user_health_modifier
// msg.defense_modifier
// msg.acting_user
action_response = function(msg){
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
}

//msg.target_user_id
//msg.acting_user_id
block_damage_response = function(msg) {
    socket.hp -= 1;
    console.log("You take one damage from" + socket.id_to_username[msg.acting_user_id])
    console.log(socket.hp)
}

calculate_data_response = function(){
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
}

action_global_response = function(msg){
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
    
}
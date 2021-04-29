play_cards = function(event){
    socket.current_creature_playing = socket.id_to_character[socket.id]
    socket.emit('play_cards',{'user_id':socket.id, 'character_id' : socket.current_creature_playing, 
        'target_user_id' : socket.character_to_id[socket.current_creature_selected],
        'current_creature_selected':socket.current_creature_selected, 
        'current_action_selected':socket.current_action_selected})

    socket.emit('action_notice_event',{'user_id':socket.id, 'character_id' : socket.current_creature_playing, 
        'target_user_id' : socket.character_to_id[socket.current_creature_selected],
        'current_creature_selected':socket.current_creature_selected, 
        'current_action_selected':socket.current_action_selected})

    $('#playCards').hide();
    $('#waiting').show()
    $('#userButton .creatureSelectButton').css('background-color','')
    $('#userButton .creatureSelectButton').attr('disabled','disabled')
    $('.actionButton').attr('disabled','disabled')
    $('.actionButton').css('background-color','unset')
    return false;
}

choose_action = function(event){
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
    socket.emit('log_message_event', {data : socket.id_to_character[msg.acting_user_id] + ' performed ' +  msg.action_performed + ' on ' + socket.id_to_character[msg.target_user_id] + '.'});
    if (cb)
        cb();
}

// msg.heal_health_modifier
// msg.damage_health_modifier
// msg.defense_modifier
// msg.acting_user
// msg.action
action_response = function(msg){
    console.log("action from " + socket.id_to_username[msg.acting_user])
    console.log("heal health: " + msg.heal_health_modifier)
    console.log("damage health: " + msg.damage_health_modifier)
    console.log("defense: " + msg.defense_modifier)
    
    msg.defense_modifier = msg.defense_modifier != null ? msg.defense_modifier : 0
    msg.heal_health_modifier = msg.heal_health_modifier != null ? msg.heal_health_modifier : 0
    msg.damage_health_modifier = msg.damage_health_modifier != null ? msg.damage_health_modifier : 0

    if(msg.action)
        console.log("action: " + msg.action) 

    if(msg.damage_health_modifier < 0)
        socket.attackers.push(msg.acting_user)

    socket.round_damage += msg.damage_health_modifier

    socket.round_defense += msg.defense_modifier

    socket.hp += msg.heal_health_modifier

    console.log("round damage: " + socket.round_damage)
    console.log("round defense: " + socket.round_defense)
    console.log("hp: " + socket.hp)
    
}

passive_response = function(msg){

}

//msg.target_user_id
//msg.acting_user_id
block_damage_response = function(msg) {
    socket.hp -= 1; //fixme make this potential hp
    socket.emit('log_message_event', {data : "You take one block damage from " + socket.id_to_character[msg.acting_user_id]});
    socket.emit('log_message_event', {data : 'Your HP is ' + socket.hp});
}

calculate_data_response = function(){
    console.log("calculating data")
    if(socket.attackers && socket.attackers.length > 0 && socket.round_defense > 0) {
        socket.hp += (socket.round_damage + socket.round_defense)
        socket.emit('block_damage_event',{'target_user_id': socket.attackers[0], 'acting_user_id':socket.id})
    }
    else if(socket.round_damage != 0) {
        socket.hp += (socket.round_damage)
    };
    console.log(socket.hp)
    console.log(socket.character_to_id[socket.current_creature_selected])
    console.log(socket)
    socket.emit('log_message_event', {data : 'Your HP is ' + socket.hp});
    socket.emit("hp_event",{'user_id':socket.id,'hp':socket.hp})
}

post_passive_calculate_data_response = function() {

}

// msg.user_id
// msg.hp
passive_response =function(msg){
    console.log("passive response")
    socket.current_action_selected = null
    socket.current_creature_selected = null
    $('#userButton .creatureSelectButton').removeAttr('disabled');
    $('.actionButton').removeAttr('disabled');
    socket.round_defense = 0;
    socket.charge = 0;
    socket.round_damage = 0;
    socket.cards_played = 0;
    socket.attackers = [];
    $('#hpSpan'+socket.id).text(socket.hp)
}


// msg.user_health_modifier
// msg.defense_modifier
// msg.acting_user
// msg.target_user
action_global_response = function(msg){
    socket.cards_played += 1;
    if(socket.cards_played == socket.room.length) {
        socket.cards_played = 0
        socket.emit('calculate_data_event',{})
        socket.emit('passive_event',{'user_id':socket.id, 'character_id' : socket.current_creature_playing, 
        'target_user_id' : socket.character_to_id[socket.current_creature_selected],
        'current_creature_selected':socket.current_creature_selected, 
        'current_action_selected':socket.current_action_selected,
        'first_attacker':socket.attackers[0]})
    }
}


// msg.fizz_points
// msg.acting_user
soda_bottle_sp_fizz_response = function(msg){
    socket.soda_bottle_fizz_points += (msg.fizz_points)
    console.log("fizz points:" + socket.soda_bottle_fizz_points)
}
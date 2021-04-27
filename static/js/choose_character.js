choose_character_button = function(event) {
    id_str = $(this).attr('id');
    if(socket.character){
        socket.removeCharacter = socket.character
    }
    socket.character = id_str;
    
    //FIXME
    socket.hp = 20
    socket.emit('character_chosen', {'character_id': $(this).attr('id'), 'user_id': socket.id, 'remove_character': socket.removeCharacter});
    return false;
}

character_chosen_local = function(msg,cb) {
    $('#header').html((msg.character_id + " chosen"));
    if (cb)
        cb();
}


character_chosen_global =  function(msg,cb) {
    $('#'+msg.character_id).attr('disabled','disabled');
    $('#'+msg.character_id).css('background','radial-gradient(circle, #423f3f, #080303)')

    socket.character_to_id[msg.character_id] = msg.user_id

    socket.id_to_character[msg.user_id] = (msg.character_id)

    socket.id_to_hp[msg.user_id] = 20

    if(msg['remove_character'] != null) {
        $('#'+msg['remove_character']).removeAttr('disabled')
        $('#'+msg['remove_character']).css('background','radial-gradient(circle, #8b0000, #8b0000)')
    }

    var first_user_ready;
    if(socket.room.length > 0 && socket.id_to_character && Object.keys(socket.id_to_character).length > 1)
    {
            first_user_ready = socket.room[0]
            var stringRoom = JSON.stringify(socket.room);
            socket.emit('first_ready', {'room': 'room1','room_size': socket.room.length, 'id': socket.id, 'first_id_ready': first_user_ready,'users_in_room':stringRoom});
    }

    if(socket.in_room) {
        $('#usersInRoom').removeClass("hidden")
        $('#usersInRoom').html("")
        socket.room.forEach(function(item,index) {
            if(socket.id_to_character[item])
            {
                var string = '<li syle="visibility:visible">';
                string += socket.id_to_username[item] + ": ";
                innerItem = socket.id_to_character[item]
                string += (innerItem + (" (hp: <span id=hpSpan"+item+'>'+socket.hp+"</span>) "));
                string += '</li>';
                $('#usersInRoom').append(string);
            }
        });

    }
    $('#log').append('<br>' + $('<div/>').text('logs #' + msg.count + ': '+ msg.username + " has chosen " + msg.character_id).html());
    if (cb)
        cb();
}
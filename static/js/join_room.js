
//msg.username
join_response_global = function(msg,cb) {
    if(!socket.room.includes(msg.username.toLowerCase())) {
        socket.room.push(msg.username.toLowerCase())
        socket.emit('num_in_room',{'num_in_room': socket.room.length })
    }
    if (cb)
        cb();
}

//msg.users
join_response_local = function(msg) {
    $('.creatureButton').show()
    $('.creatureButton').colorList()
    $('#join').hide()
    $('#waiting').show();
    console.log(msg)
    for(var username in msg.users) { 
        socket.room.push(username)

        console.log(username)
        $('#'+users[username]).attr('disabled','disabled');
        $('#'+users[username]).css('background','radial-gradient(circle, #423f3f, #080303)')
        
        socket.character_to_username[users[username]] = username

        socket.username_to_character[username] = users[username]
    
        socket.username_to_hp[username] = 20
    }

}

rejoin_room = function(msg) {
    console.log(msg)
    users = msg['users']
    console.log(users)
    //generalize below code into a function
    for(var username in users) { 
        socket.room.push(username)

        console.log(username)
        $('#'+users[username]).attr('disabled','disabled');
        $('#'+users[username]).css('background','radial-gradient(circle, #423f3f, #080303)')
        
        socket.character_to_username[users[username]] = username

        socket.username_to_character[username] = users[username]
    
        socket.username_to_hp[username] = 20
    }

    $('#usersInRoom').removeClass("hidden")
    $('#usersInRoom').html("")
    socket.room.forEach(function(item,index) {
        if(socket.username_to_character[item])
        {
            var string = '<li syle="visibility:visible;">';
            string += item + ": ";
            innerItem = socket.username_to_character[item]
            string += (innerItem + (" (hp: <span style='font-size: x-large!important' id=hpSpan"+item+'>'+socket.username_to_hp[item]+"</span>) "));
            string += '</li>';
            $('#usersInRoom').append(string);
        }
    });
}

submit_join_room = function(event) {
    localStorage.setItem("in_room","room1")
    socket.in_room = true;
    var first_user_ready;
    roomLength = socket.room ? socket.room.size : 0; 
    if(roomLength > 0)
    {
            first_user_ready = socket.room[0]
    }
    var stringRoom = JSON.stringify(socket.room);
    socket.emit('join', {rejoin:false,'room': 'room1','room_size': roomLength, 'username': localStorage.getItem("username"), 'first_username': first_user_ready,'users_in_room':stringRoom,'socket_id':socket.id,'in_game':false});
    return false;
}
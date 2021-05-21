
//msg.username
//msg.user_id
join_response_global = function(msg,cb) {
    socket.room.push(msg.user_id)
    socket.emit('num_in_room',{'num_in_room': socket.room.length } )
    if (cb)
        cb();
}

join_response_local = function() {
    $('.creatureButton').show()
    $('.creatureButton').colorList()
    $('#join').hide()
    $('#waiting').show();
}

submit_join_room = function(event) {
    socket.in_room = true;
    var first_user_ready;
    roomLength = socket.room ? socket.room.size : 0; 
    if(roomLength > 0)
    {
            first_user_ready = socket.room[0]
    }
    var stringRoom = JSON.stringify(socket.room);
    socket.emit('join', {'room': 'room1','room_size': roomLength, 'user_id': socket.id, 'first_user_id': first_user_ready,'users_in_room':stringRoom});
    return false;
}
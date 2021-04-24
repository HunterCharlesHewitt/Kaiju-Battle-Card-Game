
//msg.username
//msg.user_id
join_response_global = function(msg,cb) {
    console.log("join_response")
    socket.room.push(msg.user_id)
    console.log(socket)
    if (cb)
        cb();
}

join_response_local = function() {
    console.log("join response local")
    $('.creatureButton').show()
    $('.creatureButton').colorList()
    $('#join').hide()
    $('#waiting').show();
}

submit_join_room = function(event) {
    console.log("form join")
    socket.in_room = true;
    var first_user_ready;
    roomLength = socket.room ? socket.room.size : 0; 
    if(roomLength > 0)
    {
            console.log("room size of at least one")
            first_user_ready = socket.room[0]
            console.log(socket.room)
    }
    var stringRoom = JSON.stringify(socket.room);
    socket.emit('join', {'room': 'room1','room_size': roomLength, 'user_id': socket.id, 'first_user_id': first_user_ready,'users_in_room':stringRoom});
    return false;
}
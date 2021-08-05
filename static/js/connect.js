connect = function() {
    socket.emit('log_message_event', {data: 'connected to the SocketServer...'});
    username = null
    if(localStorage.getItem("username")){
        username = localStorage.getItem("username")
    } 
    socket.emit('connect_response',{user_id:socket.id, username:username})
}

log_message_response = function(msg, cb) {
    $('#log').append('<br>' + $('<div/>').text('logs: ' + msg.data).html());
    if (cb)
        cb();
}

broadcast = function(event) {
    socket.emit('broadcast_event', {data: $('#broadcast_data').val()});
    return false;
}

leave_room = function(msg,cb) {
    socket.emit('leave_room_event', {username: localStorage.getItem("username"), room: localStorage.getItem("in_room")})
    socket.room = []
    socket.username_to_character = {}
    socket.username_to_hp = {}
    socket.character_to_user = {}
    socket.attackers = []
    localStorage.removeItem("character_id")
    localStorage.removeItem("in_room")
    localStorage.removeItem("in_game")
    location.reload()

    if (cb)
        cb();
}

//msg.username
leave_room_global = function(msg,cb) {
    socket.room = socket.room.filter(item => item !== msg.username)
    console.log(socket.room)
    $('#'+msg['username']).removeAttr('disabled')
    $('#'+msg['username']).css('background','radial-gradient(circle, #8b0000, #8b0000)')
    delete socket.character_to_username[socket.username_to_character[msg.username]]
    delete socket.username_to_character[msg.username]
    delete socket.username_to_hp[msg.username]
    
    if(cb)
        cb();
}
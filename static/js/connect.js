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
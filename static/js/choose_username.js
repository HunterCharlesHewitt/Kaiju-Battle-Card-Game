

username_global_response = function(msg,cb) {
    socket.id_to_username[msg.user_id] = msg.username
    if (cb)
        cb();
}

submit_username = function(event) {
    console.log("here")
    socket.username = $('#username_data').val()
    socket.id_to_username[socket.id] = socket.username 
    socket.emit('username_event', {'username': $('#username_data').val(),'user_id':socket.id});
    $('#username').hide();
    $('#join').show();
    return false;
}
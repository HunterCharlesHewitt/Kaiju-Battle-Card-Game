
//msg.user_id
//msg.username
username_global_response = function(msg,cb) {
    if (cb)
        cb();
}

submit_username = function(event) {
    
    socket.username = $('#username_data').val()
    document.cookie = "username=" + socket.username;
    socket.emit('username_event', {'username': $('#username_data').val(),'user_id':socket.id});
    $('#username').hide();
    $('#join').show();
    return false;
}
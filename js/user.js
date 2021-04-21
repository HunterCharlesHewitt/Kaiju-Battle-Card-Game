function() {
    $('form#username').submit(function(event) {
        console.log("here")
        socket.nickname = $('#username_data').val()
        socket.emit('username_event', {data: $('#username_data').val()});
        return false;
    });
}
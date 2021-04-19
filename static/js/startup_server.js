var namespace = '/test';
var socket = io(namespace);

$(document).ready(function() {

    socket.on('connect', function() { socket.emit('my_event', {data: 'connected to the SocketServer...'});});

    socket.on('my_response', appendLog );

    socket.on('character_chosen_local', localCharacterSelect)

    socket.on('character_chosen_global', globalCharacterSelect)

    $('form#broadcast').submit(callBroadcast);

    $('form#username').submit(saveUsername);

    $('button').click(saveUsername)

});

var callBroadcast = function(event) {
    socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
    return false;
}

var saveUsername = function(event) {
    console.log("here")
    socket.nickname = $('#username_data').val()
    console.log(socket.nickname)
    socket.emit('username_event', {data: $('#username_data').val()});
    $('#username').html("");
    $('.creature').css("visibility","visible")
    
    return false;
}

var appendLog = function (msg, cb) {
    $("#log").append(
        "<br>" +
        $("<div/>")
            .text("logs #" + msg.count + ": " + msg.data)
            .html()
    );
    if (cb) cb();
};

var globalCharacterSelect = function (msg, cb) {
    $("#" + msg.data).attr("disabled", "disabled");

    $("#log").append(
        "<br>" +
        $("<div/>")
            .text(
                "logs #" + msg.count + ": " + msg.username + " has chosen " + msg.data
            )
            .html()
    );
    if (cb) cb();
};

var localCharacterSelect = function(id,cb) {
    $('#header').html((id.data + " chosen"));
    $('#start').css("visibility","visible")
    socket.character = id.data;
    if (cb)
        cb();
}


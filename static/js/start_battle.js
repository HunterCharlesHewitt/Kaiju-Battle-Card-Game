submit_start_battle = function(event) {
    socket.emit('start_battle',{'room':'room1'})
    return false;
}

alert_first_user_to_start_battle = function(msg,cb) {
    console.log(socket.id)
    if(msg.first_id == socket.id)
    {
        console.log(socket.id)
        $('#startBattle').show()
    }
    $('#waiting').hide()
    if (cb)
        cb();
}


room_battle_start_response = function() {
    console.log("room battle start")
    console.log("__________________")
    $('#startBattle').hide()
    $('#header').hide()
    $('.creatureButton').hide()
    $('#waiting').hide()
    $('.battle').show()
    socket.room.forEach(function(item,index) {
        innerItem = socket.id_to_character[item]
        $('#userButton').append(`<button id="${innerItem + "SelectButton"}" class="creatureSelectButton">${innerItem}</button>`)
    })
}
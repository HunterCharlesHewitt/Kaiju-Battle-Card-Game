submit_start_battle = function(event) {
    socket.emit('start_battle',{'room':'room1'})
    return false;
}

alert_first_user_to_start_battle = function(msg,cb) {
    if(msg.first_id == localStorage.getItem('username'))
    {
        $('#startBattle').show()
    }
    $('#waiting').hide()
    if (cb)
        cb();
}


room_battle_start_response = function() {
    $('#startBattle').hide()
    $('#header').hide()
    $('.creatureButton').hide()
    $('#waiting').hide()
    $('.battle').show()
    socket.room.forEach(function(item,index) {
        console.log(item)
        innerItem = socket.username_to_character[item]
        $('#userButton').append(`<button id="${innerItem + "SelectButton"}" class="creatureSelectButton">${innerItem}</button>`)
    })
}
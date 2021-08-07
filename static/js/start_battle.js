submit_start_battle = function(event) {
    socket.emit('start_battle',{'room':'room1','users':socket.room})
    return false;
}

alert_first_user_to_start_battle = function(msg,cb) {
    $('#startBattle').show()
    $('#waiting').hide()
    if (cb)
        cb();
}

//msg.username_to_character
//msg.username_to_hp
rejoin_battle_response = function(msg) {
    localStorage.setItem('in_game','true')
    $('#startBattle').hide()
    $('#header').hide()
    $('.creatureButton').hide()
    $('#waiting').hide()
    $('.battle').show()
    console.log(msg)
    console.log(msg.username_to_hp)
    socket.username_to_character = msg.username_to_character
    socket.room = Object.keys(msg.username_to_character)
    socket.username_to_hp = msg.username_to_hp
    socket.room.forEach(function(item,index) {
        console.log(item)
        innerItem = msg.username_to_character[item]
        $('#userButton').append(`<button id="${innerItem + "SelectButton"}" class="creatureSelectButton">${innerItem}</button>`)
    })  
    for(username in msg.username_to_character) {
        $('#hpSpan'+username).text(msg.username_to_hp[username])
        $('#userButton .creatureSelectButton').removeAttr('disabled');
        $('.actionButton').removeAttr('disabled');
    }
}

//TODO pass in users from db here
room_battle_start_response = function() {
    localStorage.setItem('in_game','true')
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
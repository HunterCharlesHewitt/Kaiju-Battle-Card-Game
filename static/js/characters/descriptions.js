
creature_hover_enter = function() {
    $('#centerCardDiv #cardType').creature()
    $('#centerCardDiv #cardImage').image($(this).attr('id'))
    $('#centerCardDiv #cardName').name($(this).html())
    $('#centerCardDiv').show()
}

creature_hover_exit = function() {
    $('#centerCardDiv').hide()
}


jQuery.fn.creature = function() {
    return this.html("Creature");
};

jQuery.fn.image = function(id) {
    return $(this).attr("src",img_filenames[id]);
};

jQuery.fn.name = function(str) {
    return $(this).html(str)
};

function init_filenames(data) {
    console.log("init_filenames")
    img_filenames = data;
    console.log(img_filenames)
}

const CHARACTERS = {
    'Godzilla' : {'description': 'Description:','passive':'Passive','sp':'Special Power','image':''},
    'Bard' : {'description': 'Description:','passive':'Passive','sp':'Special Power'}
}

img_filenames = {}
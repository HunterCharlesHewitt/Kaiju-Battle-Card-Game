
creature_hover_enter = function() {
    $('#centerCardDiv #cardType').creature()
    $('#centerCardDiv #cardImage').image($(this).attr('id'))
    $('#centerCardDiv #cardName').name($(this).html())
    $('#centerCardDiv > div > div > div > div.frame-text-box > p.description.ftb-inner-margin').main_description($(this).attr('id'))
    $("#centerCardDiv > div > div > div > div.frame-text-box #passive").passive($(this).attr('id'))
    $("#centerCardDiv > div > div > div > div.frame-text-box > p.description_sp").sp($(this).attr('id'))
    $('#centerCardDiv').show()
}

creature_hover_exit = function() {
    //$('#centerCardDiv').hide()
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

jQuery.fn.main_description = function(str) {
    return $(this).html(CHARACTERS[str].description)
};

jQuery.fn.passive = function(str) {
    return $(this).html(CHARACTERS[str].passive)
};

jQuery.fn.sp = function(str) {
    return $(this).html(CHARACTERS[str].sp)
};

function init_filenames(data) {
    img_filenames = data;
}

const CHARACTERS = {
    'Godzilla' : {'description': 'Description:','passive':'Passive:','sp':'Special Power: Firebreath'},
    'Bard' : {'description': 'Description:','passive':'Passive:','sp':'Special Power: Healing Word'},
    'Beholder':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Paralyze Ray'},
    'Boomhauer':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Dang Ol\' Action Man'},
    'SodaBottle':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Unscrew Lid'},
    'Donut': {'description': 'Description:','passive':'Passive:','sp':'Special Power: Add sprinkles'},   
    'Mothra':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Return'},
    'Gamera':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Shell Hide'},
    'Gamora':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Sacrificial'},
    'Jaeger':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Strength in numbers'},
    'KingKong':{'description': 'Description:','passive':'Passive:','sp':'Special Power:'},
    'Ghedora':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Triumph'},
    'Rogue':  {'description': 'Description:','passive':'Passive:','sp':'Special Power: Sneak Attack'},  
    'Wizard':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Spellbook'},
    'Zombie':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Feast'},
    'MechaGodzilla':{'description': 'Description:','passive':'Passive:','sp':'Special Power: Vivifica'},
}

img_filenames = {}
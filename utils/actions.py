#user_health_modifier, target_health_modifier, defend_modifier

def attack(target_user_id, user_id):
    return [['action_response',{'damage_health_modifier': -5,'heal_health_modifier':0,'acting_user': user_id},target_user_id]]

def defend(target_user_id, user_id):
    return [['action_response',{'damage_health_modifier': 0,'heal_health_modifier':0,'defense_modifier':5,'acting_user': user_id},target_user_id]]

def heal(target_user_id, user_id):
    return [['action_response',{'damage_health_modifier': 0,'heal_health_modifier': 3, 'acting_user': user_id},target_user_id]]

def godzilla_sp(target_user_id, user_id):
    return [
        ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -7, 'acting_user': user_id, 'action':'Godzilla: Fire Breath'},target_user_id],
        ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -2, 'acting_user': user_id, 'action':'Godzilla: Fire Breath'},user_id]
    ]

#FIXME ask michael, does all damage blocked still cause 2 damage to godzilla
#TODO change this to send to a passive response
def godzilla_passive(action_str, target_user_id, user_id):
    if(action_str in ('sp','attack')):
        return [
            ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -2, 'acting_user': user_id, 'action':'Godzilla: Reckless'},target_user_id],
            ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -2, 'acting_user': user_id, 'action':'Godzilla: Reckless'},user_id]
        ]
    return []

def soda_bottle_sp(target_user_id, user_id):
    return [
        ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -7, 'acting_user': user_id, 'action':'Soda Bottle: Unscrew Lid'},target_user_id],
        ['soda_bottle_sp_fizz_response',{'fizz_points': -2, 'acting_user': user_id, 'action':'Soda Bottle: Unscrew Lid'},"broadcast"]
    ]

#TODO change this to send to a passive response
def soda_bottle_passive(first_attacker, user_id,session):
    emit_list = [['soda_bottle_sp_fizz_response',{'fizz_points': 1, 'acting_user': user_id},"broadcast"]]
    session['fizz_points'] += 1
    print(session['hp'])
    if(session['hp'] and session['hp'] <= 1 and first_attacker != ""): #FIXME this should actually be based off of future_hp
        emit_list = [*emit_list,['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -1*session['fizz_points'], 'acting_user': user_id},first_attacker],
                    ['soda_bottle_sp_fizz_response',{'fizz_points': -1*session['fizz_points'], 'acting_user': user_id},"broadcast"]]
        session['fizz_points'] = 0
    return emit_list

def perform_action(action_str, character_id, target_user_id, user_id, session):

    if(action_str == 'attack'):
        return attack(target_user_id, user_id)

    elif(action_str == 'defend'):
        return defend(target_user_id, user_id)

    elif(action_str == 'heal'):
        return heal(target_user_id, user_id)

    elif(action_str == 'sp'):
        if(character_id == 'Godzilla'):
            return godzilla_sp(target_user_id, user_id)

        if(character_id == 'SodaBottle'):
            return soda_bottle_sp(target_user_id, user_id)

def perform_passive(action_str,character_id, target_user_id, user_id, first_attacker,session):
    if(character_id == 'Godzilla'):
        return godzilla_passive(action_str, target_user_id, user_id)
    elif(character_id == 'SodaBottle'):
        return soda_bottle_passive(first_attacker, user_id, session)

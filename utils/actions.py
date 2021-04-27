#user_health_modifier, target_health_modifier, defend_modifier

def attack(target_user_id, user_id):
    return [['action_response',{'user_health_modifier': -5,'acting_user': user_id},target_user_id]]

def defend(target_user_id, user_id):
    return [['action_response',{'user_health_modifier': 0,'defense_modifier':5,'acting_user': user_id},target_user_id]]

def heal(target_user_id, user_id):
    return [['action_response',{'user_health_modifier': 3, 'acting_user': user_id},target_user_id]]

def godzilla_sp(target_user_id, user_id):
    return [
        ['action_response',{'user_health_modifier': -7, 'acting_user': user_id},target_user_id],
        ['action_response',{'user_health_modifier': -2, 'acting_user': user_id},user_id]
    ]

#FIXME ask michael, does all damage blocked still cause 2 damage to godzilla
def godzilla_passive(action_str, target_user_id, user_id):
    if(action_str not in ('sp','attack')):
        return [
            ['action_response',{'user_health_modifier': -2, 'acting_user': user_id},target_user_id],
            ['action_response',{'user_health_modifier': -2, 'acting_user': user_id},user_id]
        ]
    return []

def soda_bottle_sp(target_user_id, user_id):
    return [
        ['action_response',{'user_health_modifier': -6, 'acting_user': user_id},target_user_id],
        ['soda_bottle_sp_fizz_response',{'fizz_points': -2, 'acting_user': user_id},"broadcast"] #FIXME implement this response
    ]

def soda_bottle_passive(target_user_id, user_id,session):
    emit_list = [['soda_bottle_sp_fizz_response',{'fizz_points': 1, 'acting_user': user_id},"broadcast"]]
    if(session['hp'] and session['hp'] >= 1):
        emit_list[*,['action_response',{'user_health_modifier': session['fizz_points'], 'acting_user': target_user_id},"broadcast"],
                    ['soda_bottle_sp_fizz_response',{'fizz_points': -1*session['fizz_points'], 'acting_user': user_id},"broadcast"]]
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

def perform_passive(action_str,character_id, target_user_id, user_id, session):
    if(character_id == 'Godzilla'):
        return godzilla_passive(action_str, target_user_id, user_id)
    elif(character_id == 'SodaBottle'):
        return soda_bottle_passive(target_user_id, user_id, session)

#user_health_modifier, target_health_modifier, defend_modifier

# def attack():
#     return 0,-5,0

# def defend():
#     return 0,0,5

# def heal():
#     return 0,3,0

def perform_action(action_str, character_id, target_user_id,user_id):
    emit_list = []
    if(action_str == 'attack'):
        return [['action_response',{'user_health_modifier': -5,'acting_user': user_id},target_user_id]]
    elif(action_str == 'defend'):
        return [['action_response',{'user_health_modifier': 0,'defense_modifier':5,'acting_user': user_id},target_user_id]]
    elif(action_str == 'heal'):
        return [['action_response',{'user_health_modifier': 3, 'acting_user': user_id},target_user_id]]
    elif(action_str == 'sp'):
        if(character_id == 'Godzilla'):
            return [
                    ['action_response',{'user_health_modifier': -7, 'acting_user': user_id},target_user_id],
                    ['action_response',{'user_health_modifier': -2, 'acting_user': user_id},user_id]
                ]
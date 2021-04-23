#user_health_modifier, target_health_modifier, defend_modifier

def attack():
    return 0,-5,0

def defend():
    return 0,0,5

def heal():
    return 0,3,0

def perform_action(action_str):
    print(action_str)
    if(action_str == 'attack'):
        return attack()
    elif(action_str == 'defend'):
        return defend()
    elif(action_str == 'heal'):
        return heal()
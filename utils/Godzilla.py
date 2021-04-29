def attack(target_user_id, user_id):
    return [
            ['action_response',{'damage_health_modifier': -7,'heal_health_modifier':0,'acting_user': user_id},target_user_id],
            ['action_response',{'damage_health_modifier': -7,'heal_health_modifier':0,'acting_user': user_id},user_id]
        ]

class Creature:

    def __init__(self,user_id,hp):
        self.user_id = user_id
        self.hp = hp
        self.round_defense_modifier = 0
        self.round_healing_modifier = 0
        self.round_unblockable_damage_modifier = 0
        self.round_damage_modifier = 0

    def attack(self,target_user_id, user_id):
        return [['action_response',{'damage_health_modifier': -5,'heal_health_modifier':0,'acting_user': user_id},target_user_id]]
    
    def defend(self,target_user_id, user_id):
        return [['action_response',{'damage_health_modifier': 0,'heal_health_modifier':0,'defense_modifier':5,'acting_user': user_id},target_user_id]]

    def heal(self,target_user_id, user_id):
        return [['action_response',{'damage_health_modifier': 0,'heal_health_modifier': 3, 'acting_user': user_id},target_user_id]]

    
    
    
    def end_round():
        self.round_defense_modifier = 0
        self.round_healing_modifier = 0
        self.round_unblockable_damage_modifier = 0
        self.round_damage_modifier = 0        
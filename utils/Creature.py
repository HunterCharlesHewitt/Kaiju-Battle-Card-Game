from utils.actions import *

class Creature:

    def __init__(self,user_id,hp):
        self.user_id =self.user_id
        self.hp = hp
        self.round_defense_modifier = 0
        self.round_healing_modifier = 0
        self.round_unblockable_damage_modifier = 0
        self.round_damage_modifier = 0

    def attack(self,target_user_id):
        send_damage(target_user_id,-5)
        return [['action_response',{'damage_health_modifier': -5,'heal_health_modifier':0,'acting_user':self.user_id},target_user_id]]
    
    def defend(self,target_user_id):
        send_defense(target_user_id,5)
        return [['action_response',{'damage_health_modifier': 0,'heal_health_modifier':0,'defense_modifier':5,'acting_user':self.user_id},target_user_id]]

    def heal(self,target_user_id):
        send_healing(target_user_id,3)
        return [['action_response',{'damage_health_modifier': 0,'heal_health_modifier': 3, 'acting_user':self.user_id},target_user_id]]


    def send_defense(target_user_id, modifier):
        session[target_user_id].round_defense_modifier += modifier

    def send_healing(target_user_id, modifier):
        session[target_user_id].round_healing_modifier += modifier

    def send_damage(target_user_id, modifier):
        session[target_user_id].round_damage_modifier += modifier

    def send_unblockable_damage(target_user_id, modifier):
        session[target_user_id].round_unblockable_damage_modifier += modifier    
    
    
    def end_round():
        self.round_defense_modifier = 0
        self.round_healing_modifier = 0
        self.round_unblockable_damage_modifier = 0
        self.round_damage_modifier = 0        
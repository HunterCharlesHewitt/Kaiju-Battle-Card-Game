from utils.Creature import Creature

class Godzilla(Creature):

    def __init__(self,user_id):
        super().__init__(user_id,20)


    def attack(self,target_user_id, user_id):
        self.round_unblockable_damage_modifier -= 2
        return [
                ['action_response',{'damage_health_modifier': -7,'heal_health_modifier':0,'acting_user': user_id},target_user_id],
                ['action_response',{'damage_health_modifier': -2,'heal_health_modifier':0,'acting_user': user_id},user_id]
            ]

    def defend(self,target_user_id, user_id):
        super.defend(target_user_id, user_id)

    def heal(self,target_user_id, user_id):
        super.heal(target_user_id, user_id)

    def sp(self,target_user_id, user_id):
        self.round_unblockable_damage_modifier -= 4
        return [
                ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -9, 'acting_user': user_id, 'action':'Godzilla: Fire Breath'},target_user_id],
                ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -4, 'acting_user': user_id, 'action':'Godzilla: Fire Breath'},user_id]
        ]

from utils.Creature import Creature

class Godzilla(Creature):

    def __init__(self,user_id):
        super().__init__(user_id,20)


    def attack(self,target_user_id):
        super().send_unblockable_damage(self.user_id, -2)
        super().send_damage(target_user_id, -7)
        return [
                ['action_response',{'damage_health_modifier': -7,'heal_health_modifier':0,'acting_user':self.user_id},target_user_id],
                ['action_response',{'damage_health_modifier': -2,'heal_health_modifier':0,'acting_user':self.user_id},user_id]
            ]

    def defend(self,target_user_id):
        super.defend(target_user_id)

    def heal(self,target_user_id):
        super.heal(target_user_id)

    def sp(self,target_user_id):
        super().send_unblockable_damage(self.user_id, -4)
        super().send_damage(target_user_id, -9)
        return [
                ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -9, 'acting_user':self.user_id, 'action':'Godzilla: Fire Breath'},target_user_id],
                ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -4, 'acting_user':self.user_id, 'action':'Godzilla: Fire Breath'},user_id]
        ]

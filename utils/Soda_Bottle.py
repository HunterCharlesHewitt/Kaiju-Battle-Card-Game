from utils.Creature import Creature

class Soda_Bottle(Creature):

    def __init__(self,user_id):
        super().__init__(user_id,20)
        self.fizz_points = 0

    def attack(self,target_user_id, user_id):
        self.fizz_points += 1
        super.attack(target_user_id, user_id)

    def defend(self,target_user_id, user_id):
        self.fizz_points += 1
        super.defend(target_user_id, user_id)

    def heal(self,target_user_id, user_id):
        self.fizz_points += 1
        super.heal(target_user_id, user_id)

    def sp(target_user_id, user_id):
        self.fizz_points -= 1 #technically subtracting 2 since we don't add one and instead subtract
        return [
            ['action_response',{'heal_health_modifier': 0,'damage_health_modifier': -7, 'acting_user': user_id, 'action':'Soda Bottle: Unscrew Lid'},target_user_id],
            ['soda_bottle_sp_fizz_response',{'fizz_points': -2, 'acting_user': user_id, 'action':'Soda Bottle: Unscrew Lid'},"broadcast"]
        ]
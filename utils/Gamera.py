from utils.Creature import Creature

class Gamera(Creature):

    def __init__(self,user_id):
        super().__init__(user_id,20)

    def attack(self,target_user_id):
        super().attack(self, target_user_id)

    def defend(self,target_user_id):
        super().send_defense(target_user_id,6,2)

    def heal(self,target_user_id):
        super().heal(target_user_id)

    def sp(self,target_user_id):
        super().send_defense(target_user_id,6,0)
        super().send_healing(target_user_id,2)

    def __str__(self):
        string = super().__str__()
        return string + "\n________________________________\n" 
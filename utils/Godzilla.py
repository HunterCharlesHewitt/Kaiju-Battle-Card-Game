from utils.Creature import Creature

class Godzilla(Creature):

    def __init__(self,user_id):
        super().__init__(user_id,20)


    def attack(self,target_user_id):
        super().send_unblockable_damage(self.user_id, -2)
        super().send_damage(target_user_id, -7)

    def defend(self,target_user_id):
        super().defend(target_user_id)

    def heal(self,target_user_id):
        super().heal(target_user_id)

    def sp(self,target_user_id):
        super().send_unblockable_damage(self.user_id, -4)
        super().send_damage(target_user_id, -9)

    def __str__(self):
        string = super().__str__()
        return string + "\n________________________________\n" 
from utils.Creature import Creature

class Godzilla(Creature):

    def __init__(self,username):
        super().__init__(username,20)


    def attack(self,target_username):
        super().send_unblockable_damage(self.username, -2)
        super().send_damage(target_username, -7)

    def defend(self,target_username):
        super().defend(target_username)

    def heal(self,target_username):
        super().heal(target_username)

    def sp(self,target_username):
        super().send_unblockable_damage(self.username, -4)
        super().send_damage(target_username, -9)

    def __str__(self):
        string = super().__str__()
        return string + "\n________________________________\n" 
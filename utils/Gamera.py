from utils.Creature import Creature

class Gamera(Creature):

    def __init__(self,username):
        super().__init__(username,20)

    def attack(self,target_username):
        super().attack(self, target_username)

    def defend(self,target_username):
        super().send_defense(target_username,6,2)

    def heal(self,target_username):
        super().heal(target_username)

    def sp(self,target_username):
        super().send_defense(target_username,6,0)
        super().send_healing(target_username,2)

    def __str__(self):
        string = super().__str__()
        return string + "\n________________________________\n" 
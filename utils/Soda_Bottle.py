from utils.Creature import Creature

class Soda_Bottle(Creature):

    def __init__(self,user_id):
        super().__init__(user_id,20)
        self.fizz_points = 0

    def attack(self,target_user_id):
        self.fizz_points += 1
        super().attack(target_user_id)

    def defend(self,target_user_id):
        self.fizz_points += 1
        super().defend(target_user_id)

    def heal(self,target_user_id):
        self.fizz_points += 1
        super().heal(target_user_id)

    def sp(target_user_id):
        self.fizz_points -= 1 #technically subtracting 2 since we don't add one and instead subtract
        super().send_damage(target_user_id,-7)

    def explode(target_user_id):
        super().send_unblockable_damage(target_user_id, -1*self.fizz_points)
        self.fizz_points = 0

    def __str__(self):
        string = super().__str__()
        return string + "Fizz Points: " + str(self.fizz_points) + "\n________________________________\n" 
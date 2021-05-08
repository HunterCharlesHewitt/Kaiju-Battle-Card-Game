from utils.Creature import Creature

class Soda_Bottle(Creature):

    def __init__(self,user_id):
        super().__init__(user_id,20)
        self.fizz_points = 0
        self.explode_target = None

    def attack(self,target_user_id):
        self.fizz_points += 1
        super().attack(target_user_id)

    def defend(self,target_user_id):
        self.fizz_points += 1
        super().defend(target_user_id)

    def heal(self,target_user_id):
        self.fizz_points += 1
        super().heal(target_user_id)

    def sp(self,target_user_id):
        self.fizz_points -= 2 
        super().send_damage(target_user_id,-7)

    def receive_damage(self, modifier):
        super().receive_damage(modifier)
        self.explode_check()

    def receive_unblockable_damage(self,modifier):
        super().receive_unblockable_damage(modifier)
        self.explode_check()

    def receive_defense(self, modifier):
        super().receive_defense(modifier)
        self.explode_check()

    def receive_healing(self, modifier):
        super().receive_healing(modifier)
        self.explode_check()

    def explode_check(self):
        damage_after_block = min(0,self.round_damage_modifier + self.round_defense_modifier)
        total_round_damage = damage_after_block + self.round_unblockable_damage_modifier + self.round_healing_modifier
        if(self.hp + total_round_damage <= 1 and len(self.round_attackers) > 0):
            self.explode_target = self.round_attackers[-1]
        else:
            self.explode_target = None

    def explode(self):
        super().send_unblockable_damage(self.explode_target, -1*self.fizz_points)
        self.fizz_points = 0

    def __str__(self):
        string = super().__str__()
        return string + "Fizz Points: " + str(self.fizz_points) + "\n________________________________\n" 
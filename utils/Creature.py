from flask import session

class Creature:

    def __init__(self,user_id,hp):
        self.user_id = user_id
        self.hp = hp
        self.round_defense_modifier = 0
        self.round_defense_damage = 0
        self.round_healing_modifier = 0
        self.round_unblockable_damage_modifier = 0
        self.round_damage_modifier = 0
        self.round_attackers = []

    def attack(self,target_user_id):
        self.send_damage(target_user_id,-5)
    
    def defend(self,target_user_id):
        self.send_defense(target_user_id,5,1)

    def heal(self,target_user_id):
        self.send_healing(target_user_id,3)

    def send_defense(self,target_user_id, modifier, dmg_modifier):
        session[target_user_id].receive_defense(modifier, dmg_modifier)

    def send_healing(self,target_user_id, modifier):
        session[target_user_id].receive_healing(modifier)

    def send_damage(self,target_user_id, modifier):
        session[target_user_id].receive_damage(modifier)
        session[target_user_id].round_attackers.append(self.user_id)

    def send_unblockable_damage(self,target_user_id, modifier):
        session[target_user_id].receive_unblockable_damage(modifier)  

    def receive_defense(self,modifier, dmg_modifier):
        self.round_defense_damage += dmg_modifier
        self.round_defense_modifier += modifier
    
    def receive_healing(self,modifier):
        self.round_healing_modifier += modifier

    def receive_damage(self,modifier):
        self.round_damage_modifier += modifier

    def receive_unblockable_damage(self,modifier):
        self.round_unblockable_damage_modifier += modifier

    def __str__(self):
        string = "\n________________________________\n" + self.__class__.__name__ + "\n"
        string += ("User ID: " + str(self.user_id) + '\n')
        string += ("Round Damage Modifier: " + str(self.round_damage_modifier) + '\n')
        string += ("Round Unblockable Damage Modifier: " + str(self.round_unblockable_damage_modifier) + '\n')
        string += ("Round Healing Modifier: " + str(self.round_healing_modifier) + '\n')
        string += ("Round Defense Modifier: " + str(self.round_defense_modifier) + '\n')
        string += ("Current HP Before Modifiers: " + str(self.hp) + '\n')
        return string
    
    
    def end_round(self):
        self.round_defense_modifier = 0
        self.round_defense_damage = 0
        self.round_healing_modifier = 0
        self.round_unblockable_damage_modifier = 0
        self.round_damage_modifier = 0
        self.round_attackers = []     
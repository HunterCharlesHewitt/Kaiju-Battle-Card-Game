
from flask import session
from utils.Godzilla import Godzilla
from utils.Soda_Bottle import Soda_Bottle
from utils.Creature import Creature

def round_finished():

    # this is not optimal for soda bottle explosion, find better way of doing
    for key,creature in session.items():
        if isinstance(creature,Creature):
            if type(creature) is Soda_Bottle:
                if creature.explode_target:
                    creature.explode()

    hp_message = {}

    # also don't need to access through session object, creatures are like bound references in java maybe?
    for key,creature in session.items():
        if isinstance(creature,Creature):
            damage_after_block = min(0,creature.round_damage_modifier + creature.round_defense_modifier)
            total_round_damage = damage_after_block + creature.round_unblockable_damage_modifier + creature.round_healing_modifier
            creature.hp += total_round_damage
            creature.end_round()
            print(creature)
            hp_message[key] = creature.hp

    return hp_message

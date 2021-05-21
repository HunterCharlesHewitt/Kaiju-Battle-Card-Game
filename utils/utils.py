
from flask import session
from utils.Godzilla import Godzilla
from utils.Soda_Bottle import Soda_Bottle
from utils.Creature import Creature

def perform_defense():
    for key,creature in session.items():
        if isinstance(creature,Creature):
            if(creature.round_damage_modifier < 0 and creature.round_defense_modifier > 0):
                if(creature.round_defense_damage == len(creature.round_attackers)):
                    for attacker in creature.round_attackers:
                        session[key].send_unblockable_damage(attacker,-1)
                else:
                    for idx,attacker in creature.round_attackers:
                        session[key].send_unblockable_damage(attacker,(-1)*creature.round_defense_damage // len(creature.round_attackers))
                        if(idx == 0):
                            session[key].send_unblockable_damage(attacker,(-1)*(creature.round_defense_damage % len(creature.round_attackers)))

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
            # print(creature)
            creature.end_round()
            hp_message[key] = creature.hp

    return hp_message

from .skill_roll import SkillRoll
from .ability_die import AbilityDie
from .dice import Dice
from typing import *
from .ranks import dict_faserip, universal_table, faserip_index, column_shift, slam_check
import random

class AttackRoll(SkillRoll):
    def __init__(self, name, ability_die: AbilityDie, damage_dice: Dice, modifier: int = 0):
        super().__init__(ability_die=ability_die, modifier=modifier, success_on_crit=True)
        self.name = name
        self.damage_dice = damage_dice

    def attack(self,
               enemy_ac: int,
               advantage: Optional[int] = None,
               add_ability_to_damage=True,
               munchkin=False) -> int:
        """
        Returns an integer of the damage incurred. 0 is fail.
        If there is a bonus on the damage, alter the ``.damage_dice.bonus`` first.

        :param enemy_ac:
        :param advantage:
        :param add_ability_to_damage:
        :param munchkin: proficiency is not added to damage RAW, however munchkins always do....
        :return:
        """
        attack_roll = self.roll(advantage=advantage)
        if attack_roll >= enemy_ac:
            # note this can allow crit trains, were one to alter the crit value.
            damage_roll = sum([self.damage_dice.roll() for i in range(self.ability_die.crit + 1)])
            if add_ability_to_damage is True:
                damage_roll += self.ability_die.bonus + self.ability_die.temp_modifier
            # proficiency is not added to damage RAW, however munchkins always do.
            if munchkin is True:
                damage_roll += self.ability_die.proficiency.bonus
        else:
            damage_roll = 0
        return damage_roll

    def attackFASERIP(self,
               enemy_ac: int,
               advantage: Optional[int] = None,
               attack_rank: str = None,
               damage_rank: str = None,
               endurance_rank: str = None,
               add_ability_to_damage=False,
               munchkin=False) -> int:
        """
        Returns an integer of the damage incurred. 0 is fail.
        If there is a bonus on the damage, alter the ``.damage_dice.bonus`` first.

        :param enemy_ac:
        :param advantage:
        :param add_ability_to_damage:
        :param munchkin: proficiency is not added to damage RAW, however munchkins always do....
        :return:
        """
        attack_roll = random.randint(1,100)
        #print("ATTACK ROLL:", attack_roll)
        #need slam - endurance check - need opponent endurance for save and opponent armour #could get slammed too far but more complicated using movement and map
        #need stun - endurance check - need opponent endurance for save and opponent armour		
        if attack_roll >= universal_table[attack_rank]['G']:  #dumb basic green roll
            damage_roll = dict_faserip[damage_rank]
            print("HIT!:", attack_roll, damage_rank)
            if attack_roll >= universal_table[attack_rank]['R']:
               print("STUN?", attack_roll, damage_rank)
			   #endurance_roll = random.randint(1,100) 
            elif attack_roll >= universal_table[attack_rank]['Y']:
               if dict_faserip[damage_rank] >= dict_faserip[endurance_rank]:
               #slam eligible #basic version, not accounting for armour or martial arts			   
                   slam_result = slam_check(endurance_rank)
                   print("SLAM?", attack_roll, damage_rank, slam_result)
					#slam_result = 2
                   if slam_result == "Slam":
                       damage_roll = damage_roll + dict_faserip[endurance_rank] + 2
                   elif slam_result == "Grand Slam":
                       damage_roll = damage_roll + dict_faserip[endurance_rank] + faserip_index[endurance_rank]*2 #many areas simulation hack
                   else:
                       pass
				
                       #3if slam_result == "Slam:
				   
					
        else:
            print("MISS!:", attack_roll)
            damage_roll = 0
        return damage_roll  #want to return condition here

    @classmethod  # old input
    def parse_list_attack(cls, attack: list, ability_die):
        # old input. ['club', 2, 0, 4]
        return cls.parse_attack(name=attack[0],
                                ability_die=ability_die,
                                damage_dice=Dice(num_faces=[int(n) for n in attack[3:]], bonus=attack[2]),
                                attack_modifier=attack[1])

    @classmethod
    def parse_attack(cls,
                     name: str,
                     ability_die: AbilityDie,
                     damage_dice: Union[str, Dice],
                     attack_modifier: int):
        """
        Returns an Attack roll

        :param name: name of weapon...
        :param ability_die: generally creature.str ... but dex for finesse weapons or wis for shileyley
        :param damage_dice: a dice obj, str or int.
        :param attack_modifier: the weapon modifier. No proficiency or ability bonus or poison etc.
            these come from the ability_die.
        :return:
        """
        # damage_dice
        if isinstance(damage_dice, Dice):
            pass  # damage_dice is good
        elif isinstance(damage_dice, str):
            damage_dice = Dice.from_notation(damage_dice)
        elif isinstance(damage_dice, int):
            damage_dice = Dice(num_faces=damage_dice)
        else:
            raise KeyError(f'Bad damage dice specified. Please use either notation or actual Dice')
        # return
        return cls(name=name, ability_die=ability_die, damage_dice=damage_dice, modifier=int(attack_modifier))

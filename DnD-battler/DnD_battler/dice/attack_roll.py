from .skill_roll import SkillRoll
from .ability_die import AbilityDie
from .dice import Dice
from typing import *
from .ranks import dict_faserip, universal_table, faserip_index, column_shift, slam_check, stun_check, kill_check, roll_faserip
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
        Unused in FASERIP-Slugfest

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
               other_attacks: Dict=None,
               talents: Dict=None,
               pc: str = None,
               opp_pc: str = None,
               munchkin=False) -> int:
        """
        Parameters
        __________
        enemy_ac: int
            Body Armour as a number
        attack_rank: str
            Rank of the particular attack
        damage_rank: str
            Damage Rank of the particular attack as relevant
        endurance_rank: str
            Target of attack's endurance rank
        other_attacks: Dict
            Alternate attacks to parse preferred type of attack and method from
        talents: Dict
            The Talents of the character attacking
        pc: str
            Attacker Probability Manipulation power descriptor, if applicable
        opp_pc: str
            Target Probability Manipulation power descriptor, if applicable

        Returns
        _______
        An integer of the damage incurred. 0 is fail to damage.

        :param enemy_ac:
        :param advantage:
        :param add_ability_to_damage:
        :param munchkin: proficiency is not added to damage RAW, however munchkins always do....
        :return:
        """
        #attack_roll = random.randint(1,100)
        attack_roll = roll_faserip(pc = pc)
        effect_type = None
        effect = None
        #print("ATTACK ROLL:", attack_roll, "BA:", enemy_ac)
        #need slam - endurance check - need opponent endurance for save and opponent armour #could get slammed too far but more complicated using movement and map
        #need stun - endurance check - need opponent endurance for save and opponent armour		
        #need start with edged just relying on strength as claws or bite for test
        #max rank or max prob attack somehow from list 
        
		##have to set these or update how now done from powers
        if other_attacks['edged'] == 1 or other_attacks['shooting'] == 1 or other_attacks['throwing-edged'] == 1 or other_attacks['energy'] == 1:
            kill_flag = 1
        else:
            kill_flag = 0
        if other_attacks['force'] == 1:
            stun_flag = 1
        else:
            stun_flag = 0
        if other_attacks['throwing-blunt'] == 1:
            throw_flag = 1
        else:
            throw_flag = 0
        if other_attacks['power'] == 1:
            power_flag = 1
        else:
            power_flag = 0
		
        if attack_roll >= universal_table[attack_rank]['G']:  #basic green roll - other possibilities below
            damage_roll = dict_faserip[damage_rank]
            damage_armour = damage_roll - enemy_ac
            damage_roll = damage_armour
            print("HIT!:", attack_roll, damage_rank, damage_roll, damage_armour)
            ##need other attack matrix here:
            if power_flag == 1:
                print("Powers_Absorbed!")
                total_rounds = 0
                for r in range(6):
                    total_rounds = total_rounds + random.randint(1,10)
                effect_type = "POWER ABSORPTION"
                effect = total_rounds
                print("Powers_Absorbed! for ", total_rounds)
                damage_roll = 1 # to get to take damage, neglibible amount
            else:
                #if dict_faserip[damage_rank] >= dict_faserip[endurance_rank] and damage_armour >= 0:
                if (dict_faserip[damage_rank] >= dict_faserip[endurance_rank] or talents['martial_arts']['A'] == 1 or kill_flag == 1) and (damage_armour >= 0 or talents['martial_arts']['D'] == 1):			
                   if attack_roll >= universal_table[attack_rank]['R']:
                      #stun or kill eligible
                      if kill_flag == 0:
                          print("STUN?", attack_roll, damage_rank)
                          stun_result = stun_check(endurance_rank, pc=opp_pc)
                          effect = stun_result
                          effect_type = "STUN"
                      else:
                          print("KILL?", attack_roll, damage_rank)
                          kill_result = kill_check(endurance_rank, pc=opp_pc)
                          effect = kill_result
                          effect_type = "KILL"
    
                   elif attack_roll >= universal_table[attack_rank]['Y']:
                      #slam eligible
                      if kill_flag == 0:
                          if other_attacks['mental'] == 1:
                              print("STUN from MENTAL?", attack_roll, damage_rank)
                              stun_result = stun_check(endurance_rank, pc=opp_pc)
                              effect = stun_result
                              effect_type = "STUN"
                          else:
                              slam_result = slam_check(endurance_rank, pc=opp_pc)
                              print("SLAM?", attack_roll, damage_rank, slam_result)
                              if slam_result == "Slam": #assume 30 rank wall smash into for now
                                  #damage_roll = damage_roll + max(dict_faserip[endurance_rank],30) + 2 
                                  damage_roll = damage_armour + max(0, 30 - enemy_ac) 				
                                  
                              elif slam_result == "Grand Slam":
                                  #damage_roll = damage_roll + max(dict_faserip[endurance_rank]) + faserip_index[damage_rank]*2 #many areas simulation hack #assuming no body armour
                                  #damage_roll = damage_armour + max(dict_faserip[endurance_rank],30) + faserip_index[damage_rank]*2 #many areas simulation hack #assuming no body armour
                                  #damage_roll = damage_armour + max(0, max(dict_faserip[endurance_rank] + faserip_index[damage_rank]*2, 30) - enemy_ac) 				
                                  damage_roll = damage_armour + max(0, 30 - enemy_ac) 				
                              else:
                                  pass					  
                              effect = slam_result
                              effect_type = "SLAM"
                      else:
                          print("STUN from KILL?", attack_roll, damage_rank)
                          stun_result = stun_check(endurance_rank, pc=opp_pc)
                          effect = stun_result
                          effect_type = "STUN"
    				   
    					
        else:
            print("MISS!:", attack_roll)
            damage_roll = 0
        return [damage_roll, effect_type, effect]  #want to return condition here too?

    @classmethod  # old input
    def parse_list_attack(cls, attack: list, ability_die):
        """
        Unused in FASERIP-Slugfest
        """

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
        Unused in FASERIP-Slugfest

        Returns an Attack roll

        :param name: name of weapon...
        :param ability_die: generally creature.str ... but dex for finesse weapons or wis for shillelagh
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

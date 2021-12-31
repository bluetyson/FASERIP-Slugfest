# inherited by CreatureInitialise

from ._base import CreatureBase
from ..dice.ability_die import AbilityDie
from ..dice import Dice, AttackRoll, SkillRoll
from typing import *
from ..dice.ranks import dict_faserip
print(dict_faserip)

class CreatueInitAble(CreatureBase):

    def set_ability_dice(self, **settings) -> None:
        """
        Rewritten so that cleaning module does the cleaning.
        Formerly it would complain if bonus and score both present.
        Currently set so score takes precedence.

        :return: None.
        """
        self.able = 1  # has abilities. if nothing at all is provided it goes to zero. This is for rocks...
        settings = self._sanitise_settings_for_abilities(settings)
        for ab in self.ability_names:
            score = settings['abilities'][ab]
            bonus = settings['ability_bonuses'][ab]
            #print("SABSCOREBONUS:", score, bonus)			            
            self.set_ability_die(ability_name=ab, score=score, bonus=bonus)
			
        self.karma = dict_faserip[self.rrank] + dict_faserip[self.irank] + dict_faserip[self.prank]
        self.stated_hp = dict_faserip[self.frank] + dict_faserip[self.arank] + dict_faserip[self.srank] + dict_faserip[self.erank]
        self.hp = self.stated_hp
        self.starting_hp = self.stated_hp #used for fighting
		
        self.initiative.modifier = int(dict_faserip[self.irank] / 10)
        if dict_faserip[self.irank] > 50:
            self.initiative.modifier = 5
        if dict_faserip[self.irank] > 75:
            self.initiative.modifier = 6
		
        if self.talents['martial_arts']['E'] == 1:
            self.initiative.modifier +=1
			
        print ("INITI MOD:", self.initiative.modifier)
        #add slugfest attack
        #print ("STR CHECK:", dict_faserip[self.srank])
        #self.attacks = [AttackRoll(name='slugfest', ability_die=self.f, damage_dice=Dice(1,dict_faserip[self.srank],avg=True), modifier=0)]
        #sself.attacks = [AttackRoll(name='slugfest', ability_die=self.f, damage_dice=Dice(1,dict_faserip[self.srank],avg=True), modifier=0)]
        self.attacks = [AttackRoll(name='slugfest', ability_die=self.f, damage_dice=Dice(1,dict_faserip[self.srank]), modifier=0)]
        #self.initiative = SkillRoll(Dice(10,0), modifier=self.initiative.modifier, success_on_crit=False)
		#add slugfest attack
		#add ranged attack
		
        print("HEALTH",self.stated_hp, self.hp, "KARMA:", self.karma, "INIT:", self.initiative.modifier, "SLUGFESTD:",dict_faserip[self.srank], "BA:",self.armour_name)
			

    def set_ability_die(self, ability_name: str, score: Optional[int] = None, bonus: Optional[int] = None):
    #def set_ability_die(self, ability_name: f, score: Optional[int] = None, bonus: Optional[int] = None):
        ability_die = self[ability_name]
        #print(ability_name, ability_die.score, score, ability_die.bonus, bonus)
        assert isinstance(ability_die, AbilityDie), f'The die for {ability_name} is not a die, but {type(ability_die)}'
        assert ability_name in self.ability_names, f'{ability_name} is not in {self.ability_names}'
        if score is not None and bonus is not None:
            if AbilityDie.score2bonus(score) != bonus:
                self.log.warning(f'Mismatch with ability {ability_name}: bonus={bonus}, score={score}')
            ability_die.score = score
            ability_die.bonus = bonus
        elif score is not None:
            ability_die.score = score
            ability_die.bonus = AbilityDie.score2bonus(score)
        elif bonus is not None:
            ability_die.bonus = bonus
            ability_die.score = AbilityDie.bonus2score(bonus)
        else:
            # no change required.
            pass

    def _sanitise_settings_for_abilities(self, settings) -> dict:
        settings = {k.lower(): v for k, v in settings.items()}
        # ---------- set blanks ----------------------------------------------------------------------------------------
        blank_abilities = {ab: None for ab in self.ability_names}
        # ability_bonuses
        if 'ability_bonuses' not in settings:
            ability_bonuses = blank_abilities.copy()
        else:
            ability_bonuses = {**blank_abilities.copy(), **settings['ability_bonuses']}
        # abilities
        if 'abilities' not in settings:
            abilities = blank_abilities
        else:
            abilities = {**blank_abilities.copy(), **settings['abilities']}
        # ---------- capture odd entries -------------------------------------------------------------------------------
        full_names = {'fighting': 'f',
                      'agility': 'a',
                      'strength': 's',
                      'endurance': 'e',
                      'reason': 'r',
                      'intuition': 'i',
                      'psyche': 'p'	}
        for full_name, short_name in full_names.items():
            if full_name in settings:
                abilities[short_name] = settings[full_name]
            if f'{full_name}_bonus' in settings:
                ability_bonuses[short_name] = settings[f'{full_name}_bonus']
        # ------- capture isolated entries -----------------------------------------------------------------------------
        for ability_name in self.ability_names:
            if ability_name in settings:
                abilities[ability_name] = settings[ability_name]
            if f'ab_{ability_name}' in settings:
                ability_bonuses[ability_name] = settings[f'ab_{ability_name}']
        # ------- correct for dice -------------------------------------------------------------------------------------
        for ability_name, score in abilities.items():
            if isinstance(score, int) or score is None:
                pass # perfect
            elif isinstance(score, AbilityDie):
                abilities[ability_name] = score.score
            else:
                #abilities[ability_name] = int(score)
                print("SANITISE:",ability_name, abilities[ability_name], score, dict_faserip[score])
                #abilities[ability_name] = int(score)
                if ability_name == "f":
                    self.frank = abilities[ability_name]
                if ability_name == "a":
                    self.arank = abilities[ability_name]
                if ability_name == "s":
                    self.srank = abilities[ability_name]
                if ability_name == "e":
                    self.erank = abilities[ability_name]
                if ability_name == "r":
                    self.rrank = abilities[ability_name]
                if ability_name == "i":
                    self.irank = abilities[ability_name]
                if ability_name == "p":
                    self.prank = abilities[ability_name]
                    print("rankcheck",self.prank)
					
                abilities[ability_name] = dict_faserip[score]
				
        for ability_name, bonus in ability_bonuses.items():
            if isinstance(bonus, int) or bonus is None:
                pass  # perfect
            else:
                ability_bonuses[ability_name] = int(bonus)
        # ------- done -------------------------------------------------------------------------------------------------
        return dict(abilities=abilities, ability_bonuses=ability_bonuses)
    #
    # def change_attribute(self, **abilities):
    #     """
    #     Setting an ability attribute directly does not result in a recalculation.
    #     For example:
    #
    #     >>> slashr = Creature('troll')
    #     >>> slashr.abilities['cha'] = 16
    #
    #     This will not change the stats dependent on that ability.
    #     This method attempts to change the dependent abilities.
    #     A late addition, so the code does not make use of it.
    #     :param attributes: key value pair
    #     :return: None
    #     """
    #     raise DeprecationWarning # TODO REMOVE ENTIRELY
    #     for attr in abilities:
    #         attr = attr[0:3].lower()  # just in case
    #         if attr in self.abilities:
    #             old_attr = self.abilities[attr]
    #             self.abilities[attr] = int(abilities[attr])
    #             delta = int(self.abilities[attr] / 2 - 5) - int(old_attr / 2 - 5)
    #             old_bonus = self.ability_bonuses[attr]
    #             self.ability_bonuses[attr] += delta  # it might differ for some reason...
    #             # con does not change
    #             if attr == "str":
    #                 pass
    #             elif attr == "dex":
    #                 pass
    #             elif attr == "con":
    #                 pass
    #             elif attr == "int":
    #                 pass
    #             elif attr == "wis":
    #                 pass
    #             elif attr == "cha":
    #                 pass
    #         else:
    #             raise ValueError('Unrecognised ability')

from .ability_die import AbilityDie
from typing import *
from ..log import log
import random

class SkillRoll:

    log = log

    def __init__(self, ability_die: AbilityDie, modifier: int = 0, success_on_crit=True):
        """
        Meant for an ability check or a saving throw.
        This allows to add an extra modifier to the ability_die (in addition to ability bonus and proficiency)
        RAW in 5e: a crit on an ability roll is not a given success.

        :param ability_die:
        :param modifier:
        :param success_on_crit:
        """
        self.ability_die = ability_die
        self.success_on_crit = success_on_crit
        self.modifier = modifier

    def base_roll(self, advantage:Optional[int]=None) -> int:
        """
        Unused in FASERIP-Slugfest
        """
        return self.ability_die.base_roll(advantage=advantage, success_on_crit=self.success_on_crit)

    def roll(self, advantage:Optional[int]=None) -> int:
        """
        Unused in FASERIP-Slugfest
        """
        return self.base_roll(advantage=advantage) + self.bonuses
		
    def roll_initiative(self, fighter, advantage:Optional[int]=None) -> int:
        """
        Parameters
        __________
        fighter: Creature
            The Creature rolling initiative
        advantage: int
            Using for initiative modifier from FASERIP - TODO: could rename

        Returns
        _______
        d10 initiative roll with appropriate modifiers
        """
        initiative_roll = random.randint(1,10)
        print("INIT ROLL", initiative_roll, advantage)
        # any character rolling initiative scores a 1, no modifier
        if initiative_roll == 1:
            fighter.initiativeFASERIP = initiative_roll		
            return initiative_roll 
        else:
            fighter.initiativeFASERIP = initiative_roll + advantage
            return initiative_roll + advantage
		

    @property
    def bonuses(self):
        """
        Unused in FASERIP-Slugfest
        """
        return self.ability_die.bonus + self.ability_die.proficiency.bonus + self.modifier

    def __str__(self):
        """
        Unused in FASERIP-Slugfest  TODO: change to get useful modifiers?
        """
        return f'{self.ability_die}+{self.ability_die.proficiency.bonus}+{self.modifier}'


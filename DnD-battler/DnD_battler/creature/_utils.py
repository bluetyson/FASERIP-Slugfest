from ._base import CreatureBase
from typing import *
from copy import deepcopy

class CreatureUtils(CreatureBase):

    def generate_character_sheet(self) -> str:
        """
        A markdown character sheet.
        
        :return: a string
        """
        rows = ['# ' + self.name.upper()]
        rows.append(self._makeline('Name', self.name))
        rows.append(self._makeline('Alignment', self.alignment))
        rows.append('## Abilities')
        for ab in self.ability_names:
            rows.append(self._makeline(ab, self[ab].score, self[ab].bonus))
        rows.append('## Combat')
        rows.append(self._makeline('Hit points (hp total)', self.hp, self.starting_hp))
        rows.append(self._makeline('Condition', self.condition))
        rows.append(self._makeline('Initiative', self.initiative))
        rows.append(self._makeline('Proficiency', self.proficiency.bonus))
        rows.append(self._makeline('Armour class', self.armor.ac))
        rows.append('### Attacks')
        rows.append(self._makeline('Potential average damage per turn', self.hurtful))
        for d in self.attacks:
            rows.append("* " + self._makeline(d['name'], d['attack'], d['damage']))
        rows.append('### Raw data')
        rows.append(str(self.__dict__).replace('<br/>', '\n'))
        return '\n'.join(rows)

    def generate_character_sheetFASERIP(self) -> str:
        """
        A markdown character sheet.
        
        :return: a string
        """
        rows = ['# ' + self.name.upper()]
        rows.append(self._makeline('Name', self.name))
        rows.append(self._makeline('Identity', self.identity))
        rows.append(self._makeline('Form', self.form))
        rows.append(self._makeline('Alignment', self.alignment))
        rows.append('## Abilities')
        for index, ab in enumerate(self.ability_names):
            if index == 0:
                abrank = self.frank
            elif index == 1:
                abrank = self.arank
            elif index == 2:
                abrank = self.srank
            elif index == 3:
                abrank = self.erank
            elif index == 4:
                abrank = self.rrank
            elif index == 5:
                abrank = self.irank
            else:
                abrank = self.prank
			
            rows.append(self._makeline(ab, abrank))
        rows.append('## Combat')
        rows.append(self._makeline('Health', self.hp))
        rows.append(self._makeline('Karma', self.karma))
        rows.append(self._makeline('Body Armour', self.body_armour))
        rows.append(self._makeline('Martial Arts', self.talents['martial_arts']))
        rows.append(self._makeline('Powers', self.powers_adj_rank))		
        rows.append(self._makeline('Equipment', self.equipment_adj_rank))				
        rows.append(self._makeline('Talents', self.talents_adj))				
        rows.append(self._makeline('Contacts', self.contacts))						
        rows.append('### Attacks')
        rows.append(self._makeline('Condition', self.condition))
        rows.append(self._makeline('Initiative', self.initiative.modifier))
        rows.append(self._makeline('Alt', self.alt_attack))
        rows.append(self._makeline('Potential average damage per turn', self.hurtfulFASERIP()))
        rows.append(self._makeline('Esoteric CS Bonus', self.level))
        rows.append(self._makeline('Attack', self.attack))
        rows.append(self._makeline('Defense', self.defense))
        for d in self.attacks:
            #rows.append("* " + self['AbilityDie']._makeline(d['name'], d['attack'], d['damage']))
            pass			
        rows.append('### Raw data')
        rows.append(str(self.__dict__).replace('<br/>', '\n'))
        return '\n'.join(rows)
    
    def _makeline(self, field: str, value: Any, secvalue: Optional[Any]=None) -> str:
        """
        dependent method for generate_character_sheet only.
        returns _field_: value (secvalue)
        secvalues is if has a secondary value to be added in brackets
        """
        if secvalue is None:
            return '_' + str(field).replace("_", " ") + '_: ' + str(value)
        else: # secondary value.
            return '_' + str(field).replace("_", " ") + '_: ' + str(value) + ' (' + str(secvalue) + ')'


    def __str__(self):
        if self.tally['battles']:
            battles = self.tally['battles']
            return self.name + ": {team=" + self.alignment + "; avg Health=" + str(
                self.tally['hp'] / battles) + " (from " + str(
                self.starting_hp) + "); damage done (per battle average)= " + str(
                round(self.tally['damage'] / battles,2)) + "; hits/slams/stuns/kills/misses (PBA)= " + str(
                round(self.tally['hits'] / battles,2)) + "/" + str(
                round(self.tally['slam'] / battles,2)) + "/" + str(
                round(self.tally['stun'] / battles,2)) + "/" + str(
                round(self.tally['kill'] / battles,2)) + "/" + str(
                round(self.tally['misses'] / battles,2)) + "; rounds (PBA)=" + str(
                round(self.tally['rounds'] / battles,2)) + ";}"
        else:
            return self.name + ": UNTESTED IN BATTLE"
#avg healing spells left=" + str(
#                self.tally['healing_spells'] / battles) + " (from " + str(
#                self.starting_healing_spells) + ");

    def copy(self):
        """
        :return: a copy of the creature. with an altered name.
        """
        self.copy_index += 1
        copy = deepcopy(self)
        copy.name += str(copy.copy_index)

    def get_settings(self):
        """
        NB. not jsonable
        :return:
        """
        return {attr: self[attr] for attr in self.__dict__}
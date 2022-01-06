#from ._fillers import CreatureFill
from ._load_beastiary import CreatureLoader
from ._init_abilities import CreatueInitAble
from ._safe_property import CreatureSafeProp
from ._level import CreatureLevel
from ..dice import AbilityDie, AttackRoll
from ..dice.ranks import dict_faserip, column_shift
import json

class CreatureAdvBase(CreatueInitAble, CreatureSafeProp, CreatureLoader, CreatureLevel):
    def __init__(self, **settings):
        super().__init__()
        self.apply_settings(**settings)

    @classmethod
    def load(cls, creature_name, **settings):
        """
        Loads from MM

        :param creature_name:
        :return:
        """
        cleaned = lambda name: name.lower().replace('_', ' ')
        #print(cls.beastiary)
        if creature_name in cls.beastiary:
            self = cls(**cls.beastiary[creature_name])
        elif cleaned(creature_name) in cls.beastiary:
            self = cls(**cls.beastiary[cleaned(creature_name)])
        else:
            raise ValueError(f'Creature "{creature_name}" not found.')
        self.base = creature_name
        self.apply_settings(**settings)
        return self

    def apply_settings(self, **settings):
        settings = {k.lower(): v for k, v in settings.items()}
        print("CHECK_SETTINGS", settings)		
        # -------------- assign fluff values ---------------------------------------------------------------------------
        #print(settings['stated_ac'])
        for key in ('name', 'base', 'type', 'alignment','stated_ac'):
            #print("key",key)
            if key in settings:
                self[key] = settings[key]
        for key in ('xp', 'hp'):
            if key in settings:
                self[key] = settings[key]
        for key in ('powers_adj_rank','equipment_adj_rank','talents_adj','attack','defense','body_armour'):
            print(key)		
            if key in settings:
                json_acceptable_string = settings[key].replace("'", "\"")
                self[key] = json.loads(json_acceptable_string)

        # -------------- set complex values ----------------------------------------------------------------------------
        # abilities
        if 'stated_ac' in settings: #everyone has Armour here in code, just Sh0 for default, so no effect
            print("STATED AC CHECK",self.armor.ac)
            self.armour_name = settings['stated_ac'] 
            print("WE HAVE STATED AC CHECK",self.armour_name, self.name)
            if ";" in self.armour_name and 'Physical' not in self.body_armour:  ##have body armour now for characters not default list
                ranklist = self.armour_name.split(';')
                del ranklist[-1]
                self.stated_ac = self.armour_name
                self.armour_name = ranklist[0]
                print("STATED AC CHECK AFTER!",self.armour_name)
                print("ranklist",ranklist)
                print("ranklist0",ranklist[0])
                #self.stated_ac = self.armour_name
                print(type(self.body_armour))
                if len(ranklist) == 1:  #if 3, good question
                    self.body_armour["Physical"] = ranklist[0]
                    self.body_armour["Energy"] = column_shift(ranklist[0], -2)
                if len(ranklist) > 1:  #if 3, good question
                ###need to make an Energy AC as well
                    self.body_armour["Physical"] = ranklist[0]
                    self.body_armour["Energy"] = ranklist[1]
                    
        else: #need a length
            #print("STATED AC CHECK AFTER!",self.armour_name)
            #default is good
            pass
            #self.body_armour["Physical"] = self.armour_name
            #self.body_armour["Energy"] = column_shift(self.armour_name, -2)
                
            #self.armour_name = "Sh0"
        self.armor.ac = dict_faserip[self.body_armour["Physical"]]
        
		
        print("FINAL AC CHECK",self.armor.ac, self.body_armour)
        
        #T = Type of Damage: E = Edged, B= Blunt, S = Shooting, H = Advanced Technology, 2 = Blunt and Edged, W = S and 2
		
        if 'att' in settings: #change this for powers etc. too
            print("OTHER ATTACKS:", settings['att'])
            if settings['att'] == 'B':
                self.alt_attack['blunt'] = 1
            if settings['att'] == 'E':
                self.alt_attack['edged'] = 1
            if settings['att'] == 'S':
                self.alt_attack['shooting'] = 1
            if settings['att'] == 'H':
                self.alt_attack['energy'] = 1
                self.alt_attack['force'] = 1
            if settings['att'] == '2':
                self.alt_attack['blunt'] = 1
                self.alt_attack['edged'] = 1
            if settings['att'] == 'W':
                self.alt_attack['blunt'] = 1
                self.alt_attack['edged'] = 1
                self.alt_attack['shooting'] = 1
            print(self.alt_attack)
            
        if self.attack['Edged']['S'] != '':
            self.alt_attack['edged'] = 1
		
		
        if 'martial_arts' in settings:  #adds a 1 for each of Martial Arts A to E found in beastiaryFASERIP - string ABCDE, ABCD etc.
            #print("MARTIAL ARTS:", settings['martial_arts'])
            for ma in settings['martial_arts']:
                self.talents['martial_arts'][ma] = 1
            print(self.talents['martial_arts'])
			
        if 'mook' in settings:  #mook rules if a 0 then character will attack everything at -4CS by default.  For testing heroes versus mobs, thugs etc.
            self.mook = settings['mook']
            #print("MOOKL", self.mook)

        self.set_ability_dice(**settings)
        # arena - battle the caracter is in
        if 'arena' in settings:
            self.arena = settings['arena']
        # size
        if 'size' in settings:
            self.size.name = settings['size']
        # level
        if 'level' in settings:
            self.set_level(**settings)
        # proficiency
        if 'proficiency' in settings:
            self.proficiency.bonus = int(settings['proficiency'])
        # hit dice
        if 'hd' in settings:  #cound use to store Endurance Ranks?
            self.hit_die.num_faces = [int(settings['hd'])]
            if 'hp' not in settings:
                self.recalculate_hp()
        # other
        if 'sc_ability' in settings:  #could adapt this setting for magic using characters and differences there
            sc_a = settings['sc_ability'].lower()
            assert sc_a in self.ability_names, f'{sc_a} is not a valid ability name {self.ability_names}'
            self.spellcasting_ability_name = sc_a
        # ac
        self.set_ac(**settings)
        if 'initiative_bonus' in settings:
            self.initiative.modifier = int(settings['initiative_bonus'])
        # attacks
        if 'attack_parameters' in settings or 'attacks' in settings:  #not used currently, likely break things
            self.attacks = self.parse_attacks(**settings)
			
			
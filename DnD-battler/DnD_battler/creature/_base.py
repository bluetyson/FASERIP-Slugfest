from ..dice import AbilityDie, Dice, SkillRoll, AttackRoll
from ..creature_properties.proficiency import Proficiency
from ..creature_properties.armor import Armor
from ..creature_properties.size import Size
from ..log import log

class CreatureBase:
    # inherited by utils

    #ability_names = ['str', 'dex', 'con', 'wis', 'int', 'cha']
    ability_names = ['f', 'a', 's', 'e', 'r', 'i', 'p']
    log = log

    def __init__(self):
        self.name = 'unnamed'
        self.base = 'none'    # human bandit
        self.type = 'unknown' # aberation, humanoid
        self.size = Size('medium')  #size bonus and penalty column shifts - could utilise for this when change size?
        self.arena = None
        self.level = 1
        self.xp = 0
        # proficiency
        # self.proficiency.bonus is dynamic based on proficiency.level + proficiency.modifier
        self.proficiency = Proficiency(0, 0)  #Not used
        # hits
        self.hp = 24  # All Typical Human HEALTH
        self.starting_hp = 24
        self.hit_die = Dice(8, 0)
        ## new
        self.karma = 18
        self.pop = 0
        self.res = "Ty"
        self.frank = "Ty"
        self.arank = "Ty"
        self.srank = "Ty"
        self.erank = "Ty"		
        self.rrank = "Ty"
        self.irank = "Ty"
        self.prank = "Ty"		
        ##
        #Ability
        self.able = 1  # has abilities. if nothing at all is provided it goes to zero. This is for rocks...  ##rolling stuff here for abilities
        self.f = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.a = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.s = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.e = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.r = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.i = AbilityDie(bonus=0, proficiency=self.proficiency)
        self.p = AbilityDie(bonus=0, proficiency=self.proficiency)

        #print(self.f, self.a) #dice associated with ranks, not really used currently
		
        # AC
        self.armor = Armor(ability_dice=[self.a], bonus=0)
        # other
        self.initiative = SkillRoll(self.i, modifier=0, success_on_crit=False)
        self.attacks = [AttackRoll(name='slugfest', ability_die=self.f, damage_dice=Dice(1,5), modifier=0)]
        self.alt_attack = {'throwing-blunt':0,'throwing-edged':0,'blunt':0,'edged':0,'shooting':0,'energy':0,'force':0,'grapple':0}  #put other abilities/weapons here
        self.powers = {}  #put other abilities/weapons here		
        self.powers_rank = {}  #put other abilities/weapons here		
        self.powers_adj = {}  #put other abilities/weapons here		
        self.powers_adj_rank = {}  #put other abilities/weapons here		
        self.equipment = {}  #put other abilities/weapons here		
        self.equipment_rank = {}  #put other abilities/weapons here		
        self.equipment_adj = {}  #put other abilities/weapons here		
        self.equipment_adj_rank = {}  #put other abilities/weapons here		
        
        self.talents = {}  #put other abilities/weapons here			
        self.talents_adj = {}  #put other abilities/weapons here					
		
        martial_arts = {"A":0,"B":0,"C":0,"D":0,"E":0}	
        self.talents['martial_arts'] = martial_arts
		
        self.contacts = {}  #put other abilities/weapons here				
        self.alignment = 'undeclared'
        self.concentrating = 0
        self.spellcasting_ability_name = None
        self.starting_healing_spells = 0
        self.healing_spells = self.starting_healing_spells
        self.healing = None  # Normally dice object
        # internal stuff
        self.tally = {'damage': 0, 'hits': 0, 'dead': 0, 'misses': 0, 'battles': 0, 'rounds': 0, 'hp': 0,
                      'healing_spells': 0, 'stun':0, 'slam':0, 'stunned':0, 'slammed':0}
        self.copy_index = 1
        self.condition = 'normal'
        self.dodge = 0
        self.temp = 0
        self.buff_spells = 0
        self.conc_fx = None
        self.cr = 0
        self.custom = []
        self.slam = 0
        self.stun = 0
        self.kill = 0
        self.mook = 0
        self.distance_areas = 0
        self.stated_ac = "Ty"
        self.body_armour = {"Physical":"Sh0","Energy":"Sh0"}
	

    @property
    def abilities(self):
        """
        A fix to compensate how abilities are handled.
        Now they have their own attribute which is a die. With score and temp_modifier as extras

        :return:
        """
        return {n: getattr(self, n) for n in self.ability_names}

    @property
    def hurtful(self):
        # this is the average damage it can do. But omits if it hits or not...
        return sum([roll.damage_dice.mean() for roll in self.attacks])

    ac = property(lambda self: self.armor.get_ac(), lambda self, value: self.armor.set_ac(value))

from ..victory import Victory
from ._adv_base import CreatureAdvBase
from ..dice.ranks import dict_faserip, universal_table, universal_color, column_shift
import random

class CreatureAction(CreatureAdvBase):

    def ready(self):
        self.dodge = 0
        self.stun = 0
        self.slam = 0
        # there should be a few more.
        # conditions.

    def isalive(self):
        if self.hp > 0:
            return True

    def isaliveFASERIP(self):
        if self.hp > 0 and not self.kill:
            return True

    def isconscious(self):
        if self.stun == 0:
            return True

    def isupright(self):
        if self.slam == 0:
            return True

    def take_damage(self, points, verbose=0):
        self.hp -= points
        if verbose:
            print(self.name + ' took ' + str(points) + ' of damage. Now on ' + str(self.hp) + ' hp.')
        if self.concentrating:
            dc = points / 2
            if dc < 10: dc = 10
            if self[self.spellcasting_ability_name].roll() < dc:
                self.conc_fx()
                if verbose:
                    print(self.name + ' has lost their concentration')

    def take_damageFASERIP(self, points, effect_type, effect, verbose=0):
        self.hp -= points
        if effect_type == "STUN":
            self.stun = effect
        if effect_type == "KILL":
            if effect == "En Loss" or effect == "E S":
                self.kill = 1
		
            
        if verbose:
            print(self.name + ' took ' + str(points) + ' of damage. Now on ' + str(self.hp) + ' hp.')

    def reset(self, hard=False):
        """
        Resets the creature back to health (a long rest). a hard reset resets its scores
        :param hard: bool, false keeps tallies
        :return: None
        """
        self.hp = self.starting_hp
        if self.concentrating:
            self.conc_fx()  # TODO this looks fishy
        self.healing_spells = self.starting_healing_spells
        self.stun = 0
        self.slam = 0
        self.kill = 0
        if hard:
            self.tally = {'damage': 0, 'hp': 0, 'hits': 0, 'misses': 0, 'rounds': 0, 'healing_spells': 0, 'battles': 0,
                          'dead': 0, 'stun':0, 'slam':0, 'kill':0}

    def check_advantage(self, opponent):
        adv = 0
        if opponent.dodge:
            adv += -1
        if (opponent.condition == 'netted') or (opponent.condition == 'restrained'):
            adv += 1
        # Per coding it is impossible that a netted creature attempts an attack.
        if (self.condition == 'netted') or (self.condition == 'restrained'):
            adv += -1
        return adv

    def net(self, opponent, verbose=0):
        self.alt_attack['attack'].advantage = self.check_advantage(opponent)
        if self.alt_attack['attack'].roll(verbose) >= opponent.armor.ac:
            opponent.condition = 'netted'
            self.tally['hits'] += 1
            if verbose:
                print(self.name + " netted " + opponent.name)
        else:
            self.tally['misses'] += 1

    def cast_barkskin(self):
        if self.concentrating == 0:
            self.temp = self.armor.ac
            self.armor.ac = 16
            self.concentrating = 1
        elif self.concentrating == 1:
            self.armor.ac = self.temp
            self.concentrating = 0

    def cast_nothing(self, state='activate'):  # Something isn't quite right if this is invoked.
        pass

    def heal(self, points, verbose=0):
        self.hp += points
        if verbose:
            print(self.name + ' was healed by ' + str(points) + '. Now on ' + str(self.hp) + ' hp.')

    def assess_wounded(self, verbose=0):
        targets = self.arena.find('bloodiest allies')
        if len(targets) > 0:
            weakling = targets[0]
            if weakling.starting_hp > (self.healing.num_faces[0] + self.healing.bonus + weakling.hp):
                if verbose:
                    print(self.name + " wants to heal " + weakling.name)
                return weakling
            else:
                return 0
        else:
            raise ValueError('A dead man wants to heal folk')

    def cast_healing(self, weakling, verbose=0):
        if self.healing_spells > 0:
            weakling.heal(self.healing.roll(), verbose)
            self.healing_spells -= 1

    #def multiattack(self, verbose=0, assess=0):
    def multiattack(self, verbose=1, assess=0):	
        print("multiattacking")
        extra_attacks = 0
        fighting_rank = self.frank
		
        if assess:
            return 0  # the default
        ##multi attack check here? add to range self.attacks #boost for Martial arts B to F rank
        if dict_faserip[self.frank] < 30:
            #no point doing multiattack except in a game karma type situation
            fighting_cs = 0
        elif dict_faserip[self.frank] < 50:
            #Rm or In fighting no point trying for 3 as Amazing intensity, try for two
            fighting_roll = random.randint(1,100)
            fighting_cs = -3  #going to need to change below to have an effective fighting rank from fighting_cs type things
            if self.frank < 40:
            #Rm
                fighting_color = universal_color(self.frank, fighting_roll)
                if fighting_color == "Y" or fighting_color == "R":
                    extra_attacks = 1
                    fighting_cs = -1
            else:
            #In
                fighting_color = universal_color(self.frank, fighting_roll)
                if fighting_color != "W":
                    extra_attacks = 1
                    fighting_cs = -1

        else:
            #Amazing fighting or better Amazing intensity, try for three
            fighting_roll = random.randint(1,100)
            fighting_cs = -3  #going to need to change below to have an effective fighting rank from fighting_cs type things
            fighting_color = universal_color(self.frank, fighting_roll)
            if fighting_color == "Y" or fighting_color == "R":
                extra_attacks = 2
                fighting_cs = -1
        ##check martial arts adjustment - put other weapon skill type adjustments etc in a place similarly
        if self.talents['martial_arts']['B'] == 1:
            fighting_cs = fighting_cs + 1
        if fighting_cs != 0:
            fighting_rank = column_shift(self.frank, fighting_cs)
		## loop for extra attacks
        for ea in range(extra_attacks + 1):
            for i in range(len(self.attacks)):  ##multi attack check here? #boost for Martial arts B to F rank
                try:
                    opponent = self.arena.find(self.arena.target, self)[0]
                except IndexError:
                    raise Victory()
                self.log.debug(f"{self.name} attacks {opponent.name} with {self.attacks[i].name}")
                # This was the hit method. put here for now.
                # THE IMPORTANT PART TO WRITE, UNIVERSAL TABLE TIME!
                print("ATTACKS", self.attacks[i], "FIGHTING", self.frank, "STRENGTH", self.srank, "OPPEND", opponent.erank, "BA", opponent.ac, opponent.armor.ac)
                #damage = self.attacks[i].attack(opponent.armor.ac, advantage=self.check_advantage(opponent))
                #damage, effect_type, effect = self.attacks[i].attackFASERIP(opponent.armor.ac, advantage=self.check_advantage(opponent), attack_rank=self.frank, damage_rank=self.srank, endurance_rank=opponent.erank, #other_attacks=self.alt_attack)  #put attack rank in
                damage, effect_type, effect = self.attacks[i].attackFASERIP(opponent.armor.ac, advantage=self.check_advantage(opponent), attack_rank=fighting_rank, damage_rank=self.srank, endurance_rank=opponent.erank, other_attacks=self.alt_attack, talents=self.talents)  #put attack rank in
                 
                print("DAMAGE", damage, "OPPONENTAC:", opponent.armor.ac)
                #damage = 2
                if damage > 0:
                    #opponent.take_damage(damage, verbose)
                    opponent.take_damageFASERIP(damage, effect_type, effect, verbose)
                    self.tally['damage'] += damage
                    self.tally['hits'] += 1
                else:
                    self.tally['misses'] += 1
    
                if effect_type == "STUN":
                    self.tally['stun'] += 1
                if effect_type == "SLAM":
                    self.tally['slam'] += 1
                if effect_type == "KILL":
                    self.tally['kill'] += 1
                ### reset to base self attacks of 1
    
        # TODO
    def check_action(self, action, verbose):
        return getattr(self, action)(assess=1)

    # TODO
    def do_action(self, action, verbose):
        # do it.
        pass

    # TODO
    def TBA_act(self, verbose=0):
        if not self.arena.find('alive enemy'):
            raise Victory()
        x = {'nothing': 'cast_nothing'}
        choice = [self.check_action(x) for x in self.actions]
        best = sorted(choice.keys(), key=choice.get)[0]
        self.do_action(best)

    def act(self, verbose=1):
        if not self.arena.find('alive enemy'):
            raise Victory()
			
        #print("ALIVE", self.arena.find('alive enemy'))
        # BONUS ACTION
        # heal  -healing word, a bonus action.
        if self.healing_spells > 0:
            weakling = self.assess_wounded(verbose)
            if weakling != 0:
                self.cast_healing(weakling, verbose)
        # Main action!
        economy = len(self.arena.find('allies')) > len(self.arena.find('opponents')) > 0
        print("ECONOMY", economy)
        print("condition", self.condition)
        # Buff?
        if self.condition == 'netted':
            # NOT-RAW: DC10 strength check or something equally easy for monsters
            if verbose:
                print(self.name + " freed himself from a net")
            self.condition = 'normal'
        elif self.stun > 0:
            if verbose:
                print(self.name + " stunned for ", self.stun, "rounds")
            self.stun -= 1
            #self.condition = 'normal'
        elif self.slam > 0:
            if verbose:
                print(self.name + " slammed ", self.slam, "areas")  #don't have a grand slam distance currently - 2 area running - can normals do, check
            self.slam -= 1
            #self.condition = 'normal'
        elif self.buff_spells > 0 and self.concentrating == 0:
            self.conc_fx()
            if verbose:
                print(self.name + ' buffs up!')
            # greater action economy: waste opponent's turn.
        elif economy and self is self.arena.find('weakest allies')[0]:
            if verbose:
                print(self.name + " is dodging")
            self.dodge = 1
        #elif economy and self.alt_attack['name'] == 'net':  #work out if an entangle attack to put in that lot
        elif economy and self.alt_attack['grapple'] == 'net':  #work out if an entangle attack to put in that lot
            #print(self.alt_attack)
            opponent = self.arena.find('fearsomest enemy alive', self)[0]
            if opponent.condition != 'netted':
                self.net(opponent, verbose)
            else:
                self.multiattack(verbose)
        else:
            self.multiattack(verbose)

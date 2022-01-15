from ..victory import Victory
from ._adv_base import CreatureAdvBase
from ..dice.ranks import faserip, dict_faserip, universal_table, universal_color, column_shift, faserip_index, feat, nearest_rank, roll_faserip
import random
import time

class CreatureAction(CreatureAdvBase):

    def ready(self):
        self.dodge = 0
        #self.stun = 0 #makes them stun proof
        #self.slam = 0 #makes them slam proof
        #self.kill = 0 #makes them kill proof
        # there should be a few more. e.g. Evasion, Blocking, Grabbing, Catching
        # conditions.

    def isalive(self):
        if self.hp > 0:
            return True

    def isaliveFASERIP(self):
        if self.hp > 0 and not self.kill == 1:  #or other things like that that last a long time
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

    def take_damageFASERIP(self, points, effect_type, effect, alt_attack, verbose=0):
        #check for energy absorption #need to check attack type too for this AB = Absorption abbreviation
        #template for dealing with strange defenses - a kinetic energy defense - e.g. Sebastian Shaw would work similarly
        #checks for overload, too
        """
        Parameters
        __________
        points: int
            damage possibly taken
        effect_type: str
            the effect type of the attack, to tell if POWER ABSORPTION or STUN etc.
        effect:
            consequence of the effect, stun rounds, slam distance, etc
            POWER ABSORPTION currently counting as Kill as have just been trialling one on ones with Rogue so far
            TODO: Alter Ego characters - absorbed powers and abilities could be checked from making a clone of opponent
        alt_attack: Dict
            Basic attack types for simplifying combat simulation branching

        Reduces Health (hp in class) of target taking the damage
        """
        if alt_attack['energy'] == 1 or alt_attack['force'] == 1:
            if ';' in self.defense['Energy']['AB']:
                absorption_list = self.defense['Energy']['AB'].split(';')
                if len(absorption_list) == 3:
                    absorption_red = absorption_list[2]
                    absorption_yellow = absorption_list[1]
                    absorption_green = absorption_list[0]
                elif len(absorption_list) == 2:
                    absorption_red = absorption_list[1]
                    absorption_yellow = absorption_list[1]
                    absorption_green = absorption_list[0]
                else:
                    absorption_red = absorption_list[0]
                    absorption_yellow = absorption_list[0]
                    absorption_green = absorption_list[0]
                endurance_roll = random.randint(1,100)
                absorption_color = universal_color(self.erank, endurance_roll)
                absorption_points = dict_faserip[absorption_green]			            
                if absorption_color == 'R':
                    absorption_points = dict_faserip[absorption_red]			            
                if absorption_color == 'Y':
                    absorption_points = dict_faserip[absorption_yellow]			            
                if absorption_points >= points :
                    #need a nearest rank function
                    self['attack']['Energy']['AB'] = points				
                    points = 0
                    print(self.name, "Absorbed", points, "of energy")
                else:
                    self['attack']['Energy']['AB'] = absorption_points				
                    points = points - absorption_points				
                    print(self.name, "Absorbed", absorption_points, "of energy and took", points)
    				
        self.hp -= points
        if effect_type == "STUN" or effect_type == "POWER ABSORPTION":
            self.stun = self.stun + effect
            print(self.name, " Stunned for: ", effect, "total:", self.stun, " rounds from ", effect_type)
            if effect_type == "POWER ABSORPTION":
                self.kill = 1
        if effect_type == "KILL":
            if effect == "En Loss" or effect == "E S":  #Abbreviation for Edged/Slashing damage
                print(self.name, " Killed!")
                self.kill = 1
		 
        if verbose:
            print(self.name + ' took ' + str(points) + ' damage. Now ' + str(self.hp) + ' Health.')

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
        #back to new battle conditions for FASERIP
        self.stun = 0 
        self.slam = 0
        self.kill = 0
        if hard:
            self.tally = {'damage': 0, 'hp': 0, 'hits': 0, 'misses': 0, 'rounds': 0, 'healing_spells': 0, 'battles': 0,
                          'dead': 0, 'stun':0, 'slam':0, 'kill':0, 'stunned':0, 'slammed':0, 'killed':0}

    def check_advantage(self, opponent):
        """
        Unused in FASERIP-Slugfest
        """
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
        """
        Unused in FASERIP-Slugfest - Grapple Attack eventually
        """
        self.alt_attack['attack'].advantage = self.check_advantage(opponent)
        if self.alt_attack['attack'].roll(verbose) >= opponent.armor.ac:
            opponent.condition = 'netted'
            self.tally['hits'] += 1
            if verbose:
                print(self.name + " netted " + opponent.name)
        else:
            self.tally['misses'] += 1

    def cast_barkskin(self):
        """
        Unused in FASERIP-Slugfest - Grapple Attack eventually
        """
        if self.concentrating == 0:
            self.temp = self.armor.ac
            self.armor.ac = 16
            self.concentrating = 1
        elif self.concentrating == 1:
            self.armor.ac = self.temp
            self.concentrating = 0

    def cast_nothing(self, state='activate'):  # Something isn't quite right if this is invoked.
        """
        Unused in FASERIP-Slugfest - Grapple Attack eventually
        """
        pass

    def heal(self, points, verbose=0):
        #TODO: Could use for Healing Powers? Already put in regeneration
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

    def multiattack(self, verbose=1, assess=0):	
        print(self.name, "is multiattacking", self.stun) #attack all at once - 6 at once? if more than 2 worth it maybe
        probability_control = None
        opponent_probability_control = None
        print(self.powers_adj_rank)		
        if 'Probability Manipulation' in self.powers_adj_rank:
            #opposite is bad - could theoretically have this - e.g. Longshot		                    
            #opponent could be given it too
            probability_control = "good" 
        pc = probability_control #for length
		
        extra_attacks = 0   
        #default attack type and damage type, with no column shifts originally		
        slugfest = 1  
        damage_rank = self.srank 
        fighting_rank = self.frank
        fighting_cs = 0
        level = self.level

		### need to check for attack type using
		### eg Edged for Wolverine and Sabretooth
		### if Agility attack - e.g. Hawkeye, make fighting rank agility rank or Mental - e.g. Jean Grey, make it Psyche
        fighting_cs = fighting_cs + level  #ad hoc bonus for extra skills like Hawkeye, Cyclops Spatial Geometry
        ##check martial arts adjustment - put other weapon skill type adjustments etc in a place similarly
		# only on slugfest
        #print("alt attacks", self.alt_attack)
        #if self.alt_attack['edged'] == 1 or self.alt_attack['blunt'] == 1 or self.alt_attack['shooting'] == 1 or self.alt_attack['energy'] == 1 or self.alt_attack['force'] == 1:
        if self.alt_attack['edged'] == 1 or self.alt_attack['blunt'] == 1 :
            slugfest = 0
        if self.alt_attack['throwing-blunt'] == 1 or self.alt_attack['throwing-edged'] == 1 or self.alt_attack['shooting'] == 1 or self.alt_attack['energy'] == 1 or self.alt_attack['force'] == 1:
            fighting_rank = self.arank
            slugfest = 0
            print ("Agility Based Combat: use Agility Rank", self.arank)
        if self.alt_attack['mental'] == 1 or self.alt_attack['magic'] == 1:
            fighting_rank = self.prank
            slugfest = 0
            print ("Mind Based Combat: use Psyche Rank", self.prank)

        ##Opponent checks section - see if Armour makes sense for testing
        try:
            opponent = self.arena.find(self.arena.target, self)[0]
            possible_opponents = self.arena.find(self.arena.target, self)
            #print("POSS OPPONENTS", len(possible_opponents), possible_opponents)
            print("checking opponent armour: P, E",opponent.body_armour["Physical"],opponent.body_armour["Physical"])
        except IndexError:
            raise Victory()
        if assess:
            return 0  # the default
        #Can't physically hurt phasing type characters - e.g. Kitty Pryde
        if 'Phasing' in opponent.powers_adj_rank:
            #need mental or mystical attack
            if self.alt_attack['mental'] == 0 and self.alt_attack['magic'] == 0:
                print(self.name, "cannot hurt phased ", opponent.name)
                return
            else:
                print(self.name, "can hurt phased ", opponent.name)	
        #TODO Work out how to handle more and more powers - Library?
        if 'Probability Manipulation' in opponent.powers_adj_rank:
            opponent_probability_control = "good"		        
        opp_pc = opponent_probability_control
				
        #check for opponent defensive abilities - eventually all functions these should be want but the flow first for understanding
        initiative_condition = 0
        ability_test = 0
        if 'Initiative' in opponent.defense['Ability']:
            initiative_condition = 1
            print('have an initiative condition')			            
            #self.initiativeFASERIP = 0 #to check below branch worked
            print(opponent.defense['Ability'])			            
        for key in faserip.keys():
            #print(key)			            
            #complex - a more powerful Nightcrawler - have to make intuition roll to even notice him! TODO: might hack to work for Invisible too?
            if key in opponent.defense['Ability']:
                print("has a defensive ability", self.name, self.initiativeFASERIP, opponent.name, opponent.initiativeFASERIP)			                
                if initiative_condition == 1 and self.initiativeFASERIP < opponent.initiativeFASERIP: #need to know the roll??
                    result_needed_index = faserip_index[opponent.defense['Ability'][key].split(';')[0]]
                    if key == "I":
                        ability_used_rank = self.irank					
                    ability_used_index = faserip_index[ability_used_rank]
                    #defense_roll = random.randint(1,100)
                    defense_roll = roll_faserip(pc = pc)
                    defense_check = universal_color(ability_used_rank, defense_roll)
                    if defense_check == "R" and (ability_used_index + 1) >= result_needed_index:
                        print(self.name, " finds ", opponent.name, "on red")
                    else:
                        print(self.name, " can't find ", opponent.name, "on red no action")
                        return
                    if defense_check == "Y" and ability_used_index >= result_needed_index:
                        print(self.name, " finds ", opponent.name, "on red")
                    else:
                        print(self.name, " can't find ", opponent.name, "on yellow no action")
                        return
                    if defense_check == "G" and ability_used_index > result_needed_index:
                        print(self.name, " finds ", opponent.name, "on red")
                    else:
                        print(self.name, " can't find ", opponent.name, "on green no action")
                        return
                else:				
                    pass
        #want to find damage rank #more sophisticated version has resistances as well for Physical and energy
        body_armour_rank = opponent.body_armour["Physical"]
        if self.alt_attack['energy'] == 1:
            body_armour_rank = opponent.body_armour["Energy"]		
		
        if slugfest == 1:
            if self.talents['martial_arts']['B'] == 1:
                fighting_cs = fighting_cs + 1
        else: #when have more - take max that applies, don't stack  #only good for Edged currently
            if 'Weapon Specialist' in self.talents or 'Weapon Specialist: (Claws)' in self.talents:
                fighting_cs = fighting_cs + 2
                print("Weapon Specialist Fighter:", self.name)
            elif 'Weapon Master' in self.talents or 'Sharp Weapons' in self.talents or 'Oriental Weapons' in self.talents or 'Thrown Weapons' in self.talents or 'Marksman' in self.talents or 'Guns' in self.talents or 'Bows' in self.talents:
                fighting_cs = fighting_cs + 1
            elif 'Thrown Objects' in self.talents: #stacks with Thrown Weapons
                fighting_cs = fighting_cs + 1
            else:
                pass #no weapon talents
            bypass_flag = 1					
            if self.alt_attack['edged'] == 1:  #compare to body armour
                print("Edged Fighting")
                damage_list = self.attack['Edged']['S'].split(';')
            elif self.alt_attack['blunt'] == 1:  #compare to body armour
                print("Blunt Fighting")
                damage_list = self.attack['Blunt']['S'].split(';')
                bypass_flag = 0
            elif self.alt_attack['throwing-blunt'] == 1:  #compare to body armour
                print("Throwing Blunt Fighting")
                damage_list = self.attack['Throwing Blunt']['R'].split(';')
                bypass_flag = 0
            elif self.alt_attack['throwing-edged'] == 1:  #compare to body armour
                print("Throwing Edged Fighting")
                damage_list = self.attack['Throwing Edged']['R'].split(';')
            elif self.alt_attack['shooting'] == 1:  #compare to body armour
                print("Shooting Fighting")
                damage_list = self.attack['Shooting']['R'].split(';')
            else:
                pass ###powers or something else
            ## Attacks that can't bypass armour
            print("sussing out :", self.alt_attack)
            if self.alt_attack['energy'] == 1:  #compare to body armour
                #print("Energy Fighting", "abs", self.attack['Energy']['AB'])
                print("Energy Fighting", "abs", self.attack['Energy']['AB'])
                bypass_flag = 0
                damage_list = self.attack['Energy']['R'].split(';') 
                #checking if Energy Absorption capabilities - TODO: other Absorptions
                if self.attack['Energy']['AB'] != '':
                    if int(self.attack['Energy']['AB']) > dict_faserip[damage_list[0]]:
                        ###this needs to be a string rank
                        damage_list[0] = nearest_rank(int(self.attack['Energy']['AB'])) 				
                        self.attack['Energy']['AB'] = 0
                        print("Blasting Back with ", damage_list[0], "absorbed energy!")
            elif self.alt_attack['force'] == 1:  #compare to body armour
                print("Force Fighting")  ##need check for the max for these or a more sophisticated preferred for ranged, area, etc. and alt_attack
                damage_list = self.attack['Force']['R'].split(';')
                if ';' not in self.attack['Force']['R']:
                    damage_list = self.attack['Force']['A'].split(';')
                bypass_flag = 0
            elif self.alt_attack['mental'] == 1:  #don't compare to body armour
                print("Mental Fighting")  ##need checks for the max for these or a more sophisticated preferred for ranged, area, etc. and alt_attack
                damage_list = self.attack['Mental']['R'].split(';')
                if ';' not in self.attack['Mental']['R']:
                    damage_list = self.attack['Mental']['C'].split(';')
                bypass_flag = 1				
            print("Damage List", damage_list)
				

            if len(damage_list) > 1:
                damage_rank = damage_list[0]
                material_strength = damage_list[1]
            else:
                damage_rank = damage_list[0]
                material_strength = damage_list[0]
            if bypass_flag == 1:
                if "Body Armour" in opponent.equipment_adj_rank:# and "Body Armour" not in opponent.power_adj_rank:  #make this for edged things only eventually
                    #weapon could penetrate and ignore
                    print("Body Armour is Equipment")
                    damage_index = faserip_index[damage_rank]
                    armour_index = faserip_index[body_armour_rank]
                    if damage_index >= armour_index:
                        print("Body Armour Penetrated")					                    
                        body_armour_rank = "Sh0"
						
                    #weapon could penetrate and ignore
                if self.alt_attack['armour-piercing'] == 1:
                    print("Armour Piercing Attack - no armour")
                    damage_index = faserip_index[damage_rank]
                    armour_index = faserip_index[body_armour_rank]
                    #need to implement if armour piercing is just a CS reduction or bypasses entirely - e.g. Shadowcat.
                    body_armour_rank = "Sh0"
                elif self.alt_attack['mental'] == 1:
                    print("Mental Attack - no armour")
                    damage_index = faserip_index[damage_rank]
                    armour_index = faserip_index[body_armour_rank]
                    #need to implement if armour piercing is just a CS reduction or bypasses entirely - e.g. Shadowcat.
                    body_armour_rank = "Sh0"
            
        ###Force Field Check
        force_field_rank = "Sh0"		        
        if 'Force Field' in opponent.powers_adj_rank:
            force_field_rank = opponent.powers_adj_rank['Force Field'].split(';')[0]  #could check if two ranks here for Physical/Energy version
        #print(self.name, " is attacking force field of ", force_field_rank)
        #Apply fighting column shifts
        if fighting_cs != 0:
            fighting_rank = column_shift(fighting_rank, fighting_cs)
            print("fighting cs rank 1", fighting_rank)
        
        print("checking self.mook", type(self.mook))
        #note mook should be an integer - not worth mooking only 2 mooks, should check for extra attacks instead
        if int(self.mook) == 0 and len(possible_opponents) > 2:  #no extra attacks
            fighting_cs = -4
            print('Mook Rule can be Used')
        else:
            ##multi attack check here? add to range self.attacks 
            print('checking Fighting Feat')
            #if dict_faserip[self.frank] < 30:
            if dict_faserip[fighting_rank] < 30:
                #no point doing multiattack except in a game karma type situation
                fighting_cs = 0  ## reset for the multattack shift
                #pass
            #elif dict_faserip[self.frank] < 50:
            elif dict_faserip[fighting_rank] < 50:
                #Rm or In fighting no point trying for 3 as Amazing intensity, try for two
                fighting_roll = random.randint(1,100)
                fighting_cs = -3  #going to need to change below to have an effective fighting rank from fighting_cs type things

                if dict_faserip[fighting_rank] < 40:
                #Rm
                    fighting_color = universal_color(fighting_rank, fighting_roll)
                    if fighting_color == "Y" or fighting_color == "R":
                        extra_attacks = 1
                        fighting_cs = -1
                else:
                #In
                    fighting_color = universal_color(fighting_rank, fighting_roll)
                    if fighting_color != "W":
                        extra_attacks = 1
                        fighting_cs = -1
    
            else:
                #Amazing fighting or better Amazing intensity, try for three
                fighting_roll = roll_faserip(pc = pc)
                fighting_cs = -3  #going to need to change below to have an effective fighting rank from fighting_cs type things
                fighting_color = universal_color(fighting_rank, fighting_roll)
                if fighting_color == "Y" or fighting_color == "R":
                    extra_attacks = 2
                    fighting_cs = -1
                
                if fighting_rank != "Am" and fighting_color == "G":
                #put adjustment for green and Monstrous or better
                    extra_attacks = 2
                    fighting_cs = -1

        #SPEED CHECK default to after multiple attack roll
        if 'Hyper-Speed' in opponent.powers_adj_rank:
            #need mental or mystical attack
            #TODO consider 'level' type bonus for Quicksilver and other ridiculously fast that won't go in standard parameters to Unearthly?
            #same for Northstar
            speed_rank = opponent.powers_adj_rank['Hyper-Speed'].split(';')[0]
            speed_index = faserip_index[speed_rank]
            if speed_index < 5:
                speed_cs = 1
                fighting_cs = fighting_cs - speed_cs
            elif speed_index < 10:
                speed_cs = 2
                fighting_cs = fighting_cs - speed_cs
            else:
                speed_cs = 3
                fighting_cs = fighting_cs - speed_cs
            print(self.name, "attacking speedster ", opponent.name, speed_cs)

        if fighting_cs != 0:
            fighting_rank = column_shift(fighting_rank, fighting_cs)
            print("fighting cs rank 2 for Combat Rolls", fighting_rank)
        ## loop for extra attacks #check for characters with extra arms or tails or some speed quirks etc.
        print("extra attacks", extra_attacks)
        if 'Extra Attacks' in self.powers_adj_rank:
            extra_attacks_rank_multiplier = faserip_index[self.powers_adj_rank['Extra Attacks'].split(';')[0]]
        else:
            extra_attacks_rank_multiplier = 1
        for ea in range(extra_attacks*extra_attacks_rank_multiplier + 1*extra_attacks_rank_multiplier): #if no extra attacks and not a mook make a -4CS
            #should be just 1 here at this level
            assert len(self.attacks) == 1
            for i in range(len(self.attacks)):  
                try:
                    opponent = self.arena.find(self.arena.target, self)[0]
                except IndexError:
                    raise Victory()
                self.log.debug(f"{self.name} attacks {opponent.name} with {self.attacks[i].name}")
                # THE IMPORTANT PART TO WRITE, UNIVERSAL TABLE TIME!
                #quite a few evolutions of this
                print("ATTACKS", "FIGHTING", fighting_rank, "DAMAGE RANK", damage_rank, "OPPEND", opponent.erank, "BA", dict_faserip[opponent.body_armour["Physical"]], "BA-Used", dict_faserip[body_armour_rank])

				#damage, effect_type, effect = self.attacks[i].attackFASERIP(dict_faserip[opponent.body_armour["Physical"]], advantage=self.check_advantage(opponent), attack_rank=fighting_rank, damage_rank=damage_rank, endurance_rank=opponent.erank,other_attacks=self.alt_attack, talents=self.talents)  #put attack rank in
                if force_field_rank == "Sh0": #dummy, e.g. everyone doesn't really have a forcefield, but they are 'commonish' in superhero games
                    damage, effect_type, effect = self.attacks[i].attackFASERIP(dict_faserip[body_armour_rank], advantage=self.check_advantage(opponent), attack_rank=fighting_rank, damage_rank=damage_rank, endurance_rank=opponent.erank,other_attacks=self.alt_attack, talents=self.talents, pc = pc, opp_pc = opp_pc)  #put attack rank in
                else:
                    effect_type = None
                    effect = None
					#Need to check if forcefield can be phased through - or density control or other powers could add here
                    force_field_index = faserip_index[force_field_rank]
                    damage_index = faserip_index[damage_rank]
                    phase_check = 0
                    if 'Phasing' in self.powers_adj_rank:
                        phasing_rank = self.powers_adj_rank['Phasing'].split(';')[0]
                        phasing_roll = roll_faserip(pc = pc)
                        feat_check = feat(phasing_rank, force_field_rank, phasing_roll)
                        if feat_check:
                            print(self.name,  "phased through Force Field for full damage")
                            phase_check = 1
                        else: 
                            print(self.name,  "failed to Phase through Force Field")

                    #assuming all Force Fields are projected and can collapse - if individual maybe handle as Armour Pierced Body Armour?		
                    if phase_check == 0:							
                        if damage_index > force_field_index:
                            damage = dict_faserip[damage_rank] - dict_faserip[force_field_rank]					
                            print("Force Field fails!", opponent.name, " takes ", damage)					
                            #stun_roll = random.randint(1,100)
                            stun_roll = roll_faserip(pc = pc)
                            feat_check = feat(force_field_rank, damage_rank, stun_roll)
                            if feat_check:
                                print(opponent.name,  "survived Force Field going down")
                            else:
                                stun_rounds = random.randint(1,10)
                                opponent.stun = opponent.stun + stun_rounds
                                effect_type = "STUN"
                                effect = stun_rounds
                        else:
                            print(opponent.name, "Force Field absorbs all ", damage_rank, "from ", self.name)					
                            damage = 0
                    else:						
                        damage = dict_faserip[damage_rank]
                        print(self.name, "passes through Force Field", opponent.name, " takes ", damage)					

				
                print("DAMAGE", damage, "OPPONENTAC:", body_armour_rank)
				
                if damage > 0:
						
                    if int(self.mook) == 1 and len(possible_opponents) > 2:
                        print("beating on Mooks")
                        #time.sleep(10)	
                        for mook in possible_opponents:
                            mook.take_damageFASERIP(damage, effect_type, effect, self.alt_attack, verbose)
                            self.tally['damage'] += damage
                            self.tally['hits'] += 1
                    else:
                        print("not finding mook")
                        opponent.take_damageFASERIP(damage, effect_type, effect, self.alt_attack, verbose)
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
			
        #print("ALIVE opponents", len(self.arena.find('alive enemy')), self.arena.find('alive enemy'))
        # BONUS ACTION
        # heal  -healing word, a bonus action.
        if "Regeneration" in self.powers_adj_rank:
            print(self.powers_adj_rank['Regeneration'])
            #print(dict_faserip[self.powers_adj_rank['Regeneration']] )
            regen_points = dict_faserip[self.powers_adj_rank['Regeneration'].split(';')[0]]/10
            print("Regenerating:", regen_points, "Current Health", self.hp)
            self.hp = min(self.stated_hp, self.hp + regen_points)
            print("Regenerating:", regen_points, "New Health", self.hp)

        if self.healing_spells > 0:
            weakling = self.assess_wounded(verbose)
            if weakling != 0:
                self.cast_healing(weakling, verbose)
        # Main action!
        economy = len(self.arena.find('allies')) > len(self.arena.find('opponents')) > 0
        #print("ECONOMY", economy)
        #print("condition", self.condition)
        # Buff?
        print("stun condition is ", self.stun)
        if self.condition == 'netted':
            # NOT-RAW: DC10 strength check or something equally easy for monsters
            if verbose:
                print(self.name + " freed himself from a net")
            self.condition = 'normal'
        elif self.stun > 0:
            if verbose:
                print(self.name + " stunned for ", self.stun, "rounds so skip")
            print(self.name + " stunned for ", self.stun, "rounds so skip")
            self.stun -= 1
            print(" now down to", self.stun)
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

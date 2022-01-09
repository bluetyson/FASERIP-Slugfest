            #make this more streamline and multi-part
			def attack_check(attack_type, power_key, update_key, weapon=None):
                if weapon is None:			
                    if attack_type in newFASERIP[power_key]:
                        assign_key = newFASERIP[power_key][attack_type]
                        newFASERIP['Attack'][attack_type][update_key] = assign_key
                else:
                    if weapon in newFASERIP[power_key]:
                        assign_key = newFASERIP[power_key][weapon]
                        newFASERIP['Attack'][attack_type][update_key] = assign_key
                
                power_base = power_key.split('_')[0]
                if 'Armour Piercing' in power_base:
                    newFASERIP['Attack'][attack_type]['AP'] = 1
                    
            ### do Attacks
            attack_check('Blunt', 'Powers_Adj_Rank', 'S')
            attack_check('Blunt', 'Equipment_Adj_Rank', 'S')
            attack_check('Blunt', 'Powers_Adj_Rank', 'R', weapon='Blunt Missile')
            attack_check('Blunt', 'Equipment_Adj_Rank', 'R', weapon='Blunt Missile')
            attack_check('Blunt', 'Equipment_Adj_Rank', 'A', weapon='Blunt Area')
            attack_check('Blunt', 'Equipment_Adj_Rank', 'A', weapon='Blunt Area')
            
            attack_check('Edged', 'Powers_Adj_Rank', 'S')
            attack_check('Edged', 'Equipment_Adj_Rank', 'S')
            attack_check('Edged', 'Powers_Adj_Rank', 'S', weapon='Claws')
            attack_check('Edged', 'Equipment_Adj_Rank', 'S', weapon='Claws')
            attack_check('Edged', 'Equipment_Adj_Rank', 'S', weapon='Sword')
            attack_check('Edged', 'Powers_Adj_Rank', 'R', weapon='Edged Missile')
            attack_check('Edged', 'Equipment_Adj_Rank', 'R', weapon='Edged Missile')
            attack_check('Edged', 'Powers_Adj_Rank', 'A', weapon='Edged Area')
            attack_check('Edged', 'Equipment_Adj_Rank', 'A', weapon='Edged Area')

            attack_check('Throwing Edged', 'Equipment_Adj_Rank', 'R', weapon='Edged Missile:Boomerang')
            attack_check('Throwing Edged', 'Equipment_Adj_Rank', 'R', weapon='Boomerang')

            if "Boomerangs" in newFASERIP['Equipment_Adj_Rank']:
                if len(newFASERIP['Equipment_Adj_Rank']['Boomerangs']) == 0:
                    newFASERIP['Attack']['Throwing Edged']['R'] = newFASERIP['A'] + ";" #default A will do as pick an Arrow later
                else:
                    attack_check('Throwing Edged', 'Equipment_Adj_Rank', 'R', weapon='Boomerangs')
            
            #Shooting Group    
            attack_check('Shooting', 'Powers_Adj_Rank', 'R')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R')
            attack_check('Shooting', 'Powers_Adj_Rank', 'A', weapon='Shooting Area')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'A', weapon='Shooting Area')

            if "Bow" in newFASERIP['Equipment_Adj_Rank']:
                print("bow")
                if len(newFASERIP['Equipment_Adj_Rank']['Bow']) == 0:
                    newFASERIP['Attack']['Shooting']['R'] = newFASERIP['A']  + ";" #default A will do as pick an Arrow later
                else:
                    attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Bow')
                
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Bow and Arrows')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Bow with Quiver')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Bow and Arrows')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Longbow and Arrows')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Compound Bow')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Crossbow')
            attack_check('Shooting', 'Equipment_Adj_Rank', 'R', weapon='Wrist Crossbow')
			
### Powers
            attack_check('Force', 'Powers_Adj_Rank', 'S')
            attack_check('Force', 'Equipment_Adj_Rank', 'S')
            attack_check('Force', 'Powers_Adj_Rank', 'R', weapon='Force Blast')
            attack_check('Force', 'Equipment_Adj_Rank', 'R', weapon='Force Blast')
            attack_check('Force', 'Equipment_Adj_Rank', 'A', weapon='Force Area')
            attack_check('Force', 'Equipment_Adj_Rank', 'A', weapon='Force Area')

            attack_check('Energy', 'Powers_Adj_Rank', 'S')
            attack_check('Energy', 'Equipment_Adj_Rank', 'S')
            attack_check('Energy', 'Powers_Adj_Rank', 'R', weapon='Energy Blast')
            attack_check('Energy', 'Equipment_Adj_Rank', 'R', weapon='Energy Blast')
            attack_check('Energy', 'Equipment_Adj_Rank', 'A', weapon='Energy Area')
            attack_check('Energy', 'Equipment_Adj_Rank', 'A', weapon='Energy Area')

            attack_check('Energy', 'Equipment_Adj_Rank', 'R', weapon='Blaster Pistols')

from DnD_battler import Creature, Encounter

#level1 = Creature.load('Cat')
billbybob2 = Creature.load('Rat')
#level1 = Creature.load('Scientist')
#billbybob2 = Creature.load('Lawyer')
#level1 = Creature.load('Lawyer')
billbybob2 = Creature.load('Rat Pack')
#level1 = Creature.load('Guard Dog')
billbybob2 = Creature.load('Cat')

level1 = Creature.load('Amazing Martial Artist')

billbybob2 = Creature.load('Lawyer')
#billbybob3 = Creature.load('Lawyer')
billbybob4 = Creature.load('Boxer')
#billbybob5 = Creature.load('Boxer')
#billbybob6 = Creature.load('Boxer')
#billbybob7 = Creature.load('Boxer')
#billbybob8 = Creature.load('Boxer')
#billbybob9 = Creature.load('Boxer')
#billbybob10 = Creature.load('Boxer')
#billbybob15 = Creature.load('Boxer')
#billbybob16 = Creature.load('Boxer')
#billbybob17 = Creature.load('Boxer')
#billbybob18 = Creature.load('Boxer')
#billbybob19 = Creature.load('Boxer')
#billbybob20 = Creature.load('Boxer')
#billbybob21 = Creature.load('Boxer')
#billbybob22 = Creature.load('Boxer')

arena2 = Encounter(level1).addmobFASERIP(12).go_to_war(1)
#print(arena2.battle())
print(arena2.go_to_war(100))

from DnD_battler import Creature, Encounter

#level1 = Creature.load('Cat')
Rat = Creature.load('Rat')
#level1 = Creature.load('Scientist')
#billbybob2 = Creature.load('Lawyer')
Lawyer = Creature.load('Lawyer')
RatPack = Creature.load('Rat Pack')
#level1 = Creature.load('Guard Dog')
billbybob2 = Creature.load('Cat')

arenaRodent = Encounter(Creature.load("Cat"), Creature.load("Rat"))

print(arenaRodent.go_to_war(100))



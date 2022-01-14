from DnD_battler import Creature, Encounter

#level1 = Creature.load('Cat')
Rat = Creature.load('Rat')
#level1 = Creature.load('Scientist')
#billbybob2 = Creature.load('Lawyer')
Lawyer = Creature.load('Lawyer')
RatPack = Creature.load('Rat Pack')
#level1 = Creature.load('Guard Dog')
billbybob2 = Creature.load('Cat')

#arenaRodent = Encounter(Creature.load("Cat"), Creature.load("Rat"))
arenaRodent = Encounter(Creature.load("Lawyer"), Creature.load("Rat Pack"))

#print(arenaRodent.go_to_war(1))
#print(arenaRodent.go_to_war(100))

print(Creature.load('Rat').generate_character_sheetFASERIP())
print(Creature.load('Lawyer').generate_character_sheetFASERIP())
print(Creature.load('Cat').generate_character_sheetFASERIP())
print(Creature.load('Cyclops').generate_character_sheetFASERIP())



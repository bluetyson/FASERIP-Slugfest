from DnD_battler import Creature, Encounter

level1 = Creature.load('Cat')
billbybob2 = Creature.load('Rat')
print(billbybob2.alignment)
#billbybob2.alignment = "green dragon evil"
arena2 = Encounter(level1, billbybob2)
print(arena2.battle())
#print(arena2.go_to_war(10000))

## notes on running
#load_beastiary from csv

#loads into settings and checks json

#make abilities and ability dice d100

#make universal table combat system
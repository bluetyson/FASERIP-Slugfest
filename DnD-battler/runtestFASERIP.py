from DnD_battler import Creature, Encounter

level1 = Creature.load('Cat')
billbybob2 = Creature.load('Rat')
#level1 = Creature.load('Scientist')
#billbybob2 = Creature.load('Lawyer')
level1 = Creature.load('Lawyer')
billbybob2 = Creature.load('Rat Pack')
level1 = Creature.load('Guard Dog')
billbybob2 = Creature.load('Cat')

level1 = Creature.load('Amazing Martial Artist')
billbybob2 = Creature.load('Lawyer')
billbybob3 = Creature.load('Lawyer')
billbybob4 = Creature.load('Plumber')
billbybob5 = Creature.load('Plumber')
billbybob6 = Creature.load('Plumber')
billbybob7 = Creature.load('Plumber')
billbybob8 = Creature.load('Plumber')
billbybob9 = Creature.load('Plumber')
billbybob10 = Creature.load('Plumber')

print(billbybob2.alignment, billbybob2.starting_hp, billbybob2.hp)
#billbybob2.alignment = "green dragon evil"
arena2 = Encounter(level1, billbybob4, billbybob2)
#print(arena2)
#print(arena2.battle())
#print(arena2.go_to_war(100))
#arena2 = Encounter(level1).addmobFASERIP(10)
#arena2 = Encounter(level1).addmobFASERIP(6)
#arena2 = Encounter(level1).addmobFASERIP(2)
arena2 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob10)
print(arena2)
#print(arena2.go_to_war(100))
print(arena2.go_to_war(1000))
#print(arena2.go_to_war(10000))

## notes on running
#load_beastiary from csv

#loads into settings and checks json

#make abilities and ability dice d100

#make universal table combat system

#make slams and stuns

#make other weapons - assume short range?

#add in armour to slow things down - possible infinite loops though if no-one can get through each other's armour

#set actions for stun and check if conscious

#add edged
#then add shooting - but for simulation purposes about the same - could assume high tech energy weapons similarly
#add martial arts in
#power fun
#then random character gen? - java things

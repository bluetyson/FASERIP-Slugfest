from DnD_battler import Creature, Encounter
import pandas as pd

arenaEarly = Encounter(Creature.load("Early Hulk"), Creature.load("Early Thing"))
arenaClobbering = Encounter(Creature.load("The Hulk"), Creature.load("The Thing"))

#print(Creature.load("The Hulk"))
#print(Creature.load("The Thing"))

#print(arenaKunLun.set_deathmatch())
#print(arenaKunLun.go_to_war(1))
#print(arenaClobbering.go_to_war(100))
#print(arenaClobbering.go_to_war(500))
#print(arenaClobbering.go_to_war(1000))
#print(arenaClobbering.go_to_war(2000))
print(arenaClobbering.go_to_war(5000))
#print(arenaKunLun.go_to_war(10000))
#print(arenaKunLun.go_to_war(100000))

#print(arenaEarly.go_to_war(1))


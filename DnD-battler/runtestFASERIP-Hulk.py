from DnD_battler import Creature, Encounter
import pandas as pd

arenaKunLun2 = Encounter(Creature.load("The Hulk"), Creature.load("The Thing"))
#arenaKunLun2 = Encounter(Creature.load("The Hulk 2"), Creature.load("The Thing"))

#print(Creature.load("The Hulk"))
#print(Creature.load("The Thing"))

#print(arenaKunLun.set_deathmatch())
#print(arenaKunLun.go_to_war(1))
#print(arenaKunLun.go_to_war(100))
#print(arenaKunLun.go_to_war(500))
#print(arenaKunLun.go_to_war(1000))
#print(arenaKunLun.go_to_war(2000))
#print(arenaKunLun.go_to_war(5000))
#print(arenaKunLun.go_to_war(10000))
#print(arenaKunLun.go_to_war(100000))

#print(arenaKunLun2.go_to_war(1))
#print(arenaKunLun2.go_to_war(100))
#print(arenaKunLun2.go_to_war(500))
#print(arenaKunLun2.go_to_war(1000))
#print(arenaKunLun2.go_to_war(5000))
#print(arenaKunLun2.go_to_war(10000))
#print(arenaKunLun2.go_to_war(20000))
print(arenaKunLun2.go_to_war(100000))
#print(level1.hp)


from DnD_battler import Creature, Encounter
import pandas as pd

arenaDangerRoom = Encounter(Creature.load("Cyclops"), Creature.load("Shadowcat"))

print(arenaDangerRoom.go_to_war(1))
#print(arenaDangerRoom.go_to_war(10))
#print(arenaDangerRoom.go_to_war(100))
#print(arenaDangerRoom.go_to_war(500))
#print(arenaDangerRoom.go_to_war(1000))
#print(arenaDangerRoom.go_to_war(2000))
#print(arenaDangerRoom.go_to_war(5000))
#print(arenaDangerRoom.go_to_war(10000))
#print(arenaDangerRoom.go_to_war(5000))

#print(arenaDangerRoomNA.go_to_war(10000))
#print(arenaDangerRoomNA.go_to_war(10000))
#print(arenaDangerRoomEarly.go_to_war(1000))
#print(arenaDangerRoomEarly.go_to_war(10000))

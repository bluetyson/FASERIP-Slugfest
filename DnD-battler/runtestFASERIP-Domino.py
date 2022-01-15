from DnD_battler import Creature, Encounter
import pandas as pd

#arenaDangerRoom = Encounter(Creature.load("Longshot"), Creature.load("Domino"))
#arenaDangerRoom = Encounter(Creature.load("Domino No Luck"), Creature.load("Domino"))
arenaDangerRoom = Encounter(Creature.load("Longshot No Luck"), Creature.load("Longshot"))


#print(arenaDangerRoom.go_to_war(1))
#print(arenaDangerRoom.go_to_war(1))
print(arenaDangerRoom.go_to_war(100))
#print(arenaDangerRoom.go_to_war(500))
#print(arenaDangerRoom.go_to_war(1000))
#print(arenaDangerRoom.go_to_war(2000))
#print(arenaDangerRoom.go_to_war(5000))
#print(arenaDangerRoom.go_to_war(50000))
#print(arenaDangerRoom.go_to_war(10000))
#print(arenaDangerRoom.go_to_war(100000))
#print(arenaDangerRoom.go_to_war(5000))

#print(arenaDangerRoomNA.go_to_war(10000))
#print(arenaDangerRoomNA.go_to_war(10000))
#print(arenaDangerRoomEarly.go_to_war(1000))
#print(arenaDangerRoomEarly.go_to_war(10000))

beastiary2 = Creature.load_beastiary(r'J:\CLONE\WORK2\FASERIP-Slugfest\DnD-battler\DnD_battler\beastiaryFASERIP.csv')


#print(beastiary2)

for key in beastiary2:
	print (beastiary2[key])
	break
	
print (beastiary2['Cyclops'])
	
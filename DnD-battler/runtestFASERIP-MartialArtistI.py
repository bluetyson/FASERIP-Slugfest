from DnD_battler import Creature, Encounter
import pandas as pd

level1 = Creature.load('Amazing Martial Artist')

#arena215 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16, billbybob17, billbybob18, billbybob19, billbybob20, billbybob21, billbybob22, billbybob23)
arenaKunLun = Encounter()

MHMA = pd.read_csv(r'J:\CLONE\WORK2\FASERIP-Slugfest\AmazingMartialArtistI.csv')
#print(MHMA)
for index, row in MHMA.iterrows():
	#if 'Shang' in 
	#print(row['Name'])
	arenaKunLun.append(Creature.load(row["Name"]))


#print(arenaKunLun.set_deathmatch())
#print(arenaKunLun.go_to_war(1))
print(arenaKunLun.go_to_war(1))
#print(arenaKunLun.go_to_war(10000))
#print(level1.hp)


from DnD_battler import Creature, Encounter

#level1 = Creature.load('Cat')
Rat = Creature.load('Rat')
#level1 = Creature.load('Scientist')
#billbybob2 = Creature.load('Lawyer')
Lawyer = Creature.load('Lawyer')
RatPack = Creature.load('Rat Pack')
#level1 = Creature.load('Guard Dog')
billbybob2 = Creature.load('Cat')

level1 = Creature.load('Amazing Martial Artist')

billbybob2 = Creature.load('Lawyer')
billbybob3 = Creature.load('Lawyer')
billbybob4 = Creature.load('Boxer')
billbybob5 = Creature.load('Boxer')
billbybob6 = Creature.load('Boxer')
billbybob7 = Creature.load('Boxer')
billbybob8 = Creature.load('Boxer')
billbybob9 = Creature.load('Boxer')
billbybob10 = Creature.load('Boxer')
billbybob15 = Creature.load('Boxer')
billbybob16 = Creature.load('Boxer')
billbybob17 = Creature.load('Boxer')
billbybob18 = Creature.load('Boxer')
billbybob19 = Creature.load('Boxer')
billbybob20 = Creature.load('Boxer')
billbybob21 = Creature.load('Boxer')
billbybob22 = Creature.load('Boxer')
billbybob23 = Creature.load('Boxer')

#print(billbybob2.alignment, billbybob2.starting_hp, billbybob2.hp)
#billbybob2.alignment = "green dragon evil"
#arena2 = Encounter(level1, billbybob4, billbybob2)
#print(arena2)
#print(arena2.battle())
#print(arena2.go_to_war(100))
#arena2 = Encounter(level1).addmobFASERIP(10)
#arena2 = Encounter(level1).addmobFASERIP(6)
#arena2 = Encounter(level1).addmobFASERIP(2)
arena2 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob10)
#print(arena2)

#arena3 = Encounter(level1).addmobFASERIP(1)
arena3 = Encounter(Creature.load('Amazing Martial Artist')).addmobFASERIP(1)
print("AddMob Martial Artist v Boxer")

billbybob4 = Creature.load('Boxer')
#level1 = Creature.load('Amazing Martial Artist')
#level1 = Creature.load('Psyched Amazing Martial Artist')
level1 = Creature.load('GHOTMU Amazing Martial Artist')
#level1 = Creature.load('GHOTMU Psyched Amazing Martial Artist')

arena2 = Encounter(level1, billbybob4)
print("Encounter Martial Artist v Boxer")


#print(arena3.go_to_war(1))
#print(arena2.go_to_war(1))
#print(arena2.go_to_war(100))
#print(arena2.go_to_war(1000))
#print(arena2.go_to_war(10000))
print(arena2)
print(arena3)

#print(dir(arena2))
#print(dir(arena3))

assert dir(arena2) == dir(arena3)

for x in arena2.__dict__:
	print(x, arena2.__dict__[x])
	
for x in arena3.__dict__:
	print(x, arena3.__dict__[x])
	
	
#print(arena2.go_to_war(1))
#print(arena3.go_to_war(1))

#billbybob15 = Creature.load('Boxer', alignment="mob")
#level15 = Creature.load('Amazing Martial Artist')
#arena4 = Encounter(billbybob15, level15)
#print(arena4.go_to_war(1))

#billbybob16 = Creature.load('Boxer', alignment="mob")
#level16 = Creature.load('Amazing Martial Artist')
#arena5 = Encounter(level16, billbybob16)
#print(arena5.go_to_war(1000))


#arena2 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob10)
print(arena2)
#level1.hp = 120
#arena21 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9)
#arena27 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15)
#arena28 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16)
#arena210 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16, billbybob17, billbybob18)
#arena211 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16, billbybob17, billbybob18, billbybob19)
#arena212 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16, billbybob17, billbybob18, billbybob19, billbybob20)
#arena213 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16, billbybob17, billbybob18, billbybob19, billbybob20, billbybob21)
#arena214 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16, billbybob17, billbybob18, billbybob19, billbybob20, billbybob21, billbybob22)
arena215 = Encounter(level1, billbybob4, billbybob5, billbybob6, billbybob7, billbybob8, billbybob9, billbybob15, billbybob16, billbybob17, billbybob18, billbybob19, billbybob20, billbybob21, billbybob22, billbybob23)
arenaHerbert = Encounter(Lawyer, RatPack)
#print(arena2.go_to_war(1000))
#print(arena2.go_to_war(10000))
#print(arena21.go_to_war(100))
#print(arena21.go_to_war(1000))
#print(arena21.go_to_war(10000))
#print(arena22.go_to_war(1000))

#print(arena27.go_to_war(100))
#print(arena27.go_to_war(1000))
#print(arena28.go_to_war(1000))
#print(arena27.go_to_war(10000))
#print(arena210.go_to_war(1000))
#print(arena211.go_to_war(1000))
#print(arena212.go_to_war(1000))
#print(arena213.go_to_war(1000))
#print(arena214.go_to_war(1000))
#print(arena215.go_to_war(100))
#print(arena215.battle())
#print(arena215.go_to_war(1000))
print(arenaHerbert.go_to_war(10))
#print(level1.hp)


## notes on running
#load_beastiary from csv

#loads into settings and checks json

#make abilities and ability dice d100 - DONE

#make universal table combat system - DONE

#make slams and stuns - DONE

#make other weapons - assume short range?

#add in armour to slow things down - possible infinite loops though if no-one can get through each other's armour  #need to check for armour stopping damage on slams
#standard reduction if type is Energy/Force?  Forcefield reductions?

#set actions for stun and check if conscious - DONE

#add edged
#then add shooting - but for simulation purposes about the same - could assume high tech energy weapons similarly
#add martial arts in - DONE
#power fun
#then random character gen? - java things - to this and get powers list - then need to somehow add them to a simulator - much more work than a random generator
#could we get GPT or clone to name characters sensibly(ish)?

#add group initiative

#simulate maximum opponents slugfest at a time - one roll to hit and damage everyone left have to work this out - have to be in waves, or it is just roll, then maybe take out a bunch of mooks in two hits? Whether
#6 or 60 - half a dozen at once, six hex facing? how to 'damage all at once'?

#find > 2 opponents - DONE
# do attack - apply results to all? - DONE


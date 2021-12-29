from DnD_battler import Creature, Encounter

level1 = Creature.load('young black dragon')
billbybob2 = Creature.load('young green dragon')
billbybob2.alignment = "green dragon evil"
arena2 = Encounter(level1, billbybob2)
print(arena2.go_to_war(10000))
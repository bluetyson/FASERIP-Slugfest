# FASERIP Slugfest simulator
Simulate who would win in a FASERIP encounter
Based largely on :- https://github.com/matteoferla/DnD-battler/tree/dev

> This is a python 3 script and is not intended to work with 2. 
> This is a very messy work in progress translating Matteo Ferla's DnD battler to work with FASERIP, so may go through many changes.
> So name of module etc. will change eventually,
> 
Welcome to the FASERIP Encounter simulator.
It was written to determine victory probabilities and to test some hypotheses.

## Opponents list
The simulator relies on creature information present in the `beastiaryFASERIP.csv` file. 
This is basically taken from my FATERIP hack table https://docs.google.com/document/d/1Rmk-3fX2JG3tJPJrtTnhWatT8gcQfGf4e_nqK-4lNz0/edit
There are also characters added for the various sample ```runtestFASERIP.py``` type scripts.
These now have Powers, Equipment, Talents, Contacts columns with _Adj_ and _Rank_ additional columns to attempt some standardisation and simplication for purposes of combat simulation, never going to be perfect unless go back and edit all the characters - which won't happen, but anyone could do, especially for those they are interested in,
   
- If you want to simulate a -4 CS multiattack on everyone at once - set mook = 1 for one side and leave zero on the other.  To turn off, have everyone be mooks.
    - still need a mode where can attack, say in groups of 6 at any given time.

- Code is a work in progress, so breaking changes will happen to abilities in the CSV and old runtest* files.  Copy the latest version into the bestiaryFASERIP to run in that case.
- If stuck, open an issue, or ask on the blog if you prefer.  Probably notice here more quickly

# Tests
- Note that Hawkeye has a Bow and a Wrist Crossbow so if in Powers or Equipment data someone has two of the same type, the second will overwrite the first - you can rearrange the character sheet to fix, or just edit in beastiaryFASERIP.

# Documentation
This module allows the simulation of a FASERIP encounter.
It has three main classes:  Dice (and its derivatives), Character, Encounter. 

**Teams.** Multiple creatures of the same alignment will team up to fight creatures of different alignments in a simulation (`Encounter().battle()` for a single iteration or `Encounter().go_to_war()` for multiple).
**Gridless.** The game assumes everyone is in contact with everyone and not on a grid. The reason being is tactics.
**Tactics.** Tactics are highly problematic both in targetting and actions to take. Players do not play as strategically as they should due to heroism and kill tallies, while the GM might play enemies really dumbly to avoid a TPD.
**Targeting.** The simulator is set up as a munchkin combat where everyone targets the weakest opponent (The global variable `TARGET="enemy alive weakest"` makes the `find_weakest_target` method of the `Encounter` be used, but could be changed (unwisely) to a permutation of enemy/ally alive/dead weakest/random/fiercest.
The muchkinishness has a deleterious side-effect when the method deathmatch of the Encounter class is invoked —this allocates each Creature object in the Encounter object in a different team.
- e.g. have a 25 Martial Artist contest and 'enemy alive weakest' means that the characters will basically be eliminated in general reverse order of Health, so those with the highest will win all the time, even if just slightly more.   Use 'enemy alive random' for this setting, instead.
- 
**Actions.** Action choice is dictated by turn economy. A character of a team with the greater turn economy will dodge (if it knows itself a target) or throw a net (if it has one), and so forth while a creature on the opposed side will opt for a slugfest.  This needs to be updated and implemented for FASERIP, no grappling yet.

```
>>> from DnD_battler import Creature, Encounter
>>> Creature.load('Cyclops') # get from beastiary
>>> level1 = Creature(name="Wolverine")
>>> billybob = Creature("Sabretooth")
>>> billybob.alignment = "psychopath"
>>> level1.alignment = "x-men"
>>> arena = DnD.Encounter(level1, billybob)  #Encounter accepts both Creature and strings.
>>> print(arena.go_to_war(10000)) #simulate 10,000 times
>>> print(arena.battle()) # simulate one encounter and tell what happens.
>>> print(Creature.load('Cyclops').generate_character_sheet())  #md character sheet.  ### this won't be much use for FASERIP
>>> print(Encounter.load("Cyclops").addmob(12).go_to_war(10))  .Shang-Chi vs a dozen Plumbers.

```

## Creature: parameters and attributes

The creature class can be started from scratch or from a monster from the manual:

```python
from DnD_battler import Creature
Creature()
Creature.load('Cyclops')
```
Both accept several arguments. 

An ongoing work in progress, see the bestiaryFASERIP.csv an benriely.csv for the general idea.

- level - using for assorted CS bonuses, e.g. when it says 'Cyclops has Incredible Agility with Optic Blasts' and he has Excellent, put 2 in there.  Descriptive Weapon Specialist bonus.
- Attack - dictionary to approximate different types of attacks
- Defense - dictionary to approximate different types of attacks
- a basic heuristic attack_preferred best attack calculation is done
- - stated_ac = a Body Armour string from the data.
- body_armour - attempt at approximate parsing of vs Physical and Energy versions - applied a - 2CS not a -20 points for now for Physical to Energy where not stated.  These need to be checked when you use them, as just an algorithmic guess at counting which one is where in the description.
- resistances - parsed list of resitance powers
- level use to put added CS bonus for power related Weapon Specialists etc.
- FASERIP - self explantaory, String rank 2 character abbreviation
- Powers, Powers_Rank, Powers_Adj, Powers_Adj_Rank, various stages of parsing of the character writeups to attempt to assign ranks heuristically to things and standardise
- Equipment, see Powers above
- Vehicle - not done yet
- Talents, Talents_Adj, parsing them out to standardise
- Contacts, see Talents
- Weakness, not really attempted yet, but some will have
- Powers_Form - bonus powers from the Form for random characters from the Ultimate Powers Book.
- Spd = speed rank in usual terrain, relative to humans.  Not used as yet.
- Attack - standardising combat types simply to allow for simulation algorithms to work
- Defense - as above, but most of these not implemented in simulation yet
- Dam - for some esoteric Damage bonus if needed, not implemented yet. e.g. if someone has an attack not doing a set Rank if Damage - Great Sword, Axe perhaps.
- Climbing
- Escaping - probably not needed with Defense, likely will remove eventually when change parsing
- T = Type of Damage: E = Edged, B= Blunt, S = Shooting, H = Advanced Technology, 2 = Blunt and Edged, W = S and 2
    - It will currently check to see if a Killing type is possible - but doesn't do anything about ranged anything or movement.
- martial_arts - add one letter to a string for each type, eg ABCDE, AE etc. Occasionally parser may find multiples, so could trim to 5 characters max.
    - other Talents can be handled similarly and put them in self.talents in the Creature class
- mook - set to allow simulation of hero vs hoods
- H, K, Res, Pop should be self-explanatory from the character data - the first two are calculated in code anyway 
- Climbing, Escaping [other standard type actions will likely get columns at some stage]


- to use characters in Simulations may require a bit of editing of the csv or the character parsing routines if many instances that can be handled, the csvs are designed so most of the handcoding is done.



## Logging

The module uses a shared `logging.Logger` with a `sys.stdout` stream set to `logging.INFO`.

```python
from DnD_battler import Creature, log

log is Creature.log
```

Therefore, alter the logging to a different handler if needed as per usual.

```python
from DnD_battler import log
import logging, io

# change the default...
log.handlers[0].setLevel(logging.DEBUG)  # logging.DEBUG = 20
# add a new one.
stream = io.StringIO('started')
handler = logging.StreamHandler(stream)
handler.set_name('stream')
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
log.addHandler(handler)
log.info('Next battle!')
```

## Note on altering methods

The behaviour of a Creature is dictated by `act()` class method.
Specifically, the simulations runs _n_ encounters via `Encounter(<...>).go_to_war(n)_`, which runs `.battle()` _n_ times. The latter method iterates across the creatures running their `Creature().act()` method, which makes them decide whether to heal, dodge, attack, free themselves, buff, throw net etc. The attack is called `.multiattack()`
If you want to override the behaviour of say a creature to attack regardlessly and at random you can change the class's method `act()`

```

# Class summary
## Dice
There is a roll_faserip function in ranks module instead, here.  An initiative roll as well.

## Character
Character has a boatload of attributes. It can be initialised with a dictionary or an unpacked one... or a single name matching a preset.  The boatload will get bigger for FASERIP to eventually deal with powers, different types of attacks, etc.
## Encounter
Encounter includes the following method:
    battle(reset=1) does a single battle (after a reset of values if asked). it calls a few other fuctions such as roll_for_initiative()
    go_to_war(rounds=1000) performs many battles and gives the team results
verbosity (verbose=1) is optional. And will be hopefully be written out of the code.

There is some code messiness resulting from the unclear distinction between Encounter and Creature object, namely
a Creature interacting with another is generally a Creature method, while a Creature searching across the list of Creatures in the Encounter is an Encounter method.

There are one or two approximations that are marked `#NOT-RAW`. In the Encounter.battle method there are some thought on the action choices.



# class Creature(builtins.object)
Creature class handles the creatures and their actions and some interactions with the encounter.

Methods defined here:

TBA_act(self, verbose=0)
    # TODO

__init__(self, wildcard, **kwargs)
    Creature object creation. A lot of paramaters make a creature so a lot of assumptions are made (see __init__`).
    :param wildcard: the name of the creature.
      If nothing else is passed it will take it from the beastiary.
      If a dictionary is passed, it will process it like **kwargs,
      If a Creature object is passed it will make a copy
    :param kwargs: a lot of arguments...
    :return: a creature.
    
    The arguments are many. The below is not up to date, as of 20220105, but will give you an idea.
    >>> print(Creature.load('Amazing Martial Artist').__dict__)
    `CHECK_SETTINGS {'name': 'Cyclops', 'identity': 'Scott Summers', 'alignment': 'Cyclops', 'stated_ac': 'Ex;', 'body_armour': "{'Physical': 'Ex', 'Energy': 'Ex'}", 'level': '2', 'f': 'Ex', 'a': 'Ex', 's': 'Gd', 'e': 'Rm', 'r': 'Gd', 'i': 'Rm', 'p': 'Ex', 'h': '80', 'k': '60', 'res': 'Gd', 'powers': '{\'Optic Blast\': \'up to Mn Force at 3 areas. Each area beyond that is decreased by 1 rank\', \'Break Fall\': \'to slow fall w/ Ty damage to target\', \'Wide Angle Beam\': \'In to 2 areas\', \'Transform energy into Optic Blast\': \'a Red Psyche FEAT. must be made or he takes normal damage\', \'Partial Immunity\': "Cyclops is immune to Havok\'s powers"}', 'powers_rank': "{'Optic Blast': 'Mn;', 'Break Fall': 'Ty;', 'Wide Angle Beam': 'In;', 'Transform energy into Optic Blast': '', 'Partial Immunity': ''}", 'powers_adj': "{'Force Blast': 'Testing One Only', 'Flight': 'Testing One Only', 'Force Area': 'Testing One Only', 'Energy Control:On Red': 'Testing One Only', 'Resist:Havok': 'Testing One Only'}", 'powers_adj_rank': "{'Force Blast': 'Mn;', 'Flight': 'Ty;', 'Force Area': 'In;', 'Energy Control:On Red': '', 'Resist:Havok': ''}", 'equipment': '{\'Ruby Quartz Visor\': "Am material, Can\'t control blasts when he opens his eyes if damaged or taken off", \'X-Men Uniform\': \'Rm material, the Uniforms are constructed out of unstable molecule fabric. It provides him with the following:\', \'Body Armour\': \'Ex protection vs. Physical and Energy\', \'Insulated\': \'Gd protection vs. Heat and Cold\', \'Comlink\': \'250 mile range and a GPS tracking device built into it\', \'Detection Scrambler\': \'Am protection vs. Electronic Mutant Detection\', \'Jet Pack\': \'Rm Flight\'}', 'equipment_rank': "{'Ruby Quartz Visor': 'Am;', 'X-Men Uniform': 'Rm;Un;', 'Body Armour': 'Ex;', 'Insulated': 'Gd;', 'Comlink': '', 'Detection Scrambler': 'Am;', 'Jet Pack': 'Rm;'}", 'equipment_adj': '{\'Ruby Quartz Visor\': "Am material, Can\'t control blasts when he opens his eyes if damaged or taken off", \'X-Men Uniform\': \'Rm material, the Uniforms are constructed out of unstable molecule fabric. It provides him with the following:\', \'Body Armour\': \'Ex protection vs. Physical and Energy\', \'Insulated\': \'Gd protection vs. Heat and Cold\', \'Comlink\': \'250 mile range and a GPS tracking device built into it\', \'Detection Scrambler\': \'Am protection vs. Electronic Mutant Detection\', \'Jet Pack\': \'Rm Flight\'}', 'equipment_adj_rank': "{'Ruby Quartz Visor': 'Am;', 'X-Men Uniform': 'Rm;Un;', 'Body Armour': 'Ex;', 'Insulated': 'Gd;', 'Comlink': '', 'Detection Scrambler': 'Am;', 'Jet Pack': 'Rm;'}", 'vehicle': '{}', 'talents': "{'Leadership': 1, 'Pilot': 1, 'Geometry': 1, 'Martial Arts A': 1, 'Martial Arts B': 1, 'Linguist': 1, 'Russian': 1, 'Japanese': 1}", 'talents_adj': "{'Leadership': 1, 'Pilot': 1, 'Spatial Geometry': 1, 'Martial Arts A,B': 1, 'Multi-Lingual (English': 1, 'Russian': 1, 'Japanese)': 1}", 'contacts': "{'X-Men': 1, 'Xavier Institute for Higher Learning': 1}", 'contacts_adj': '{}', 'weaknesses': "['']", 'weaknesses_adj': '{}', 'powers_form': '{}', 'spd': '0', 'att': '0', 'attack': "{'Blunt': {'S': '', 'R': '', 'A': ''}, 'Edged': {'S': '', 'R': '', 'A': ''}, 'Throwing Blunt': {'S': '', 'R': '', 'A': ''}, 'Throwing Edged': {'S': '', 'R': '', 'A': ''}, 'Shooting': {'S': '', 'R': '', 'A': ''}, 'Energy': {'S': '', 'R': '', 'A': ''}, 'Force': {'S': '', 'R': 'Mn;', 'A': 'In;'}, 'Grappling': {'S': '', 'R': '', 'A': ''}, 'Grabbing': {}, 'Charging': {}}", 'defense': "{'Escaping': {}, 'Dodging': {}, 'Evading': {}, 'Blocking': {}, 'Catching': {}}", 'dam': '0', 'climbing': '0', 'escaping': '0', 'martial_arts': 'AB', 'mook': '0'}
STATED AC CHECK 0
WE HAVE STATED AC CHECK Ex; Cyclops
FINAL AC CHECK 20 {'Physical': 'Ex', 'Energy': 'Ex'}
Mn;
In;
BEST ATTACK: {'Force': {'S': '', 'R': 'Mn;', 'A': 'In;'}} <class 'dict'>
OTHER ATTACKS: 0
{'throwing-blunt': 0, 'throwing-edged': 0, 'blunt': 0, 'edged': 0, 'shooting': 0, 'energy': 0, 'force': 0, 'grappling': 0}
best alt attack {'throwing-blunt': 0, 'throwing-edged': 0, 'blunt': 0, 'edged': 0, 'shooting': 0, 'energy': 0, 'force': 1, 'grappling': 0}
{'A': 1, 'B': 1, 'C': 0, 'D': 0, 'E': 0}
CHECK_SETTINGS {}
FINAL AC CHECK 20 {'Physical': 'Ex', 'Energy': 'Ex'}
Mn;
In;
BEST ATTACK: {'Force': {'S': '', 'R': 'Mn;', 'A': 'In;'}} <class 'dict'>
best alt attack {'throwing-blunt': 0, 'throwing-edged': 0, 'blunt': 0, 'edged': 0, 'shooting': 0, 'energy': 0, 'force': 1, 'grappling': 0}`

## SOME OF THE BELOW WILL NOT CURRENTLY BE RELEVANT

__str__(self)
    Return str(self).

act(self, verbose=0)

assess_wounded(self, verbose=0)


check_action(self, action, verbose)
    # TODO


copy(self)
    :return: a copy of the creature.

do_action(self, action, verbose)
    # TODO

generate_character_sheet(self)  #needs updating to FASERIP version
    An markdown character sheet.
    :return: a string

heal(self, points, verbose=0)

isalive(self)

multiattack(self, verbose=0, assess=0)

net(self, opponent, verbose=0)

ready(self)

reset(self)

set_level(self, level=None)
    Alter the level of the creature.
    :param level: opt. int, the level. if absent it will set it to the stored level.
    :return: nothing. changes self.

take_damage(self, points, verbose=0)

----------------------------------------------------------------------
Static methods defined here:

clean_settings(dirtydex)
    Sanify the settings
    :return: a cleaned dictionary

----------------------------------------------------------------------
Data descriptors defined here:

__dict__
    dictionary for instance variables (if defined)

__weakref__
    list of weak references to the object (if defined)

----------------------------------------------------------------------
Data and other attributes defined here:

ability_names = ['F', 'A', 'S', 'E', 'R', 'I', 'P']

beastiary = {'aboleth': {'AB_Cha': '4', 'AB_Con': '0', 'AB_Dex': '0', ...  ##update to FASERIP version
    
# class Dice(builtins.object)
Methods defined here:

__init__(self, bonus=0, dice=20, avg=False, twinned=None, role='ability')
    Class to handle dice and dice rolls
    :param bonus: int, the bonus added to the attack roll
    :param dice: list of int, the dice size.
    :param avg: boolean flag marking whether the dice always rolls average, like NPCs and PCs on Mechano do for attack rolls.
    :param twinned: a dice. ja. ehrm. this is the other dice. The crits are passed to it. It should be a weak ref or the crits passed more pythonically.
    :param role: string, but actually on a restricted vocabulary: ability, damage, hd or healing. Extras can be added, but they won't trigger some things
    :return: a rollable dice!
    
    The parameters are set to attributes. Other attributes are:
    * critable: determined from `role` attribute
    * cirt: 0 or 1 ... or more if you want to go 3.5 and crit train.
    * advantage: trinary int. -1 is disadvantage, 0 normal, 1 is advantage.

__str__(self)
    This is rather inelegant piece of code and is not overly flexible. If the dice fail to show, they will still work.
    :return: string in dice notation.

roll(self, verbose=0)  ##update to FASERIP
    The roll method, which calls either icosaroll or multiroll.
    :param verbose: debug
    :return: the value rolled (and alters the dice too if need be)
    
# class Encounter(builtins.object)
In a dimentionless model, move action and the main actions dash, disengage, hide, shove back/aside, tumble and overrun are meaningless.
weapon attack —default
two-weapon attack —
    Good when the opponent has low AC (<12) if 2nd attack is without proficiency.
    Stacks with bonuses such as sneak attack or poisoned weapons —neither are in the model.
    Due to the 1 action for donning/doffing a shield, switch to two handed is valid for unshielded folk only.
    Best keep two weapon fighting as a prebuild not a combat switch.
dodge —targetted and turn economy  #institute FASERIP version
help —high AC target (>18), turn economy, beefcake ally
ready —teamwork preplanning. No way.
grapple/climb —very situational. grapple/shove combo or barring somatic.
disarm —disarm… grey rules about whether picking it up or kicking it away is an interact/move/bonus/main action.
    netting is a better option albeit a build.
called shot —not an official rule. Turn economy.

Methods defined here:

__add__(self, other)

__getitem__(self, item)

__init__(self, *lineup)
    Initialize self.  See help(type(self)) for accurate signature.

__iter__(self)

__len__(self)

__str__(self)
    Return str(self).

addmob(self, n)

append(self, newbie)

battle(self, reset=1, verbose=1)

blank(self)

extend(self, iterable)

find(self, what, searcher=None, team=None)

go_to_war(self, rounds=1000)

json(self)

predict(self)

reset(self)

roll_for_initiative(self, verbose=0)

set_deathmatch(self)


----------------------------------------------------------------------
Data and other attributes defined here:

Victory = <class 'DnD_Battler.Encounter.Victory'>
    The way the encounter ends is a victory error is raised to stop the creatures from acting further.




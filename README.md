# FASERIP-Slugfest
A fighting simulator for the FASERIP and other compatible RPGs..

# Installation
- git clone
- change directory to DnD-Battler
- pip install .
- pip install -e . to tinker with code.

# Tests / Examples
- change to the DnD-Battler directory
- python runtestFASERIP.py
  - the below loads two characters that are in beastiaryFASERIP.csv and runs 100 battles
```python
from DnD_battler import Creature, Encounter
import pandas as pd

arenaDangerRoom = Encounter(Creature.load("Cyclops"), Creature.load("Corsair"))

print(arenaDangerRoom.go_to_war(100))
```

# Binder link
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/bluetyson/FASERIP-Slugfest/HEAD?urlpath=https%3A%2F%2Fgithub.com%2Fbluetyson%2FFASERIP-Slugfest%2Fblob%2Fmain%2FFASERIP%2520Character%2520Generator.ipynb)
- You can run Simulations and the Character generator here in a Jupyter Hub - download results, etc.  Use the FASERIP Character Generator Notebook, not the test version.  First cell of characters runs 100 of the original style, the second runs in beastiaryFASERIP style for the simulator.

# Simulation
See https://github.com/bluetyson/FASERIP-Slugfest/blob/main/DnD-battler/README.md for more technical details.
For developers, the base DnD-battler Simulation module folder is at that level. 

## Discussion
Some here:- http://cosmicheroes.space/blog/index.php/tag/faserip-slugfest/

# Character Generator
Work in progress on an Ultimate Powers Book version - 
- Notebook here that can do a loop of characters, output to json and make a dataframe and csv that is customised to use with the bestiaryFASERIP.csv type format for FASERIP-Slugfests https://github.com/bluetyson/FASERIP-Slugfest/blob/main/FASERIP%20Character%20Generator.ipynb
  - work in progress, so will have more columns/attributes added
- Training-Data parses Ben Riely's character website and creates a csv in beastiaryFASERIP.csv format as above
- Martial-Artists provides some martial artist analysis similarly.

## Notes on Character Generator
- There are two Forms - Composite and Compound Form - which basically involve making up multiple characters - may possibly be implemented later, but unlikely. For now I will replace them with Mutants [because X-Men].  For the purposes of tying into a simulation that would be difficult - in programming terms, sub-Creature character objects switching out stats.  Even just for a character generator, annoying.
- Metamorphic robots can also generate an extra form, this is not currently implemented either.
- Some types like animal, vegetable, mineral of course would pick something on creation - another could make a customised list for each, same with Extra Parts, others like that.

## Notes on Character Parsing
- To turn a list of 3000 characters with many varied made up things into something a little more standardised, a bit of mapping of some uniques
  - PowersFix.csv and .txt
  - TalentsFix.csv
  - Equipment.csv
- Probably will do some standardising on Advanced powers, more notes to come here.
- General theory is to make things more generic as you can, add to the Riely character parser
- Tweak for new characters you want to use and add code as necessary/request such

## Attacking
- At the moment, assuming Bullseyes are Stuns for faster combat

## Powers Attempted or sort of looked at
- Generally speaking, must be changed to be spelled like this:
- Body Armour
- Claws - generic Edged mapping
- Energy Absorption [not kinetic]
- Energy Blast
- Extra Attacks
- Extra Body Parts [see above]
- Force Blast
- Force Field
- Hyper-Speed [defensive bonus from moving, can substitute for multiple attacks roll - or just flat out hand out at a level]
  - This is handled in various ways in character writeups
  - Generally will lump Lightning Speed and these together in the interests of simplification
- Phasing
- Power Absorption - just as a takedown
- Probability Manipulation [just the good side]
- Regeneration
- Resistances [framework, but not implemented]

## Equipment Attempted
- Generally speaking, should transform these into the generic attack types, Shooting, Thrown Edged etc.
- Blaster Pistols
- Boomerangs
- Bows
- Guns
- Swords

## Other versions
- Java - You can find a java GUI FASERIP Character Generator at http://sourceforge.net/projects/javamcc/files/JMCC%28betav4.5%29.jar/download
- Javascript - https://github.com/jinniaflyer450/Jins-FASERIP-Char-Creator

## Resources
- FASERIP : https://gurbintrollgames.wordpress.com/faserip/
- 4CS : https://www.drivethrurpg.com/product/50837/Four-Color-System-Core-Rules
- Classic Marvel Forever : https://classicmarvelforever.com/
- DnD Battler : https://github.com/matteoferla/DnD-battler
- Ben Riely Marvel : https://www.angelfire.com/comics/benriely/index.html
- Unofficial Canon Project - https://drive.google.com/drive/folders/1B4FIJ1gUksHQFLqrNYZ439JSkpm8uH4U
- FASERIPing - http://cosmicheroes.space/blog/index.php/tag/faserip/




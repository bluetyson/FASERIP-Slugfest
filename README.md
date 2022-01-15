# FASERIP-Slugfest
A fighting simulator for the FASERIP and other compatible RPGs..

See https://github.com/bluetyson/FASERIP-Slugfest/blob/main/DnD-battler/README.md for more details.
The base module folder is there. 
- pip install -e . to tinker with code.

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
- At the moment, assuming Bullseyes can be Stuns for faster combat

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


from ._base import EncounterBase
from ..creature import Creature
from ..victory import Victory
from ..dice.ranks import dict_faserip
print("BATTLE:", dict_faserip)
import math
N = "\n"

class EncounterAction(EncounterBase):

    def addmob(self, n:int):
        """
        Adds _n_ commoners to the battle
        :param n: number of commoners
        :return: self
        """
        for x in range(int(n)):
            self.append(Creature.load("commoner", alignment='mob'))
        return self

    def set_deathmatch(self):
        """
        Alters all the alignments to make it a free-for-all deathmatch.

        :return:
        """
        colours = ['red',
                     'blue',
                     'green',
                     'orange',
                     'yellow',
                     'lime',
                     'cyan',
                     'violet',
                     'ultraviolet',
                     'pink',
                     'brown',
                     'black',
                     'white',
                     'octarine',
                     'teal',
                     'magenta',
                     'blue-green',
                     'fuchsia',
                     'purple',
                     'cream'
                     'grey']
        for schmuck in self:
            schmuck.alignment = colours.pop(0) + " team"
        return self

    def roll_for_initiative(self, verbose=0):
        #self.combattants = sorted(self.combattants, key=lambda fighter: fighter.initiative.roll(), reverse=True)  #need a d10 initiative roll
        self.combattants = sorted(self.combattants, key=lambda fighter: fighter.initiative.roll_initiative(), reverse=True)  #need a d10 initiative roll
		
        #print(self.combattants)
        self.log.debug(f"Turn order: {[x.name for x in self]}")
        print(f"Turn order: {[x.name for x in self]}")

    def predict(self):
        print("doing predict")
        def safediv(a, b, default=0):
            try:
                return a / b
            except:
                return default

        def not_us(side):
            (a, b) = list(self.sides)
            if a == side:
                return b
            else:
                return a

        if len(self.sides) != 2:
            # print('Calculations unavailable for more than 2 teams')
            return "Prediction unavailable for more than 2 teams"
        t_ac = {x: [] for x in self.sides}
        #print(t_ac)
        for character in self:
            #t_ac[character.alignment].append(character.armor.ac)
            t_ac[character.alignment].append(0)
            #print["AC:", character.armor.ac]
        ac = {x: sum(t_ac[x]) / len(t_ac[x]) for x in t_ac.keys()}
        print(t_ac)
        damage = {x: 0 for x in self.sides}
        hp = {x: 0 for x in self.sides}
        for character in self:
            for move1 in character.attacks:
                move = move1.ability_die
                move.avg = True
                damage[character.alignment] += safediv((20 + move.bonus - ac[not_us(character.alignment)]), 20 * move.roll())
                move.avg = False
                hp[character.alignment] += character.starting_hp
        (a, b) = list(self.sides)
        rate = {a: safediv(hp[a], damage[b], 0.0), b: safediv(hp[b], damage[a], 0.0)}
        return ('Rough a priori predictions:' + N +
                '> ' + str(a) + '= expected rounds to survive: ' + str(
                    round(rate[a], 2)) + '; crudely normalised: ' + str(
                    round(safediv(rate[a], (rate[a] + rate[b]) * 100))) + '%' + N +
                '> ' + str(b) + '= expected rounds to survive: ' + str(
                    round(rate[b], 2)) + '; crudely normalised: ' + str(
                    round(safediv(rate[b], (rate[a] + rate[b]) * 100))) + '%' + N)

    def battle(self, reset=1, verbose=1):
        print("in battle")
        if verbose: self.masterlog.append('==NEW BATTLE==')
        self.tally['battles'] += 1
        print("reset",reset)
		
        if reset: self.reset()
        for schmuck in self: schmuck.tally['battles'] += 1
        for schmuck in self: print(schmuck.name)
        self.roll_for_initiative(self.masterlog)
        while True:
            try:
                if verbose: self.masterlog.append('**NEW ROUND**')
                self.tally['rounds'] += 1
                for character in self:
                    print("ready",character.name)
                    character.ready()
                    if character.isalive():
                        self.active = character
                        character.tally['rounds'] += 1
                        character.act(self.masterlog)
                    else:
                        character.tally['dead'] += 1
                #break #got to take this one out
            except Victory:
                break
        # closing up maths
        side = self.active.alignment
        team = self.find('allies')
        self.tally['victories'][side] += 1
        perfect = 1
        close = 0
        for x in team:
            if x.hp < x.starting_hp:
                perfect = 0
            if x.hp < 0:
                close = 1
        if not perfect:
            self.tally['perfect'][side] += perfect
        self.tally['close'][side] += close
        for character in self:
            character.tally['hp'] += character.hp
            character.tally['healing_spells'] += character.healing_spells
        if verbose: self.masterlog.append(str(self))
        # return self or side?
        return self

    def go_to_war(self, rounds=1000):
        for i in range(rounds):
            self.battle(1, 0)
        x = {y: self.tally['victories'][y] for y in self.sides}
        se = {}
        for i in list(x):
            x[i] /= rounds
            try:
                se[i] = math.sqrt(x[i] * (1 - x[i]) / rounds)
            except Exception:
                se[i] = "NA"
        self.reset()
        for i in list(x):
            try:
                self.note += str(i) + ': ' + str(round(float(x[i]), 2)) + ' ± ' + str(round(float(se[i]), 2)) + '; '
            except:
                self.note += str(i) + ': ' + str(x[i]) + ' ± ' + str(se[i]) + '; '
        return self

    def find(self, what, searcher=None, team=None):

        def _enemies(folk):
            return [query for query in folk if (query.alignment != team)]

        def _allies(folk):
            return [query for query in folk if (query.alignment == team)]

        def _alive(folk):
            return [query for query in folk if (query.hp > 0)]

        def _normal(folk):
            return [joe for joe in folk if joe.condition == 'normal']

        def _random(folk):
            random.shuffle(folk)
            return folk

        def _weakest(folk):
            return sorted(folk, key=lambda query: query.hp)

        def _bloodiest(folk):
            return sorted(folk, key=lambda query: query.hp - query.starting_hp)

        def _fiersomest(folk):
            return sorted(folk, key=lambda query: query.hurtful, reverse=True)

        def _opponents(folk):
            return _alive(_enemies(folk))

        searcher = searcher or self.active
        team = team or searcher.alignment
        folk = self.combattants
        agenda = list(what.split())
        opt = {
            'enemies': _enemies,
            'enemy': _enemies,
            'opponents': _opponents,
            'allies': _allies,
            'ally': _allies,
            'normal': _normal,
            'alive': _alive,
            'fiersomest': _fiersomest,
            'weakest': _weakest,
            'random': _random,
            'bloodiest': _bloodiest
        }
        for cmd in list(agenda):  # copy it.
            if folk == None:
                folk = []
            for o in opt:
                if (cmd == o):
                    folk = opt[o](folk)
                    agenda.remove(cmd)
        if agenda:
            raise Exception(str(cmd) + ' field not found')
        return folk
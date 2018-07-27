from game_objects.battlefield_objects import BattlefieldObject
from mechanics.AI import SearchNode
from battlefield.Battlefield import Cell
from GameLog import gamelog
from contextlib import contextmanager
import my_context
import copy

class SimGame:

    @contextmanager
    def temp_context(self):
        old_game = my_context.the_game
        my_context.the_game = self
        yield
        my_context.the_game = old_game

    @contextmanager
    def simulation(self):
        old_game = my_context.the_game
        sim = copy.deepcopy(self)
        sim.is_sim = True
        my_context.the_game = sim
        with gamelog.muted():
            yield sim
        my_context.the_game = old_game


    def get_all_neighbouring_states(self, _unit):

        with self.temp_context():
            unit = self.find_unit(_unit)
            if unit is None:
                return []
            choices = self.get_all_choices(unit)
            nodes = [self.get_neighbour(c) for c in choices]
            return nodes

    def get_neighbour(self, c):

        active, target = c
        if active.simulate_callback:
            sim = None
        else:
            sim = self.step_into_sim(active, target)

        return SearchNode(SearchNode(None,None,self), c, sim)

    def step_into_sim(self, active, target):

        with self.simulation() as sim:
            sim_active = sim.find_active(active)
            sim_target = sim.find_unit(target) if isinstance(target, BattlefieldObject) else target
            sim_active.activate(sim_target)

        return sim


    def fake_measure(self, choice, fraction, use_position=True):
        active, target = choice
        with self.temp_context():
            with active.simulate(target):
                return self.utility(fraction, use_position=use_position)

    def delta(self, choice, fraction = None):
        _fraction = fraction or self.fractions[choice[0].owner]
        _delta = self.get_neighbour(choice).utility(_fraction) - self.utility(_fraction)
        return _delta

    @staticmethod
    @contextmanager
    def virtual(unit):
        health_before = unit.health
        mana_before = unit.mana
        stamina_before = unit.stamina
        readiness_before = unit.readiness

        yield

        unit.health = health_before
        unit.mana = mana_before
        unit.stamina = stamina_before
        unit.readiness = readiness_before

    # The marvel of convoluted math,
    # we evaluate how good the game is for a given fraction with a single number!

    def utility(self, fraction, use_position=True):
        total = 0

        own_units = [unit for unit in self.units if self.fractions[unit] is fraction]
        opponent_units = [unit for unit in self.units if self.fractions[unit] is not fraction]

        total += sum([self.unit_utility(unit) for unit in own_units])
        total -= sum([self.unit_utility(unit) for unit in opponent_units])

        if use_position:
            total += self.position_utility(own_units, opponent_units) / (1 + 1e13 * len(self.units))

        return total

    def position_utility(self, own, opponent):

        total = 0
        for own_unit in own:
            for other in opponent:
                importance = (self.unit_utility(own_unit) * self.unit_utility(other)) ** (1/2)

                dist = self.battlefield.distance(own_unit, other)

                # the closer the better
                total += 1e5 * (6 - dist **(1/2)) * importance

                # we want to face towards opponents
                total += 1e9 * (1/dist) * ( 6 - self.battlefield.angle_to(own_unit, other)[0] / 45) * importance

                #its best for opponents to face away from us
                total += (1/dist) * self.battlefield.angle_to(other, own_unit)[0] / 45 * importance

        # DELTA SPLIT!
        # for unit in own:
        #     for other in own:
        #         importance = (unit.utility * other.utility) ** (1 / 2)
        #         total -= importance * self.battlefield.distance(unit, other) ** (1/2)

        return total

    @staticmethod
    def unit_utility(unit):
        hp_factor = 1 + unit.health
        # other_factors = (1+ self.mana + self.stamina + self.readiness*3) * len(self.actives) / 10
        magnitude = sum([unit.str, unit.end, unit.agi, unit.prc, unit.int, unit.cha])
        return magnitude * hp_factor * 1



    # extracting all possible transitions

    def get_all_choices(self, unit):
        actives = unit.actives

        choices = []
        for a in actives:
            if a.owner_can_afford_activation():
                tgts = self.get_possible_targets(a)
                if tgts:
                    choices += [(a, tgt) for tgt in tgts]
                elif tgts is None:
                    choices.append( (a, None) )

        return choices


    def get_possible_targets(self, active):

        targeting_cls = active.targeting_cls
        if targeting_cls is None:
            return None

        result = list()

        if targeting_cls is Cell:
            for c in self.battlefield.all_cells:
                if active.check_target(c):
                    result.append(c)
            return result

        if targeting_cls is BattlefieldObject:
            for unit in self.battlefield.unit_locations:
                if active.check_target(unit):
                    result.append(unit)
            return result



    # Identifying objects between different sim instances

    def find_unit(self, unit):
        for other in self.battlefield.unit_locations:
            if unit.uid == other.uid:
                return other

    def find_active(self, active):
        for unit in self.battlefield.unit_locations:
            for other in unit.actives:
                if active.uid == other.uid:
                    return other
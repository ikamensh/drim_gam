class Cost:
    def __init__(self, stamina=0, mana=0, health=0, readiness = 1):
        self.stamina = stamina
        self.mana = mana
        self.health = health
        self.readiness = readiness

    def __mul__(self, other):

        return Cost(self.stamina * other,
                    self.mana * other,
                    self.health * other,
                    self.readiness * other)

    def __truediv__(self, other):
        return self.__mul__(1 / other)

    def __add__(self, other):
        stamina = self.stamina + other.stamina
        mana = self.mana + other.mana
        health = self.health + other.health
        readiness = self.readiness + other.readiness

        return Cost(stamina, mana, health, readiness)

    def __sub__(self, other):
        return self + other * -1

    def __eq__(self, other):
        return all((self.stamina == other.stamina,
                    self.mana == other.mana,
                    self.health == other.health,
                    self.readiness == other.readiness))

    def __hash__(self):
        return hash(self.stamina * 1e12 + self.mana * 1e8 + self.health * 1e4 +self.readiness)

    def __repr__(self):
        return f"{self.readiness} rdy, {self.stamina} sta, {self.mana} mp,  {self.health} hp"

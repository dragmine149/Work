import typing
from dataclasses import dataclass


@dataclass
class Base:
    name: str = "Unknown"
    attack: float = 0
    defence: float = 0
    effect: typing.List[any] = None
    durability: float = 100
    characterStrength: float = 0
    characterHealth: float = 0
    removeOnUse: bool = False

    def getName(self):
        return self.name

    def getAttack(self):
        return self.attack

    def getDefence(self):
        return self.defence

    def getEffect(self):
        return self.effect

    def getDurability(self):
        return self.durability

    def changeDurability(self, amount):
        self.durability += amount

    def getRemoveOnUse(self):
        return self.removeOnUse

    def getInfo(self):
        return {
            "name": self.name,
            "attack": self.attack,
            "defence": self.defence,
            "effect": self.effect,
            "durability": self.durability
        }

    def initialized(self, character):
        character.changeStrength(self.characterStrength)
        character.changeHealth(self.characterHealth)


@dataclass
class Function:
    name: str = "Unknown"

    def initialized(self, character):
        match self.name:
            case "Death":
                character.reset()

    def getRemoveOnUse(self):
        return True


@dataclass
class Spell:
    name: str = "Unknown"
    encoded: bool = True
    removeOnUse: bool = False

    def getName(self):
        return self.name

    def getEncoded(self):
        return self.encoded

    def getRemoveOnUse(self):
        return self.removeOnUse

    def getInfo(self):
        return {
            "name": self.name,
            "effect": self.encoded,
        }

    def initialized(self, character):
        pass


@dataclass
class Effect:
    name: str = "Unknown"

    def getName(self):
        return self.name

    def initialized(self, character):
        pass

    def getRemoveOnUse(self):
        return False

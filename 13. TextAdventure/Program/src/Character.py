from .Equipment import Equipment
from PythonFunctions import Save


class Character:
    def __init__(self, health: float, strength: float) -> None:
        self.__default = {
            "health": health,
            "strength": strength,
            "equipment": {}
        }
        self.__health = health
        self.__strength = strength
        self.__equipment = {}

    def reset(self):
        self.__health = self.__default.get("health")
        self.__strength = self.__default.get("strength")
        self.__equipment = self.__default.get("equipment")

    def getHealth(self) -> float:
        """Get the character health value

        Returns:
            float: The character health value
        """
        return self.__health

    def changeHealth(self, amount: float):
        """Change the characters health

        Args:
            amount (float): The amount to change by
        """
        self.__health += amount

    def changeStrength(self, amount: float):
        """Change the characters strength

        Args:
            amount (float): The amount to change by
        """
        self.__strength += amount

    def getStrength(self) -> float:
        """Returns the characters strength

        Returns:
            float: The characters strength
        """
        return self.__strength

    def newEquipment(self, equipment: Equipment):
        """Give the character a new piece of equipmenet

        Args:
            equipment (Equipment): The equipement to give the character
        """
        oEquipment = equipment
        if isinstance(equipment, str):
            for item in Equipment:
                if item.name == equipment[1:]:
                    equipment = item
                    break

        equipName = equipment.name
        if oEquipment[0] == "+":
            self.__equipment[equipName] = equipment.value
            self.__equipment.get(equipName).initialized(self)
            equip = self.__equipment.get(equipName)
            if equip:
                remove = equip.getRemoveOnUse()
                if remove:
                    self.__equipment[equipName] = None
        if oEquipment[0] == "-":
            self.__equipment[equipment.name] = None

    def getEquipment(self, equipment: Equipment) -> Equipment:
        """Get a piece of equipment from the character

        Args:
            equipment (Equipment): The equipment to get

        Returns:
            Equpment: The equpment.
        """
        return self.__equipment.get(equipment.name)

    def getDialogueInfo(self):
        return f"Health: {self.__health}. Strength: {self.__strength}"

    def saveEquipment(self):
        sv = Save.save()
        sv.Save(self.__equipment, "characterEquipment.json",
                encoding=[sv.encoding.JSON])

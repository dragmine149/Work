import enum
from . import EquipmentBase


class Equipment(enum.Enum):
    BSword = EquipmentBase.Base("Basic Sword", 10, 0, None, 100)
    BShield = EquipmentBase.Base("Basic Shield", 0, 5, None, 100)
    BPotion = EquipmentBase.Base("Basic Potion", 1, 1, "WIP", 1)
    BArmor = EquipmentBase.Base("Basic Armor", 0, 10, None, 200)
    D = EquipmentBase.Function("Death")
    BHealth = EquipmentBase.Base(
        "Health", characterHealth=10, removeOnUse=True)
    BStrength = EquipmentBase.Base(
        "Strength", characterStrength=10, removeOnUse=True)
    NBHealth = EquipmentBase.Base(
        "NHealth", characterHealth=-10, removeOnUse=True
    )
    NBStrength = EquipmentBase.Base(
        "NStrength", characterStrength=-10, removeOnUse=True
    )
    TeleportSpell = EquipmentBase.Spell("Teleport Spell")
    Ghost = EquipmentBase.Effect("Ghost")
    PGun = EquipmentBase.Base("Portal Gun")
    Creature = EquipmentBase.Base("Creature", 20, 10, None, 2_147_483_648)

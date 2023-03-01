import logging
import os
from src import Character, dialogue

c = Character.Character(100, 100)
d = dialogue.dialogue(c)

try:
    os.mkdir("logs")
except FileExistsError:
    pass

with open("logs/adventure.log", "w") as f:
    f.write("")

formatting = logging.Formatter(
    "[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s")

logging.basicConfig(
    level=logging.NOTSET,
    format="[%(asctime)s] - [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

log = logging.getLogger("adventure")
log.setLevel(logging.NOTSET)

loggingFileData = logging.FileHandler("logs/adventure.log", "w")
loggingFileData.setFormatter(formatting)
log.addHandler(loggingFileData)


def main():
    d.OutputDialogue()
    print(d.Choices)


if __name__ == "__main__":
    main()

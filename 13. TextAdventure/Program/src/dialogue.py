import logging
import random
from PythonFunctions import Save
from PythonFunctions import TerminalDisplay as Display
from .Character import Character


class dialogue:
    def __init__(self, character: Character) -> None:
        self.sv = Save.save()
        self.display = Display.Display()
        self.char = character

        self.location = "Adventure/loading.csv"  # loading, default chapter.
        self.chapter = "Loading"
        self.chapterInfo = self.__GetChapterInfo()
        self.dialogue = []
        self.placeIndex = 0

        self.Choices = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0
        }

        self.game = True
        self.ReadDialogue(self.location)
        self.logger = logging.getLogger("adventure.dialogue")

    def __GetChapterInfo(self):
        return self.sv.Read("main.csv", self.sv.encoding.CSV)

    def ReadDialogue(self, Location):
        """Get information about the current dialogue
        """

        self.dialogue = self.sv.Read(
            Location, self.sv.encoding.CSV
        )

    def __TranslateLine(self):
        """Translate the current row into the dialogue, options and results.

        Returns:
            Tuple: Questions, answers, positions, effects
        """
        currentInfo = self.dialogue.get("row")[self.placeIndex]
        currentInfo: dict
        question = currentInfo.get("Question")
        answers = [currentInfo.get("answer1"), currentInfo.get("answer2"),
                   currentInfo.get("answer3"), currentInfo.get("answer4")]
        positions = [currentInfo.get("location1"), currentInfo.get("location2"),
                     currentInfo.get("location3"), currentInfo.get("location4")]
        effects = [currentInfo.get("effect1"), currentInfo.get("effect2"),
                   currentInfo.get("effect3"), currentInfo.get("effect4")]
        return question, answers, positions, effects

    def newEffect(self, effect):
        self.char.newEquipment(effect)

    def AnswerCallback(self, *answer):
        # answers = (answers[index], positions[index], effects[index], index)
        self.logger.info("[%s] %s", self.chapter, answer)
        answerInfo = answer[0]

        if answerInfo[2] != "/\\":
            self.newEffect(answerInfo[2])

        self.Choices[str(answerInfo[3])] += 1  # staticstics
        nextPlace = answerInfo[1]
        if nextPlace.find("E") < 0:
            self.placeIndex = int(nextPlace)
            return -1

        nextPlace: str
        nextPlace = nextPlace.replace("E", "")
        self.logger.info("End of chapter, going to next chapter!")
        self.logger.info("Chapters: %s", self.chapterInfo)
        self.logger.info("Code: %s", nextPlace)

        if nextPlace == "!":
            return self.EndDialogue()

        for row in self.chapterInfo.get("row"):
            if row.get("Code") == nextPlace:
                self.logger.info("Found place!")
                self.logger.info("Row: %s", row)
                self.chapter = row.get("Chapter")
                self.location = row.get("Location")
                self.placeIndex = 0
                self.ReadDialogue(self.location)
                break

        return -1

    def OutputDialogue(self):
        while self.game:
            print("\x1b[2J\x1b[H", end='')
            question, answers, positions, effects = self.__TranslateLine()
            options = {}
            for index, answer in enumerate(answers):
                if answer != "/\\":
                    options[len(options) + 1] = (self.AnswerCallback,
                                                 answers[index], positions[index], effects[index], index)
            self.logger.info(question)
            self.display.SetOptions(options)

            pace = 25  # default printing time
            if self.chapter == "Loading":
                # If chapter is loading, change the output time randomly
                pace = random.randrange(10, 50)

            self.display.ShowHeader(
                text=f"Chapter: {self.chapter}\n{question}\nCurrent Stats:\t{self.char.getDialogueInfo()}", typewriter=True, pace=pace)
            result = self.display.ShowOptions()
            if result is None:
                return

    def EndCallback(self, *args):
        self.char.saveEquipment()
        self.display.ShowHeader(
            text=f"Your Items are saved in characterEquipment.json, Dialogue and path in logs/adventure.log\nStats:{self.char.getDialogueInfo()}"
        )

    def EndDialogue(self):
        self.display.SetOptions({
            "1": (self.EndCallback, "Continue")
        })
        self.display.ShowHeader(
            text="Chapter: End\nWell done for winning without dying! I hope you enjoy this and the easter eggs and refrences i added."
        )
        self.display.ShowOptions()

import sys
import os
import random
import datetime
import time
import json
import copy

import importlib
Templates = importlib.import_module('Templates', '...')


class playerData(Templates.PlayerData):
    def __init__(self, name: str = None) -> bool:
        super().__init__(name)

        self.Info = {
            "WordInfo": {
            },
            "BestInfo": {
            }
        }
        self.Info = self.GetData()

    def GetData(self):
        return super().GetData(self.name, self.Info)

    def SaveData(self):
        return super().SaveData(self.Info, self.name)

    def __CheckForWorseData(self, data):
        """Check to see if data stored for that word is better of worser than new data

        Args:
            data (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            wordData = self.Info["BestInfo"][data["word"]]

            if wordData["Guess"] > data["guess"]:
                return True
            if wordData["Guess Timer"] > data["guessTime"]:
                return True
            if wordData["Difficulty"] > data["difficulty"]:
                return True
            if not wordData["Passed"] and data["passed"]:
                return True
        except KeyError:
            return True

    def UpdatePlayerData(self, word: str, guess: int = -1, guessTime: int = -1, timeAchieved: int = -1, difficulty: int = -1, passed: bool = False):
        """Updates the player data with new information

        Args:
            word (str): The word guessed.
            guess (int): The amount of guesses. Defaults to -1.
            guessTime (int): The time it took to guess. Defaults to -1.
            timeAchieved (int): The datetime when it happened. Defaults to -1.
            difficulty (int): The difficulty of guessing the word. Defaults to -1.
            passed (bool): Did they pass. Deafults to False.
        """
        # make data
        data = {
            "Guess": guess,
            "Guess Timer": guessTime,
            "Time Achieved": timeAchieved,
            "Difficulty": difficulty,
            "Passed": passed
        }

        # find attempt no
        attempt = -1

        for guessWord in self.Info["WordInfo"]:
            if guessWord == word:
                try:
                    attempt = self.Info["WordInfo"][word]["Attempt"] + 1
                except KeyError:
                    pass
                break

        if attempt == -1:
            attempt = 1

        data["Attempt"] = attempt
        self.Info["wordInfo"][word] = data

        # Check if best data has been beten
        better = self.__CheckForWorseData({
            "guess": guess,
            "guessTime": guessTime,
            "difficulty": difficulty,
            "passed": passed,
            "word": word
        })

        if better:
            self.Info["BestInfo"][word] = data

        self.SaveData()


class Main(Templates.main):
    @property
    def name(self) -> str:
        return "Vowel Game"

    def __init__(self, main) -> None:
        super().__init__(main)

        self.frame = self.ui.CreateFrame()
        self.ui.AddLabel("Vowel Game", 0, 0, frame=self.frame)
        self.ui.AddButton("Back", None, 1, 0, frame=self.frame)
        self.ui.ChangeState({
            "Element": self.frame
        }, False)

        self.player = main.player

    def GetDifficulty(self):
        # get the user to input the difficulty they want
        while True:
            difficulty = None
            print("""Difficulty levels:
0: Easy (3 guesses / word)
1: Medium (2 guess / word)
2: Hard (1 guess / word)
3: Impossible: (All vowels required)""")
            print("""
Information about Easy / Medium / Hard difficulty
- X guess per word
- Every correct guess equals +1 guess

Information about impossible difficulty
- You only get one guess
- You have to include all the vowels in the word, even if they are repeated twice
- If you get one vowel guess wrong, you lose that round.
- Example: repeated -> rptd. Your Guess: eeae
""")
            # get input and verify input
            difficulty = input("Please enter your chosen difficulty: ")
            if difficulty.isdigit():
                difficulty = int(difficulty)
                if 0 >= difficulty <= 3:
                    return difficulty

                # not in range error
                print("Difficulty is not in the range 0 -> 3 (inclusive)")
                time.sleep(1)
                print("\x1b[2J\x1b[H", end='')
                continue

            # not an interger error
            print("Difficulty is not an interger!")
            time.sleep(1)
            print("\x1b[2J\x1b[H", end='')
            continue

    def Main(self):
        # self.player.UpdatePlayerData("Test", 1, 1, 1, 1, True)
        self.ui.ChangeState({
            "Element": self.frame,
            "row": 0,
            "column": 0
        })

# class playerData(Templates.PlayerData):
#     def __init__(self) -> None:
#         print("Loading player data!")
#         self.name = self.GetName()
#         self.path = "Players/{}/".format(self.name)

#         self.wordInfo = {}
#         self.bestWordInfo = {}

#         # load old player data
#         self.wordInfo = self.__LoadData("")
#         self.bestWordInfo = self.__LoadData("Best")

#         self.difficulty = self.GetDifficulty()
#         self.guess = [3, 2, 1, 0][self.difficulty]

#     def __LoadData(self, extra):
#         # Loads the player data
#         if os.path.exists("{}PlayerInfo{}.json".format(self.path, extra)):
#             with open("{}PlayerInfo{}.json".format(self.path, extra), "r") as f:
#                 try:
#                     return json.loads(f.read())
#                 except json.decoder.JSONDecodeError:
#                     exit("WARNING! File is corrupt!")
#         return {}

#     def GetName(self):
#         # Get the player to input their name (data saving)
#         name = None
#         while name is None:
#             name = input("Please enter player name: ")

#             if name.find("/") != -1 and name.find("\\") != -1:
#                 name = None
#                 print("Name cannot contain '/' or '\\'")

#         # Make apparopiate folders
#         if not os.path.exists("Players"):
#             print("Making dir: Players")
#             os.mkdir("Players")

#         if not os.path.exists("Players/{}".format(name)):
#             print("Making dir: Players/{}".format(name))
#             os.mkdir("Players/{}".format(name))

#         return name

#     def GetDifficulty(self):
#         # get the user to input the difficulty they want
#         while True:
#             difficulty = None
#             print("""Difficulty levels:
# 0: Easy (3 guesses / word)
# 1: Medium (2 guess / word)
# 2: Hard (1 guess / word)
# 3: Impossible: (All vowels required)""")
#             print("""
# Information about impossible difficulty
# - You only get one guess
# - You have to include all the vowels in the word, even if they are repeated twice
# - If you get one vowel guess wrong, you lose that round.
# - Example: repeated -> rptd. Your Guess: eeae
# """)
#             # get input and verify input
#             difficulty = input("Please enter your chosen difficulty: ")
#             if difficulty.isdigit():
#                 difficulty = int(difficulty)
#                 if difficulty >= 0 and difficulty <= 3:
#                     return difficulty

#                 # not in range error
#                 print("Difficulty is not in the range 0 -> 3 (inclusive)")
#                 time.sleep(1)
#                 print("\x1b[2J\x1b[H", end='')
#                 continue

#             # not an interger error
#             print("Difficulty is not an interger!")
#             time.sleep(1)
#             print("\x1b[2J\x1b[H", end='')
#             continue

#     def UpdateWordInfo(self, index, data):
#         print({"index": index, "data": data})
#         # Update the player data
#         try:
#             oldData = self.wordInfo[index]
#             if data["Guess Count"] < oldData["Guess Count"] or data["Time"] < oldData["Time"]:
#                 self.bestWordInfo[index] = data

#         # if errors happen, assume that it is not already in the list.
#         except (KeyError, TypeError):
#             self.wordInfo[index] = data
#             self.bestWordInfo[index] = data

#             with open("{}PlayerInfo.json".format(self.path), "w") as f:
#                 f.write(json.dumps(self.wordInfo))

#         # Update best save either way.
#         with open("PlayerInfoBest.json", "w") as f:
#             json.dumps(self.bestWordInfo)

#     def Reset(self):
#         self.guess = [3, 2, 1, 0][self.difficulty]


# class wordList:
#     def __init__(self, player) -> None:
#         self.player = player
#         self.vowels = ['a', 'e', 'i', 'o', 'u']
#         self.guessedVowels = []
#         print("Loading word list")
#         # check if file can be found
#         if not os.path.exists("wordList.txt"):
#             sys.exit(
#                 "Please make sure you have wordList.txt downloaded in the same directory!")

#         with open("wordList.txt", "r") as words:
#             self.words = words.readlines()

#     def randomWord(self):
#         # returns a random word
#         return self.words[random.randint(0, len(self.words))].strip()

#     def removeVowels(self, word):
#         # stores info about the current word and the word without vowels
#         self.currentWord = word
#         self.removedVowels = ''.join([l for l in word if l not in self.vowels])
#         self.guessedWord = self.removedVowels
#         self.reality = self.removedVowels

#     def AddGuess(self):
#         """By using the guessed letters, show a word with the guesses underlined.
#         """
#         self.guessedWord = ""
#         self.reality = ""
#         for letter in self.currentWord:
#             # Give already guessed vowels a special underline
#             if letter in self.guessedVowels:
#                 self.guessedWord += "\033[04m{}\033[0m".format(letter)
#                 self.reality += letter
#                 continue

#             # Add normally otherwise
#             if letter not in self.vowels:
#                 self.guessedWord += letter
#                 self.reality += letter

#     def EasyMode(self, roundIndex):
#         guessUsed = 0
#         startGuess = datetime.datetime.now()
#         while guessUsed < self.player.guess:
#             print("\x1b[2J\x1b[H", end='')

#             if self.currentWord == self.reality:
#                 print("All vowels guessed")
#                 break

#             print("Current round: {}".format(roundIndex))
#             print("Starting guess {}/{}".format(guessUsed, self.player.guess))
#             print("Current progress: {}".format(self.guessedWord))
#             print("Vowels guessed: {}".format(self.guessedVowels))

#             guess = None
#             while guess is None:
#                 try:
#                     guess = input(
#                         "Please enter a vowel to guess (ctrl / cmd + c to end program): ")
#                     # Checks if the guess, is a vowel, not already guess and in the word
#                     # Verification
#                     if guess not in self.guessedVowels:
#                         if guess in self.vowels:
#                             guessUsed += 1

#                             if guess in self.currentWord:
#                                 self.guessedVowels.append(guess)
#                                 self.AddGuess()

#                                 print("Correct guess! well done! (+1 guess)")
#                                 if self.player.guess != 5:
#                                     self.player.guess += 1
#                                 time.sleep(2)
#                                 continue

#                 # Errors in input

#                             print("Oh oh, this letter was not found in the word.")
#                             self.guessedVowels.append(guess)
#                             time.sleep(2)
#                             continue
#                         guess = None
#                         print("Invaid guess, please try again!")
#                         time.sleep(1)
#                     guess = None
#                     print("You have already guessed this letter!")
#                     time.sleep(1)
#                 except KeyboardInterrupt:
#                     exit("Thank you for player, read 'PlayerInfo.json' for your result.")
#         endGuess = datetime.datetime.now()

#         print()
#         print("Completed word!")
#         print("Guesses used: {}/{}".format(guessUsed, self.player.guess))
#         print("Word: {}".format(self.currentWord))
#         time.sleep(1)

#         self.player.UpdateWordInfo(self.currentWord, {
#             "Guess Count": guessUsed,
#             "Time": (endGuess - startGuess).total_seconds(),
#             "difficulty": self.player.difficulty,
#             "Date achieved": str(datetime.datetime.now().date()),
#             "Passed": self.currentWord == self.reality
#         })
#         time.sleep(1)  # give time to save
#         self.Reset()

#     def Impossible(self, roundIndex):
#         print("Current round: {}".format(roundIndex))
#         print("No vowel word: {}".format(self.guessedWord))

#         guess = None
#         while guess is None:
#             # Get the input
#             startGuess = datetime.datetime.now()
#             try:
#                 guess = input(
#                     "Please enter all the vowels in the word (duplicates and the same position) (CTRL / CMD + C to stop): ")
#             except KeyboardInterrupt:
#                 exit("Thank you for playing!")

#             # Check if all the characters are vowels
#             NoneVowels = [l for l in guess if l not in self.vowels]
#             if len(NoneVowels) > 0:
#                 print("Please enter ONLY vowels!")
#                 guess = None
#                 continue

#             endGuess = datetime.datetime.now()

#             # loop through
#             vowelsGuessed = [l for l in guess if l in self.vowels]
#             wordVowels = len([l for l in self.currentWord if l in self.vowels])
#             vowelGuessedIndex = -1
#             correctVowels = 0

#             print("Vowels in word: {}".format(wordVowels))

#             if len(vowelsGuessed) == wordVowels:
#                 for vowelIndex in range(len(self.currentWord)):
#                     print("Checking {}, {}".format(
#                         vowelIndex, self.currentWord[vowelIndex]))
#                     if self.currentWord[vowelIndex] in self.vowels:
#                         vowelGuessedIndex += 1

#                         if vowelsGuessed[vowelGuessedIndex] == self.currentWord[vowelIndex]:
#                             correctVowels += 1
#                             print("Vowel: {}... Correct!".format(
#                                 vowelsGuessed[vowelGuessedIndex]))
#                             continue

#                         print("Vowel: {}... Incorrect :(".format(
#                             vowelsGuessed[vowelGuessedIndex]))

#             print({correctVowels})

#             self.player.UpdateWordInfo(self.currentWord, {
#                 "Time": (endGuess - startGuess).total_seconds(),
#                 "difficulty": self.player.difficulty,
#                 "Date achieved": str(datetime.datetime.now().date()),
#                 "Passed": correctVowels == len(vowelsGuessed)
#             })

#             if correctVowels == len(vowelsGuessed):
#                 print("Well done! you did the word!!")
#                 continue
#             print("Sorry you made at least {} mistakes...".format(
#                 len(vowelsGuessed) - correctVowels))
#             continue

#         time.sleep(1)  # give time to save
#         self.Reset()

#     def GuessLetters(self, roundIndex):
#         # Main function to choosen between the 2 different functions
#         if self.player.difficulty != 3:
#             self.EasyMode(roundIndex)
#         if self.player.difficulty == 3:
#             self.Impossible(roundIndex)

#     def Reset(self):
#         print("\x1b[2J\x1b[H", end='')
#         # Makes everything work again
#         self.guessedVowels = []
#         self.player.Reset()


# if __name__ == "__main__":
#     print("\x1b[2J\x1b[H", end='')
#     print("""\033[04mInstructions and information\033[0m
# Welcome to vowel changer, made by dragmine149 ('\u001b]8;;https://twitter.com/DragMine149\u001b\\Twitter\u001b]8;;\u001b\\', '\u001b]8;;https://youtube.com/channel/UCOnORrEI4GhYtivLQJpOoJQ\u001b\\Youtube\u001b]8;;\u001b\\')

# \033[04mHow to use:\033[0m
# After enterting some information (everything gets stored on the local device) you will be put into the game.

# \033[04mAim of the game:\033[0m
# When you enter the game, you will have a word that is missing the vowels, your goal add in the reminder vowels.
# Depending on the difficulty you choose, will depend on the challenges you face (Explained in more detail later)

# There are 370099 words that can be picked from, which can be viewed in wordList.txt

# \033[04mEnding Game:\033[0m
# The game ends by either CTRL / CMD + C or running out of words inputted, your data can then be viewed in Players/{NAME}/PlayerInfo.json and Players/{NAME}/PlayerInfoBest.json

# \033[04mGoal:\033[0m
# There is not really an overall goal, this is designed to have some fun and maybe learn some spellings on new words. If you want to have some fun though, you compare your results to a friends results.
# """)

#     input("Press enter to continue")

#     print("\x1b[2J\x1b[H", end='')
#     pd = playerData()
#     print("\x1b[2J\x1b[H", end='')
#     wl = wordList(pd)

#     # Get how many words they want to do
#     rounds = None
#     while rounds is None:
#         rounds = input("Please enter number of words to do: ")
#         if rounds.isdigit():
#             rounds = int(rounds)
#             if rounds > 0:
#                 continue
#             print("You need at least one round")
#             rounds = None
#             continue
#         print("Rounds is not a digit!")
#         rounds = None

#     # Loop through ammount of words.
#     for i in range(rounds):
#         word = wl.randomWord()
#         wl.removeVowels(word)
#         print(wl.removedVowels)
#         wl.GuessLetters(i)

#     print("Thank you, please read PlayerInfo.json and PlayerInfoBest.json for your score.")

def load(main):
    return Main(main)

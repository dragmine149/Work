# Read time table and display it
import importlib
import tkinter as tk
Templates = importlib.import_module('Templates', '...')

class Save(Templates.save):
    def __init__(self) -> bool:
        super().__init__()
    
    def GetData(self, name: str):
        with open(name, 'r') as f:
            return self.DecodeDataJson(f.read())

class Main(Templates.main):
    @property
    def name(self) -> str:
        return "Time Table"
    
    def __init__(self, ui: Templates.ui) -> None:
        super().__init__(ui)
        
        self.save = Save()
        self.data = self.save.GetData("Data/TimeTable.json")
        
        self.__GenerateFrame()
        
    def __GenerateFrame(self):
        # Frame for the days
        self.dayFrame = self.ui.CreateFrame()
        
        self.ui.AddLabel("Time Table", 0, 0, frame=self.dayFrame)
        self.ui.AddButton("Back", self.Back, 1, 0, frame=self.dayFrame)
        self.ui.AddButton("Monday", self.ChangeDay, 2, 0, frame=self.dayFrame)
        self.ui.AddButton("Tuesday", self.ChangeDay, 3, 0, frame=self.dayFrame)
        self.ui.AddButton("Wednesday", self.ChangeDay, 4, 0, frame=self.dayFrame)
        self.ui.AddButton("Thursday", self.ChangeDay, 5, 0, frame=self.dayFrame)
        self.ui.AddButton("Friday", self.ChangeDay, 6, 0, frame=self.dayFrame)
        
        self.ui.ChangeState({
            "Element": self.dayFrame,
        }, False)
        
        # Frame for the lessons
        self.LessonFrame = self.ui.CreateFrame(0, 1)
        self.ui.AddLabel("Lessons", 0, 0, frame=self.LessonFrame)
        self.ui.AddButton("Lesson 1", self.ChangeLesson, 1, 0, frame=self.LessonFrame)
        self.ui.AddButton("Lesson 2", self.ChangeLesson, 2, 0, frame=self.LessonFrame)
        self.ui.AddButton("Lesson 3", self.ChangeLesson, 3, 0, frame=self.LessonFrame)
        self.ui.AddButton("Lesson 4", self.ChangeLesson, 4, 0, frame=self.LessonFrame)
        self.ui.AddButton("Lesson 5", self.ChangeLesson, 5, 0, frame=self.LessonFrame)
        
        self.ui.ChangeState({
            "Element": self.LessonFrame,
        }, False)
        
        # Lesson Information
        self.LessonInfoFrame = self.ui.CreateFrame(0, 2)
        
        self.lessonVar = tk.StringVar(self.LessonInfoFrame, "Lesson: ")
        self.roomVar = tk.StringVar(self.LessonInfoFrame, "Room: ")
        self.teacherVar = tk.StringVar(self.LessonInfoFrame, "Teacher: ")
        
        self.ui.AddLabel("Lesson information", 0, 0,
                         frame=self.LessonInfoFrame)
        self.ui.AddLabel("Lesson: ", 1, 0, frame=self.LessonInfoFrame, textVar=self.lessonVar)
        self.ui.AddLabel("Room: ", 2, 0, frame=self.LessonInfoFrame, textVar=self.roomVar)
        self.ui.AddLabel("Teacher: ", 3, 0, frame=self.LessonInfoFrame, textVar=self.teacherVar)
        
        self.ui.ChangeState({
            "Element": self.LessonInfoFrame,
        }, False)
    
    def ChangeDay(self, name: str):
        """Change the currently visible day

        Args:
            name (str): The name of the day
        """
        print(f"Changing day to: {name}")
        self.ui.ChangeState({
            "Element": self.LessonFrame,
            "row": 0,
            "column": 1
        })
        self.ui.ChangeState({
            "Element": self.LessonInfoFrame,
            "row": 0,
            "column": 2
        }, False)
        
        self.day = name
    
    def ChangeLesson(self, name: str):
        """Changes the data based on the lesson period

        Args:
            name (str): Lesson period
        """
        print(f"Changing lesson to {name}")
        self.ui.ChangeState({
            "Element": self.LessonInfoFrame,
            "row": 0,
            "column": 2
        })
        
        # Set the lesson ui
        ls = self.data[self.day][name]["Lesson"]
        if ls == "":
            ls = "None"
        rm = self.data[self.day][name]["Room"]
        if rm == "":
            rm = "None"
        tc = self.data[self.day][name]["Teacher"]
        if tc == "":
            tc = "None"
        
        self.lessonVar.set(f"Lesson: {ls}")
        self.roomVar.set(f"Room: {rm}")
        self.teacherVar.set(f"Teacher: {tc}")
    
    def Back(self, _):
        """Go back to main menu
        """
        self.ChangeView(False)
        self.ui.ChangeState({
            "Element": self.LessonFrame,
        }, False)
        self.ui.ChangeState({
            "Element": self.LessonInfoFrame,
        }, False)
    
    def ChangeView(self, new:bool = True):
        """Change view from normal to time table

        Args:
            new (bool, optional): The flip option. Defaults to True.
        """
        self.ui.ChangeState({
            "Element": self.dayFrame,
            "row": 0,
            "column": 0
        }, new)
        self.ui.ChangeState({
            "Element": self.ui.mainFrame,
            "row": 0,
            "column": 0
        }, not new)

    def Main(self):
        print("Loading...")
        self.ChangeView()
        

def load(ui):
    return Main(ui)
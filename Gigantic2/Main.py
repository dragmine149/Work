import os
import watermark
import Templates
import importlib

watermark.main()


class PlayerData(Templates.PlayerData):
    def __init__(self, main, *, name=None) -> bool:
        # self.canvas = main.ui.canvas
        # self.Frames = []

        # super().__init__(name)
        # main.name = self.name
        super().__init__(main.ui)

# Create UI


class Ui(Templates.ui):
    def __init__(self, title: str = "", callback=None) -> None:
        super().__init__(title, callback)

        self.FontSettings(("verdaba", 20))

        # Menu
        self.mainFrame = self.CreateFrame(0, 0)
        self.AddLabel("Main Menu", 0, 0, frame=self.mainFrame)
        self.AddButton("Time Table", callback, 1, 0, frame=self.mainFrame)
        self.AddButton("Vowel Game", callback, 2, 0, frame=self.mainFrame)
        self.AddButton("Change from £5", callback, 3, 0, frame=self.mainFrame)
        self.AddButton("Clock", callback, 4, 0, frame=self.mainFrame)
        self.AddButton("Register", callback, 5, 0, frame=self.mainFrame)
        self.AddLabel("Move functions comming soon!",
                      6, 0, frame=self.mainFrame)
        self.AddButton("Settings", None, 7, 0,
                       frame=self.mainFrame, callbackArgs=False)
        self.AddButton("Quit", self.canvas.quit, 8, 0,
                       frame=self.mainFrame, callbackArgs=False)

    def mainloop(self):
        """Call this AFTER everything has loaded in.
        """
        self.canvas.mainloop()


class Main:
    """Special type of main clas
    """

    def __init__(self) -> None:
        self.ui = Ui("Menu", self.__UiCallback)
        self.player = PlayerData(main=self)

        self.modules = []
        self.ImportModule()

        self.ui.mainloop()

    def ImportModule(self):
        """Import all modules
        """
        for module in os.listdir("modules"):
            try:
                mdle = importlib.import_module(f'modules.{module}.main')
                self.modules.append(mdle.load(self))
            except ModuleNotFoundError as e:
                print(f"Skipping loading: {module} due to not being found!")
                print(e)

    def __UiCallback(self, text: str):
        """Callback for button click

        Args:
            text (str): The text on the button
        """
        for module in self.modules:
            if text == module.name:
                return module.Main()

        raise NotImplementedError(f"Failed to find a module for: {text}")


Main()

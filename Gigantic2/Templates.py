import json
import pickle
import tkinter as tk
import typing
import os


class save:
    def __init__(self) -> bool:
        pass

    def SaveData(self, data, name: str):
        """Save data to a file

        Args:
            data (_type_): The data to save
            name (str): The name of the file

        Raises:
            NotImplementedError: If this is called without being implemented
        """
        raise NotImplementedError()

    def GetData(self, name: str):
        """Retrieve data from a file

        Args:
            name (str): The name of the file

        Raises:
            NotImplementedError: If this is called without being implemented.

        Returns:
            _type_: The data in the file
        """
        raise NotImplementedError()

    def UpdateData(self, data, name: str):
        """Updates data in a file

        Args:
            data (_type_): The data to add to the file
            name (str): The name of the file

        Raises:
            NotImplementedError: If this is called without being implemented.
        """
        raise NotImplementedError()

    def EncodeDataJson(self, data: dict) -> str:
        """Encodes the data from json (dict) to string

        Args:
            data (dict): The data to encode

        Returns:
            str: The result of the encode
        """
        return json.dumps(data)

    def DecodeDataJson(self, data: str) -> dict:
        """Decodes data from str to dict

        Args:
            data (str): The data to decode

        Returns:
            dict: The result of the decode
        """
        return json.loads(data)

    def EncodeDataBinary(self, data: str) -> bytes:
        """Encodes the data into binary

        Args:
            data (str): The data to encode

        Returns:
            bytes: The result of the encode
        """
        return pickle.dumps(data)

    def DecodeDataBinary(self, data: bytes) -> str:
        """Decode data from binary into a string

        Args:
            data (bytes): The data to decode

        Returns:
            str: The result of the decode
        """
        return pickle.loads(data)

    def MakeFolder(self, name: str) -> str:
        """Makes a folder

        Args:
            name (str): Name of the folder

        Returns:
            str: Path to the folder
        """
        os.makedirs(name)
        return name


class ui:
    def __init__(self, title: str = "", callback=None) -> None:
        """Makes a new TK window with title as the name

        Args:
            title (str, optional): The name of the window. Defaults to "".
            callback (def, optional): An external class callback
        """
        self.canvas = tk.Tk()
        self.canvas.title(title)

        self.Elements = []  # list of elements (Buttons, labels)
        self.Frames = []  # List of frames
        self.callback = None
        pass

    def FontSettings(self, fontData=()):
        self.font = fontData

    def CreateFrame(self, row: int = 0, column: int = 0) -> tk.Frame:
        """Creates a new frame

        Args:
            row (int, optional): The row position of the frame. Defaults to 0.
            column (int, optional): The column position of the frame. Defaults to 0.

        Returns:
            tk.Frame: The frame object
        """
        Frame = tk.Frame(self.canvas)
        Frame.grid(row=row, column=column)
        self.Frames.append({
            "Element": Frame,
            "row": row,
            "column": column
        })

        return Frame

    def __GetUiElement(self, frame=None) -> tk.Canvas or tk.Frame:
        """Returns the default canvas or frame

        Args:
            frame (_type_, optional): The frame to return. Defaults to None.

        Returns:
            _type_: Frame or canvas
        """
        return self.canvas if frame is None else frame

    def __Callback(self, buttonName: str, **kwargs):
        """Callback function for button press

        Args:
            buttonName (string): The name of the button
        """
        if self.callback is not None:
            return self.callback()

        raise NotImplementedError(
            f"{buttonName} has no designated callback function!")

    def AddButton(self, text: str, callback, row: int = 0, column: int = 0, *, textVar: tk.StringVar = None, frame=None, sticky: str = 'nesw', callbackArgs: bool = True, rowspan: int = 1, columnspan: int = 1) -> tk.Button:
        """Add a new button to the UI

        Args:
            name (str): the text to display on the button
            callback (function): The callback function on button click
            row (int, optional): The row position of the button. Defaults to 0.
            column (int, optional): The column position of the button. Defaults to 0.
            textVar (tk.StringVar, optional): A string variable to assign to the button. Defaults to None.
            frame (optional): Where to add the element to.
            sticky (str, optional): Whever to make the box stick to a side or not. Defaults to nesw.
            rowspan (int, optional): How many rows it covers. Defaults to 1.
            columnspan (int, optional): How many columns it covers. Defaults to 1.

        Returns:
            tk.Button: The button object
        """

        if callback is None:
            callback = self.__Callback

        Button: tk.Button = None

        if callbackArgs:
            Button = tk.Button(self.__GetUiElement(frame), text=text,
                               textvariable=textVar, command=lambda: callback(text), font=self.font)
        else:
            Button = tk.Button(self.__GetUiElement(frame), text=text,
                               textvariable=textVar, command=callback)

        Button.grid(row=row, column=column, sticky=sticky,
                    rowspan=rowspan, columnspan=columnspan)
        self.Elements.append({
            "Element": Button,
            "row": row,
            "column": column
        })
        return Button

    def AddLabel(self, text: str, row: int = 0, column: int = 0, *, textVar: tk.StringVar = None, frame=None, sticky: str = 'nesw', rowspan: int = 1, columnspan: int = 1) -> tk.Label:
        """Adds a new label to the UI

        Args:
            text (str): The text to display on the label
            row (int, optional): The row position of the label. Defaults to 0.
            column (int, optional): The column position of the label. Defaults to 0.
            textVar (tk.StringVar, optional): A string variable to assign to the button. Defaults to None.
            frame (optional): Where to add the element to.
            sticky (str, optional): Whever to make the box stick to a side or not. Defaults to nesw.
            rowspan (int, optional): How many rows it covers. Defaults to 1.
            columnspan (int, optional): How many columns it covers. Defaults to 1.

        Returns:
            tk.Label: The label object
        """

        Label = tk.Label(self.__GetUiElement(frame),
                         text=text, textvariable=textVar, font=self.font)
        Label.grid(row=row, column=column, sticky=sticky,
                   rowspan=rowspan, columnspan=columnspan)
        self.Elements.append({
            "Element": Label,
            "row": row,
            "column": column
        })
        return Label

    def AddTexBox(self, textVar: tk.StringVar, row: int = 0, column: int = 0, *, frame: tk.Frame = None, sticky: str = 'nesw', rowspan: int = 1, columnspan: int = 1, show: str = '') -> tk.Entry:
        """Adds a new text box to the UI

        Args:
            textvar (str): The text variable to assign the data to
            row (int, optional): The row position of the label. Defaults to 0.
            column (int, optional): The column position of the label. Defaults to 0.
            text (str, optional): The default text in the textbox. Defaults to "".
            frame (tk.Frame, optional): The frame of the textbox. Defaults to None.
            sticky (str, optional): The sides to stick the box to. Defaults to 'nesw'.
            rowspan (int, optional): How many rows it covers. Defaults to 1.
            columnspan (int, optional): How many columns it covers. Defaults to 1.
            show (str, optional): The text to replace the input with. Defaults to ''.

        Returns:
            tk.Text: The textbox object
        """
        textBox = tk.Entry(self.__GetUiElement(
            frame), font=self.font, textvariable=textVar, show=show)
        textBox.grid(row=row, column=column, sticky=sticky,
                     rowspan=rowspan, columnspan=columnspan)
        self.Elements.append({
            "Element": textBox,
            "row": row,
            "column": column
        })
        return textBox

    def ChangeState(self, Element: dict, state: bool = True):
        """Changes a Frame visibility from X to Y

        Args:
            Element (dict): The dictionary object containg the element
            state (bool, optional): The new state of the frame. Defaults to True.
        """
        if state:
            Element["Element"].grid(
                row=Element["row"], column=Element["column"])
        else:
            Element["Element"].grid_forget()


class main:
    @property
    def name(self) -> str:
        raise NotImplementedError()

    def __init__(self, main) -> None:
        self.main = main
        self.ui: ui = main.ui

    def Main(self, **data):
        raise NotImplementedError()


class PlayerData(save):
    def __init__(self, ui: ui):
        if not os.path.exists("Data/player"):
            self.MakeFolder("Data/player")

        self.ui = ui
        self.username = None
        self.password = None

        self.ui.ChangeState({
            "Element": self.ui.mainFrame,
        }, False)
        self.CreateFrame()

    def CreateFrame(self):
        """Create a frame for the user to log in
        """
        self.frame = self.ui.CreateFrame()

        self.info = tk.StringVar(self.frame, "Log In")
        self.usernameVar = tk.StringVar(self.frame)
        self.passwordVar = tk.StringVar(self.frame)

        self.ui.AddLabel("Log In", 0, 0, columnspan=2,
                         textVar=self.info, frame=self.frame)
        self.ui.AddLabel("Name: ", 1, 0, frame=self.frame)
        self.ui.AddTexBox(self.usernameVar, 1, 1, frame=self.frame)

        self.ui.AddLabel("Password: ", 2, 0, frame=self.frame)

        self.ui.AddTexBox(
            self.passwordVar, 2, 1, frame=self.frame, show='*')

        cnt = self.ui.AddButton("Continue", self.__Verify,
                                3, 1, frame=self.frame, callbackArgs=False)
        if not os.path.exists("Data/Player") or len(os.listdir("Data/Player")) == 1:
            cnt.config(state='disabled')

        self.ui.AddButton("New", self.__Verify, 3, 0, frame=self.frame)
        self.ui.AddButton("Quit", self.ui.canvas.quit, 4, 0,
                          frame=self.frame, columnspan=2, callbackArgs=False)

    def __Verify(self, txt: str = ''):
        """Do some verification with the user, and make user if not exists alerady
        """
        self.username = self.usernameVar.get().replace('\n', '')
        self.usernameVar.set("")
        self.password = self.passwordVar.get().replace('\n', '')
        self.passwordVar.set("")

        if self.username.find('/') > -1 or self.username.find('\\') > -1:
            print("Invalid Character ('\\', '/')")
            self.username = ""
            self.info.set("Sorry, `/` or `\\` are not allowed in a name!")
            return

        if self.username == "":
            print("Blank")
            self.info.set("Sorry, but no blank names allowed")
            return

        if self.username in os.listdir("Data/Player") and txt == "New":
            print("Taken")
            self.username = ""
            self.info.set("Sorry, this username has already been taken")
            return

        if self.password == "":
            print("Blank password.")
            self.info.set("Please enter a password")
            return

        if txt != "New":
            data = self.GetData(self.username, '/in.fo')
            if self.password != data.get("Password"):
                print("Incorrect password")
                self.info.set("Incorrect password")
                return

        self.SaveData({
            "Username": self.username,
            "Password": self.password
        }, self.username, "/in.fo")

        self.ui.ChangeState({
            "Element": self.ui.mainFrame,
            "row": 0,
            "column": 0
        })
        self.ui.ChangeState({
            "Element": self.frame,
        }, False)

    def GetData(self, name: str, filename: str = ''):
        if not os.path.exists(f"Data/Player/{name}"):
            self.MakeFolder(f"Data/Player/{name}")
            return None

        with open(f"Data/Player/{name}{filename}", 'rb') as f:
            return self.DecodeDataJson(self.DecodeDataBinary(f.read()))

    def SaveData(self, data, name: str, filename: str = '') -> bool:
        if not os.path.exists(f"Data/Player/{name}"):
            self.MakeFolder(f"Data/Player/{name}")

        with open(f"Data/Player/{name}{filename}", 'wb') as f:
            f.write(self.EncodeDataBinary(self.EncodeDataJson(data)))

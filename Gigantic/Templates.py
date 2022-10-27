import json
import pickle
import tkinter as tk
import typing
import os

class save:
    def __init__(self) -> bool:
        pass
    
    def SaveData(self, data, name: str) -> bool:
        """Save data to a file

        Args:
            data (_type_): The data to save
            name (str): The name of the file

        Raises:
            NotImplementedError: If this is called without being implemented

        Returns:
            bool: Did it successfully save?
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
    
    def UpdateData(self, data, name:str) -> bool:
        """Updates data in a file

        Args:
            data (_type_): The data to add to the file
            name (str): The name of the file

        Raises:
            NotImplementedError: If this is called without being implemented.

        Returns:
            bool: Did updating the file work
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

    def MakeFolder(self, name:str) -> str:
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
    
    def CreateFrame(self, row:int=0, column:int=0) -> tk.Frame:
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
        
        raise NotImplementedError(f"{buttonName} has no designated callback function!")
    
    def AddButton(self, name: str, callback, row: int=0, column: int=0, *, textVar: tk.StringVar=None, frame=None, sticky: str='nesw', callbackArgs: bool=True) -> tk.Button:
        """Add a new button to the UI

        Args:
            name (str): the text to display on the button
            callback (function): The callback function on button click
            row (int, optional): The row position of the button. Defaults to 0.
            column (int, optional): The column position of the button. Defaults to 0.
            textVar (tk.StringVar, optional): A string variable to assign to the button. Defaults to None.
            frame (optional): Where to add the element to.
            sticky (str, optional): Whever to make the box stick to a side or not. Defaults to nesw.
        
        Returns:
            tk.Button: The button object
        """
        
        if callback is None:
            callback = self.__Callback
        
        Button: tk.Button = None
        
        if callbackArgs:
            Button = tk.Button(self.__GetUiElement(frame), text=name,
                            textvariable=textVar, command=lambda: callback(name))
        else:
            Button = tk.Button(self.__GetUiElement(frame), text=name,
                               textvariable=textVar, command=callback)

        Button.grid(row=row, column=column, sticky=sticky)
        self.Elements.append({
            "Element": Button,
            "row": row,
            "column": column
        })
        return Button
    
    def AddLabel(self, text: str, row: int = 0, column: int = 0, *, textVar: tk.StringVar = None, frame=None, sticky:str='nesw') -> tk.Label:
        """Adds a new label to the UI

        Args:
            text (str): The text to display on the label
            row (int, optional): The row position of the label. Defaults to 0.
            column (int, optional): The column position of the label. Defaults to 0.
            textVar (tk.StringVar, optional): A string variable to assign to the button. Defaults to None.
            frame (optional): Where to add the element to.
            sticky (str, optional): Whever to make the box stick to a side or not. Defaults to nesw.
        
        Returns:
            tk.Label: The label object
        """
        
        Label = tk.Label(self.__GetUiElement(frame),
                         text=text, textvariable=textVar)
        Label.grid(row=row, column=column, sticky=sticky)
        self.Elements.append({
            "Element": Label,
            "row": row,
            "column": column
        })
        return Label
        """Adds multiple labels

        Args:
            data (_type_): The data of the labels

        Returns:
            typing.List: The list of labels
        """
        Labels = []
        for label in data:
            Labels.append(self.AddLabel(**label))

        return Labels
    
    def ChangeState(self, Element: dict, state:bool=True):
        """Changes a Frame visibility from X to Y

        Args:
            Element (dict): The dictionary object containg the element
            state (bool, optional): The new state of the frame. Defaults to True.
        """
        if state:
            Element["Element"].grid(row=Element["row"], column=Element["column"])
        else:
            Element["Element"].grid_forget()

class main:
    @property
    def name(self) -> str:
        raise NotImplementedError()
    
    def __init__(self, ui: ui) -> None:
        self.ui = ui
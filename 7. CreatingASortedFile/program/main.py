import Functions
import colours
import os

class Main:
    def __init__(self) -> None:
        pass
    
    def GetPath(self) -> str:
        path = None
        while path is None:
            print("\x1b[2J\x1b[H", end='')
            path = input("Please enter location of user information: ")
            pathInfo = os.path.split(path)
            file = Functions.search(pathInfo[0], pathInfo[1])
            fileLocation = file.Locate()
            print(fileLocation)

            if len(fileLocation) == 0:
                path = None
                input(f"{colours.c('r')}Failed to find file! Please press enter and choose a different location!{colours.c()}")
                continue
            
            return fileLocation[0]
    
    def Sort(self, path):
        data = []
        with open(path, 'r') as f:
            data = f.readlines()
        
        sorted = False
        while not sorted:
            sorted = True
            for i in range(len(data) - 1):
                if ord(data[i][0]) > ord(data[i + 1][0]):
                    data[i], data[i + 1] = data[i + 1], data[i]
                    sorted = False
        
        fileData = os.path.splitext(path)
        filename = f"{fileData[0]}-sorted{fileData[1]}"
        with open(filename, 'w') as f:
            f.writelines(data)
    
    def main(self):
        path = self.GetPath()
        self.Sort(path)
        
Main().main()
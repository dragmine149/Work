import os
import glob
import time
from colours import Print

class search:
    """
    directory -> where to start search
    target -> what to search for (Supports '()' arrays (tuples))
    layers -> How many directories above the current directory to search.
              Default 2: '../../../'
    sti -> how long to wait between messages and stuff, just for fun.
           Recommendation don't add if you want speed.
    """

    def __init__(self, directory, target, layers=2, sti=0):
        self.directory = directory
        self.target = target
        self.searched = ''
        self.layers = layers
        self.sti = sti
        self.__FoundList = []

    def Locate(self):
        self.__searchDirectory(self.directory)
        return self.__FoundList

    def __FindFile(self, directory, file):
        # Using glob, finds files with `directory/file`
        files = glob.glob(os.path.join(directory, file))
        self.__FoundList.extend(files)

    """
    __searchDirectory(self, directory, sub)
    - Searches for a file in directory
    Loops though pretty much the whole fs until the file is found.
    Goes up directories, down into directories and more!
    """

    def __searchDirectory(self, directory, sub=False):
        if self.layers > 0:
            fileText = "file"
            if isinstance(self.target, tuple) and len(self.target) > 1:
                fileText = "files"
            Print('Searching Dir: "{}". Target {}: "{}"'.format(directory, fileText, self.target), "green")  # noqa E501
            time.sleep(self.sti)  # makes it look cool

            # checks if in current directory, returns if it is.
            if isinstance(self.target, tuple):
                for file in self.target:
                    self.__FindFile(directory, file)

            # get files in current directory and remove the folder the user
            # just came out of (doesn't search the folder again)
            try:
                files = os.listdir(directory)
            except PermissionError:
                Print('Missing permissions for for {}'.format(directory), "red", "bold")  # noqa E501
                return

            # Skip over directory we just came out of
            if self.searched in files:
                files.remove(self.searched)
            
            # if self.target in files and os.path.join(directory, self.target) not in self.__FoundList:
            #     self.__FoundList.append(os.path.join(directory, self.target))

            # loops though all the files
            for file in files:
                time.sleep(self.sti)
                Print('Looking at {}'.format(file), "yellow")
                # Skips the folder if it's a well know not going to have files.
                if file == ".git":
                    print(".git, no just no.")
                    continue
                
                # if file.startswith("."):
                #     print("Hidden file, skipping")
                #     continue

                if file == self.target:
                    self.__FoundList.append(os.path.join(directory, file))

                # checks if the folder is a directory
                newFile = os.path.join(directory, file)
                if os.path.isdir(newFile):
                    self.__searchDirectory(newFile, True)  # noqa E501

            # if sub directory, don't go back up 1 directory.
            if not sub:
                self.searched = os.path.basename(os.path.abspath(directory))
                self.layers -= 1
                self.__searchDirectory(os.path.abspath(os.path.join(directory, '../')))  # noqa

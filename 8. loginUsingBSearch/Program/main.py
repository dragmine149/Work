import typing
import getpass
import os
import csv

class save:
    def __init__(self) -> None:
        """Class to write and read data
        """
        pass

    def __CreateCheck(self):
        """Check if file exists, else makes it
        """
        if not os.path.exists("info"):
            self._SaveFile()
            

    def _ReadFile(self) -> typing.List:
        """Read data from a file

        Returns:
            typing.List: The csv data
        """
        self.__CreateCheck()
        with open("info", "r") as f:
            csvreader = csv.reader(f)
            fields = next(csvreader)
            rows = []
            for row in csvreader:
                rows.append(row)
            
            return rows
    
    def _SaveFile(self, data=None) -> None:
        """Save a file

        Args:
            data (Array, optional): The data to save. Defaults to None.
        """
        with open("info", "w") as f:
            fields = ["Name", "Password"]
            csvWriter = csv.writer(f)
            csvWriter.writerow(fields)
            if data is not None:
                csvWriter.writerows(data)

    def _AppendFile(self, data) -> None:
        """Append to the end of a file

        Args:
            data (typing.List): The data to save
        """
        with open("info", "a") as f:
            csvWriter = csv.writer(f)
            csvWriter.writerows(data)

class searching(save):
    def __init__(self) -> None:
        """Main function todo stuff with.
        """
        pass

    def FindItem(self, value: str) -> int:
        """Test to see if value is in the list using binary search

        Args:
            value (str): The value to find

        Returns:
            int: The location of the value
        """
        data = self._ReadFile()
        
        if data is None:
            return -1
        
        if len(data) == 1:
            if data[0] == value:
                return 0
            return -1
        
        lower, higher = 0, len(data) - 1
        while lower <= higher:
            mid = (higher + lower) // 2

            if data[mid] < value:
                lower = mid + 1
                continue

            if data[mid] > value:
                higher = mid - 1
                continue

            if data[mid] == value:
                return mid

        # Really wanted to have this inside the loop
        return -1
            

    def main(self):
        """Main function
        """
        user = input("Please enter your username: ")
        pwrd = getpass.getpass("Please enter your password: ")
        
        r = self.FindItem([user, pwrd])
        
        print("User does not exist" if r == -1 else "Found user! Logging in...")
        
        if r == -1:
            add = input("Do you want to add your user? (y/n): ")
            if add.lower()[0] == "n":
                print("Okay, not adding user. Goodbye")
                return
            
            print("Adding user to file")
            self._AppendFile([[user, pwrd]])
            print("Added user to file. Goodbye")
            return

# Outside of OOP functions
search = searching()
search.main()

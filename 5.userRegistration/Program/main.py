import typing
import watermark
import getpass

# Save class thing
class Save:
    def __init__(self) -> None:
        pass
    
    def GetData(self) -> typing.List[str]:
        """Returns the data found in a file

        Returns:
            typing.List[str]: The data in the file (per line)
        """
        try:
            with open("Information.secret", "r") as f:
                return f.readlines()
        except FileNotFoundError:
            self.MakeFile()
            return []
    
    def UpdatedData(self, username, password) -> None:
        """Updates data in a file

        Args:
            username (string): The username for that user
            password (string): The password for that user
        """
        try:
            with open("Information.secret", "a") as f:
                f.write(f"{username}, {password}\n")
        except FileNotFoundError:
            self.MakeFile()
    
    def MakeFile(self):
        """Makes the file if it's not already found
        """
        with open("Information.secret", "w") as f:
            f.write("")
    

class Main:
    def __init__(self):
        self.Save = Save()
    
    def CheckUsername(self, user):
        data = self.Save.GetData()
        for userInfo in data:
            userInfo = userInfo.split(",")[0]
            userInfo = userInfo.strip()
            if user in userInfo:
                return False
        return True
    
    def GetUsername(self) -> str:
        username = None
        while username is None:
            username = input("Please enter your uesrname: ")
            if username == "":
                useSystem = input(f"No username entered! Use system username ({getpass.getuser()})?: ")
                if useSystem == "y" or useSystem == "":
                    username = getpass.getuser()
            
            # Removing this check will allow any number of usernames to be entered into the system.
            if not self.CheckUsername(username):
                username = None
                print("Username chosen is already in our database")
                continue
            
            if username == "":
                username = None
                print("Username cannot be blank")
                continue
        
        return username

    def GetPassword(self) -> str:
        password = None
        while password is None:
            password = getpass.getpass("Please enter your password: ")
            if "," in password:
                password = None
                print("You can not have ',' in your password")
                continue
            
            if password == "":
                password = None
                print("Password cannot be blank")
                continue

        return password
    
    def Main(self):
        """Main loop
        """
        username = self.GetUsername()
        password = self.GetPassword()
        
        self.Save.UpdatedData(username, password)


Main().Main()

class Test:
    def __init__(self):
        """Test class to test the save system.
        """
        self.Save = Save()
        print(self.Save.GetData())
        self.Save.UpdatedData("Test", "123")
        self.Save.UpdatedData("Test2", "8290")
        print(self.Save.GetData())
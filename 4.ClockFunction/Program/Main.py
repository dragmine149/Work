from re import S
import watermark

"""
This code is HELLA jank.
It works, but there are so many places which i really do not like.

Clean-ish code (Option 2)
Jank code (option 2)
"""

class Main:
    def __init__(self) -> None:
        self.time = None
        pass
    
    def __GenerateUI(self) -> str:
        uiInfo = f"""Time: {self.time}
Converted: {self.__ConvertTime(self.time)}
        """
        return uiInfo
    
    def __ConvertTime(self, time) -> str:
        hours = time.split(":")
        h = int(hours[0])
        
        end = hours[1:]
        emsg = ""
        for i in end:
            emsg += f":{i}"
        
        if h > 12:
            return f"{h % 12}{emsg}pm"

        if h < 12 and self.mode == "p":
            return f"{h + 12}{emsg}"

        return f"{time}{self.mode}m"
    
    def __clearInput(self, msg):
        self.time = None
        print(msg)
    
    def getTime(self):
        self.time = None
        while self.time is None:
            self.time = input("Please enter time (HH:MM:SS): ")
            args = self.time.split(":")
            
            # length check
            if len(args) < 2:
                self.__clearInput(
                    "Please enter the time in the required format! (HH:MM:SS)")
                continue
            
            # hour check 1
            if not args[0].isdigit():
                self.__clearInput("Please enter an interger for hours!")
                continue
            
            # hour check 2
            if int(args[0]) < 0 or int(args[0]) > 23:
                self.__clearInput(
                    "Please make sure that the hours are between 0 and 23 (inclusive)")
                continue
            
            # hour fix (2 digit minute)
            if int(args[0]) < 10:
                args[0] = f"0{args[0]}"
            
            # Minute check 1
            if not args[1].isdigit():
                self.__clearInput("Please enter an interger for the minutes!")
                continue
            
            # Minute check 2
            if int(args[1]) < 0 or int(args[1]) > 59:
                self.__clearInput(
                    "Please make sure that the minutes are between 0 and 59 (inclusive)")
                continue
            
            # Minute fix (2 digit minute)
            if int(args[1]) < 10:
                args[1] = f"0{args[1]}"
            
            # Return if no seconds argument found
            if len(args) < 3:
                return f"{args[0]}:{args[1]}"
            
            # Seconds check 1
            if not args[2].isdigit():
                self.__clearInput("Please enter an interger for seconds!")
                continue
            
            # seconds check 2
            if int(args[2]) < 0 or int(args[2]) > 59:
                self.__clearInput(
                    "Please make sure that the seconds are between 0 and 59 (inclusive)")
                continue
            
            # return string of all data
            return f"{args[0]}:{args[1]}:{args[2]}"
    
    def getMode(self):
        # get the mode of the time
        if int(self.time.split(":")[0]) <= 12:
            self.mode = None
            while self.mode is None:
                self.mode = input("Please enter either p (pm) or a (am) for the time: ")
                if self.mode[0] != "a" and self.mode[0] != "p":
                    self.mode = None
                    print("Please enter either p or a!")
                    continue
    
    def getChoice(self):
        self.choice = None
        while self.choice is None:
            print("""
1. Translate time (hours -> minutes, etc...)
2. Show time in 12h and 24h
                  """)
            self.choice = input("What would you like to do?: ")
            if not self.choice.isdigit():
                print("Please enter a number!")
                self.choice = None
                continue
            
            self.choice = int(self.choice)
            
            if self.choice < 0 or self.choice > 2:
                print("Please make sure the input is within the range (1, 2): ")
                self.choice = None
                continue


    def InputTimeInfo(self):
        print("""
1. Year
2. Month
3. Weeks
4. Days
5. Hours
6. Minutes
7. Seconds
8. Miliseconds
              """)
        format = None
        while format is None:
            format = input("Please enter the format of your input: ")
            if not format.isdigit():
                format = None
                print("Please enter a digit!")
                continue
            
            format = int(format)
            
            if format < 0 or format > 8:
                format = None
                print("Please enter a number within the range (1, 8)")
                continue
            
            return format - 1

    def InputTime(self, unit):
        time = None
        while time is None:
            time = input(f"Please enter amount of {unit}(s): ")
            if not time.isdigit():
                print("Please enter a digit for the time!")
                time = None
                continue
            
            return int(time)
        
    def CalculateResult(self, st, ed, unit):
        # Well, needed to convert so i made an array.
        match st:
            case 0:
                func = [1, 12, 52, 365, (365 * 24), (365 * 24 * 60), (365 * 24 * 60 * 60), (365 * 24 * 60 * 60 * 1000)]
                return unit * func[ed]
            case 1:
                func = [(1 / 12), 1, 4, 30, (30 * 24), (30 * 24 * 60), (30 * 24 * 60 * 60), (30 * 24 * 60 * 60 * 1000)]
                return unit * func[ed]
            case 2:
                func = [(1 / 52), (1 / 4), 1, 7, (7 * 24), (7 * 24 * 60), (7 * 24 * 60 * 60), (7 * 24 * 60 * 60 * 1000)]
                return unit * func[ed]
            case 3:
                func = [(1 / 365), (1 / 30), (1 / 7), 1, 24, (24 * 60), (24 * 60 * 60), (24 * 60 * 60 * 1000)]
                return unit * func[ed]
            case 4:
                func = [(1 / 24 / 365), (1 / 24 / 7 / 4), (1 / 24 / 7), (1 / 24), 1, 60, (60 * 60), (60 * 60 * 1000)]
                return unit * func[ed]
            case 5:
                func = [(1 / 60 / 24 / 365), (1 / 60 / 24 / 7 / 4), (1 / 60 / 24 / 7), (1 / 60 / 24), (1 / 60), 1, 60, (60 * 1000)]
                return unit * func[ed]
            case 6:
                func = [(1 / 60 / 60 / 24 / 365), (1 / 60 / 60 / 24 / 7 / 4), (1 / 60 / 60 / 24 / 7), (1 / 60 / 60 / 24), (1 / 60 / 60), (1 / 60), 1, 1000]
                return unit * func[ed]
            case 7:
                func = [(1 / 1000 / 60 / 60 / 24 / 365), (1 / 1000 / 60 / 60 / 24 / 7 / 4), (1 / 1000 / 60 / 60 / 24 / 7), (1 / 1000 / 60 / 60 / 24), (1 / 1000 / 60 / 60), (1 / 1000 / 60), (1 / 1000), 1]
                return unit * func[ed]
    
    def Main(self):
        # Main loop
        watermark.main()

        self.getChoice()

        if self.choice == 2:
            self.time = self.getTime()
            self.getMode()
            
            watermark.main()
            timeInfo = self.__GenerateUI()
            print(timeInfo)

        elif self.choice == 1:
            data = ["Year", "Month", "Week", "Day", "Hour", "Minute", "Second", "Milisecond"]
            stFormat = self.InputTimeInfo()
            edFormat = self.InputTimeInfo()
            timeUnit = self.InputTime(data[stFormat])
            
            watermark.main()
            print(f"Converting {timeUnit}{data[stFormat]} to {data[edFormat]}")
            result = self.CalculateResult(stFormat, edFormat, timeUnit)
            print(f"Result:")
            print(f"{timeUnit} {data[stFormat]}(s) in {data[edFormat]} is {result}")
        

if __name__ == "__main__":
    tc = Main()
    tc.Main()
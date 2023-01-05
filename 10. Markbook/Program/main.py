import pickle
import os

canGraph = True
try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    canGraph = False


class save():
    def __init__(self) -> None:
        pass

    def save(self, data) -> None:
        """Saves data to a file

        Args:
            data (any): The data to save
        """
        with open("students.pcke", "wb") as f:
            pickle.dump(data, f)

    def load(self):
        """Load data from a file

        Returns:
            any: The data in the file
        """
        if not os.path.exists("students.pcke"):
            return {}

        with open("students.pcke", "rb") as f:
            return pickle.load(f)


class graph:
    def __GraphCheck(self):
        return canGraph

    def DrawGraph(self, data):
        if not self.__GraphCheck():
            print(
                "You are missing matplotlib to draw a graph. (Run pip install -U matplotlib to get it)")
            input("Press enter to continue")
            return None

        x, y = self.GetAxis(data)
        plt.scatter(x, y, label="Score", color="Red",
                    marker="*", s=30)

        plt.xlabel("Students")
        plt.ylabel("Score")
        plt.title("Students and score graph")
        plt.legend()
        plt.show()

        return None

    def GetAxis(self, students: dict):
        if not self.__GraphCheck():
            return None

        x = []
        y = []
        for item in students.items():
            y.append(str(item[1].get('score')))
            x.append(item[1].get('name'))

        return x, y


class main:
    def __init__(self) -> None:
        self.sv = save()
        self.gr = graph()

        self.students = self.sv.load()

    def main(self):
        """main loop
        """
        os.system("cls" if os.name == "nt" else "clear")
        print("-" * os.get_terminal_size().columns)
        print("What would you like to do?")
        print()
        print("-" * os.get_terminal_size().columns)
        print("Error: None")

        option = None

        while option is None:
            print("\033[3;0H" + " " * os.get_terminal_size().columns)
            option = input(
                "\033[3;0H0: Enter data. \t1: List data\t2: Graph\t3: Exit\t: ")
            if not option.isdigit():
                print("\033[5;0HError: Invalid option!")
                option = None
                continue

            option = int(option)

            if option < 0 or option > 3:
                print("\033[5;0HError: Invalid option (Out of range)!")
                option = None
                continue

        print("\033[5;0H" + " " * os.get_terminal_size().columns)
        print("\033[5;0HSuccess!")

        if option == 0:
            self.EnterData()
        elif option == 1:
            self.LoadData()
        elif option == 2:
            self.gr.DrawGraph(self.students)
            self.main()
        elif option == 3:
            return

    def RemoveData(self):
        remove = False
        while not remove:
            input("Please enter the ID of the student to remove: ")

    def EnterData(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("-" * os.get_terminal_size().columns)
        print("Please fill in the form for the student (When you click enter, you will go to the next field): ")
        print("Student ID: ")
        print("Student Name: ")
        print("Student Score:")
        print("-" * os.get_terminal_size().columns)

        sid = input("\033[3;0HStudent ID: ")
        name = input("\033[4;0HStudent Name: ")
        score = input("\033[5;0HStudent Score: ")

        if "" in (sid, name, score):
            print("\033[6;0H")
            print("A field can not be empty!")
            input("Press eneter to go back to main menu")
            self.main()

        print("\033[6;0HDone!")
        self.students[sid] = {"name": name,
                              "score": int(score)}
        self.sv.save(self.students)

        input("Press enter when you are ready to move on")
        self.main()

    def LoadData(self):
        print("\nName\t\tScore")
        for item in self.students.items():
            print(
                f"({item[0]}):{item[1].get('name')}\t\t{item[1].get('score')}")

        input("Press enter when you are ready to move on")
        self.main()


if __name__ == "__main__":
    m = main()
    m.main()

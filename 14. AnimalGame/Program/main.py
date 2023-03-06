from PythonFunctions import Save, Check


class data:
    def __init__(self) -> None:
        self.sv = Save.save()
        self.data = self.LoadData()

    def LoadData(self):
        return self.sv.Read('data.csv', encoding=[self.sv.encoding.CSV])

    def TranslateData(self, position):
        lineData = self.data.get('row')[position]
        return lineData.get('data'), [lineData.get('yes'), lineData.get('no')]


class main:
    def __init__(self) -> None:
        self.position = 0
        self.chk = Check.Check()
        self.data = data()

    def askQuestion(self, question, direction):
        result = self.chk.getInput(question, self.chk.ModeEnum.yesno)
        return int(direction[0]) if result else int(direction[1])

    def main(self):
        while self.position != -1:
            lineData = self.data.TranslateData(self.position)
            if lineData[1][0] == '-1' and lineData[1][1] == '-1':
                return print(f"Your animal is a {lineData[0]}!")

            self.position = self.askQuestion(*lineData)


if __name__ == "__main__":
    m = main()
    m.main()

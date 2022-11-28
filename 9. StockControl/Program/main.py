import csv
import ui


class UI(ui.ui):
    """Stores information about the ui really.
    """

    def __init__(self) -> None:
        """Declaries variables and other ui related stuff
        """
        super().__init__("Stock Control")

        # variables
        self.id = ui.tk.StringVar(self.canvas)
        self.name = ui.tk.StringVar(self.canvas)
        self.price = ui.tk.StringVar(self.canvas)
        self.quantity = ui.tk.StringVar(self.canvas)

        # frames
        self.secEditFrm = self.CreateFrame(0, 1)
        self.editFrm = self.CreateFrame(0, 2)
        self.infoFrm = self.CreateFrame(0, 1)
        self.itemFrm = self.CreateFrame(0, 0)

        # hide frames
        self.ChangeState({"Element": self.infoFrm}, False)
        self.ChangeState({"Element": self.editFrm}, False)
        self.ChangeState({"Element": self.secEditFrm}, False)

    def MakeUI(self):
        """Make all the labels and text boxes for the ui
        """
        self.AddLabel(
            "", textVar=self.id, row=0, frame=self.infoFrm, sticky='w', image=None)
        self.AddLabel(
            "", textVar=self.name, row=1, frame=self.infoFrm, sticky='w', image=None)
        self.AddLabel(
            "", textVar=self.price, row=2, frame=self.infoFrm, sticky='w', image=None)
        self.AddLabel(
            "", textVar=self.quantity, row=3, frame=self.infoFrm, sticky='w', image=None)

        self.AddLabel("", textVar=self.id, row=0,
                         frame=self.secEditFrm, sticky='w', image=None)
        self.AddTexBox(self.name, 1, frame=self.secEditFrm, sticky='w')
        self.AddTexBox(self.price, 2, frame=self.secEditFrm, sticky='w')
        self.AddTexBox(self.quantity, 3, frame=self.secEditFrm, sticky='w')

        self.AddButton("Quit", self.canvas.quit, 0, 0,
                          frame=self.itemFrm, callbackArgs=False)

    def ShowUI(self):
        """Run the mainloop so that the ui is shown and is listening for responses
        """
        self.canvas.mainloop()


class main(UI):
    def __init__(self) -> None:
        """Set up the UI class, and other requirements for this class
        """
        super().__init__()
        self.data = []
        self.fields = None

        self.visible = None


    def __Read(self):
        """Read the file and use the data accordingly
        """
        with open("stock.csv", "r") as f:
            reader = csv.DictReader(f)
            self.fields = reader.fieldnames

            self.data = []
            for item in reader:
                self.data.append(item)

    def __Save(self):
        """Write the data back to the file
        """
        with open("stock.csv", "w") as f:
            writer = csv.DictWriter(f, self.fields)
            writer.writeheader()
            writer.writerows(self.data)

    def BtnCallback(self, info):
        """Callback function for argument click

        Args:
            info (string): The name of the button clicked
        """
        item = None
        for _, row in enumerate(self.data):
            if row.get("name") == info:
                item = row

        # Set the variables to the desginated infomation
        self.id.set(f"{'ID':15} : {item.get('id'):}")
        self.name.set(f"{'Name':11} : {item.get('name')}")
        self.price.set(f"{'Price':13} : £{item.get('cost')}")
        self.quantity.set(f"{'Quantity':10} : {item.get('quantity')}")

        # Change the state of active ui.
        self.ChangeState({"Element": self.infoFrm, "row": 0, "column": 1})
        self.ChangeState({"Element": self.editFrm, "row": 0, "column": 2})

        self.visible = item

    def OnEdit(self, *_):
        """Change the state of the edit ui if the user has requested to edit the data
        """
        self.ChangeState({"Element": self.infoFrm}, False)
        self.ChangeState({"Element": self.secEditFrm, "row": 0, "column": 1})

    def OnEndEdit(self, *_):
        """Callback when the user requests to save the data they edited.
        """
        self.ChangeState({"Element": self.secEditFrm}, False)
        self.ChangeState({"Element": self.infoFrm, "row": 0, "column": 1})

        # Split the name up to get the name
        name = self.name.get()
        name = name.split(":")[1]
        name = name[1:]

        # Split the cost up to get the cost
        cost = self.price.get()
        cost = cost.split(":")[1]
        cost = cost[2:]

        # Split the quantity up to get the quantity
        quantity = self.quantity.get()
        quantity = quantity.split(":")[1]
        quantity = quantity[1:]

        # Update the data in the array and save it
        info = {
            "id": self.visible.get("id"),
            "name": name,
            "cost": float(cost),
            "quantity": int(quantity)
        }
        self.data[int(self.visible.get("id")) - 1] = info

        self.__Save()

    def MakeUI(self):
        """Outer function to use custom callbacks and self.data
        """
        for rowIndex, row in enumerate(self.data):
            self.AddButton(row.get("name"), self.BtnCallback,
                              rowIndex + 1, 0, callbackArgs=True, frame=self.itemFrm)

        self.AddButton("Edit", self.OnEdit,
                          0, 0, columnspan=2, frame=self.editFrm)

        self.AddButton("Save", self.OnEndEdit,
                          2, 0, columnspan=2, frame=self.editFrm)
        return super().MakeUI()


    def main(self):
        """Main function, just to have all of the other functions join together.
        """
        self.__Read()
        self.MakeUI()
        self.ShowUI()

if __name__ == "__main__":
    m = main()
    m.main()

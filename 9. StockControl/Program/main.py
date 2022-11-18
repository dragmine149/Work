import csv
import os
import sys

class Load:
    def __init__(self) -> None:
        pass
    
    def ReadData(self):
        """Read the data
        """
        with open("stock.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.headers = reader.fieldnames
            
            self.data = []
            for item in reader:
                self.data.append(item)
    
    def WriteData(self, index, header, data):
        """Write the data

        Args:
            index (_type_): The item index
            header (_type_): The item info
            data (_type_): The data of the item
        """
        self.data[index][header] = data

        with open("stock.csv", "w", encoding="utf-8") as f:
            writer = csv.DictWriter(f, self.headers)
            writer.writeheader()
            writer.writerows(self.data)
    
    def GetItem(self):
        """Get the user input from a list of items"""
        # Can do a while true loop as we return
        while True:
            searchItem = input("Please enter the name of the item you want to search for (-1: list, 0 to exit): ")
            
            # Show a list of all the items
            if searchItem == "-1":
                data = ""
                for item in self.data:
                    data += item.get("name") + "\n"
                print(f"""
Items:
{data}""")
            
            # Exit the program
            if searchItem == "0":
                sys.exit("Thank you for using this program")
            
            # Get the item info from the input
            for index, item in enumerate(self.data):
                if item.get("name") == searchItem:
                    self.index = index
                    return item
    
    def ShowData(self):
        """Show a list of items formatted nicely
        """
        item = self.GetItem()
        print("-" * os.get_terminal_size().columns)
        
        print(f"""
{"ID":10}: {item.get("id")}
{"NAME":10}: {item.get("name")}
{"Cost":10}: £{item.get("cost")}
{"Quantity":10}: {item.get("quantity")}
""")
        
        print("-" * os.get_terminal_size().columns)
        
    def EditData(self):
        """Allow the user to edit data in the csv file

        Returns:
            _type_: False to choose a different item, quit to quit. nothing to carry on.
        """
        edit = None
        while not edit:
            edit = input("Please enter the value you want to change (0 to choose a different item, 1 to quit): ")
            
            if edit == 0:
                return False
            
            if edit == 1:
                sys.exit("Thank you for using this program")
            
            # check if it's a valid item
            if edit not in self.headers:
                print("Please enter a valid value to edit!")
                edit = None
                self.ShowData()
                continue
            
            value = input(f"Please enter the new value for {edit}: ")
            self.WriteData(self.index, edit, value)
            print("Saving....")
            self.ShowData()
        
    
    def main(self):
        """main loop
        """
        while True:
            self.ReadData()
            self.ShowData()
            self.EditData()

if __name__ == "__main__":
    ld = Load()
    ld.main()
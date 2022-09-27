import json
import random
import time
import os
import watermark

class Load:
    def __init__(self) -> None:
        print("Loading data...")
        self.data = self.ReadFile("items.json")
    
    def ReadFile(self, path):
        """Reads and decodes the data stored in the json part

        Args:
            path string: the path to read from

        Returns:
            json: The loaded json data
        """
        try:
            with open(path, 'r') as f:
                data = json.loads(f.read())
                return data
        except json.JSONDecodeError:
            exit("Data is invalid json form! Please redownload the data or ask for help!")

class Shop:
    def __init__(self) -> None:
        self.dataManager = Load()
        self.budget = 5
    
    def ShowShop(self):
        storedItems = self.dataManager.data
        index = 0
        
        print("-1: Exit\t 0: Random\n")
        
        # Shows all the items in a grid like view
        for item in storedItems:
            index += 1
            print("{}: {}".format(index, item), end='\t')
            if index % 4 == 0:
                print("\n")
        
        print("\n")
    
    def BuyItem(self):
        # Gets the user to input the item they would like to buy
        itemToBuy = None
        while itemToBuy is None:
            itemToBuy = input("Please enter the number of the item you would like to buy: ")
            if self.isdigit(itemToBuy):
                itemToBuy = int(itemToBuy)
                
                # in range check
                if itemToBuy > -2 and itemToBuy <= len(self.dataManager.data):
                    continue
                
                print("Please select an item from the list")
                itemToBuy = None
                continue
            
            print("Please enter a digit (interger) as your input!")
            itemToBuy = None

        return itemToBuy
    
    def GetItemInfoAtIndex(self, index):
        # Returns the item in the json array at the selected item
        data = list(self.dataManager.data)
        return data[index]
    
    def isdigit(self, item):
        if item[0] == "-":
            return item[1:].isdigit()
        
        # Checks if the "item" is a valid input
        if item.find(".") == -1:
            return item.isdigit()
        
        itemInfo = item.split(".")
        
        if len(itemInfo) != 2:
            return False
        
        return itemInfo[0].isdigit() and itemInfo[1].isdigit()
    
    def _GetUserInputs(self, info):
        # Asks the user for information
        items = None
        while items is None:
            limit = int(self.budget // self.dataManager.data[info])
            items = input("How many items do you want to buy: ")
            if items.isdigit():
                items = int(items)
                
                if items <= limit:
                    continue
                    
                print("The ammount of items you requested is more than you have the budget for!")
                items = None
                continue
            
            print("Please enter a digit (interger) as your input!")
            items = None
            continue
        
        print("If you guess the ammount of money you will have left over, we will give you an extra item for free!")
        extra = None
        while extra is None:
            extra = input("Ammount left over (1 attempt): ")
            if self.isdigit(extra):
                extra = float(extra)
                continue
            
            print("Please enter your answer in format X.Y!")
            extra = None
            continue
        
        return items, extra
    
    def ItemInfo(self, index):
        info = self.GetItemInfoAtIndex(index - 1)  # get information about the item
        
        # print out information about the item
        print("\x1b[2J\x1b[H", end='')
        print("Infomation about this item: ")
        print("Name: {}".format(info))
        print("Price: £{}".format(self.dataManager.data[info]))
        print("")
        print("Your budget: £{}".format(self.budget))
        
        items, extra = self._GetUserInputs(info)
        
        bonus = extra == (self.budget - 
                          (self.dataManager.data[info] * items))
        bonusItem = 0 if not bonus else 1
        
        # print out information about the user inputs
        print('-' * os.get_terminal_size().columns)
        time.sleep(0.5)
        print("Items purchased: {}".format(items))
        time.sleep(0.5)
        print("Amount Left guess: {}".format(extra))
        print()
        time.sleep(0.5)
        print("Amount Spent: £{}".format(self.dataManager.data[info] * items))
        time.sleep(0.5)
        print("Amount left: £{}".format(self.budget - (self.dataManager.data[info] * items)))
        time.sleep(1)
        print("Bonus item: {}".format(bonus))
        time.sleep(0.5)
        print()
        print("Items gained: {}".format(items + bonusItem))

    def Main(self):
        # Always shopping
        
        while True:
            watermark.main()
            self.ShowShop()
            item = self.BuyItem()
            
            if item == -1:
                exit("Thank you for buying at {SHOP NAME HERE}")
            
            if item == 0:
                item = random.randint(1, len(self.dataManager.data) + 1)
            shop.ItemInfo(item)

if __name__ == "__main__":
    shop = Shop()
    shop.Main()

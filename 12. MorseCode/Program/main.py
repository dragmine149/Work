class binaryList:
    def __init__(self, inputs:list, zeroIndex:list, oneIndex:list, *, other:list = None) -> None:
        """Make a binary tree.

        Args:
            inputs (list): A list of inputs and answers (E.g. ['a', 'b', 'c', 1, 2, 3])
            zeroIndex (list): A list of inputs for where to go to when a 0 is retrieved
            oneIndex (list): A list of inputs for where to go to when a 1 is retrieved
            other (list): A list of answers or other stuff to use when a number is not required.
        """
        self.inputs = inputs
        self.zeroIndex = zeroIndex
        self.oneIndex = oneIndex
        self.position = 0
        self.user_input = None

    def getInput(self, user_input=None):
        self.user_input = user_input
        if user_input is None:
            self.user_input = input(f"{self.inputs[self.position]}: ")
    
    def TranslateInput(self):
        

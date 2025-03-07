import string
from random import choices

class Generator:
    def __init__(self,k,options):
        self.k = k
        self.options = options
    def passwordGenerate(self):
        self.optionactive = ''
        for i in self.options:
            if i == 1:
                self.optionactive += string.ascii_uppercase
            elif i == 2:
                self.optionactive += string.ascii_lowercase
            elif i == 3:

                self.optionactive += string.digits
        if not self.optionactive:
            return "Error: No options selected!"

        return ''.join(choices(self.optionactive, k=self.k))

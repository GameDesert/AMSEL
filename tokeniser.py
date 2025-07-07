import decimal

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZΑαΔδΗηΒβΕεΘθΓγΖζΙιΚκΝνΠπΛλΞξΡρΜμΟοΣςΤτΧχσΥυΨψΦφΩω"
numbers = "0123456789"
operations = "-+/*="
functions = [
    ""
]

# region
# class Line:
#     def __init__(self, linetext):
#         self.linetext = linetext
#         self.current_sequence = []
#         self.brackets = {
#             "count":0,
#             "indices":[]
#         }

    
#     def _bracket_detect(self, type, index):
#         if type == "open":
#             self.brackets["count"] += 1
#             self.brackets["indices"].append(index)
#         elif type == "closed":
#             if self.brackets["count"] == 0:
#                 raise SyntaxError("Mismatched brackets.")
#             else:
#                 self.brackets["count"] += -1
#                 _build_term(self.brackets["indices"].pop(), index)

#     def _identify(self, character):
#         char = character[1]
#         index = character[0]
#         if char == "(":
#             _bracket_detect("open", index)
#         elif char == ")":
#             _bracket_detect("closed", index)

#     def _crawl(linetext):
#         for character in enumerate(linetext):
#             _identify(character)
# endregion

class Document:
    def __init__(self):
        self.variables = {}

        Line(self)

class Line:
    def __init__(self, document, line=""):
        self.linetext = str(line)
        self.sequence = []

        Variable(document, "aaaa")

class Element:
    def __init__(self, document):
        pass


class Constant(Element):
    def __init__(self, document, digits):

        if "." in digits:
            num = decimal.Decimal(digits)
        else:
            num = int(digits)

        self.num = num
    
    def build(self):
        return ["constant", self.num]

class Variable(Element):
    def __init__(self, document, name, immutable=False, value=None):
        self.name = str(name)
        self.immutable = int(immutable)
        document.variables[name] = value

    def build(self):
        return ["variable", self.immutable, self.name]

class Term(Element):
    def __init__(self):
        pass

    # Process of Constructing
    """
    - Look for an open bracket
    - If you find one, increment a counter and add its index to the end of an array
    - Next, if you find a close bracket, decrement the counter, pop the index of the last bracket in the array
    - Evaluate a new term using all the characters between the two indices, also check if there's a negative sign 1 char before (if there's something else inbetween, that's a multiplication with another term) and a power caret 1 char after.
    """

class Operation(Element):
    def __init__(self):
        pass

class Function(Element):
    def __init__(self):
        pass

class Equation(Element):
    def __init__(self):
        pass

class Output(Element):
    def __init__(self):
        pass

x = Document()
print(x.variables)
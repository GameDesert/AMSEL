letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZΑαΔδΗηΒβΕεΘθΓγΖζΙιΚκΝνΠπΛλΞξΡρΜμΟοΣςΤτΧχσΥυΨψΦφΩω"
numbers = "0123456789."
operations = "-+/*"

# Tokeniser Plan:
"""
- Go through and nest that shit.
- I.e. Don't worry about the data structures for now,
- just split the highest-level string into terms,
- broken up into the first layer of a list.
- Next, cycle through the first layer and see if there's anything more to break up.
"""

# RULES:
"""
- There must be a leading and trailing space on each operator.
- Everything to the left of a division will be the numerator, everything to the right will be the denominator. This is limited to the term the division is nested in (either the surface or any bracketed).
"""

# test = "9 + -(A + 99 * Bar)^(31 + F) / 18(6 / 2)H3^2 - 6 = Z^2 - 14 * 6"
# How this _should_ be parsed:
"""
- Group a "9 + " with a negated term "A + 99Bar" with another term as a power "31+F".
- Identify the division operator.
- Group a denominator term "18(6 / 2)H3^2 - 6"
- Reevaluate the negated numerator term...
"""

def split_into_terms(instring): # Effectively, parse each term, then push to the out stack.
    string = instring + " "
    out = []
    buffer = []

    bracket_count = 0

    for char in enumerate(string):
        if char[1] == "(":
            if buffer != []:
                out.append(''.join(buffer))
                buffer = []
            bracket_count += 1
            buffer.append(char[1])

            continue

        if char[1] == ")":
            bracket_count += -1
            buffer.append(char[1])

            if bracket_count == 0:
                out.append(''.join(buffer))
                buffer = []
                continue
            else:
                continue

        if bracket_count == 0:            
            if char[1] in letters: # Encounter a letter
                if (buffer == []) or (buffer[-1] in letters): # If buffer so far is a variable or empty
                    buffer.append(char[1])
                else: # If buffer is something else, terminate it and start a new buffer
                    out.append(''.join(buffer))
                    buffer = []

                    buffer.append(char[1])


            elif char[1] in numbers:
                if (buffer == []) or (buffer[-1] in numbers): # If buffer so far is a number or empty
                    buffer.append(char[1])
                else: # If buffer is something else, terminate it and start a new buffer
                    out.append(''.join(buffer))
                    buffer = []

                    buffer.append(char[1])

            elif (char[1] in operations) or (char[1] == "^"):
                if buffer != []:
                    out.append(''.join(buffer))
                    buffer = []

                out.append(char[1])
            
            elif char[1] == "=":
                if buffer == ["="]:
                    buffer.append(char[1])
                    out.append(''.join(buffer))
                    buffer = []
                    continue
                elif buffer != []:
                    out.append(''.join(buffer))
                    buffer = []
                buffer.append(char[1])

            elif char[1] == " ":
                if buffer == []:
                    pass
                elif (buffer[-1] in letters) or (buffer[-1] in numbers):
                    out.append(''.join(buffer))
                    buffer = []
        else:
            buffer.append(char[1])
    print(out)
    tidied = cleanup_and_reiterate(out)
    return tidied
    

def cleanup_and_reiterate(tokenised_level):
    tidied_out = []
    for element in tokenised_level:
        print(element)
        assessment = valid_term(element)
        assessment_name = assessment[0]
        if assessment_name == "del":
            pass
        elif assessment_name == "invalid":
            raise SyntaxError("Parsing failed. Invalid syntax.")
        elif assessment_name == "pass":
            tidied_out.append(element)
        elif assessment_name == "reeval":
            reevaluated = split_into_terms(assessment[2])
            tidied_out.append(reevaluated)
    return tidied_out


def valid_term(term): # Outputs: Valid Terms: Pass or Reevaluate, Invalid Terms: Delete or Raise Syntax Error (Invalid)
    if len(term) == 0:
        return ("del", False)
    elif term == " ":
        return ("del", False)
    elif ((term in operations) or (term == "^")) and (len(term) == 1):
        return ("pass", True)
    elif ((term == "=") or (term == "==")):
        return ("pass", True)
    elif term in letters:
        return ("pass", True)
    elif all(c in numbers for c in term):
        if (term[0] != ".") and (term[-1] != "."):
            if term.count(".") <= 1:
                return ("pass", True)
            else:
                return ("invalid", False)
        else:
            return ("invalid", False) # Perhaps eventually add functionality to add a 0 if there is a leading "."
    elif all(c in letters for c in term):
        return ("pass", True)
    elif (term[0] == "(") and (term[-1] == ")"):
        if len(term) <= 2:
            return ("del", False)
        elif len(term) >= 3:
            newterm = term[1:-1]
            return ("reeval", True, newterm)    
    else:
        return ("invalid", False)

print(split_into_terms("A(3BA)^(5 * 2) - 91.23 =="))
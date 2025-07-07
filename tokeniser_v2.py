import decimal

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZΑαΔδΗηΒβΕεΘθΓγΖζΙιΚκΝνΠπΛλΞξΡρΜμΟοΣςΤτΧχσΥυΨψΦφΩω"
numbers = "0123456789"
operations = "-+/*="


# Function to parse a string and convert to array
# If it comes across any nested, it recalls the parser

# teststring = "-A^93 + 6D / 8 * 5 - 3"
# Build term stack
# If encounter division, nest the first half buffer in a division operation before returning

teststring = "-abb"


def evaluate(string):
    stack = []
    brackets = {"count": 0, "indices": []}
    for char in enumerate(string):
        # If encounter - sign:
        # - Check if next character is an open bracket, delimit by matching close bracket and send to term builder (which will re-evaluate anything inside)
        # - If next character is a number or character, start saving buffer until encountering space or operator (before a caret). Also watch for opening brackets, and do not stop evaluating until closing bracket matched too. If double-equal or single equal encountered while brackets are open or when not evaluating top layer, tweak out.
        # - If next character is a space, blah blah blah

        # Build automatic collector for terms.

        # If encountering - sign:
        # If there's no space after it, begin a multiplication by ("sign", 0) and begin collecting terms until next delimiter.

        if char[1] == "-":  # Evaluate a negative object
            if string[char[0] + 1] != " ":
                # Now what:
                # Begin building a string, and cease when encountering a space (if not immediately followed by a multiplication)
                reeval_buffer = []
                substring = string[char[0] + 1 :]
                print("Substring:", substring)
                for subchar in enumerate(substring):

                    if subchar[0] + 1 == len(substring):
                        print(subchar[0], len(substring) - 1)
                        if reeval_buffer == []:
                            raise SyntaxError("Unpaired Negation")
                        else:
                            return [
                                "operation",
                                ["sign", 0],
                                evaluate("".join(reeval_buffer)),
                                "multiply",
                            ]  # This, using the test string "-abb" will evaluate to None, as there is no setup for evaluating products of variables yet. But everything else here works!

                    globalindex = char[0] + subchar[0]
                    print(subchar)
                    print(brackets)

                    if subchar[1] == "(":
                        brackets["count"] += 1
                        brackets["indices"].append(subchar[0])
                        reeval_buffer.append(subchar[1])

                    elif subchar[1] == ")":
                        brackets["count"] += -1
                        reeval_buffer.append(subchar[1])

                    elif brackets["count"] > 0:
                        if subchar[1] != "=":
                            reeval_buffer.append(subchar[1])
                        else:
                            raise SyntaxError("Misplaced Equals Sign")
                    else:
                        if subchar[1] == " ":
                            if (substring[subchar[0] + 1] != "*") and (
                                substring[subchar[0] - 1] != "*"
                            ):
                                if brackets["count"] < 0:
                                    raise SyntaxError("Mismatched Brackets")
                                return [
                                    "operation",
                                    ["sign", 0],
                                    evaluate("".join(reeval_buffer)),
                                    "multiply",
                                ]
                            else:
                                reeval_buffer.append(subchar[1])
                        else:
                            reeval_buffer.append(subchar[1])
                            print("Appending:", subchar[1])

                    # Later, add a thing here to also include functions.

        elif char[1] == "(":  # Evaluate a bracketed term
            reeval_buffer = []
            index_buffer = []
            index_evaluating = False
            substring = string[char[0] :]

            for subchar in enumerate(substring):
                if brackets["count"] > 0:
                    if subchar[1] == "(":
                        brackets["count"] += 1
                    elif subchar[1] == ")":
                        brackets["count"] += -1
                    if index_evaluating == False:
                        reeval_buffer.append(subchar[1])
                    else:
                        index_buffer.append(subchar[1])
                elif subchar[1] == "(":
                    brackets["count"] += 1
                    if index_evaluating == False:
                        reeval_buffer.append(subchar[1])
                    else:
                        index_buffer.append(subchar[1])
                elif subchar[1] == ")":
                    brackets["count"] += -1
                    if index_evaluating == False:
                        reeval_buffer.append(subchar[1])
                    else:
                        index_buffer.append(subchar[1])
                elif subchar[1] == " ":
                    if (substring[subchar[0] + 1] != "*") and (
                        substring[subchar[0] - 1] != "*"
                    ):
                        if brackets["count"] < 0:
                            raise SyntaxError("Mismatched Brackets")
                        break
                    else:
                        if index_evaluating == False:
                            reeval_buffer.append(subchar[1])
                        else:
                            index_buffer.append(subchar[1])
                elif (subchar[1] == "^") and (index_evaluating == False):
                    index_evaluating = True
                else:
                    if index_evaluating == False:
                        reeval_buffer.append(subchar[1])
                    else:
                        index_buffer.append(subchar[1])
                print(reeval_buffer)

            if index_buffer == []:
                return ["term", ["constant", 1], "".join(reeval_buffer)]
            else:
                return ["term", evaluate("".join(index_buffer)), "".join(reeval_buffer)]
        elif char[1] in letters: # Begin evaluating a variable
            reeval_buffer = []
            term_evaluating = False
            substring = string[char[0]:]

            for subchar in enumerate(substring):
                if subchar in letters:
                    reeval_buffer.append(subchar[1])


print(evaluate(teststring))
